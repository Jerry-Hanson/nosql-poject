import numpy as np
from PyQt5.QtCore import QThread
from bson import json_util
import json
from utils.MsgUtils import recvMsg
from utils.ConfigFileReader import ConfigFileReader

con = ConfigFileReader('../config/client_config.yaml')
buffersize = con.info['buffersize']

# class MsgRecvThread(QThread):
#     """
#     实时消息接收线程
#     """
#     def __init__(self, s, parent_ui, data_list):
#         self.s = s  # socket
#         self.parent_ui = parent_ui  # 好友列表中的ui， 好友列表的ui同时控制着其他聊天窗口的ui和widget
#         self.data_list = data_list
#         super(MsgRecvThread, self).__init__()
#
#     def run(self) -> None:
#         while True:
#             data = recvMsg(self.s, buffersize)
#
#             data_dict = json_util.loads(data)
#             print(f"data_dict: {data_dict}")
#
#             if data_dict['type'] == 'showHistory':
#                 receiver = data_dict['receiver']
#                 info = data_dict['info']
#                 self.parent_ui.ui_dict[receiver].message = info
#
#             elif data_dict['type'] == 'search':
#                 friends = data_dict['info']
#                 self.parent_ui.ui3.friends = friends
#             elif data_dict['type'] == 'searchFriend':
#                 # 刷新好友列表的相应
#                 friends = data_dict['friends']
#                 self.parent_ui.friends = friends
#             else:
#                 # sendMsg
#                 sender = data_dict['sender']
#                 data = data_dict['data']
#                 time = data_dict['time']
#                 print(self.parent_ui.ui_dict.keys())
#                 print("sender", sender)
#                 if sender in self.parent_ui.ui_dict.keys():
#                     #  sender, send_time, msg
#                     self.parent_ui.ui_dict[sender].convert_send(sender, time, data)

class MsgRecvThread(QThread):
    """
    实时消息接收线程
    """
    def __init__(self, s, parent_ui, data_list, username):
        self.s = s  # socket
        self.username = username
        self.parent_ui = parent_ui  # 好友列表中的ui， 好友列表的ui同时控制着其他聊天窗口的ui和widget
        self.data_list = data_list
        super(MsgRecvThread, self).__init__()

    def run(self) -> None:
        while True:
            data_dict = recvMsg(self.s, buffersize)
            recv_info = json_util.loads(data_dict['info'])
            # print(f"data_list: {self.data_list}")

            # 主动式接收消息
            if data_dict["type"] == 'Initiative':
                self.data_list.append(data_dict)
                print(self.data_list)

            #被动式接收数据
            else:
                sender = recv_info['sender']
                data = recv_info['data']
                time = recv_info['time']

                # 发送给群聊
                send_type = recv_info['send_type'] # 是否是群聊的方式发送消息
                print("sender", sender)
                if send_type == "personal":
                    if sender in self.parent_ui.ui_dict.keys():
                        if recv_info["message_type"] == "str":
                            self.parent_ui.ui_dict[sender].convert_send(sender, time, data)
                        elif recv_info["message_type"] == "pic":
                            data = np.array(data)
                            self.parent_ui.ui_dict[sender].convert_Picture(sender, time, data)
                        elif recv_info["message_type"] == "file":
                            self.parent_ui.ui_dict[sender].convert_send(sender, time, data)
                            pass
                elif send_type == "group":
                    group_name = recv_info['group_name']
                    if group_name in self.parent_ui.ui_dict.keys() and sender != self.username:
                        if recv_info["message_type"] == "str":
                            self.parent_ui.ui_dict[group_name].convert_send(sender, time, data)
                        elif recv_info["message_type"] == "pic":
                            data = np.array(data)
                            self.parent_ui.ui_dict[group_name].convert_Picture(sender, time, data)
                        elif recv_info["message_type"] == "file":
                            self.parent_ui.ui_dict[group_name].convert_send(sender, time, data)
                            pass




