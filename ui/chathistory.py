# -*- coding: utf-8 -*-

# Form implementation generated from reading ui-submit file 'chathistory.ui-submit'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import json

from PyQt5.QtWidgets import QLabel
from bson import json_util
import numpy as np
import cv2
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QDate, QDateTime
class Ui_Formt2(object):
    def __init__(self, myname, sendname, message):
        self.myname = myname
        self.sendname = sendname
        self.message = message
        self.count_pic = 0

    def quick_sort(self):
        for i in range(1, len(self.message)):
            for j in range(i, 0, -1):
                if self.message[j]['date'] < self.message[j - 1]['date']:
                    self.message[j], self.message[j - 1] = self.message[j - 1], self.message[j]



    def show_data(self):
        for i in self.message:
            print(type(i), i)
            if i['send_user'] == self.myname:
                if i['message_type'] == 'str':
                    self.textBrowser.append("<font color='red'>" + str(i['send_user']) + str(i['date']))
                    self.textBrowser.append(i['msg'])
                elif i['message_type'] == 'pic':
                    self.show_image_myself(i)

            else:
                if i['message_type'] == 'str':
                    self.textBrowser.append("<font color='blue'>" + str(i['send_user']) + str(i['date']))
                    self.textBrowser.append(i['msg'])
                elif i['message_type'] == 'pic':
                    self.show_image_other(i)


    def show_data_time(self, time_start, time_end):
        chose_time = list()
        for i in self.message:
            if i['date']>=time_start and i['date']<=time_end:
                chose_time.append(i)


        for i in chose_time:
            print(type(i), i)
            if i['send_user'] == self.myname:
                if i['message_type'] == 'str':
                    self.textBrowser.append("<font color='red'>" + str(i['send_user']) + str(i['date']))
                    self.textBrowser.append(i['msg'])
                elif i['message_type'] == 'pic':
                    self.show_image_myself(i)
            else:
                if i['message_type'] == 'str':
                    self.textBrowser.append("<font color='blue'>" + str(i['send_user']) + str(i['date']))
                    self.textBrowser.append(i['msg'])
                elif i['message_type'] == 'pic':
                    self.show_image_other(i)


    def show_image_myself(self, i):
        i['msg'] = np.array(i['msg'])
        try:
            self.write_Pic(i['msg'], i['send_user']+str(self.count_pic)+".jpg")
        finally:
            pass
        self.textBrowser.append(
            "<font color='red' style='position: absolute;right:0px'>" + str(i['send_user']) + str(i['date']) + "</font>")
        self.textBrowser.append(r"<img src='./content/{}'/>".format(i['send_user']+str(self.count_pic)+".jpg"))
        self.count_pic += 1
    def show_image_other(self, i):
        i['msg'] = np.array(i['msg'])
        try:
            self.write_Pic(i['msg'], str(i['send_user'])+str(self.count_pic)+".jpg")
        finally:
            pass
        self.textBrowser.append(
            "<font color='blue' style='position: absolute;right:0px'>" + str(i['send_user']) + str(i['date']) + "</font>")
        self.textBrowser.append(r"<img src='./content/{}'/>".format(i['send_user']+str(self.count_pic)+".jpg"))
        self.count_pic += 1

    def write_Pic(self, res, name):
        cv2.imwrite('./content/{}'.format(name), res)



    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 650)
        Form.setMinimumSize(QtCore.QSize(400, 650))
        Form.setMaximumSize(QtCore.QSize(400, 650))
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(0, 50, 400, 600))
        self.textBrowser.setMinimumSize(QtCore.QSize(400, 600))
        self.textBrowser.setMaximumSize(QtCore.QSize(400, 600))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, -10, 400, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./pics/6.png"))
        self.label.setObjectName("label")
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setGeometry(QtCore.QRect(50, 50, 296, 236))
        self.calendarWidget.setStyleSheet("")
        self.calendarWidget.setVisible(False)
        self.calendarWidget.setObjectName("calendarWidget")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(310, 610, 28, 26))
        self.pushButton.setStyleSheet("QPushButton{border-image: url(./pics/cal1.png)}\n"
"QPushButton:hover{border-image: url(./pics/cal2.png)}\n"
"QPushButton:pressed{border-image: url(./pics/cal3.png)}")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 610, 28, 26))
        self.pushButton_2.setStyleSheet("QPushButton{border-image: url(./pics/cal4.png)}\n"
"QPushButton:hover{border-image: url(./pics/cal5.png)}\n"
"QPushButton:pressed{border-image: url(./pics/cal6.png)}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.calendarWidget.show) # type: ignore
        self.pushButton_2.clicked.connect(self.calendarWidget.hide) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)
        date = self.calendarWidget.selectedDate()
        self.calendarWidget.clicked[QDate].connect(self.show_date)

        self.quick_sort()
        self.show_data()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def show_date(self, date):
        date_time = date.toString("yyyy-MM-dd")
        date_time_satrt = date_time+' 00:00:00'
        date_time_end = date_time+' 23:59:59'
        self.textBrowser.clear()
        self.show_data_time(date_time_satrt, date_time_end)



if __name__ == "__main__":
	import sys
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

	app =  QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_Formt2()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())