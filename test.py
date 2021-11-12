import pymysql

db = pymysql.connect(user = "root", password = "root", host = "127.0.0.1",
                database = "nosql", port = 3306)
cur = db.cursor()
sql = "select * from jerry where friendUsername = %s"
cur.execute(sql, ('jerry',))
print(cur.fetchone())

