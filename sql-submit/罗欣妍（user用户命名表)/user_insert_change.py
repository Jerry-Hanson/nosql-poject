
# tcp_address : "127.0.0.1" 
# tcp_port : 4567 
# buffersize : 1024 
# max_connection : 12 
# mysql_username : "root" 
# mysql_host : "127.0.0.1" 
# mysql_pwd : "root" 
# mysql_database : "test" 
# mongodb_address : "mongodb://localhost:27017/" 
# mongodb_database : "test"
import pymongo
import pymysql
import pandas as pd
import pymysql
from datetime import datetime
class UserDao: 
    def __init__(self, host, user, password, database): 
        self.db = pymysql.connect(
                                host = 127.0.0.1,
                                port=4567, 
                                user = root, 
                                password = root, 
                                database = 'user',
                                charset = 'utf8'
                                ) 
    def insertUser(self, username, password, gender, age, nickName): 
        """ 
        向数据表中插入数据 
        params: 
            username : 用户名 
            password : 密码 
            gender : 性别 
            age : 年龄 
            nickName : 昵称 
        returns: 
            isSuccess(Boolean)因为username是key值， 所以如果username与表中其 他值重复就会 插入失败， 
            插入失败返回False， 插入成功返回True
        """
        # 读入数据
        file=
        data=
        #获取游标对象
        cursor = self.db.cursor()
        query ='insert into user(self.usernamr,self.password,self.gender,self.age,self.nickName) values (%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql)
            for r in range(0, len(data)):
                username= 
                password=  
                gender= 
                age=
                nickName= 
                values = (varchar(username), varchar(password),varchar(gender),int(age),varchar(nickName))
                cursor.execute(query, values)
        except Exception as e:
            self.db.rollback()
            print("插入数据失败",e)
        else:
            print("插入数据成功",cursor.rowcount)
        #关闭游标，提交，关闭数据库连接
        finally:
            cursor.close()
            db.commit()
            db.close() 

    def changePwd(self, username, newPwd): 
        """ 
        改变user表中对应user的pwd 
        params : 
            username : 用户名 
            newPwd : 新的密码 
        returns : 
            isSuccess(Boolean) 如果username不存在返回False， 修改成功返回True 
        """ 
        #获取游标对象
        cursor = self.db.cursor()
        query ='update from user set newPwd=%s where username='aaa')
        try:
            print("修改数据成功",cursor.rowcount)
        except Exception as e:
            self.db.rollback()
            print("修改数据失败",e)
        #关闭游标，提交，关闭数据库连接
        finally:
            cursor.close()
            db.commit()
            db.close() 


    def changeGender(self, username, newGender): 
        cursor = self.db.cursor()
        query ='update from user set newGender=%s where username='aaa')
        try:
            print("修改数据成功",cursor.rowcount)
        except Exception as e:
            self.db.rollback()
            print("修改数据失败",e)
        #关闭游标，提交，关闭数据库连接
        finally:
            cursor.close()
            db.commit()
            db.close() 
    def changeAge(self, username, newAge): 
        cursor = self.db.cursor()
        query ='update from user set newAge=%s where username='aaa')
        try:
            print("修改数据成功",cursor.rowcount)
        except Exception as e:
            self.db.rollback()
            print("修改数据失败",e)
        #关闭游标，提交，关闭数据库连接
        finally:
            cursor.close()
            db.commit()
            db.close() 