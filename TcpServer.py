# -*-coding:utf-8-*-

from socket import *
import threading
import json
from utils.ConfigFileReader import ConfigFileReader
from sql.UserDao import UserDao
from sql.MongodbDao import MongodbDao
from bson import json_util

config = ConfigFileReader("config/server_config.yaml")
address = config.info['server_address']
port = config.info['server_port']
buffsize = config.info['buffersize']
s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
# 设置最大连接数
s.listen(config.info['max_connection'])
connect_ip = dict()  # 用来建立用户和其对应的ip的联系
connect_socket = dict()  # 用来建立ip和套接字之间的联系


def getDao():
    dao = UserDao(host=config.info['mysql_host'],
                  port=config.info['mysql_port'],
                  user=config.info['mysql_username'],
                  password=config.info['mysql_pwd'],
                  database=config.info['mysql_database'])
    return dao


def getMongodbDao():
    dao = MongodbDao()
    return dao


def searchmongoDB(myname, sendname):  # 查找mogodb中的聊天记录
    dao = MongodbDao()
    filter_1 = {"send_user": str(myname), "recv_user": str(sendname)}
    chatlist_1 = dao.search(str(myname), str(sendname), filter_1)
    filter_2 = {"send_user": str(sendname), "recv_user": str(myname)}
    chatlist_2 = dao.search(str(sendname), str(myname), filter_2)
    chatlist = chatlist_1 + chatlist_2
    return chatlist


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


def send_Message(send_user, recv_user, data, send_time):
    # 向MongoDB中写入聊天记录
    try:
        mongodao = getMongodbDao()
        # 把数据存入MongoDB
        data = [{"send_user": str(send_user), "recv_user": str(recv_user), "msg": data, 'date': send_time}]
        mongodao.insert(send_user, recv_user, data)
    except:
        return False
    else:
        return 'Success'


def tcplink(clientsock, clientaddress):
    global connect_ip
    global connect_socket

    while True:
        recvdata = clientsock.recv(buffsize).decode('utf-8')
        user_ip, user_port = clientaddress

        if recvdata == '':
            # sock被关闭
            print(clientaddress, "shutdown")
            for i in list(connect_ip):
                if connect_ip[i] == str(user_ip) + '-' + str(user_port):
                    print(1)
                    del connect_ip[i]
                    del connect_socket[i]
            break

        info_dict = json.loads(recvdata)
        info_type = info_dict['type']

        # log
        print(f'recv data:{recvdata}')
        print(f"msg type:{info_type}")

        # 登录
        if info_type == "login":
            username = info_dict['username']
            password = info_dict['password']
            # 数据查询
            status = login(username, password)
            # 判断如果登录成功, 那需要将sock保存到dict中
            if status == 'Success':
                connect_ip.update({username: str(user_ip) + '-' + str(user_port)})
                connect_socket.update({username: clientsock})
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
                status = {"type":"search", "info":"UserNotExists"}
            else:
                status = {"type":"search", "info":info}
            status_str = json.dumps(status)
            clientsock.send(status_str.encode())

        if info_type == "addFriend":
            send_user = info_dict['send_user']
            recv_user = info_dict['recv_user']
            # 两个人都要有添加好友的操作
            addFriend(send_user, recv_user)

        if info_type == "searchFriend":
            username = info_dict['username']
            friend_list = searchFriend(username)
            info = {'type': "searchFriend", "friends":friend_list}
            info_str = json.dumps(info)
            clientsock.send(info_str.encode())

        if info_type == "sendMessage":
            send_user = info_dict['sender']
            recv_user = info_dict['receiver']
            data = info_dict["msg"]
            time_send = info_dict["time"]
            send_Message(send_user, recv_user, data, time_send)  # 把数据存入本地的MongoDB中
            message = {'type':'sendMsg', 'sender': send_user, 'data': data, 'time': time_send}
            data2 = json.dumps(message)
            # 将数据抓发给接受者
            if recv_user in list(connect_socket) and data:
                # 如果用户socket在线就把消息发送给客户端
                connect_socket[recv_user].send(data2.encode())


        if info_type == "chatList":
            send_user = info_dict['sender']
            recv_user = info_dict['receiver']
            info = searchmongoDB(send_user, recv_user)

            if info is None:
                status = {'type':'showHistory', 'receiver':recv_user, "info":[]}
            else:
                status = {'type':'showHistory', 'receiver':recv_user, "info":info}
            data_str = json_util.dumps(status)
            clientsock.send(data_str.encode())  # 把聊天记录发送回去

    clientsock.close()


while True:
    clientsock, clientaddress = s.accept()
    print('connect from:', clientaddress)
    # 每当接收到一个sock的时候就开启一个线程进行tcpLink
    # 多线程处理sock消息
    t = threading.Thread(target=tcplink, args=(clientsock, clientaddress))
    t.start()

s.close()
