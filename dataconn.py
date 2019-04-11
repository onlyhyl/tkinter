# dbfile = 'std.db'
#
# def getconn():
#     try:
#         import sqlite3
#         conn = sqlite3.connect(dbfile)
#         return conn
#     except Exception as ex:
#         print('数据库访问出错：', ex)
#         raise ex

def getconn():
    try:
        import pymysql
        conn = pymysql.Connect('localhost', 'root', 'h', 'manage', charset='utf8')
        return conn
    except Exception as ex:
        print('数据库访问出错：', ex)
        raise ex