# -*-coding:utf-8-*-

from socket import *
import threading
import json
from utils.ConfigFileReader import ConfigFileReader
from sql.UserDao import UserDao


config = ConfigFileReader("config/server_config.yaml")
address = config.info['server_address']
port = config.info['server_port']
buffsize = config.info['buffersize']
s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
# 设置最大连接数
s.listen(config.info['max_connection'])

client_list = []

# 用户名 密码
user_list = [[2097557613, 123456], [2097557614, 123456], [2097557615, 123456], [2097557616, 123456],
             [2097557617, 123456], [2097557618, 123456]]
user_l = len(user_list)
user_client = []
group_list = [['tcp群'], ['兼职群'], ['同学群'], ['学习资料群']]


def getDao():
    dao = UserDao(host=config.info['mysql_host'],
                  port=config.info['mysql_port'],
                  user=config.info['mysql_username'],
                  password=config.info['mysql_pwd'],
                  database=config.info['mysql_database'])
    return dao

def login(username, password):
    """
    将状态分成一下几种， 用户名不存在， 密码错误， （用户已登录）, 登录成功
    :param username:
    :param password:
    :return:
        "UserNotExist",
        "WrongPwd",
        "AlreadyLogin"，
        “Success”
    """
    dao = getDao()
    res = dao.getInfo(username)
    if res is not None:
        # 用户名存在
        if res['password'] == password:
            return "Success"
        else:
            return "WrongPwd"
    else:
        return "UserNotExist"

def search(username):
    dao = getDao()
    info = dao.getInfo(username)
    return info

def register(username, password, gender, age, nickName):
    """
    注册用户， 并返回状态码
    :param username:
    :param password:
    :param gender:
    :param age:
    :param nickName:
    :return:
        "userExists":用户已经存在，
        ”Success“:成功
    """
    dao = getDao()
    if dao.isUserExists(username):
        return "userExists"
    else:
        dao.createUser(username, password, gender, age, nickName)
        dao.createFriendTable(username)
        return "Success"

def addFriend(send_user, recv_user):
    """
    暂时还没有添加好友验证功能
    :param send_user:
    :param recv_user:
    :return:
    """
    dao = getDao()
    dao.addFriend(send_user, recv_user)
    dao.addFriend(recv_user, send_user)


def searchFriend(username):
    """
    查询一个用户的所有好友
    :param username:
    :return:
    """
    dao = getDao()
    friends = dao.getFriends(username)
    friend_list = []
    for friend in friends:
        friend_list.append(friend[0])
    return friend_list


def tcplink(clientsock, clientaddress):
    # group_l = len(group_list)
    while True:
        recvdata = clientsock.recv(buffsize).decode('utf-8')

        if recvdata == '':
            # sock被关闭
            print(clientaddress, "shutdown")
            break
        print(recvdata)
        info_dict = json.loads(recvdata)
        info_type = info_dict['type']

        # 登录
        if info_type == "login":
            username = info_dict['username']
            password = info_dict['password']
            print(username, password)
            # TODO 数据查询
            status = login(username, password)
            # 将状态返回
            clientsock.send(status.encode())

        if info_type == "register":
            username = info_dict['username']
            password = info_dict['password']
            gender = info_dict['gender']
            age = info_dict['age']
            nickName = info_dict['nickName']
            status = register(username, password, gender, age, nickName)
            # 将状态返回
            clientsock.send(status.encode())

        if info_type == "search":
            # 根据指定的username查询所有的个人信息
            username = info_dict['username']
            info = search(username)
            if info is None:
                status = "UserNotExist"
            else:
                status = json.dumps(info)
            print(status)
            clientsock.send(status.encode())

        if info_type == "addFriend":
            send_user = info_dict['send_user']
            recv_user = info_dict['recv_user']
            # log
            print("addFriend", send_user, recv_user)
            # 两个人都要有添加好友的操作
            addFriend(send_user, recv_user)
            addFriend(recv_user, send_user)

        if info_type == "searchFriend":
            username = info_dict['username']
            # log
            print("searchFriend", username)
            friend_list = searchFriend(username)
            info_str = json.dumps(friend_list)
            clientsock.send(info_str.encode())

        # if str(logindata[0])=='login':
        #     login(logindata,clientsock)
        #
        # elif str(logindata[0])=='wechat_req':
        #     #reqci=1
        #     for y in range(0,group_l):
        #         if str(group_list[y][0])==str(logindata[1]):
        #             requser=str(logindata[2])+' '+'加入'
        #             group_list[y].append(clientsock)
        #             groupl=len(group_list[y])
        #             if groupl>2:
        #                 for h in range(1,groupl):
        #                     group_list[y][h].send(requser.encode())
        #             else:
        #                 clientsock.send(requser.encode())
        #             break
        #
        # elif str(logindata[0])=='wechat':
        #     for wl in range(0,group_l):
        #         if str(group_list[wl][0])==str(logindata[1]):
        #             senddata=str(logindata[2])+":"+str(logindata[3])
        #             l = len(group_list[wl])
        #             try:
        #                 if l >=2:
        #                     for x in range(1, l):
        #                         group_list[wl][x].send(senddata.encode())
        #                 else:
        #                     clientsock.send(senddata.encode())
        #                     break
        #                 print("群聊信息" + str(senddata)+str(clientaddress))
        #             except ValueError:
        #                 break
        #
        # elif str(logindata[0])=='personal':
        #     #print(logindata)
        #     user_cl = len(user_client)
        #     #print(user_client)
        #     send_info = str(logindata[1])+":"+str(logindata[3])
        #     z=1
        #     for pl in range(0,user_cl):
        #         if user_client[pl][0]==logindata[2]:
        #             user_client[pl][1].send(send_info.encode())
        #             #clientsock.send(send_info.encode())
        #             break
        #         elif z==user_cl:
        #             back=str(logindata[2])+'不在线'
        #             clientsock.send(back.encode())
        #         z+=1
        #
        # elif str(logindata[0])=='':
        #     print('无法识别：')
        #     print(logindata[0])
        #     break

    clientsock.close()
    # del client_list[-1]


while True:
    clientsock, clientaddress = s.accept()
    client_list.append(clientsock)
    print('connect from:', clientaddress)
    # 每当接收到一个sock的时候就开启一个线程进行tcpLink
    # 多线程处理sock消息
    t = threading.Thread(target=tcplink, args=(clientsock, clientaddress))
    t.start()

s.close()
