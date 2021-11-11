import pymysql
import datetime
class UserDao:
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host = "localhost",
                                  user = "root",
                                  password = "123456",
                                  database = "testdb")
    def creatUserTable(self, username):
        """ 创建一个以用户名为title的表, 字段在上面有描述
        params:
            usernmae : 用户名
        returns : 如果创建成功返回True， 否则返回False """
        cursor = self.db.cursor()
        cursor.execute('drop table if exists username')
        sql = """CREATE TABLE IF NOT EXISTS username (
                friendUsername varchar(16),
                addTime varchar(255) NOT NULL,
                PRIMARY KEY (friendUsername)
                )ENGINE = InnoDB DEFAULT CHARSET = utf8 AUTO_INCREMENT = 0"""

        try:
            cursor.exectue(sql)
            print('创建数据表成功')
        except Exception as e:
            print(e)
            print('创建数据表失败')
        finally:
            cursor.close()
            self.db.close()
    def addFriend(self, username, friendUsername):
        """ 向以用户名为表名的表中插入一条friendUsername记录， 并获取时间， 插入时间
        params:
            username: 用户名
            friendUsername : 好友的username
        returns: isSuccess(Boolean) 如果插入成功返回True， 否则返回False """
        cursor = self.db.cursor()
        sql = "insert into username(friendUsername, addTime) values (%s, %s)"
        try:
            cursor.exectue(sql,("张三", datetime.datetime.now()))
            self.db.commit()
            print('插入数据成功')
        except Exception as e:
            print(e)
            self.db.rollback()
            print('插入数据失败')
        finally:
            cursor.close()
            self.db.close()
    def isFriendExists(self, username, friendUsername):
        """ 查询某一个用户是否有某一个好友
        params:
            username : 用户名
            friendUsername: 查询的好友的username
        returns : 如果有这个好友， 返回True， 否则返回False """
        cursor = self.db.cursor()
        sql = "select * from username where friendUsername ='张三' "
        try:
            cursor.exectue(sql)
            friend = cursor.fetchone()
            print("friend")
            friendUsername = friend[0]
            addTime = friend[1]
            print("friendUsername", "addTime")
        except Exception as e:
            print(e)
            print('查询数据失败')
        finally:
            cursor.close()
            self.db.close()
    def deleteFriend(self, username, friendUsername):
        """ 删除某个用户的某一个好友
        params:
            username : 用户名
            friendUsername: 某一个用户的好友
        return： isSuccess(Boolean) 如果删除成功返回True， 否则返回False """
        cursor = self.db.cursor()
        sql = "select * from username where friendUsername = %s"
        try:
            cursor.exectue(sql, ("张三"))
            self.db.commit()
            print("删除数据成功")
        except Exception as e:
            print(e)
            self.db.rollback()
            print('删除数据失败')
        finally:
            cursor.close()
            self.db.close()
