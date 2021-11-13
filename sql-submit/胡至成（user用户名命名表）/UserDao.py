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
            return 1
        else:
            return 0
            # 返回值
            # if rows:
            #     return 1
            # else:
            #     return 0

    def getInfo(self, username):
        """
        根据用户名返回user的信息
        params:
            username : 用户名
        returns:
        {"gender" : gender, "age" : age, "nickName" : nickName}
        如果username不存在, 返回None
        """
        username = input('输入用户名:').strip()
        # sql语句
        sql = 'select * from user where username = %s'
        rows = self.cursor.execute(sql, username)
        res= self.cursor.fetchone()
        self.cursor.close()
        return res
# i=UserDao()
# print(i.getInfo("huhu"))
    def getPwd(self, username):
        """
        根据用户名返回对应user的密码
        params:
        username : 用户名
        returns:
        pwd(str)
        如果用户名不存在， 返回None
        """
        username = input('输入用户名:').strip()
        # sql语句
        sql = 'select * from user where username = %s'
        rows = self.cursor.execute(sql, username)
        res = self.cursor.fetchone()
        self.cursor.close()
        return res[1]
# i=UserDao()
# print(i.getPwd("huhu"))
    def changeNickname(self, username, nickName):
        """ """
        username = input('输入用户名:').strip()
        sql = 'update user set nickName=%s where username=%s'
        update_data = ['new_nickName']
        rows = self.cursor.execute(sql, nickName)
        res = self.cursor.fetchone()
        self.cursor.close()
        return res[5]
        print('修改成功')

