from multiprocessing import Process

from PyQt5.QtCore import QThread
from bson import json_util
import json

class MsgRecvThread(QThread):
    """
    实时消息接收线程
    """
    def __init__(self, s, parent_ui):
        self.s = s  # socket
        self.parent_ui = parent_ui  # 好友列表中的ui， 好友列表的ui同时控制着其他聊天窗口的ui和widget
        super(MsgRecvThread, self).__init__()

    def run(self) -> None:
        while True:
            data = ""
            while True:
                buf = self.s.recv(1024).decode('utf-8')
                data += buf
                if len(buf) < 1024:
                    break
            # send msg
            data_dict = json_util.loads(data)
            print(f"data_dict: {data_dict}")

            if data_dict['type'] == 'showHistory':
                receiver = data_dict['receiver']
                info = data_dict['info']
                self.parent_ui.ui_dict[receiver].message = info

            elif data_dict['type'] == 'search':
                friends = data_dict['info']
                self.parent_ui.ui3.friends = friends
            elif data_dict['type'] == 'searchFriend':
                # 刷新好友列表的相应
                friends = data_dict['friends']
                self.parent_ui.friends = friends
            else:
                # sendMsg
                sender = data_dict['sender']
                data = data_dict['data']
                time = data_dict['time']
                print(self.parent_ui.ui_dict.keys())
                if sender in self.parent_ui.ui_dict.keys():
                    #  sender, send_time, msg
                    self.parent_ui.ui_dict[sender].convert_send(sender, time, data)



