# -*- coding: utf-8 -*-
# writer： Hongxuan Zhang
# date: 7.7
import logging

from gensim.models import word2vec


def main():
    sentences = word2vec.LineSentence("wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=250)
    model.save("word2vec.model")
    # load 模型
    # model = word2vec.Word2Vec.load("your_model_name")


if __name__ == "__main__":
    main()
