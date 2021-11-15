# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
import json

class Ui_Form(object):
    def __init__(self, s, bufferSize=1024):
        # socket object
        super(Ui_Form,self).__init__()
        self.s = s
        self.bufferSize = bufferSize

    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(450, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(450, 300))
        Form.setMaximumSize(QtCore.QSize(450, 300))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 0, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(67, 57, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(97, 90, 41, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(87, 117, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(157, 57, 221, 20))
        self.lineEdit.setCursorPosition(0)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(157, 90, 221, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(157, 127, 221, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 250, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("background:#426ab3;\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.register)

        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(157, 167, 221, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(97, 157, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(157, 205, 221, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(97, 195, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def register(self):
        # 获取输入框内容
        nickName = self.lineEdit.text()
        pwd = self.lineEdit_2.text()
        retryPwd = self.lineEdit_3.text()
        gender = self.lineEdit_4.text()
        age = self.lineEdit_5.text()

        if nickName == '' or pwd == '' or retryPwd == '' or gender == '' or age == '':
            QMessageBox.information(self.Form, '提示', '输入框不能为空', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        elif pwd != retryPwd:
            QMessageBox.information(self.Form, '提示', '两次密码必须一致', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        elif not age.isdigit():
            QMessageBox.information(self.Form, '提示', '年龄必须是数字', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)

            """
                "type":"register"
                "username":"..."
                "password":"..."
                "gender":"male" // "female"
                "age":16
                "nickname":"" // 昵称
            """
        else:
            register_info_dict = {"type":"register", "username":nickName, "password":pwd,
                               "gender":gender,"age":int(age), "nickName":nickName}
            register_info = json.dumps(register_info_dict)
            print(register_info)
            self.s.send(register_info.encode())
            self.login_recv()


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "欢迎注册"))
        self.label_2.setText(_translate("Form", "昵称(用户名)"))
        self.label_3.setText(_translate("Form", "密码"))
        self.label_4.setText(_translate("Form", "确认密码"))
        self.pushButton.setText(_translate("Form", "立即注册"))
        self.label_5.setText(_translate("Form", "性别"))
        self.label_7.setText(_translate("Form", "年龄"))

    def login_recv(self):
        recv_info = self.s.recv(self.bufferSize).decode('utf-8')
        print(recv_info)
        if str(recv_info) == 'Success':
            self.Form.close()
        elif str(recv_info) == "userExists":
            QMessageBox.information(self.Form, '提示', '用户已存在', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form(None)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())