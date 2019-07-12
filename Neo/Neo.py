# coding=gbk
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, walk

graph = Graph('http://localhost:7474',username='neo4j',password='root')

# a = Node("Person", name="aaa")
# b = Node("Person", name="bbb")
# graph.create(a|b)
# r = Relationship(a, "knows", b)
# graph.create(a|b|r)


# 作者：邹鑫
# 作用：创建一个node并提交
# labels : 即CQL中的 <label-name> ,可以有多个
# node_properties_list : 要增加的node的属性，以字典的形式传入,如：name = "a",id = 10
# return : 创建的node
def create_node(*labels, **node_properties_list):
    node = Node(*labels, **node_properties_list)
    graph.create(node)
    return node


# 作者：邹鑫
# 作用：创建一个relationship并提交
# nodes : node,可以有多个
# properties : 要增加的relationship的属性，以字典的形式传入,如：name = "a",id = 10
# return : 创建的relationship
# 注意，每次插入只插入一个关系，且参数格式为（from_node,关系名,to_node,properties字典）
def create_relationship(*nodes,**properties):
    relationship = Relationship(*nodes,**properties)
    graph.create(relationship)
    return relationship


# 作用：删除一个节点
# 作者：邹鑫
# node : 节点对象
def delete_node(node):
    graph.delete(node)


# 作用：删除一个节点数组
# 作者：邹鑫
# 能删除node数组吗？
# node : 节点对象
def delete_nodes(nodes):
    for node in nodes:
        graph.delete(node)


# 作用：删除一个关系
# 作者：邹鑫
# relationship : 关系对象
def delete_relationship(relationship):
    graph.delete(relationship)


# 作用：删除一个关系数组
# 作者：邹鑫
# relationships : 关系对象数组
def delete_relationships(relationships):
    for relationship in relationships:
        graph.delete(relationship)


# 作用：一个node的修改,但不会提交到数据库中，要提交需用push
# 作者：邹鑫
# node : 要修改的node对象
# data ： 要更新的内容
def update_node(node, **data):
    node.update(data)


# 作用：多个nodes的修改，但不会提交到数据库中，要提交需用push
# 作者：邹鑫
# nodes : node 的数组或元组，只要能使用for循环的node的集合皆可
# data ： 要更新的内容
def update_nodes(nodes, **data):
    for node in nodes:
        node.update(data)


# 作用：单个relationship的修改，但不会提交到数据库中，要提交需用push
# 作者：邹鑫
# relationship : 要修改的relationship对象
# data : 要更新的内容
def update_relationship(relationship,**data):
    relationship.update(data)


# 作用：多个relationship的修改，但不会提交到数据库中，要提交需用push
# 作者：邹鑫
# relationship : 要修改的relationship数组或元组，只要能使用for循环的relationship的集合皆可
# data : 要更新的内容
def update_relationships(relationships, **data):
    for relationship in relationships:
        relationship.update(data)


# 作用 ： 通过条件（也可以不写条件，则返回所有相同标签的）查询node，返回一个node的list
# 作者 : 石亮禾
# node_label sting : node_label
# where string : 查询条件，其中用下划线"_"来表示节点名，如："_.name = \"abc\""
# return : 查询的node的list
# 示例 ： res = search_nodes("Person","_.name = \'bbb\'")
def search_nodes(node_label, where=""):
    if where == "":
        node_matcher = NodeMatcher(graph)
        res = node_matcher.match(node_label)
        return list(res)
    else:
        node_matcher = NodeMatcher(graph)
        res = graph.nodes.match(node_label).where(where)
        return list(res)


