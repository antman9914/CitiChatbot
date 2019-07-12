# coding=gbk
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, walk

graph = Graph('http://localhost:7474',username='neo4j',password='root')

# a = Node("Person", name="aaa")
# b = Node("Person", name="bbb")
# graph.create(a|b)
# r = Relationship(a, "knows", b)
# graph.create(a|b|r)


# ���ߣ�����
# ���ã�����һ��node���ύ
# labels : ��CQL�е� <label-name> ,�����ж��
# node_properties_list : Ҫ���ӵ�node�����ԣ����ֵ����ʽ����,�磺name = "a",id = 10
# return : ������node
def create_node(*labels, **node_properties_list):
    node = Node(*labels, **node_properties_list)
    graph.create(node)
    return node


# ���ߣ�����
# ���ã�����һ��relationship���ύ
# nodes : node,�����ж��
# properties : Ҫ���ӵ�relationship�����ԣ����ֵ����ʽ����,�磺name = "a",id = 10
# return : ������relationship
# ע�⣬ÿ�β���ֻ����һ����ϵ���Ҳ�����ʽΪ��from_node,��ϵ��,to_node,properties�ֵ䣩
def create_relationship(*nodes,**properties):
    relationship = Relationship(*nodes,**properties)
    graph.create(relationship)
    return relationship


# ���ã�ɾ��һ���ڵ�
# ���ߣ�����
# node : �ڵ����
def delete_node(node):
    graph.delete(node)


# ���ã�ɾ��һ���ڵ�����
# ���ߣ�����
# ��ɾ��node������
# node : �ڵ����
def delete_nodes(nodes):
    for node in nodes:
        graph.delete(node)


# ���ã�ɾ��һ����ϵ
# ���ߣ�����
# relationship : ��ϵ����
def delete_relationship(relationship):
    graph.delete(relationship)


# ���ã�ɾ��һ����ϵ����
# ���ߣ�����
# relationships : ��ϵ��������
def delete_relationships(relationships):
    for relationship in relationships:
        graph.delete(relationship)


# ���ã�һ��node���޸�,�������ύ�����ݿ��У�Ҫ�ύ����push
# ���ߣ�����
# node : Ҫ�޸ĵ�node����
# data �� Ҫ���µ�����
def update_node(node, **data):
    node.update(data)


# ���ã����nodes���޸ģ��������ύ�����ݿ��У�Ҫ�ύ����push
# ���ߣ�����
# nodes : node �������Ԫ�飬ֻҪ��ʹ��forѭ����node�ļ��ϽԿ�
# data �� Ҫ���µ�����
def update_nodes(nodes, **data):
    for node in nodes:
        node.update(data)


# ���ã�����relationship���޸ģ��������ύ�����ݿ��У�Ҫ�ύ����push
# ���ߣ�����
# relationship : Ҫ�޸ĵ�relationship����
# data : Ҫ���µ�����
def update_relationship(relationship,**data):
    relationship.update(data)


# ���ã����relationship���޸ģ��������ύ�����ݿ��У�Ҫ�ύ����push
# ���ߣ�����
# relationship : Ҫ�޸ĵ�relationship�����Ԫ�飬ֻҪ��ʹ��forѭ����relationship�ļ��ϽԿ�
# data : Ҫ���µ�����
def update_relationships(relationships, **data):
    for relationship in relationships:
        relationship.update(data)


# ���� �� ͨ��������Ҳ���Բ�д�������򷵻�������ͬ��ǩ�ģ���ѯnode������һ��node��list
# ���� : ʯ����
# node_label sting : node_label
# where string : ��ѯ�������������»���"_"����ʾ�ڵ������磺"_.name = \"abc\""
# return : ��ѯ��node��list
# ʾ�� �� res = search_nodes("Person","_.name = \'bbb\'")
def search_nodes(node_label, where=""):
    if where == "":
        node_matcher = NodeMatcher(graph)
        res = node_matcher.match(node_label)
        return list(res)
    else:
        node_matcher = NodeMatcher(graph)
        res = graph.nodes.match(node_label).where(where)
        return list(res)


# ���ã����ز��ҵ��Ĺ�ϵ�ļ��ϣ�list���ͣ�
# ���ߣ�ʯ����
# ����������String���ͣ���rel_type:��ϵ���ͣ�node1:ǰ�ڵ㣬node2����ڵ�
# �����������Ǳ�ѡ���������������ָ��������˫���š�������
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

# ���ã����������޸��ύ�����ݿ���
# ���ߣ�����
# subgraph : ��Ҫ�ύ�޸ĵ���graph
def push_one(subgraph):
    graph.push(subgraph)


# ���ã����������޸��ύ�����ݿ���
# ���ߣ�����
# subgraphs : ��Ҫ�ύ�޸ĵ���graph�ļ���
def push_many(subgraphs):
    for subgraph in subgraphs:
        graph.push(subgraph)


# ���ã���node��relationship�ϵ�ĳһlabel��ĳһ�����Ͻ�������
# ���ߣ�����
# # label : node��relationship��label(Ҫ����������label)
# # property : node��relationship��property(Ҫ����������property)
def create_index_on(label, property):
    graph.run("create index on:%s(%s)" % (label, property))


# δ����
# ���ã���node��relationship�ϵ�ĳһ����ɾ��
# ���ߣ�����
# label : node��relationship��label(Ҫɾ��������label)
# property : node��relationship��property(Ҫɾ��������property)
def drop_index_on(label, property):
    graph.run("drop index on:%s(%s)" % (label, property))


# ���ã���node��relationship�ϵ�ĳһlabel��ĳһ������ΪUnique
# ���ߣ�ʯ����
# label: node��relationship��label(Ҫ��ΪUnique��property��label)
# property : node��relationship��property(Ҫ��ΪUnique��property)
def set_unique(label, property):
    graph.run("CREATE CONSTRAINT ON (cc:%s) ASSERT cc.%s IS UNIQUE" % (label, property))


# ���ã���node��relationship�ϵ�ĳһlabel��ĳһ���Ե�UniqueԼ��ȡ��
# ���ߣ�ʯ����
# label: node��relationship��label(Ҫȡ��Unique��property��label)
# property : node��relationship��property(Ҫȡ��Unique��property)
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