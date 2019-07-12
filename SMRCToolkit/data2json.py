import json


# 1.作者：邹鑫、石亮禾、张红轩
# 2.作用：将一个问题和相应的有答案的文章转化为能被CMRCReader读取的json文件
# 3.用法：首先，json文件的格式为：
#         (1) 整个文件为一个list，list中的元素是article
#         (2) 每个article是一个字典：{context_id:"string",context_text:"string",qas:[question_answer],title:"string"}
#         (3) 每个question_answer是一个字典：{query_text:"string" ,query_id:"string" ,answers:[answer]}
#         (4) 每个answer是一个字符串
#        使用时，先创建一个对象translator，然后使用将候选文章做成一个list，调用add_data(question,contexts)设置内容，再调用
#        translate(path)输出，path为json文件的保存地址
class JsonTranstlator:
    def __init__(self):
        self._article_list = []

    # 作用：在_article_list 中添加一个article
    # article ：即为要添加的article
    def _add_article(self, article):
        self._article_list.append(article)

    # 作用：添加需要的内容
    # question： 问题  string
    # contexts： 文章   string的list
    # 注： 此函数可以调用多次，之后再调用translate函数，即：将要加入的数据分多次加入
    def add_data(self, question, contexts):
        i = len(self._article_list)
        for context in contexts:
            context_id = "CONTEXT_"+str(i)
            query_id = context_id+"_QUERY_0"
            title = "答案候选文章"+str(i)
            qas = self._get_qas(query_id,question)
            article = self._get_article(context_id,context,qas,title)
            print(article)
            print(i)
            self._article_list.append(article)
            i += 1


    # 作用：通过文章的id，内容，问答对，标题获得一个article字典
    # context_id：文章id   string
    # context_text：文章内容 string
    # qas：问答对  qas，一个list
    # title：文章标题  string
    def _get_article(self, context_id, context_text, qas, title):
        article = {}
        article["context_id"] = context_id
        article["context_text"] = context_text
        article["qas"] = qas
        article["title"] = title
        return article

    # 作用：通过问题的id，内容获得qas（问答对）
    # query_id：问题的id  string
    # query_text：问题的内容 string
    def _get_qas(self, query_id, query_text):
        qas = []
        question_answer = {}
        question_answer["query_id"] = query_id
        question_answer["query_text"] = query_text
        qas.append(question_answer)
        return qas

    # 作用：将加入的数据转换为json文件
    # path：输出路径  string
    def translate(self, path):
        json_str = json.dumps(self._article_list)
        with open(path, 'w') as json_file:
            json_file.write(json_str)


#示例：
# question = "问题"
# contexts1 = ["文章内容1","文章内容2","文章内容3","文章内容4"]
# contexts2 = ["文章内容5"]
# translator = JsonTranstlator()
# translator.add_data(question,contexts1)
# translator.add_data(question,contexts2)
# translator.translate("F:/zx.json")