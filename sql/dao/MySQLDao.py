import pymysql
from datetime import datetime


class MySQLDao:
    def __init__(self, host, port, user, password, database):
        self.db = pymysql.connect(host=host,
                                  port=port,
                                  user=user,
                                  password=password,
                                  database=database)

    def selectAll(self, table):
        """
        返回一张表中的所有信息
        :param table: 
        :return: 
        """
        cursor = self.db.cursor()
        sql = "select * from {}"
        cursor.execute(sql.format(table))
        res = cursor.fetchall()
        self.db.commit()
        cursor.close()
        return res

    def execute(self, sql, *args):
        cursor = self.db.cursor()
        cursor.execute(sql, args)
        self.db.commit()
        res = cursor.fetchall()
        cursor.close()
        return res


    def selectAllTable(self):
        cursor = self.db.cursor()
        sql = "show tables"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return [i[0] for i in res]

    def dropTable(self, table):
        cursor = self.db.cursor()
        sql = "drop table {}"
        cursor.execute(sql.format(table))
        self.db.commit()
        cursor.close()

    def __del__(self):
        self.db.close()


if __name__ == "__main__":
    dao = MySQLDao(host='localhost', port=3306, user='root', password='root',
                   database='nosql')
    print(dao.selectAll("user"))