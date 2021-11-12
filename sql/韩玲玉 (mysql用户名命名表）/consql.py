import pymysql
import datetime

class UserDao:
    def __init__(self, host, user, password, database, port):
        """
        init the mysql connector
        :param host:
        :param user:
        :param password:
        :param database:
        :param port:
        """
        self.db = pymysql.connect(host = host,
                                  user = user,
                                  password = password,
                                  database = database,
                                  port = port)

    def __del__(self):
        self.db.close()

    def isUserExists(self, username):
        """
        查询指定的表是否存在
        :param username:
        :return:
        """
        username = username.lower()
        cursor = self.db.cursor()
        cursor.execute("show tables")
        tables = cursor.fetchall()
        cursor.close()
        for table in tables:
            if table[0].strip() == username.strip():
                return True

        return False

    def createUserTable(self, username):
        """ 创建一个以用户名为title的表, 字段在上面有描述
        params:
            usernmae : 用户名
        returns : 如果创建成功返回True， 否则返回False """
        username = username.lower()
        cursor = self.db.cursor()
        # 表已经存在， 创建失败
        if self.isUserExists(username):
            return False

        sql = """CREATE TABLE IF NOT EXISTS {} (
                friendUsername varchar(16) UNIQUE,
                addTime varchar(255) NOT NULL,
                PRIMARY KEY (friendUsername)
                )ENGINE = InnoDB DEFAULT CHARSET = utf8 AUTO_INCREMENT = 0"""
        try:
            cursor.execute(sql.format(username))
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            print('创建数据表失败')
            return False
        finally:
            cursor.close()

    def addFriend(self, username, friendUsername):
        """ 向以用户名为表名的表中插入一条friendUsername记录， 并获取时间， 插入时间
        params:
            username: 用户名
            friendUsername : 好友的username
        returns: isSuccess(Boolean) 如果插入成功返回True， 否则返回False """
        username = username.lower()

        cursor = self.db.cursor()
        sql = "insert into {}(friendUsername, addTime) values (%s, %s)"
        try:
            cursor.execute(sql.format(username), (friendUsername, datetime.datetime.now()))
            self.db.commit()

            # LOG
            print('插入数据成功')

            return True
        except Exception as e:
            print(e)
            self.db.rollback()

            # LOG
            print('插入数据失败')

            return False
        finally:
            cursor.close()

    def isFriendExists(self, username, friendUsername):
        """ 查询某一个用户是否有某一个好友
        params:
            username : 用户名
            friendUsername: 查询的好友的username
        returns : 如果有这个好友， 返回这个好友的info (friendUsername, addTime)， 否则返回None"""
        cursor = self.db.cursor()
        sql = "select * from {} where friendUsername = %s"
        try:
            cursor.execute(sql.format(username), (friendUsername, ))
            info = cursor.fetchone()
            return info
        except Exception as e:
            print(e)
            print('查询数据失败')
        finally:
            cursor.close()

    def deleteFriend(self, username, friendUsername):
        """ 删除某个用户的某一个好友
        params:
            username : 用户名
            friendUsername: 某一个用户的好友
        return： isSuccess(Boolean) 如果删除成功返回True， 否则返回False """

        cursor = self.db.cursor()
        sql = "delete from {} where friendUsername = %s"
        try:
            cursor.execute(sql.format(username), (friendUsername))
            self.db.commit()
            print("删除数据成功")
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            print('删除数据失败')
            return False
        finally:
            cursor.close()


if __name__ == "__main__":

    dao = UserDao(host = '127.0.0.1', user = 'root', password = 'root',
                  database = 'nosql', port = 3306)
    print(dao.deleteFriend("jerry", "hurry"))