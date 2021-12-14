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
        self.username = username  # 现在登录的用户
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
        self.label.setText(_translate("Form", "请输入需要查询的群聊名称"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("Form", "查询结果"))
        self.listWidget.itemClicked.connect(self.itemClickedFun)


    def itemClickedFun(self, item):
        group_name = item.text()
        ret = QMessageBox.information(self.Form, '提示', '您确定要添加群聊' + group_name + "吗?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                QMessageBox.No)
        # 发送请求信息
        if ret == QMessageBox.Yes:
            info_dict = {"type": "addGroup", "send_user": self.username, "groupName": group_name}
            sendMsg(self.s, "passive", info_dict)
            self.Form.hide()
            time.sleep(0.3)
            self.parent_ui.showFriendsAndGroups()


    def search(self):
        #查询群聊
        self.listWidget.clear()  # 清空结果框
        group_name = self.lineEdit.text()
        if group_name == "":
            QMessageBox.information(self.Form, '失败', '输入不能为空', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return

        search_info_dict = {"type": "searchGroup", "group_name": group_name}
        get_id = sendMsg(self.s, "Initiative", search_info_dict)
        flag = 1
        while flag:
            for i_sub, i in enumerate(self.data_list):
                if get_id == i["id"]:
                    recv_info = json_util.loads(i['info'])
                    if recv_info == "SUCCESS":
                        self.item(group_name)
                        # self.parent_ui.friends = get_info['friends']
                    else:
                        QMessageBox.information(self.Form, '失败', '查无此群', QMessageBox.Ok | QMessageBox.Close,
                                                QMessageBox.Close)
                    self.data_list.pop(i_sub)
                    flag = 0
                    break

    def item(self, text):
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("Form", text))
        self.listWidget.addItem(item)

