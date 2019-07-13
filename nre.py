import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
import pprint
#接口地址
url1 = "http://ltpapi.xfyun.cn/v1/dp"
url2 = "http://ltpapi.xfyun.cn/v1/cws"
url3 = "http://ltpapi.xfyun.cn/v1/pos"
url4 = "http://ltpapi.xfyun.cn/v1/srl"
#开放平台应用ID
x_appid = "5d18c2d0"
#开放平台应用接口秘钥
api_key = "5c942addd1f019273733dca398188d21"
#语言文本
TEXT = "你知道姚明的身高是多少吗"

def main():
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url1, body, x_header)
    result = urllib.request.urlopen(req)
    result = json.loads(result.read().decode('utf-8'))
    arcs = result["data"]["dp"]
    req = urllib.request.Request(url2, body, x_header)
    result = urllib.request.urlopen(req)
    result = json.loads(result.read().decode('utf-8'))
    words = result["data"]["word"]
    print(words)
    req = urllib.request.Request(url3, body, x_header)
    result = urllib.request.urlopen(req)
    result = json.loads(result.read().decode('utf-8'))
    postags = result["data"]["pos"]
    req = urllib.request.Request(url4, body, x_header)
    result = urllib.request.urlopen(req)
    result = json.loads(result.read().decode('utf-8'))
    pprint.pprint(result)
    child_dict_list = build_parse_child_dict(words, postags, arcs)
    print(child_dict_list)
    for index in range(len(postags)):
        # 抽取以谓词为中心的事实三元组
        if postags[index] == 'v':
            child_dict = child_dict_list[index]
            # 主谓宾
            if 'SBV' in child_dict.keys() and 'VOB' in child_dict.keys():
                e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                r = words[index]
                e2 = complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                print("主语谓语宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
            # 定语后置，动宾关系
            if arcs[index]["relate"] == 'ATT':
                if 'VOB' in child_dict.keys():
                    e1 = complete_e(words, postags, child_dict_list, arcs[index]["parent"] - 1)
                    r = words[index]
                    e2 = complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                    temp_string = r + e2
                    if temp_string == e1[:len(temp_string)]:
                        e1 = e1[len(temp_string):]
                    if temp_string not in e1:
                        print("定语后置动宾关系\t(%s, %s, %s)\n" % (e1, r, e2))
            # 含有介宾关系的主谓动补关系
            if 'SBV' in child_dict.keys() and 'CMP' in child_dict.keys():
                # e1 = words[child_dict['SBV'][0]]
                e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                cmp_index = child_dict['CMP'][0]
                r = words[index] + words[cmp_index]
                if child_dict_list[cmp_index].has_key('POB'):
                    e2 = complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                    print("介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2))


def build_parse_child_dict(words, postags, arcs):
    child_dict_list = []
    for index in range(len(words)):
        child_dict = dict()
        for arc_index in range(len(arcs)):
            if arcs[arc_index]["parent"] == index:
                if arcs[arc_index]["relate"] in child_dict.keys():
                    child_dict[arcs[arc_index]["relate"]].append(arc_index)
                else:
                    child_dict[arcs[arc_index]["relate"]] = []
                    child_dict[arcs[arc_index]["relate"]].append(arc_index)
        child_dict_list.append(child_dict)
    return child_dict_list

def complete_e(words, postags, child_dict_list, word_index):
    child_dict = child_dict_list[word_index]
    prefix = ''
    if 'ATT' in child_dict.keys():
        for i in range(len(child_dict['ATT'])):
            prefix += complete_e(words, postags, child_dict_list, child_dict['ATT'][i])

    postfix = ''
    if postags[word_index] == 'v':
        if 'VOB' in child_dict.keys():
            postfix += complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
        if 'SBV' in child_dict.keys():
            prefix = complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

    return prefix + words[word_index] + postfix

if __name__=='__main__':
    main()