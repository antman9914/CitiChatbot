# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
Changes:
  Parts of the code that are related to the translation is removed. Input/Output data paths are changed.
"""

import os
import re
import sys

from tensorflow.python.platform import gfile
import tensorflow as tf

from ..util import fs

# Special vocabulary symbols - we always put them at the start.
_PAD = b"_PAD"
_GO = b"_GO"
_EOS = b"_EOS"
_UNK = b"_UNK"
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3

# Regular expressions used to tokenize.
_WORD_SPLIT = re.compile(b"([.,!?\"':;)(])")
_DIGIT_RE = re.compile(br"\d")


def basic_tokenizer(sentence):
    """Very basic tokenizer: split the sentence into a list of tokens."""
    words = []
    for space_separated_fragment in sentence.strip().split():
        words.extend(_WORD_SPLIT.split(space_separated_fragment))
    return [w for w in words if w]


def create_vocabulary(vocabulary_path, data_path, max_vocabulary_size,
                      tokenizer=None, normalize_digits=True):
    """Create vocabulary file (if it does not exist yet) from data file.
    Data file is assumed to contain one sentence per line. Each sentence is
    tokenized and digits are normalized (if normalize_digits is set).
    Vocabulary contains the most-frequent tokens up to max_vocabulary_size.
    We write it to vocabulary_path in a one-token-per-line format, so that later
    token in the first line gets id=0, second line gets id=1, and so on.
    Args:
      vocabulary_path: path where the vocabulary will be created.
      data_path: data file that will be used to create vocabulary.
      max_vocabulary_size: limit on the size of the created vocabulary.
      tokenizer: a function to use to tokenize each data sentence;
        if None, basic_tokenizer will be used.
      normalize_digits: Boolean; if true, all digits are replaced by 0s.
    """
    if not gfile.Exists(vocabulary_path):
        print("Creating vocabulary %s from data %s" % (vocabulary_path, data_path))
        vocab = {}
        with gfile.GFile(data_path, mode="rb") as f:
            counter = 0
            for line in f:
                counter += 1
                if counter % 100000 == 0:
                    print("  processing line %d" % counter)
                line = tf.compat.as_bytes(line)
                tokens = tokenizer(line) if tokenizer else basic_tokenizer(line)
                for w in tokens:
                    word = _DIGIT_RE.sub(b"0", w) if normalize_digits else w
                    if word in vocab:
                        vocab[word] += 1
                    else:
                        vocab[word] = 1
            vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
            if len(vocab_list) > max_vocabulary_size:
                vocab_list = vocab_list[:max_vocabulary_size]
            with gfile.GFile(vocabulary_path, mode="wb") as vocab_file:
                for w in vocab_list:
                    vocab_file.write(w + b"\n")


def initialize_vocabulary(vocabulary_path):
    """Initialize vocabulary from file.
    We assume the vocabulary is stored one-item-per-line, so a file:
      dog
      cat
    will result in a vocabulary {"dog": 0, "cat": 1}, and this function will
    also return the reversed-vocabulary ["dog", "cat"].
    Args:
      vocabulary_path: path to the file containing the vocabulary.
    Returns:
      a pair: the vocabulary (a dictionary mapping string to integers), and
      the reversed vocabulary (a list, which reverses the vocabulary mapping).
    Raises:
      ValueError: if the provided vocabulary_path does not exist.
    """
    if gfile.Exists(vocabulary_path):
        rev_vocab = []
        with gfile.GFile(vocabulary_path, mode="rb") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [tf.compat.as_bytes(line.strip()) for line in rev_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_path)


def sentence_to_token_ids(sentence, vocabulary,
                          tokenizer=None, normalize_digits=True):
    """Convert a string to list of integers representing token-ids.
    For example, a sentence "I have a dog" may become tokenized into
    ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
    "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].
    Args:
      sentence: the sentence in bytes format to convert to token-ids.
      vocabulary: a dictionary mapping tokens to integers.
      tokenizer: a function to use to tokenize each sentence;
        if None, basic_tokenizer will be used.
      normalize_digits: Boolean; if true, all digits are replaced by 0s.
    Returns:
      a list of integers, the token-ids for the sentence.
    """

    if tokenizer:
        words = tokenizer(sentence)
    else:
        words = basic_tokenizer(sentence)
    if not normalize_digits:
        return [vocabulary.get(w, UNK_ID) for w in words]
    # Normalize digits by 0 before looking words up in the vocabulary.
    return [vocabulary.get(_DIGIT_RE.sub(b"0", w), UNK_ID) for w in words]


def data_to_token_ids(data_path, target_path, vocabulary_path,
                      tokenizer=None, normalize_digits=True):
    """Tokenize data file and turn into token-ids using given vocabulary file.
    This function loads data line-by-line from data_path, calls the above
    sentence_to_token_ids, and saves the result to target_path. See comment
    for sentence_to_token_ids on the details of token-ids format.
    Args:
      data_path: path to the data file in one-sentence-per-line format.
      target_path: path where the file with token-ids will be created.
      vocabulary_path: path to the vocabulary file.
      tokenizer: a function to use to tokenize each sentence;
        if None, basic_tokenizer will be used.
      normalize_digits: Boolean; if true, all digits are replaced by 0s.
    """
    if not gfile.Exists(target_path):
        print("Tokenizing data in %s" % data_path)
        vocab, _ = initialize_vocabulary(vocabulary_path)
        with gfile.GFile(data_path, mode="rb") as data_file:
            with gfile.GFile(target_path, mode="w") as tokens_file:
                counter = 0
                for line in data_file:
                    counter += 1
                    if counter % 100000 == 0:
                        print("  tokenizing line %d" % counter)
                    token_ids = sentence_to_token_ids(tf.compat.as_bytes(line), vocab,
                                                      tokenizer, normalize_digits)
                    tokens_file.write(" ".join([str(tok) for tok in token_ids]) + "\n")


def multidata_to_token_ids(data_path, target_path, vocabulary_path,
                           tokenizer=None, normalize_digits=True):
    """Tokenize data file and turn into token-ids using given vocabulary file.
    This function loads data line-by-line from data_path, calls the above
    sentence_to_token_ids, and saves the result to target_path. See comment
    for sentence_to_token_ids on the details of token-ids format.
    Args:
      data_path: path to the data file in one-sentence-per-line format.
      target_path: path where the file with token-ids will be created.
      vocabulary_path: path to the vocabulary file.
      tokenizer: a function to use to tokenize each sentence;
        if None, basic_tokenizer will be used.
      normalize_digits: Boolean; if true, all digits are replaced by 0s.
    """
    if not gfile.Exists(target_path):
        print("Tokenizing data in %s" % data_path)
        vocab, _ = initialize_vocabulary(vocabulary_path)
        with gfile.GFile(data_path, mode="rb") as data_file:
            with gfile.GFile(target_path, mode="w") as tokens_file:
                counter = 0
                for line in data_file:
                    counter += 1
                    if counter % 100000 == 0:
                        print("  tokenizing line %d" % counter)

                    utterences = tf.compat.as_bytes(line).split(b"\t")

                    tokenized_utterences = []
                    for utter in utterences:
                        token_ids = sentence_to_token_ids(utter, vocab, tokenizer, normalize_digits)
                        tokenized_utterences.append(" ".join([str(tok) for tok in token_ids]))

                    tokens_file.write("\t".join(tokenized_utterences) + "\n")


def prepare_dialogue_data(data_dir, train_path, dev_path,
                          vocabulary_size, vocab_file_name,
                          tokenizer=None):
    """Get dialogue data from data_dir, create vocabularies and tokenize data.
    Args:
      data_dir: directory in which the data sets will be stored.
      vocabulary_size: size of the vocabulary to create and use.
      tokenizer: a function to use to tokenize each data sentence;
        if None, basic_tokenizer will be used.
    Returns:
      A tuple of 6 elements:
        (1) path to the token-ids for question training data-set,
        (2) path to the token-ids for response training data-set,
        (3) path to the token-ids for question development data-set,
        (4) path to the token-ids for response development data-set,
        (5) path to the question vocabulary file,
        (6) path to the response vocabulary file.
    """

    vocab_path = os.path.join(data_dir, vocab_file_name)
    create_vocabulary(vocab_path, train_path, vocabulary_size)

    # Create token ids for the training data.
    train_ids_path = os.path.join(data_dir, "%s.ids%d.in" % (fs.file_name(train_path), vocabulary_size))
    multidata_to_token_ids(train_path, train_ids_path, vocab_path, tokenizer)

    # Create token ids for the development data.
    dev_ids_path = os.path.join(data_dir, "%s.ids%d.in" % (fs.file_name(dev_path), vocabulary_size))
    multidata_to_token_ids(dev_path, dev_ids_path, vocab_path, tokenizer)

    return (train_ids_path, dev_ids_path, vocab_path)


def prepare_data(data_dir, from_train_path, to_train_path, from_dev_path, to_dev_path, from_vocabulary_size,
                 to_vocabulary_size, tokenizer=None):
    """Preapre all necessary files that are required for the training.
      Args:
        data_dir: directory in which the data sets will be stored.
        from_train_path: path to the file that includes "from" training samples.
        to_train_path: path to the file that includes "to" training samples.
        from_dev_path: path to the file that includes "from" dev samples.
        to_dev_path: path to the file that includes "to" dev samples.
        from_vocabulary_size: size of the "from language" vocabulary to create and use.
        to_vocabulary_size: size of the "to language" vocabulary to create and use.
        tokenizer: a function to use to tokenize each data sentence;
          if None, basic_tokenizer will be used.
      Returns:
        A tuple of 6 elements:
          (1) path to the token-ids for "from language" training data-set,
          (2) path to the token-ids for "to language" training data-set,
          (3) path to the token-ids for "from language" development data-set,
          (4) path to the token-ids for "to language" development data-set,
          (5) path to the "from language" vocabulary file,
          (6) path to the "to language" vocabulary file.
      """
    # Create vocabularies of the appropriate sizes.
    to_vocab_path = os.path.join(data_dir, "vocab%d.to" % to_vocabulary_size)
    from_vocab_path = os.path.join(data_dir, "vocab%d.from" % from_vocabulary_size)
    create_vocabulary(to_vocab_path, to_train_path, to_vocabulary_size, tokenizer)
    create_vocabulary(from_vocab_path, from_train_path, from_vocabulary_size, tokenizer)

    # Create token ids for the training data.
    to_train_ids_path = to_train_path + (".ids%d" % to_vocabulary_size)
    from_train_ids_path = from_train_path + (".ids%d" % from_vocabulary_size)
    data_to_token_ids(to_train_path, to_train_ids_path, to_vocab_path, tokenizer)
    data_to_token_ids(from_train_path, from_train_ids_path, from_vocab_path, tokenizer)

    # Create token ids for the development data.
    to_dev_ids_path = to_dev_path + (".ids%d" % to_vocabulary_size)
    from_dev_ids_path = from_dev_path + (".ids%d" % from_vocabulary_size)
    data_to_token_ids(to_dev_path, to_dev_ids_path, to_vocab_path, tokenizer)
    data_to_token_ids(from_dev_path, from_dev_ids_path, from_vocab_path, tokenizer)

    return (from_train_ids_path, to_train_ids_path,
            from_dev_ids_path, to_dev_ids_path,
            from_vocab_path, to_vocab_path)


def read_2way_data(tokenized_dialog_path, buckets, max_size=None, reversed=False):
    """Read data from source file and put into buckets.
    Args:
      source_path: path to the files with token-ids.
      max_size: maximum number of lines to read, all other will be ignored;
        if 0 or None, data files will be read completely (no limit).
    Returns:
      data_set: a list of length len(_buckets); data_set[n] contains a list of
        (source, target) pairs read from the provided data files that fit
        into the n-th bucket, i.e., such that len(source) < _buckets[n][0] and
        len(target) < _buckets[n][1]; source and target are lists of token-ids.
    """
    data_set = [[] for _ in buckets]

    with gfile.GFile(tokenized_dialog_path, mode="r") as fh:
        utterences = fh.readline().split('\t')
        source = utterences[0] if len(utterences) > 0 else None
        target = utterences[1] if len(utterences) > 1 else None

        if reversed:
            source, target = target, source  # reverse Q-A pair, for bi-direction model

        counter = 0
        while source and target and (not max_size or counter < max_size):
            counter += 1
            if counter % 100000 == 0:
                print("  reading data line %d" % counter)
                sys.stdout.flush()

            source_ids = [int(x) for x in source.split()]
            target_ids = [int(x) for x in target.split()]
            target_ids.append(EOS_ID)

            for bucket_id, (source_size, target_size) in enumerate(buckets):
                if len(source_ids) < source_size and len(target_ids) < target_size:
                    data_set[bucket_id].append([source_ids, target_ids])
                    break

            utterences = fh.readline().split('\t')
            source = utterences[0] if len(utterences) > 0 else None
            target = utterences[1] if len(utterences) > 1 else None
    return data_set


def seq2words(seq, inverse_target_dictionary):
    words = []
    for w in seq:
        if w == EOS_ID:
            break

        word = inverse_target_dictionary[w] if w in inverse_target_dictionary else _UNK
        if isinstance(word, bytes):
            word = word.decode()
        words.append(word)

    return ' '.join(words)