# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chathistory.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import pics
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
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
        self.label.setPixmap(QtGui.QPixmap(":/pics/6.png"))
        self.label.setObjectName("label")
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setGeometry(QtCore.QRect(50, 50, 296, 236))
        self.calendarWidget.setStyleSheet("")
        self.calendarWidget.setVisible(False)
        self.calendarWidget.setObjectName("calendarWidget")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(310, 610, 28, 26))
        self.pushButton.setStyleSheet("QPushButton{border-image: url(:/pics/cal1.png)}\n"
"QPushButton:hover{border-image: url(:/pics/cal2.png)}\n"
"QPushButton:pressed{border-image: url(:/pics/cal3.png)}")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 610, 28, 26))
        self.pushButton_2.setStyleSheet("QPushButton{border-image: url(:/pics/cal4.png)}\n"
"QPushButton:hover{border-image: url(:/pics/cal5.png)}\n"
"QPushButton:pressed{border-image: url(:/pics/cal6.png)}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.calendarWidget.show) # type: ignore
        self.pushButton_2.clicked.connect(self.calendarWidget.hide) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    uiwindow = Ui_MainWindow()#?????????Ui_MainWindow
    mainwindow = QtWidgets.QMainWindow() #?????????QMainWindow
    uiwindow.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
