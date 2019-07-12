from  stanfordcorenlp import StanfordCoreNLP
#"张红轩明天后天长沙武汉美国中国13日周六腾讯谷歌基金股价"
with StanfordCoreNLP(r'C:\Users\Admin\Desktop\stanford-corenlp-full-2018-10-05\stanford-corenlp-full-2018-10-05', lang='zh') as nlp:
        text = input("请输入：")
        print(nlp.word_tokenize(text))
        print(nlp.pos_tag(text))
        print(nlp.ner(text))
        print(nlp.parse(text))
        print(nlp.dependency_parse(text))
        # print(nlp.coref(text))

# 预先设置好的意图槽
slots = (
    {
        "tags": "ticket",
        "component": {
            "type":{
                "important":"true",
                "content":"",
                "q":"what ticket do you want to buy?"
            },
            "LOCATION":{
                "important":"true",
                "content":"",
                "q":"where do you want to buy?"
            },
            "DATE":{
                "important":"false",
                "content":"",
                "q":"when"
            },
            "number":{
                "important":"false",
                "content":"",
                "q":"only yourself?"
            }
        }
    },
    {
        "tags": "weather",
        "component": {
            "type":{
                "content":"",
                "q":"what ticket do you want to buy?"
            },
            "where":{
                "content":"",
                "q":"where do you want to buy?"
            },
            "when":{
                "content":"",
                "q":"when"
            },
            "number":{
                "content":"",
                "q":"only yourself?"
            }
        }
    }
)

def intent(sentence):
    #调用意图分析方法
    return "ticket"

# 待改进：话题突然强行转换
def multi_interact():
    inputs = []
    print("robot:hi! Can I help you?")
    answer = input("I:")
    inputs.append(answer)
    yitu = intent(inputs[len(inputs) - 1])

    # 搜寻到指定意图槽
    i = 0
    while slots[i]["tags"] != yitu and i < len(slots):
        i += 1

    # # print(ner)
    # for key in slots[i]["component"]:
    #     k = 0
    #     while k < len(ner):
    #         if key in ner[k]:
    #             slots[i]["component"][key]["content"] = ner[k][1]
    #             k += 1
    #             break
    #         k += 1


    if i < len(slots):
        # 抽取出其中已有的槽位
        ner = nlp.ner(inputs[len(inputs) - 1])
        for key in slots[i]["component"]:
            for tupe in ner:
                if key == tupe[1]:
                    slots[i]["component"][key]["content"] = tupe[0]
                    break
        # 遍历意图槽中的槽位
        for key in slots[i]["component"]:
            if slots[i]["component"][key]["content"] == "":
                if slots[i]["component"][key]["important"] == "true":
                    # 可以添加一个模块，利用信息抽取抽取回复中的特定词类
                    print("robot:"+slots[i]["component"][key]["q"])
                    answer = input("I:")
                    ner = nlp.ner(answer)
                    for k in ner: # 遍历抽取结构
                        for key in slots[i]["component"]:
                            if k[1] == key:
                                slots[i]["component"][key]["content"] = k[0]
                                break
                    # 存在一个问题，即如果用户回答的问题不被识别成功，则会导致该空缺位直接被跳过
                    # 如果用户直接转移话题，还需要设计一个意图识别来判断用户是否存在明显的话题转移。
                    inputs.append(answer)

    print(slots[i]["component"])

multi_interact()
