import pymysql
from datetime import datetime

class UserDao:
    def __init__(self, host, port, user, password, database):
        self.db = pymysql.connect(host=host,
                                  port=port,
                                  user=user,
                                  password=password,
                                  database=database)


        # 关于用户账户的操作

    def isUserExists(self, username):
        """
        查询用户是否存在
        params:
            username : 用户名
        returns:
            存在返回True, 否则False
        """
        cursor = self.db.cursor()
        # sql语句
        sql = 'select * from user where username = %s'
        rows = cursor.execute(sql, username)
        return rows

    def getInfo(self, username):
        """
        根据用户名返回user的信息
        params:
            username : 用户名
        returns:
            {"password" : password, "gender" : gender, "age" : age, "nickName" : nickName}
        如果username不存在, 返回None
        """
        # sql语句
        cursor = self.db.cursor()
        sql = 'select * from user where username = %s'
        rows = cursor.execute(sql, username)

        if rows == 0:
            # 没有该用户
            return None

        res = cursor.fetchone()
        cursor.close()
        return {"password": res[1], 'gender': res[2], 'age': res[3], 'nickName': res[4]}

    def changeNickname(self, username, newNickName):
        cursor = self.db.cursor()
        sql = "update user set nickName = %s where username = %s"
        rows = cursor.execute(sql, (newNickName, username,))
        if rows == 0:
            return False
        self.db.commit()
        cursor.close()
        return True

    def changePwd(self, username, newPassword):
        cursor = self.db.cursor()
        sql = "update user set password = %s where username = %s"
        rows = cursor.execute(sql, (newPassword, username,))
        if rows == 0:
            return False
        self.db.commit()
        cursor.close()
        return True

    def changeAge(self, username, newAge):
        cursor = self.db.cursor()
        sql = "update user set age = {} where username = %s"
        rows = cursor.execute(sql.format(str(newAge)), (username,))
        if rows == 0:
            return False
        self.db.commit()
        cursor.close()
        return True

    def createUser(self, username, password, gender, age, nickName):
        cursor = self.db.cursor()
        sql = "insert into user values(%s, %s, %s, {}, %s)"
        cursor.execute(sql.format(age), (username, password, gender, nickName))
        self.db.commit()
        cursor.close()


    def createFriendTable(self, username):
        cursor = self.db.cursor()
        sql = "create table {} (friendUsername varchar(32) primary key, addTime varchar(32))"
        cursor.execute(sql.format(username))
        self.db.commit()
        sql = "insert into {} values(%s, %s)"
        time_now = datetime.now()
        time_str = '-'.join([str(time_now.year), str(time_now.month), str(time_now.day)])
        cursor.execute(sql.format(username), ('QQ机器人', time_str,))
        self.db.commit()
        cursor.close()

    # 单方面的向一个用户的表中添加好友
    def addFriend(self, send_user, recv_user):
        cursor = self.db.cursor()
        time_now = datetime.now()
        time_str = '-'.join([str(time_now.year), str(time_now.month), str(time_now.day)])
        sql = "insert into {} values(%s, %s)"
        cursor.execute(sql.format(send_user), (recv_user, time_str, ))
        self.db.commit()
        cursor.close()

    # 获取一个用户的所有好友
    def getFriends(self, username):
        cursor = self.db.cursor()
        sql = "select friendUsername from {}"
        cursor.execute(sql.format(username))
        res = cursor.fetchall()
        self.db.commit()
        cursor.close()
        return res

if __name__ == "__main__":
    dao = UserDao(host="localhost", port=3306, user='root', password='root',
                  database='nosql')
    print(dao.getFriends("jerry"))
