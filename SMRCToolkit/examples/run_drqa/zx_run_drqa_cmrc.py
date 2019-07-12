# coding: utf-8
from sogou_mrc.data.vocabulary import Vocabulary
from sogou_mrc.dataset.cmrc import CMRCReader, CMRCEvaluator
from sogou_mrc.model.drqa import DrQA
import logging
from sogou_mrc.utils.feature_extractor import FeatureExtractor
from sogou_mrc.data.batch_generator import BatchGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
data_folder = '../../data_folder/'
embedding_folder = '../../embedding_folder/'

# Prepare the dataset reader and evaluator.
print("step 1:Prepare the dataset reader and evaluator...")
train_file = data_folder+"cmrc2018_train.json"
dev_file = data_folder+"cmrc2018_dev.json"
reader = CMRCReader()
train_data = reader.read(train_file)
eval_data = reader.read(dev_file)
evaluator = CMRCEvaluator(dev_file)

# Build a vocabulary and load the pretrained embedding
print("step 2:Build a vocabulary and load the pretrained embedding...")
vocab = Vocabulary(do_lowercase=False)
vocab.build_vocab(train_data + eval_data, min_word_count=3, min_char_count=10)
word_embedding = vocab.make_word_embedding(embedding_folder+"glove.840B.300d.txt")

# Use the feature extractor,which is only necessary when using linguistic features
print("step 3:Use the feature extractor,which is only necessary when using linguistic features...")
feature_transformer = FeatureExtractor(features=['match_lemma','match_lower','pos','ner','context_tf'],build_vocab_feature_names=set(['pos','ner']),word_counter=vocab.get_word_counter())
train_data = feature_transformer.fit_transform(dataset=train_data)
eval_data = feature_transformer.transform(dataset=eval_data)

#
print("step 4:xxx...")
train_batch_generator = BatchGenerator(vocab,train_data,training=True,batch_size=32,additional_fields=feature_transformer.features,feature_vocab=feature_transformer.vocab)
eval_batch_generator = BatchGenerator(vocab,eval_data,batch_size=32,additional_fields=feature_transformer.features,feature_vocab=feature_transformer.vocab)

# original paper adamax optimizer
print("step 5:original paper adamax optimizer...")
model = DrQA(vocab, word_embedding,features=feature_transformer.features,feature_vocab=feature_transformer.vocab)
model.compile()
model.train_and_evaluate(train_batch_generator, eval_batch_generator,evaluator, epochs=40, eposides=2)
model.evaluate(eval_batch_generator,eval_data,evaluator)
print("finished")
