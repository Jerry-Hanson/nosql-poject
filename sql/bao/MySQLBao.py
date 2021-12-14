import sys

sys.path.append('../')
from sql.dao.MySQLDao import MySQLDao
from datetime import datetime


class MySQLBao:
    """
    业务层
    """

    def __init__(self, host, port, user, password, database):
        self.dao = MySQLDao(host, port, user, password, database)

    def createUser(self, username: str, password: str, gender: str, age: str, nickname: str) -> None:
        """
        创建用户
        :param username:
        :param password:
        :param gender:
        :param age:
        :param nickname:
        :return:
        """
        # 创建用户的好友列表
        createFriendListTableSql = "create table {} (`friendUsername` varchar(32) primary key, `addTime` varchar(32) not null )"
        self.dao.execute(createFriendListTableSql.format(username))

        # 创建用户的群聊列表
        createGroupListTableSql = "create table {} (`groupName` varchar(32) primary key, `addTime` varchar(32))"
        self.dao.execute(createGroupListTableSql.format(username + "_grouplist"))

        # 添加机器人
        sql = "insert into {} values(%s, %s)"
        time_now = datetime.now()
        time_str = '-'.join([str(time_now.year), str(time_now.month), str(time_now.day)])
        self.dao.execute(sql.format(username), "robot", time_str)

        # 向总表中添加用户信息
        insertUserInfoSql = "insert into user values(%s, %s, %s, %s, %s)"
        self.dao.execute(insertUserInfoSql, username, password, gender, age, nickname)

        # TODO 创建mongodb的记录表

    def addFriend(self, usera, userb):
        time_now = datetime.now()
        time_str = '-'.join([str(time_now.year), str(time_now.month), str(time_now.day)])
        sql = "insert into {} values(%s, %s)"
        # 两个人的好友列表中都要加入信息
        self.dao.execute(sql.format(usera), userb, time_str)
        self.dao.execute(sql.format(userb), usera, time_str)

    def isUserExist(self, username):
        if username in self.dao.selectAllTable():
            return True
        else:
            return False

    def getUserInfo(self, username):
        """
        返回指定用户名的所有信息
        :param username:
        :return:
        """
        sql = "select * from user where username = %s"
        res = self.dao.execute(sql, username)[0]
        return {"username": res[0], "password": res[1], "gender": res[2],
                "age": res[3], "nickName": res[4]}

    def getPwd(self, username):
        sql = "select password from user where username = %s"
        res = self.dao.execute(sql, username)
        return res[0][0]

    def getAllFriend(self, username):
        """
        获取一个用户的所有好友
        :param username:
        :return:
        """
        sql = "select friendUsername from {}"
        res = self.dao.execute(sql.format(username))
        return [i[0] for i in res]

    def createGroup(self, groupName):
        # 创建群聊
        sql = "create table {} (`username` varchar(32) primary key not null, `addTime` varchar(32))".format(groupName)
        self.dao.execute(sql)

        # 在总的群聊表中添加这个群
        time_now = datetime.now()
        time_str = '-'.join([str(time_now.year), str(time_now.month), str(time_now.day)])
        sql = "insert into `group` values(%s, %s)"
        self.dao.execute(sql, groupName, time_str)

    def joinGroup(self, username, groupName):
        time_now = datetime.now()
        time_str = '-'.join([str(time_now.year), str(time_now.month), str(time_now.day)])
        # 在群的用户列表中添加用户
        sql1 = "insert into {} values(%s, %s)".format(groupName)
        # 在用户的群列表中添加表记录
        sql2 = "insert into {} values(%s, %s)".format(username + "_grouplist")
        self.dao.execute(sql1, username, time_str)
        self.dao.execute(sql2, groupName, time_str)

    def isGroupExists(self, group_name):
        if group_name in self.dao.selectAllTable():
            return True
        else:
            return False

    def getGroupsByUser(self, username):
        # 获取一个用户添加的所有群聊
        res = self.dao.selectAll(username + "_grouplist")
        return [s[0] for s in res]

    def getAllUserByGroup(self, group_name):
        # 获取一个群聊中所有的用户
        res = self.dao.selectAll(group_name)
        return [s[0] for s in res]


if __name__ == "__main__":
    bao = MySQLBao("localhost", 3306, "root", "root", "nosql")
    print(bao.getUserInfo("jerry"))
