import json
import typing

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from functools import partial
import time
from PyQt5.QtWidgets import *
from bson import json_util
import threading
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
import re
import cv2

from ui.login import Ui_MainWindow

"""class RecvMsgThread(QThread):

    def __init__(self, s, ui):
        super(RecvMsgThread, self).__init__()
        self.s = s
        self.ui = ui


    def run(self):
        while True:
            data = ""
            while True:
                buf = self.s.recv(1024).decode('utf-8')
                print(buf)
                data += buf
                if len(buf) < 1024:
                    break
            try:
                print(data)
                data2 = json.loads(data)
            except Exception as ret:
                # try:
                print(data)
                data2 = json_util.loads(data)
            if isinstance(data2, list):
                self.ui.message = data2
            else:
                self.ui.convert_send(data2)
"""

class WidgetChat(QtWidgets.QWidget):
    """
    自定义聊天窗口的widget， 修改closeEvent
    关闭窗口的时候删除父窗口（hylb）中dict对应的窗口对象
    """
    def __init__(self, parent_ui, friendUsername):
        self.parent_ui = parent_ui
        self.friendUsername = friendUsername
        super(WidgetChat, self).__init__(None)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        del self.parent_ui.widget_dict[self.friendUsername]
        del self.parent_ui.ui_dict[self.friendUsername]
        a0.accept()

