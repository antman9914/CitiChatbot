# coding=utf-8
# writer： Hongxuan Zhang
# date: 7.4
# 该文件用于实体替换


import pkuseg
from stanfordcorenlp import StanfordCoreNLP


def change_the_word():
    with StanfordCoreNLP(r'C:\Users\Admin\Desktop\stanford-corenlp-full-2018-10-05\stanford-corenlp-full-2018-10-05',lang='zh') as nlp:
        # 上述模型较大，使用while循环进行防止多次载入
        while(True):
            str1 = input("请输入第一个句子：")
            str2 = input("请输入第二个句子：")
            seg1 = nlp.ner(str1)
            seg2 = nlp.ner(str2)
            newStr = []
            for word1 in seg1:
                for word2 in seg2:
                    # res = model.similarity(word1[0], word2[0])
                    if word1[1] == word2[1] and word1[1] not in ['O','MISC','GPE']:
                        tuple_new = (word2[0],word2[1],word1[0])
                        print(tuple_new)
                        newStr.append(tuple_new)
            re_str = []
            for word1 in seg1:
                find = False
                for word in newStr:
                    if word1[0] == word[2]:
                        re_str.append(word[0])
                        find = True
                        break
                if not find:
                    re_str.append(word1[0])
            str3 = ''
            for str in re_str:
                str3 += str
            print(str3)

def main():
    print("输入两个句子，进行借代替换\n")
    change_the_word()


if __name__ == "__main__":
	main()
