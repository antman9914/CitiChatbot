import fastText.FastText as ff
import jieba
#使用训练数据集进行有监督的训练
classifier = ff.train_supervised("data/train.txt")
#模型进行持久化
model = classifier.save_model('data/try.model')