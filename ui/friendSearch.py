# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'friendSearch.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import json

from PyQt5.QtWidgets import QMessageBox


class Ui_Form(object):
    def __init__(self, s, bufferSize=1024):
        self.s = s
        self.bufferSize = bufferSize

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
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
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
        item = self.listWidget.item(0)
        item.setText(_translate("Form", "好友1"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("Form", "查询结果"))
        self.listWidget.itemClicked.connect(self.itemClickedFun)


    def itemClickedFun(self, item):
        username = item.text().split('\t')[0]
        # 发送请求信息


    def search(self):
        self.listWidget.clear()  # 清空结果框
        username = self.lineEdit.text()
        if username == "":
            QMessageBox.information(self.Form, '失败', '输入不能为空', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return
        # log
        print("searching " + username)

        search_info_dict = {"type": "search", "username": username}
        search_info = json.dumps(search_info_dict)
        self.s.send(search_info.encode())
        self.recv_msg()

    def item(self, text):
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("Form", text))
        self.listWidget.addItem(item)

    def recv_msg(self):
        recv_info = self.s.recv(self.bufferSize).decode('utf-8')
        print(recv_info)
        if recv_info == "UserNotExist":
            QMessageBox.information(self.Form, '失败', '用户不存在', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        else:
            user_info = json.loads(recv_info)
            username = self.lineEdit.text()
            age = user_info['age']
            gender = user_info['gender']
            nickName = user_info['nickName']
            text = '\t'.join([username, gender, str(age), nickName])
            self.item(text)

if __name__ == "__main__":
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form(None)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
