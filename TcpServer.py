# -*-coding:utf-8-*-
from socket import *
import threading
import json
from utils.ConfigFileReader import ConfigFileReader
from sql.bao.MySQLBao import MySQLBao
from sql.MongodbDao import MongodbDao
from bson import json_util
from utils.ConnectedSockPool import ConnectedSockPool

config = ConfigFileReader("config/server_config.yaml")
address = config.info['server_address']
port = config.info['server_port']
buffersize = config.info['buffersize']
s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
# 设置最大连接数
s.listen(config.info['max_connection'])

# connected client socket pool
sockedPool = ConnectedSockPool()


def getBao():
    bao = MySQLBao(host=config.info['mysql_host'],
                   port=config.info['mysql_port'],
                   user=config.info['mysql_username'],
                   password=config.info['mysql_pwd'],
                   database=config.info['mysql_database'])
    return bao


bao = getBao()


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
        "AlreadyLogin",
        “Success”
    """
    if bao.isUserExist(username) is False:
        return "UserNotExist"
    elif bao.getPwd(username) == password:
        return "Success"
    else:
        return "WrongPwd"


def search(username):
    info = bao.getUserInfo(username)
    return info


def register(username, password, gender, age: str, nickName):
    """
    注册用户， 并返回状态码
    :param username:
    :param password:
    :param gender:
    :param age:
    :param nickName:
    :return:
        "userExists":用户已经存在
        ”Success“:成功
    """
    if bao.isUserExist(username):
        return "userExists"
    else:
        bao.createUser(username, password, gender, age, nickName)
        return "Success"


def addFriend(send_user, recv_user):
    """
    暂时还没有添加好友验证功能
    :param send_user:
    :param recv_user:
    :return:
    """
    bao.addFriend(send_user, recv_user)


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


def readMsg(clientsock, buffersize):
    msg = ""
    while True:
        buf = clientsock.recv(buffersize).decode('utf-8')
        # 这里的特例需要单独判别
        if buf == "":
            return ""
        msg += buf
        if buf.endswith("\0"):  # 加入消息终止标记
            break
    return msg[:-1]


def tcplink(clientsock, clientaddress):
    user_ip, user_port = clientaddress
    try:
        while True:
            recvdata = readMsg(clientsock, buffersize)

            if recvdata == '':
                # sock被关闭
                print(clientaddress, "shutdown")
                if sockedPool.has(user_ip, user_port):
                    sockedPool.delSocket(user_ip, user_port)

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
                    sockedPool.add(user_ip, username, clientsock)

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
                    status = {"type": "search", "info": "UserNotExists"}
                else:
                    status = {"type": "search", "info": info}
                status_str = json.dumps(status)
                clientsock.send(status_str.encode())

            if info_type == "addFriend":
                send_user = info_dict['send_user']
                recv_user = info_dict['recv_user']
                # 两个人都要有添加好友的操作
                addFriend(send_user, recv_user)

            if info_type == "searchFriend":
                username = info_dict['username']
                friend_list = bao.getAllFriend(username)
                info = {'type': "searchFriend", "friends": friend_list}
                info_str = json.dumps(info)
                clientsock.send(info_str.encode())

            if info_type == "sendMessage":
                send_user = info_dict['sender']
                recv_user = info_dict['receiver']
                data = info_dict["msg"]
                time_send = info_dict["time"]
                send_Message(send_user, recv_user, data, time_send)  # 把数据存入本地的MongoDB中
                message = {'type': 'sendMsg', 'sender': send_user, 'data': data, 'time': time_send}
                data2 = json.dumps(message)
                # 将数据抓发给接受者
                # if recv_user == 'QQ机器人':  # 机器人的对话
                #     import requests
                #     import urllib
                #     import time
                #     response = requests.get(
                #         url='http://api.qingyunke.com/api.php',
                #         params={
                #             'key': 'free',
                #             'appid': 0,
                #             'msg': urllib.parse.quote(data)
                #         })
                #     if response.status_code == 200:
                #         content = response.json()
                #         time_now = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                #         send_Message(recv_user, send_user, content['content'], time_now)
                #         message = {'type': 'sendMsg', 'sender': 'QQ机器人', 'data': content['content'], 'time': time_now}
                #         data3 = json.dumps(message)
                #         # connect_socket[send_user].send(data3.encode())
                # else:
                if sockedPool.isAlive(recv_user) and data:  # 和好友对话
                    # 如果用户socket在线就把消息发送给客户端
                    sockedPool.getSocket(recv_user).send(data2.encode())

            if info_type == "chatList":
                send_user = info_dict['sender']
                recv_user = info_dict['receiver']
                info = searchmongoDB(send_user, recv_user)

                if info is None:
                    status = {'type': 'showHistory', 'receiver': recv_user, "info": []}
                else:
                    status = {'type': 'showHistory', 'receiver': recv_user, "info": info}
                data_str = json_util.dumps(status)
                clientsock.send(data_str.encode())  # 把聊天记录发送回去
    except ConnectionResetError as e:
        if sockedPool.has(user_ip, user_port):
            sockedPool.delSocket(user_ip, user_port)
    clientsock.close()


while True:
    clientsock, clientaddress = s.accept()
    print('connect from:', clientaddress)
    # 每当接收到一个sock的时候就开启一个线程进行tcpLink
    # 多线程处理sock消息
    t = threading.Thread(target=tcplink, args=(clientsock, clientaddress))
    t.start()

s.close()
