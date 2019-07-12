'''import pymysql


def add():
    # 1.建立连接
    conn = pymysql.connect(
        host = "localhost",
        port = 3306,
        db = "sports_sys",
        user = "root",
        password = "root",
        charset = "utf8"
    )
    # 2.获得游标对象
    cls = conn.cursor()
    # 3.执行sql语句
    row = cls.execute("sql  value(%s,%s)",['name1','name2'])#mysql里不管是整数还是什么，统一用%s
    conn.commit()
    print(row)
    cls.close()
    conn.close()

# 查询


def show():
    # 1.建立连接
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="sports_sys",
        user="root",
        password="root",
        charset="utf8"
    )
    # 2.获得游标对象
    cls = conn.cursor()
    cls.execute()
    c = cls.fetchone()#单条查询

    c = cls.fetchall()#多条查询   返回二维元组

    cls.close()
    conn.close()
'''