import datetime
import pymysql

class UserDao:
    def __init__(self, host, user, password, database, port):
        self.db=pymysql.connect(host=host,
                                user=user,
                                password=password,
                                database=database,
                                port=port)

    # 关于好友的操作
    def creatUserTable(self, username):
        # 创建游标对象
        cur=self.db.cursor()
        # 编写创建表的sql
        sql= """
            create table self.username(
            friendUsername varchar(16) not null primary key,
            addTime datetime COMMENT '加好友的时间'
            )
            """
        try:
            # 执行创建表的sql
            cur.execute(sql)
            print("创建表成功")
        except Exception as e:
            print(e)
            print("创建表失败")
        finally:
            # 关闭游标连接
            cur.close()
            # 关闭数据库连接
            self.db.close()

    def addFriend(self, username, friendUsername):
        """ 向以用户名为表名的表中插入一条friendUsername记录， 并获取时间， 插入时间"""
        cur = self.db.cursor()
        sql = "insert into self.username (friendUsername,addTime) values (%s,%s)"
        try:
            # 执行sql
            cur.execute(sql, ("小强",datetime.datetime.now()))
            self.db.commit()
            print("插入数据成功")
        except Exception as e:
            print(e)
            self.db.rollback()
            print("插入数据失败")
        finally:
            # 关闭游标连接
            cur.close()
            # 关闭数据库连接
            self.db.close()

    def isFriendExists(self, username, friendUsername):
        """ 查询某一个用户是否有某一个好友"""
        cur = self.db.cursor()
        # 编写查询的sql
        sql = "select * from self.username where friendUsername=self.friendUsername"
        try:
            # 执行sql
            cur.execute(sql)
            # 处理结果集
            friend=cur.fetchone()

            print("查询成功！")
            print("好友：", friend[0],"添加好友时间：",friend[1])
        except Exception as e:
            print(e)
            print("查询失败")
        finally:
            # 关闭游标连接
            cur.close()
            # 关闭数据库连接
            self.db.close()

    def deleteFriend(self, username, friendUsername):
        """ 删除某个用户的某一个好友"""
        cur = self.db.cursor()
        # 编写删除的sql
        sql = 'delete from self.username where friendUsername=%s'
        try:
            # 执行sql
            cur.execute(sql,self.friendUsername)
            self.db.commit()
            print("删除成功")
        except Exception as e:
            print(e)
            self.db.rollback()
            print("删除失败")
        finally:
            # 关闭游标连接
            cur.close()
            # 关闭数据库连接
            self.db.close()