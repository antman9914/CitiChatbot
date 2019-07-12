#作者：肖劲宇 李蕴琦
#用途：对aiml模板进行翻译
#时间：2019.7.3
from bs4 import BeautifulSoup
import requests
import string
import time
import hashlib
import json
import os
import random
#百度翻译api的url，以及appid和密钥
api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
my_appid = '20151113000005349'
cyber = 'osubCEzlGjzvw8qdQc41'
lower_case = list(string.ascii_lowercase)
num = 0
#请求百度翻译API进行翻译，返回Json格式请求
def requests_for_dst(word):
    # init salt and final_sign
    salt = str(time.time())[:10]
    final_sign = str(my_appid) + word + salt + cyber
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    # 区别en,zh构造请求参数
    if list(word)[0] in lower_case:

        paramas = {
            'q': word,
            'from': 'en',
            'to': 'zh',
            'appid': '%s' % my_appid,
            'salt': '%s' % salt,
            'sign': '%s' % final_sign
        }

        my_url = api_url + '?appid=' + str(
            my_appid) + '&q=' + word + '&from=' + 'en' + '&to=' + 'zh' + '&salt=' + salt + '&sign=' + final_sign

    else:
        paramas = {
            'q': word,
            'from': 'en',
            'to': 'zh',
            'appid': '%s' % my_appid,
            'salt': '%s' % salt,
            'sign': '%s' % final_sign
        }
        my_url = api_url + '?appid=' + str(
            my_appid) + '&q=' + word + '&from=' + 'en' + '&to=' + 'zh' + '&salt=' + salt + '&sign=' + final_sign
    response = requests.get(api_url, params=paramas).content
    content = str(response, encoding="utf-8")
    json_reads = json.loads(content)
    try:
        return json_reads['trans_result'][0]['dst']
    except KeyError as e:
        print("error")
        return ""

def translate(word):
    return requests_for_dst(word)

# import requests
# import bs4
# import shutil
# import urllib
# import re
# import os
# import xml.dom.minidom
# def getLogin(loginurl):
#
#     # rs = requests.get(loginurl)
#     # html = rs.text
#     # with open('ai.xml', "wb") as f:
#     #      html = f.read()
#     # print(html)
#     # soup = BeautifulSoup(html, 'lxml')
#     # text = soup.find_all('pattern')
#     # print(text)
#     # verifyurl = soup.find_all('img',id='captcha-img')[0]['src']
#     # verifyurl = loginurl+verifyurl
#     # print(verifyurl)
#     # conn = urllib.request.urlopen(verifyurl)
#     # path = "verifyimage.jpg"
#     # with open(path, "wb") as f:
#     #     f.write(conn.read())
# getLogin('http://210.42.121.241')

#遍历XML标签标记的树结构，同时对字符串进行翻译
def tranverse(tag):
    try:
        for child in tag.children:
            try:
                c = child.children
                tranverse(child)
            except AttributeError:
                chinese = translate(str(child))
                print(chinese)
                time.sleep(1.5)
                if num % 10 == 0:
                    time.sleep(2)
                child.replace_with(chinese)
    except AttributeError:
        return

#对xml里面的categories进行翻译	
def xmlTranslate(src,dest):
    with open(src, 'r') as infile:
        xml = infile.read()
    with open(dest,'a') as outfile:
        soup = BeautifulSoup(xml, 'lxml')
        xml = soup.find_all('category')
        for item in xml:
            item = str(item).replace('\n', '')
            tag = BeautifulSoup(item, 'lxml').find_all('category')[0]
            print(tag)
            tranverse(tag)
            print(tag)
            outfile.write(str(tag))
            outfile.write('\n')
        #         # outfile.close()
        #         # item = str(xml).replace('\n', '')
        #         # tag = BeautifulSoup(item, 'lxml').find_all('category')[0]
        #         # tranverse(tag)
#对文件夹里面的所有文件进行翻译
def TranslateAll(srcfolder,destfolder):
    for root, dirs, files in os.walk(srcfolder):
        for fn in files:
            xmlTranslate(srcfolder+"/"+fn,destfolder+"/"+fn)
            print(fn+" has been translated")
#对文件夹里面的aiml文件进行命名，改成txt文件
def rename(folder):
    for parent, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            newName=filename.split('.')[0]+'.'+'txt'
            os.rename(os.path.join(parent, filename), os.path.join(parent, newName))
if __name__ == '__main__':
    # xmlTranslate('ai.txt','ai-c.txt')
    # rename('alice-e')
    # rename('standard-e')
    # tag = BeautifulSoup('<category><pattern>HAVE WHAT</pattern><template><srai>what do you have</srai></template></category>', 'lxml').find_all('category')[0]
    # print(tag)
    # tranverse(tag)
    # print(tag)
	#翻译alice-c文件夹里面的文件到alice-e
    TranslateAll('alice-e','alice-c')