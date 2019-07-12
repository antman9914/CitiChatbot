# coding:utf-8
#作者：肖劲宇
#时间：6.29
#对语料库进行处理生成Bert模型可以识别的语料
import yaml
import os
#从原始语料生成label标记的语料，可以用于Bert模型训练
def gerenatecorpus(folder):
    out = open("srfcorpus.txt", 'w', encoding='utf-8')
    for root, dirs, files in os.walk(folder):
        for fn in files:
            path = folder+"/" + fn
            f = open(path, 'r', encoding='utf-8')
            for line in f:
                print(line)
                label = fn[0:len(fn) - 4]
                out.write(label + '\t' + line)
            out.write('\n')
#生成意图类别
def gerenateLabel(corpus):
    labellist = []
    out = open(corpus, 'r', encoding='utf-8-sig')
    for line in out:
        x = line.split('\t', 1)
        labellist.append(x[0])
        s = set(labellist)
    # print(list(s))
    for i in list(s):
        print('"'+i+'"', end="")
        print(',',end="")
#用yml文件来生成语料库
def gerenatecorpuswithyml(folder):
    # 遍历文件夹chinesecorpus里面的文件并读取
    result = open("corpus.txt", mode='w', encoding='utf-8')
    for root, dirs, files in os.walk("chinesecorpus"):
        for fn in files:
            path = "chinesecorpus/" + fn
            # f是yml文件
            f = open(path, 'r', encoding='utf-8')
            cfg = f.read()
            d = yaml.load(cfg)  # 用load方法将yml转字典
            print(d)
            # 将yml文件转换为txt文件
            with open("txt1/" + d['categories'][0] + ".txt", mode='a', encoding='utf-8') as ff:
                for list in d['conversations']:
                    ff.write(list[0] + '\n')
            # print(d['categories'][0])
            # with open("chinesecorpus/" + d['categories'][0] + ".txt", mode='a', encoding='utf-8') as ff:

            # 消除txt1中文件的重复记录,写入txt2
            with open("txt1/" + d['categories'][0] + ".txt", mode='r', encoding='utf-8') as infile:
                lines_seen = set()
                with open("txt2/" + d['categories'][0] + ".txt", mode='a', encoding='utf-8') as outfile:
                    for line in infile:
                        if line not in lines_seen:
                            outfile.write(line)
                            lines_seen.add(line)
                    outfile.close()
            inf = open("txt2/" + d['categories'][0] + ".txt", mode='r', encoding='utf-8')
            for line in inf:
                result.write(d['categories'][0] + "\t" + line)
gerenatecorpus("srfcorpus")
#gerenateLabel("srfcorpus.txt")