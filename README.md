# TcpServer 说明

## 配置参数

配置文件采用yaml文件格式

- address 服务器地址
- port 开放端口
- buffersize 消息接收缓存区大小
- max_connection 最大连接数

```yaml
tcp_address : "127.0.0.1"
tcp_port : 4567
buffersize : 1024
max_connection : 12

mysql_username : "root"
mysql_host : "127.0.0.1"
mysql_pwd : "root"
mysql_database : "test" 
mysql_port : 3306

mongodb_address : "mongodb://localhost:27017/"
mongodb_database : "test"
```





## 消息流

消息流的数据格式采用json格式

具体的信息交互的规则就是：

```json
"type":"" // 这里定义信息的类型， 也是区分信息功能的关键
```

- login

  ```json
  "type":"login"
  "username":"..."
  "password":"..."
  ```

- register

  ```json
  "type":"register"
  "username":"..."
  "password":"..."
  "gender":"male" // "female"
  "age":16
  "nickname":"" // 昵称
  ```

- send msg(text) to someone else

  ```json
  "type":"sendmsg"
  "sender":""
  "receiver":""
  "msg":"..."
  ```

- send file to someone else(optional)

  ```json
  //"type":"sendfile"
  //"sender":""
  //"receiver":""
  ```

- search user by username

  ```json
  "type":"search"
  "username":"xxx"
  ```

  ```json
  
  [
      {"username":"xxx", "gender":"xxx", "nickName":"xxx", "age":20},
      {}
  	
  ]
  ```
  
  - 添加好友
    ```json
      "type":"addFriend"
      "recv_user":"userA"
      "send_user":"userB"
    ```

  

## 数据表

- mysql

  - **user表**：
    	username : (key) varchar(16)

    ​	password : varchar(16)

    ​	gender : varchar(8)

    ​	age : int

    ​	nickName : varchar(32)

  - **(以每一个用户的用户名命名的表)**

    ​	friendUsername : (key) varchar(16)

    ​	addTime : Time -- 加好友的时间

  - 设计接口：

    ```python
    class UserDao:
        def __init__(self, host, user, password, database):
            self.db = pymysql.connect(host = host,
                                       user = user,
                                       password = password,
                                       database = database)
            
    
        # 关于用户账户的操作
        def isUserExists(self, username):
            """
            查询用户是否存在
            params:
                username : 用户名
            returns:
                存在返回True, 否则False
            """
    
            pass
    
        def getInfo(self, username):
            """
            根据用户名返回user的信息
            params:
                username : 用户名
            returns:
                {"gender" : gender, "age" : age, "nickName" : nickName}
                如果username不存在, 返回None
            """
            
            pass
    
        def getPwd(self, username):
            """
            根据用户名返回对应user的密码
            params:
                username : 用户名
            returns:
                pwd(str)
                如果用户名不存在， 返回None
            """
            pass
    
        def insertUser(self, username, password, gender, age, nickName):
            """
            向数据表中插入数据
            params:
                username :  用户名
                password : 密码
                gender : 性别
                age : 年龄
                nickName : 昵称
            returns:
                isSuccess(Boolean)因为username是key值， 所以如果username与表中其他值重复就会
                插入失败， 插入失败返回False， 插入成功返回True
            """
            
            pass
    
        def changePwd(self, username, newPwd):
            """
    		改变user表中对应user的pwd
    		params :
    			username : 用户名
    			newPwd : 新的密码
    		returns :
    			isSuccess(Boolean) 如果username不存在返回False， 修改成功返回True
            """
            pass
    
        def changeGender(self, username, newGender):
            """
    
            """
            pass
    
        def changeAge(self, username, newAge):
            """
    
            """
            pass
    
        def changeNickname(self, username, nickName):
            """
    
            """
    		pass
        
        
        
        # 关于好友的操作
        def creatUserTable(self, username):
            """
            创建一个以用户名为title的表, 字段在上面有描述
            params:
            	usernmae : 用户名
            returns :
            	如果创建成功返回True， 否则返回False
            """
            
            pass
      
        def addFriend(self, username, friendUsername):
            """
            向以用户名为表名的表中插入一条friendUsername记录， 并获取时间， 插入时间
            params:
            	username: 用户名
            	friendUsername : 好友的username
            returns:
            	isSuccess(Boolean) 如果插入成功返回True， 否则返回False
            """
            pass
        
        def isFriendExists(self, username, friendUsername):
            """
            查询某一个用户是否有某一个好友
            params:
            	username : 用户名
            	friendUsername: 查询的好友的username
            returns : 
            	如果有这个好友， 返回True， 否则返回False
            """
            pass
        
        def deleteFriend(self, username, friendUsername):
            """
            删除某个用户的某一个好友
            params:
            	username : 用户名
            	friendUsername: 某一个用户的好友
            return：
            	isSuccess(Boolean) 如果删除成功返回True， 否则返回False
            """
            pass
            
    ```
    
    

- msgHistory (mongodb) 信息记录

  mongodb中需要对每用户创建一个collection

  每一个用户的collection中保存着该用户的消息记录

  字段：

  - SendTime  消息发送的时间
  - receiver  消息接者的username
  - msg  消息

  ```python
  class UserMsgDao:
      def __init__(self, mongodb_address, database):
          self.client = pymongo.MongoClient(mongodb_address)
          self.dbDao = self.client[database]
          
  	def createCollection(self, username):
          """
          创建以username为名字的collection
  		params:
  			username : 用户名
  		"""
          pass
      
      def insertMsg(self, username, time, receiver, msg):
         	"""
         	向指定user的消息表中插入信息记录
         	params:
         		username : 信息的发送者
         		time : 消息产生的时间
         		reveiver : 消息的接受者
         		msg : 消息
         	returns:
  			如果插入成功返回True， 否则返回False
         	"""
          pass
      
      def getMsgByUsernameReceiver(self, username, receiver):
          """
          根据指定的username和receiver， 从指定的user表中查询出指定reveiver的消息记录
          就是筛选出指定receiver的消息记录
          params:
          	username : 指定的user消息记录表
          	receiver : 指定的receiver
          returns:
          	a list that contains all the msg tuples that meets the criteria
          """
          pass
      
      def deleteByUsername(self, username):
          """
          删除指定的collection
          params:
          	username : 指定的user信息表
          returns:
          	如果删除成功返回True， 否则False
          """
          pass
      
  ```
  
  
  
  

