def sendMsg(socket, msg):
    """
    在消息的末尾加上一个结束符
    :param socket:
    :param msg:
    :return:
    """
    msg = msg + "\0"
    socket.send(msg.encode("utf-8"))


def processMsgDict(info_dict):
    """
    给发送的消息字典添加id
    :param info_dict:
    :return:
    """
    info_dict.update({"id": hash(info_dict)})
    return info_dict


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
        str += buf
        if buf.endswith("\0"):
            break


class MsgFlag:
    """
    用于生成 hash - Id 的一个工具类， 用于生成不同的hash
    """

    def __init__(self, *args):
        self.li = args

if __name__ == "__main__":
    info = {"type": "login", "username": "jerry", "password": "jerry"}
    MsgFlag(info)
