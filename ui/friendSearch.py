# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'friendSearch.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import time

from PyQt5 import QtCore, QtGui, QtWidgets
import json
from sql.UserDao import UserDao
from utils.ConfigFileReader import ConfigFileReader
from PyQt5.QtWidgets import QMessageBox
from utils.MsgUtils import sendMsg
from bson import json_util

config = ConfigFileReader("../config/server_config.yaml")

class Ui_Form(object):
    def __init__(self, s, username, data_list, parent_ui, bufferSize=1024 ):
        self.s = s
        self.bufferSize = bufferSize
        self.username = username  # 先在登录的用户
        self.parent_ui = parent_ui
        self.data_list = data_list

    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Form")
        Form.resize(400, 248)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(79, 54, 181, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(259, 54, 56, 21))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 111, 361, 121))
        self.listWidget.setObjectName("listWidget")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 41, 9))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.search)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.label.setText(_translate("Form", "请输入需要查询的用户的用户名"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("Form", "查询结果"))
        self.listWidget.itemClicked.connect(self.itemClickedFun)


    def itemClickedFun(self, item):
        send_user = item.text().split('\t')[0]
        ret = QMessageBox.information(self.Form, '提示', '您确定要加' + send_user + "为好友吗？", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                QMessageBox.No)
        # 发送请求信息
        if ret == QMessageBox.Yes:
            info_dict = {"type": "addFriend", "send_user": self.username, "recv_user": send_user}
            sendMsg(self.s, "passive", info_dict)
            self.Form.hide()
            time.sleep(0.3)
            self.parent_ui.showFriends()

    def search(self):
        self.listWidget.clear()  # 清空结果框
        username = self.lineEdit.text()
        if username == self.username:
            QMessageBox.information(self.Form, '失败', '只能添加自己以外的用户', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return
        if username == "":
            QMessageBox.information(self.Form, '失败', '输入不能为空', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return

        search_info_dict = {"type": "search", "username": username}
        get_id = sendMsg(self.s, "Initiative", search_info_dict)
        flag = 1
        while flag:
            for i_sub, i in enumerate(self.data_list):
                if get_id == i["id"]:
                    user_info = json_util.loads(i['info'])['info']

                    user_info_str = "\t".join([user_info['username'], user_info['gender'], str(user_info['age']), user_info['nickName']])

                    self.item(user_info_str)
                    # self.parent_ui.friends = get_info['friends']
                    self.data_list.pop(i_sub)
                    flag = 0
                    break

    def item(self, text):
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("Form", text))
        self.listWidget.addItem(item)

    def recv_msg(self):

        if self.friends == "UserNotExist":
            QMessageBox.information(self.Form, '失败', '用户不存在', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        else:
            username = self.lineEdit.text()
            age = self.friends['age']
            gender = self.friends['gender']
            nickName = self.friends['nickName']
            text = '\t'.join([username, gender, str(age), nickName])
            self.item(text)
