# coding=utf-8
# writer： Hongxuan Zhang
# date: 7.7
from gensim.models import word2vec
from gensim import models
import pkuseg

model = models.Word2Vec.load('word2vec.model')
str1 = input("请输入第一个句子：")
str2 = input("请输入第二个句子：")
res = model.similarity(str1, str2)
print(res)