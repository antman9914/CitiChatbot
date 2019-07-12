# -*- coding: utf-8 -*-
# writer： Hongxuan Zhang
# date: 7.4
# 该文件用于处理WiKiCorpus中的数据

import logging
import sys
from gensim.corpora import WikiCorpus


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 " + sys.argv[0] + " wiki_data_path")
        exit()
    wiki_corpus = WikiCorpus(sys.argv[1], dictionary={})
    texts_num = 0
    with open("wiki_texts.txt",'w',encoding='utf-8') as output:
        for text in wiki_corpus.get_texts():
            output.write(' '.join(text) + '\n')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("已处理 %d 篇文章" % texts_num)


if __name__ == "__main__":
    main()
