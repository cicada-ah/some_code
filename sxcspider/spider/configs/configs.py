import pymysql.cursors
TEST_DB = {'host': '127.0.0.1',
           'user': 'root',
           'password': 'asdasd',
           'db': 'sxcdb',
           'charset': 'utf8mb4',
           'cursorclass': pymysql.cursors.DictCursor,
           }
