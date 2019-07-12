import fastText.FastText as ff
#加载模型
classifier = ff.load_model('data/try.model')
#使用训练后的模型进行预测意图
str ='《 断箭 》 北京 台 热播   三 兄弟 暗地里 飙戏 '
print(str)
pre = classifier.predict(str, 3) #输出改文本的预测结果
print(pre)