class UiChat():

    def __init__(self, s, sendname, myname):
        self.s = s
        self.sendname = sendname
        self.myname = myname

        # print('thread starting')
        # self.thread = RecvMsgThread(s, self)


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 650)
        Form.setMinimumSize(QtCore.QSize(750, 650))
        Form.setMaximumSize(QtCore.QSize(1000, 1000))
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 750, 650))
        self.frame.setMinimumSize(QtCore.QSize(750, 650))
        self.frame.setMaximumSize(QtCore.QSize(750, 650))
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 750, 60))
        self.label.setMinimumSize(QtCore.QSize(750, 60))
        self.label.setMaximumSize(QtCore.QSize(750, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./pics/1.png"))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(0, 110, 750, 360))
        self.textBrowser.setMinimumSize(QtCore.QSize(750, 360))
        self.textBrowser.setMaximumSize(QtCore.QSize(750, 360))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(0, 500, 750, 150))
        self.textEdit.setMinimumSize(QtCore.QSize(750, 150))
        self.textEdit.setMaximumSize(QtCore.QSize(750, 150))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(0, 470, 750, 30))
        self.label_2.setMinimumSize(QtCore.QSize(750, 30))
        self.label_2.setMaximumSize(QtCore.QSize(750, 30))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./pics/4.png"))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(0, 10, 750, 40))
        self.label_3.setMinimumSize(QtCore.QSize(750, 40))
        self.label_3.setMaximumSize(QtCore.QSize(750, 40))
        font = QtGui.QFont()
        font.setFamily("Alibaba PuHuiTi")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(540, 610, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 610, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(0, 60, 750, 50))
        self.label_4.setMinimumSize(QtCore.QSize(750, 50))
        self.label_4.setMaximumSize(QtCore.QSize(750, 50))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("./pics/5.png"))
        self.label_4.setObjectName("label_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(650, 471, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.picture = QtWidgets.QPushButton(self.frame)
        self.picture.setGeometry(QtCore.QRect(215, 473, 28, 26))
        self.picture.setMinimumSize(QtCore.QSize(28, 26))
        self.picture.setMaximumSize(QtCore.QSize(28, 26))
        self.picture.setStyleSheet("QPushButton{border-image: url(./pics/7.png)}\n"
                                   "QPushButton:hover{border-image: url(./pics/7-1.png)}\n"
                                   "QPushButton:pressed{border-image: url(./pics/7-2.png)}")
        self.picture.setText("")
        self.picture.setObjectName("picture")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton_2.clicked.connect(self.convert)
        self.textBrowser.setText(str(self.textEdit.toPlainText()))
        self.pushButton_3.clicked.connect(self.history_Message)
        self.picture.clicked.connect(self.select_pic)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:auto; margin-right:auto; -qt-block-indent:0; text-indent:0px;\"><img src=\":/pics/3.png\" /></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align='center'><span style=\" color:#ffffff;\">"+str(self.sendname)+"</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "关闭"))
        self.pushButton_2.setText(_translate("Form", "发送"))
        self.pushButton_3.setText(_translate("Form", "聊天记录"))


    def convert(self):
        # 把自己发送的消息添加到消息显示框中
        data = str(self.textEdit.toPlainText())
        self.time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        self.textBrowser.append("<font color='red'>" + str(self.myname) + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        self.textBrowser.append(data)
        self.sendtoTcpserver(data)
        # 将输入框清空
        self.textEdit.clear()


    def sendtoTcpserver(self, data):
        info_dict = {"type": "sendMessage", "sender": self.myname, "receiver": self.sendname, "msg": data, "time": self.time}
        info_str = json.dumps(info_dict)
        self.s.send(info_str.encode())

    def sendpictoTcpserver(self, data):
        info_dict = {"type": "sendMessage", "sender": self.myname, "receiver": self.sendname, "msg": data.tolist(), "time": self.time}
        info_str = json.dumps(info_dict)
        self.s.send(info_str.encode())

    def history_Message(self):  # 打开聊天的历史记录窗口

        # 从tcp服务器上下载数据显示到文本上
        login_info_dict = {"type": "chatList", "sender": self.myname, "receiver": self.sendname}
        login_info = json.dumps(login_info_dict)

        self.s.send(login_info.encode('utf-8'))

        # 等待线程返回结果
        time.sleep(1)

        # 显示聊天记录窗口
        from chathistory import Ui_Formt2
        self.widget1 = QtWidgets.QWidget()
        # 把sock传到新的窗口中
        self.ui1 = Ui_Formt2(self.myname, self.sendname, self.message)
        self.ui1.setupUi(self.widget1)
        self.widget1.show()

    def convert_send(self, sender, send_time, msg):
        # 向消息界面中添加一条消息
        self.textBrowser.append("<font color='blue' style='position: absolute;right:0px'>" + sender + str(send_time) + "</font>")
        self.textBrowser.append(msg)

    def select_pic(self):
        openfile_name = QFileDialog.getOpenFileName(None, '选择文件', '', "Image Files(*.jpg *.jpeg *.png)")
        pattern = re.compile(r'[^/]*?\.(jpg|png|jpeg)$')
        Pic_name = pattern.search(openfile_name[0])
        if Pic_name != None:
            import cv2  #导入cv2
            pic = cv2.imread(openfile_name[0])
            a, b, c = pic.shape
            print(a, b)
            a, b = self.reshapePic(a, b)
            print(a, b)
            res = cv2.resize(pic, (a, b))
            self.write_Pic(res, Pic_name.group(0))
            self.Pic_showintheBrowser(Pic_name.group(0))
            self.sendpictoTcpserver(pic)




    def Pic_showintheBrowser(self, Pic_name):
        self.time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        self.textBrowser.append("<font color='red'>" + str(self.myname) + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        self.textBrowser.append(r"<img src='./content/{}'/>".format(Pic_name))


    def write_Pic(self, res, name):
        cv2.imwrite('./content/{}'.format(name), res)

    def reshapePic(self, width, height):
        if width > 500:
            a = 500
            b = int(500/width*height)
        return b, a

    def showpicintextBrowser(self, sender, send_time, Pic_name):
        self.textBrowser.append(
            "<font color='blue' style='position: absolute;right:0px'>" + sender + str(send_time) + "</font>")
        self.textBrowser.append(r"<img src='./content/{}'/>".format(Pic_name))


    def convert_Picture(self, sender, send_time, pic):
        a, b, c = pic.shape
        a, b = self.reshapePic(a, b)
        res = cv2.resize(pic, (a, b))
        Pic_name = str(sender)+str(send_time)+".jpg"
        self.write_Pic(res, Pic_name)
        self.showpicintextBrowser(sender, send_time, Pic_name)


import pics