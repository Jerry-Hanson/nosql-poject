from bson import json_util
from PyQt5.QtCore import QThread
from bson import json_util
import json
from utils.ConfigFileReader import ConfigFileReader

con = ConfigFileReader('../config/client_config.yaml')
buffersize = con.info['buffersize']
def sendMsg(socket, type, info):#type 实现的功能, info 实际包含的数据.
    """
    info的类型为字典!!!!
    在消息的末尾加上一个结束符
    :param socket:
    :param msg:
    :return:
    """
    msg = processMsgDict(info)
    info = json_util.dumps(info)
    send_msg = {"id": msg, "type": type, "info": info}
    send_msg_copy = send_msg.copy()
    send_msg = json_util.dumps(send_msg)
    send_msg = send_msg + "\0"
    socket.send(send_msg.encode("utf-8"))
    return send_msg_copy["id"]    #返回消息的哈希值以便后续查找服务器返回的消息


def processMsgDict(info_dict):
    """
    给发送的消息字典添加id
    :param info_dict:
    :return:
    """
    return hash(MsgFlag(info_dict))


def recvMsg(socket, buffersize):
    """
    堵塞式接收消息, 当接收到结束符时停止接收消息
    :param socket:
    :param buffersize:
    :return:
    """
    str = ""
    while True:
        buf = socket.recv(buffersize).decode("utf-8")
        print(buf)
        str += buf
        if buf.endswith("\0"):
            str = str.strip("\0")
            break
    msg = json_util.loads(str)
    return msg


class MsgFlag:
    """
    用于生成 hash - Id 的一个工具类， 用于生成不同的hash
    """

    def __init__(self, *args):
        self.li = args

# if __name__ == "__main__":
#     info = {"type": "login", "username": "jerry", "password": "jerry"}
#     #传过去的字典可能包含的元素{"id":,"sender":,"recevier":."message_type":,"message":,"serve_type":,"password":,}
#     print(processMsgDict(info))
