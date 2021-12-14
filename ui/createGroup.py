# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createGroup.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from bson import json_util
from utils.MsgUtils import sendMsg


class Ui_Form(object):
    def __init__(self, s, parent_ui, widget, username):
        """
        创建群聊
        :param s: socket
        :param parent_ui:
        """
        self.s = s
        self.username = username
        self.parent_ui = parent_ui
        self.widget = widget

    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Form")
        Form.resize(300, 150)
        Form.setMinimumSize(QtCore.QSize(300, 150))
        Form.setMaximumSize(QtCore.QSize(300, 150))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(210, 80, 56, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 40, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(30, 80, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "创建群聊"))
        self.pushButton.setText(_translate("Form", "创建"))
        self.label.setText(_translate("Form", "请输入创建群聊的名称"))

        # 设置点击事件
        self.pushButton.clicked.connect(self.createGroup)

    def createGroup(self):
        groupName = self.lineEdit.text()

        info_dict = {"type": "createGroup", "send_user":  self.username, "group_name":
                     groupName}

        sendMsg(self.s, "passive", info_dict)

        QMessageBox.information(self.Form, '成功', '群聊创建成功', QMessageBox.Ok | QMessageBox.Close,
                                QMessageBox.Close)

        self.widget.hide()
        self.parent_ui.showFriendsAndGroups()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())