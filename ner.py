import json
import requests
import pprint
from urllib import parse
import string
# url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=24.f81be2527287502027fb8999f369716e.2592000.1564313350.282335-16671867"  #用于情感测试
# data = json.dumps({"text": "百度是垃圾公司"})    #情感测试

# for d in data['entity_annotation']:
#     print(d['_bdbkUrl'])  #处理NER的代码
# url = "http://tsn.baidu.com/text2audio?"  #这里开始是语音合成
# value = {}
# value['tex'] = "邹鑫太美"
# value['lan'] = "zh"
# value['tok'] = '24.fad79cad786319ff766ad2ba20a4558d.2592000.1564404489.282335-16676547'
# value['ctp'] = '1'
# value['cuid'] = '00-50-56-C0-00-08'
# d1 = parse.urlencode(value)
# url_encode = url+d1
# r = requests.post(url_encode)
# with open('C:/Users/lenovo/Desktop/test.mp3','wb') as f:
#     f.write(r.content)






import jieba
import csv
import time
import urllib.request
import urllib.parse
import hashlib
import base64
# def readCSVbyColumn(filename ,columnname):   ##读取csv列名对应列，不包括列名
# 	List = []
# 	with open(filename,'r') as csvfile:
# 		reader = csv.reader(csvfile, delimiter=',')
# 		p = -1
# 		i = 0
# 		j = 0
# 		for row in reader:
# 			if i == 0:
# 				for c in row:
# 					if c == columnname :
# 						p = j
# 					j += 1
# 			else:
# 				List.append(row[p])
# 			i += 1
# 			if p == -1:
# 				break
# 	return List
# list = readCSVbyColumn('C:/Users/lenovo/Desktop/hudongbaike2.csv','entry_context')
# with open('C:/Users/lenovo/Desktop/testresult.text','w') as f:
#     for entry in list:
#         seg_list = jieba.cut(entry, cut_all=False)
#         for seg in seg_list:
#             f.write(seg+'\n')