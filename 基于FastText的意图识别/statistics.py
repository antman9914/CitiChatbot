#作者：肖劲宇 张红轩
#用途：进行意图分析
#时间：2019.6.26

import fastText.FastText as ff
import jieba
classifier = ff.load_model('data/try.model')
labels_right = []
texts = []
with open("data/test.txt") as fr:
    for line in fr:
        line = line.decode("utf-8").rstrip()
        labels_right.append(line.split("\t")[1].replace("__label__",""))
        texts.append(line.split("\t")[0])

labels_predict = [e[0] for e in classifier.predict(texts)] #预测输出结果为二维形式
# print labels_predict
text_labels = list(set(labels_right))
text_predict_labels = list(set(labels_predict))
print(text_predict_labels)
print(text_labels)

A = dict.fromkeys(text_labels,0)  #预测正确的各个类的数目
B = dict.fromkeys(text_labels,0)   #测试数据集中各个类的数目
C = dict.fromkeys(text_predict_labels,0) #预测结果中各个类的数目
for i in range(0,len(labels_right)):
    B[labels_right[i]] += 1
    C[labels_predict[i]] += 1
    if labels_right[i] == labels_predict[i]:
        A[labels_right[i]] += 1
print(A)
print(B)
print(C)
#计算准确率，召回率，F值
for key in B:
    try:
        r = float(A[key]) / float(B[key])
        p = float(A[key]) / float(C[key])
        f = p * r * 2 / (p + r)
        print("%s:\t p:%f\t r:%f\t f:%f" % (key, p, r, f))
    except:
        print("error:", key, "right:", A.get(key, 0), "real:", B.get(key,0), "predict:", C.get(key, 0))
predict_list = []
# predict_list.append(' '.join(jieba.lcut(test_sentence)))
# print(predict_list)
# pred = classifier.predict(predict_list)
# print("分类为：" + str(pred))
# #输出预测结果以及类别概率
# print(classifier.predict_proba(test_sentence))
# # 得到前k个类别
# lables_top3 = classifier.predict(test_sentence)
# print(lables_top3)
# # 得到前k个类别+概率
# lables_prob3 = classifier.predict_proba(test_sentence)
# print(lables_prob3)