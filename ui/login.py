# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.2

# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from socket import *
import threading
import json

import sys

sys.path.append("../")

from utils.ConfigFileReader import ConfigFileReader

class Ui_MainWindow(object):

    # 开启一个sock， 连接服务器
    def tcp_start(self):
        config = ConfigFileReader('../config/client_config.yaml')
        address = config.info['server_address']
        port = config.info['server_port']
        self.buffsize = config.info['buffersize']
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((address, port))

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(360, 340)
        self.MainWindow.setMinimumSize(QtCore.QSize(360, 340))
        self.MainWindow.setMaximumSize(QtCore.QSize(360, 340))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/QQicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MainWindow.setWindowIcon(icon)
        # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 160, 191, 30))
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setText("")
        self.lineEdit.setMaxLength(32767)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 210, 191, 31))
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setMaxLength(32767)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setCursorPosition(0)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 260, 221, 41))
        self.pushButton.setStyleSheet("background-color: rgb(7, 85, 240);\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # set button click event
        self.pushButton.clicked.connect(self.login)

        self.formFrame = QtWidgets.QFrame(self.centralwidget)
        self.formFrame.setGeometry(QtCore.QRect(0, -1, 361, 151))
        self.formFrame.setStyleSheet("border-color: rgb(0, 85, 255);\n"
                                     "background-image: url(images/loginicon.jpg);")
        self.formFrame.setObjectName("formFrame")
        self.formLayout = QtWidgets.QFormLayout(self.formFrame)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 170, 31, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 220, 31, 16))
        self.label_2.setObjectName("label_2")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 305, 56, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.register)

        # MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "QQ登录"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.label.setText(_translate("MainWindow", "账号："))
        self.label_2.setText(_translate("MainWindow", "密码："))
        self.pushButton_2.setText(_translate("MainWindow", "注册账号"))

    def register(self):
        widget2.show()

    def login(self):
        """
        点击登录按钮
        :return:
        """
        self.user = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if self.user == '':
            QMessageBox.information(self.MainWindow, '提示', 'QQ账号不能为空!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        else:
            if password == '':
                QMessageBox.information(self.MainWindow, '提示', '密码不能为空!', QMessageBox.Ok | QMessageBox.Close,
                                        QMessageBox.Close)
            else:
                login_info_dict = {"type": "login", "username": self.user, "password": password}
                login_info = json.dumps(login_info_dict)
                self.s.send(login_info.encode())
                self.login_recv()

    # login的响应窗口
    def login_recv(self):
        recv_info = self.s.recv(self.buffsize).decode('utf-8')
        print(recv_info)
        if str(recv_info) == 'Success':
            QMessageBox.information(self.MainWindow, '登录成功', '登录成功!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            # QtCore.QCoreApplication.instance().quit()
            # 打开QQ界面
            widget.hide()

            # QQ界面的widget
            from hylb import Ui_Dialog
            from hylb import Dialog

            # 把sock传到新的窗口中
            self.ui1 = Ui_Dialog(ui.s, self.user)
            self.widget1 = Dialog(self.ui1)
            self.ui1.setupUi(self.widget1)

            self.widget1.show()

        elif str(recv_info) == 'UserNotExist':
            QMessageBox.information(self.MainWindow, '失败', '登录失败，无此账号!!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        elif str(recv_info) == 'WrongPwd':
            QMessageBox.information(self.MainWindow, '失败', '登录失败，密码错误!!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        # elif str(recv_info) == 'flase-login':
        #     QMessageBox.information(self.MainWindow, '失败', '此账号已登录!', QMessageBox.Ok | QMessageBox.Close,
        #                             QMessageBox.Close)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    ui.tcp_start()
    widget.show()

    # # QQ界面的widget
    # from hylb import Ui_Dialog
    # widget1 = QtWidgets.QWidget()
    # # 把sock传到新的窗口中
    # ui1 = Ui_Dialog(ui.s, "")
    # ui1.setupUi(widget1)

    # register 界面的widget
    from register import Ui_Form

    widget2 = QtWidgets.QWidget()
    ui2 = Ui_Form(ui.s)
    ui2.setupUi((widget2))

    sys.exit(app.exec_())
