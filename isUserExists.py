import pymysql

class UserDao:
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='',
                                  database='hh',
                                  charset='utf8')

        #创建游标
        self.cursor = self.db.cursor()

        # 关于用户账户的操作
    def isUserExists(self, username):
        """
        查询用户是否存在
        params:
        username : 用户名
        returns:
        存在返回True, 否则False
        """
        username = input('输入用户名:').strip()
        # sql语句
        sql = 'select * from user where username = %s'
        rows = self.cursor.execute(sql, username)

        self.cursor.close()
            # 测试
        if rows:
            print("用户名存在")
        else:
            print("用户名不存在")
            # 返回值
            # if rows:
            #     return 1
            # else:
            #     return 0
# i=UserDao()
# i.isUserExists("huhu")