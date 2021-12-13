# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fileWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMessageBox

from ftp.dao.FTPDao import FTPDao

class Ui_FileWindow(object):

    def __init__(self, file_list: list, ftp_dao: FTPDao, username: str):
        self.file_list = file_list
        self.ftp_dao = ftp_dao
        self.username = username

    def setupUi(self, FileWindow):
        FileWindow.setObjectName("FileWindow")
        FileWindow.resize(300, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileWindow.sizePolicy().hasHeightForWidth())
        FileWindow.setSizePolicy(sizePolicy)
        FileWindow.setMaximumSize(QtCore.QSize(300, 350))
        self.listWidget = QtWidgets.QListWidget(FileWindow)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 301, 351))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.clicked.connect(self.click_func)

        self.retranslateUi(FileWindow)
        QtCore.QMetaObject.connectSlotsByName(FileWindow)

    def click_func(self, item):
        filename = item.data()
        # 确认是否要下载
        res = QMessageBox.question(None, "确认", "确认是否要下载?", QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            self.download_file(filename, self.username)

    def retranslateUi(self, FileWindow):
        _translate = QtCore.QCoreApplication.translate
        FileWindow.setWindowTitle(_translate("FileWindow", "Form"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        for file_name in self.file_list:
            self.addItem(file_name)

        self.listWidget.setSortingEnabled(__sortingEnabled)

    def download_file(self, filename, remote_file_dir):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")
        self.ftp_dao.download(directory, filename, remote_file_dir)


    def addItem(self, text):
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("FileWindow", text))
        self.listWidget.addItem(item)


if __name__ == "__main__":
    if __name__ == "__main__":
        import sys

        app = QtWidgets.QApplication(sys.argv)

        widget = QtWidgets.QWidget()
        ui = Ui_FileWindow()
        ui.setupUi(widget)
        widget.show()
        sys.exit(app.exec_())