# 作用：返回查找到的关系的集合（list类型）
# 作者：石亮禾
# 参数（都是String类型）：rel_type:关系类型，node1:前节点，node2：后节点
# 三个参数都是必选项，但是如果不想具体指定可以用双引号“”代替
def search_relationships(rel_type = '',node1 = '',node2 = ''):
    # data = graph.run('match (a:A)-[r:R]-(b:B) return r')
    data = []
    if rel_type == '':
        if node1 == '' and node2 == '':
            data += list(graph.match())
        elif node1 != '' and node2 != '':
            for node_1 in node1:
                for node_2 in node2:
                    data = list(graph.match((node_1, node_2), r_type=None))
        elif node2 == '':
            for node_1 in node1:
                data = list(graph.match((node_1, None), r_type=None))
        else:
            for node_2 in node2:
                data = list(graph.match((None, node_2), r_type=None))
    else:
        if node1 == '' and node2 == '':
            data += list(graph.match(r_type=rel_type))
        elif node1 != '' and node2 != '':
            for node_1 in node1:
                for node_2 in node2:
                    data = list(graph.match((node_1, node_2), r_type=rel_type))
        elif node2 == '':
            for node_1 in node1:
                data = list(graph.match((node_1, None), r_type=rel_type))
        else:
            for node_2 in node2:
                data = list(graph.match((None, node_2), r_type=rel_type))
        # data = graph.match(nodes=None,r_type=rel_type)
    # print(list(data))
    # data = graph.run('match (a:A) return a')
    print(data)
    return data

# 作用：将所做的修改提交到数据库中
# 作者：邹鑫
# subgraph : 需要提交修改的子graph
def push_one(subgraph):
    graph.push(subgraph)


# 作用：将所做的修改提交到数据库中
# 作者：邹鑫
# subgraphs : 需要提交修改的子graph的集合
def push_many(subgraphs):
    for subgraph in subgraphs:
        graph.push(subgraph)


# 作用：在node或relationship上的某一label的某一属性上建立索引
# 作者：邹鑫
# # label : node或relationship的label(要建立索引的label)
# # property : node或relationship的property(要建立索引的property)
def create_index_on(label, property):
    graph.run("create index on:%s(%s)" % (label, property))


# 未测试
# 作用：将node或relationship上的某一索引删除
# 作者：邹鑫
# label : node或relationship的label(要删除索引的label)
# property : node或relationship的property(要删除索引的property)
def drop_index_on(label, property):
    graph.run("drop index on:%s(%s)" % (label, property))


# 作用：将node或relationship上的某一label的某一属性设为Unique
# 作者：石亮禾
# label: node或relationship的label(要设为Unique的property的label)
# property : node或relationship的property(要设为Unique的property)
def set_unique(label, property):
    graph.run("CREATE CONSTRAINT ON (cc:%s) ASSERT cc.%s IS UNIQUE" % (label, property))


# 作用：将node或relationship上的某一label的某一属性的Unique约束取消
# 作者：石亮禾
# label: node或relationship的label(要取消Unique的property的label)
# property : node或relationship的property(要取消Unique的property)
def drop_unique(label, property):
    graph.run("DROP CONSTRAINT ON (cc:%s) ASSERT cc.%s IS UNIQUE" % (label, property))



# a = create_node("A",name="a")
# b = create_node("B",name="b")
# c = create_node("C",name="c")
# d = create_node("D",name="d")

# create_relationship(a,b,c,"haha")


#delete_nodes(search_nodes("Person","_.name = \'ccc\'"))
# node = search_nodes("Person","_.name = \'aaa\'")
# update_nodes(node,name="vvv")
# push_many(node)
# print(node)
#node = search_nodes("Person")
# delete_nodes(node)

#delete_node(node[0])
#print(node)
# print(search_nodes("Person"))

# res = search_nodes("Person")
# a = Node("Person", name="ccc")
# graph.create(a)
# update_node(a,name="d")
#print(list(res))
# print(res)

# node = Node("B",name=1)
# graph.create(node)
# node["name"] = 3


#create_index_on("Person","name")
#drop_index_on("Person","name")

#set_unique("Person","name")
#drop_unique("Person","name")