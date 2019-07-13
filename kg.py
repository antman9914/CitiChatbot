from aip import AipNlp
import json
import requests
import pprint
import jiagu

def nerampnre(s):
    url = "https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/entity_annotation?access_token=24.fad79cad786319ff766ad2ba20a4558d.2592000.1564404489.282335-16676547"
    data = json.dumps({"data": s})
    r = requests.post(url, data)
    data = json.loads(r.text)
    # concept1 = []
    # concept2 = []
    mention = []
    confidence = []
    for e in data['entity_annotation']:
        # concept1.append(e['concept']['level1'])
        # concept2.append(e['concept']['level2'])
        mention.append(e['mention'])
        confidence.append(e["confidence"])
    print(mention)
    print(confidence)
    print("\n")

    APP_ID = '16676547'
    API_KEY = '60m3VTOI0XOGrrPmVerKrnjH'
    SECRET_KEY = 'ockik3nG7wLvrZR0xcy7BjxHtwp6b1ZU'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    dt = client.depParser(s)
    items = dt['items']
    child_list = build_list(items)
    print(child_list)
    pprint.pprint(dt)

    for index in range(len(child_list)):
        child_dict = child_list[index]
        # 抽取以谓词为中心的事实三元组
        if items[index]["postag"] == 'v':
            # 主谓宾
            if "SBV" in child_dict.keys() and "VOB" in child_dict.keys():
                e1 = complete_e(items, child_list, child_dict["SBV"][0])
                r = items[index]["word"]
                e2 = complete_e(items, child_list, child_dict["VOB"][0])
                print("主谓宾:"+e1+"->"+r+"->"+e2)
            # 动宾关系
            if items[index]["deprel"] == 'ATT':
                if 'VOB' in child_dict.keys():
                    e1 = complete_e(items, child_list, items[index]["head"] - 1)
                    r = items[index]["word"]
                    e2 = complete_e(items, child_list, items[index]['VOB'][0])
                    temp_string = r+e2
                    if temp_string == e1[:len(temp_string)]:
                        e1 = e1[len(temp_string):]
                    if temp_string not in e1:
                        print("动宾:"+e1+"->"+r+"->"+e2)
            # 介宾关系
            if 'SBV' in child_dict.keys() and 'CMP' in child_dict.keys():
                e1 = complete_e(items, child_list, child_dict['SBV'][0])
                cmp_index = child_dict['CMP'][0]
                r = items[index]["word"] + items[cmp_index]["word"]
                if 'POB' in child_dict[cmp_index].keys():
                    e2 = complete_e(items, child_list, child_list[cmp_index]['POB'][0])
                    print("介宾:"+e1+"->"+r+"->"+e2)
        #的关系
        elif items[index]["deprel"] == "DE" and items[index]["word"] == "的":
            e1 = complete_e(items, child_list, child_dict['DE'][0])
            e2 = complete_e(items, child_list, items[index]["head"] - 1)
            print("的结构:"+e1+"->"+e2)
        #部分状语前置信息
        elif items[index]["deprel"] == "ADV" and "POB" in child_dict.keys():
            e1 = complete_e(items, child_list, child_dict["POB"][0])
            e2 = complete_e(items, child_list, items[index]["head"] - 1)
            print("状语前置:"+e1+"->"+e2)

def build_list(items):
    lists = []
    for i in range(len(items)):
        tmp = {}
        for j in range(len(items)):
            if items[j]["head"] == i + 1:
                if items[j]["deprel"] in tmp.keys():
                    tmp[items[j]["deprel"]].append(j)
                else:
                    tmp[items[j]["deprel"]] = []
                    tmp[items[j]["deprel"]].append(j)
        lists.append(tmp)
    return lists

def complete_e(items, child_list, word_index):
    prefix = ''
    if "ATT" in child_list[word_index].keys():
        for i in range(len(child_list[word_index]["ATT"])):
            prefix += complete_e(items, child_list, child_list[word_index]['ATT'][i])
    postfix = ''
    if items[word_index]["postag"] == 'v':
        if 'VOB' in child_list[word_index].keys():
            postfix += complete_e(items, child_list, child_list[word_index]['VOB'][0])
        if 'SBV' in child_list[word_index].keys():
            prefix = complete_e(items, child_list, child_list[word_index]['SBV'][0]) + prefix
    if "COO" in child_list[word_index].keys():
        for i in range(len(child_list[word_index]["COO"])):
            postfix += complete_e(items, child_list, child_list[word_index]["COO"][0])

    return prefix + items[word_index]["word"] + postfix

if __name__=="__main__":
    nerampnre("既可用于送存现金也可用于转账的支票是什么支票")
