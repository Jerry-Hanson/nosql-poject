# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hylb.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox

from friendSearch import Ui_Form
from groupSearch import Ui_Form as group_UiForm
from createGroup import Ui_Form as create_group_UiForm
import json
from utils.MsgUtils import sendMsg
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from MsgRecvThread import MsgRecvThread
from bson import json_util


class Dialog(QtWidgets.QWidget):
    """
    重写好友列表的Widget， 为了重写closeEvent
    关闭父窗口的时候关闭所有的子窗口
    """
    def __init__(self, ui, parent = None):
        super(Dialog, self).__init__(parent = parent)
        self.ui = ui

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        for w in self.ui.widget_dict.values():
            w.close()
        a0.accept()


class Ui_Dialog(object):

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        for s, w in self.widget_dict.items():
            w.close()
        event.accept()

    def __init__(self, s, username, bufferSize=1024):
        self.s = s
        self.bufferSize = bufferSize
        self.username = username
        # 子窗口dict
        self.ui_dict = {}
        self.widget_dict = {}
        self.data_list = []

        # 好友搜索
        self.widget3 = QtWidgets.QWidget()
        self.ui3 = Ui_Form(s, self.username, self.data_list, parent_ui = self)
        self.ui3.setupUi(self.widget3)

        # 群聊搜索
        self.widget_groupSearch = QtWidgets.QWidget()
        self.ui_groupSearch = group_UiForm(s, self.username, self.data_list, parent_ui = self)
        self.ui_groupSearch.setupUi(self.widget_groupSearch)

        # 群聊创建
        self.widget_create_group = QtWidgets.QWidget()
        self.ui_create_group = create_group_UiForm(s = self.s, parent_ui = self,username =  self.username, widget = self.widget_create_group)
        self.ui_create_group.setupUi(self.widget_create_group)

        self.msgRecvThread = MsgRecvThread(self.s, self, self.data_list, self.username)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 617)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 401, 61))
        self.frame.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(160, 10, 91, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 61, 71))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(330, 10, 56, 41))
        self.pushButton.setStyleSheet("background-image:url(./images/QQ-5.jpg);\n"
                                      "")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 60, 401, 561))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_2.setFont(font)
        self.frame_2.setStyleSheet("background-color: rgb(222, 222, 222);\n"
                                   "border-color: rgb(230, 230, 230);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setGeometry(QtCore.QRect(0, 0, 401, 61))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_5.setFont(font)
        self.frame_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                   "border-color: rgb(230, 230, 230);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_5)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 10, 341, 41))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgb(230, 230, 230);\n"
                                      "selection-background-color: rgb(255, 255, 255);\n"
                                      "border-color: rgb(230, 230, 230);")
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setMaxLength(32768)
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setCursorPosition(0)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 10, 71, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.pushButton_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.pushButton_2.setAutoDefault(True)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setGeometry(QtCore.QRect(0, 70, 401, 121))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_6.setFont(font)
        self.frame_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                   "border-color: rgb(230, 230, 230);")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.toolButton = QtWidgets.QToolButton(self.frame_6)
        self.toolButton.setGeometry(QtCore.QRect(20, 20, 361, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.toolButton.setFont(font)
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setArrowType(QtCore.Qt.RightArrow)
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(self.frame_6)
        self.toolButton_2.setGeometry(QtCore.QRect(20, 70, 361, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.toolButton_2.setFont(font)
        self.toolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setArrowType(QtCore.Qt.RightArrow)
        self.toolButton_2.setObjectName("toolButton_2")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_2)
        self.tabWidget.setGeometry(QtCore.QRect(0, 200, 401, 361))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.frame_8 = QtWidgets.QFrame(self.tab)
        self.frame_8.setGeometry(QtCore.QRect(0, 0, 401, 341))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_8.setFont(font)
        self.frame_8.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                   "border-color: rgb(230, 230, 230);")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.frame_8)
        self.treeWidget_2.setGeometry(QtCore.QRect(0, 0, 401, 331))
        self.treeWidget_2.setObjectName("treeWidget_2")
        # 下面分别是四个主节点和其分支
        # self.first_item0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        # item_1 = QtWidgets.QTreeWidgetItem(self.first_item0)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/20140707211410_GiSLf.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # item_1.setIcon(0, icon)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/20191225154057_YYLWT.thumb.700_0.jpeg"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        # item_1.setIcon(0, icon1)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap("images/duitang_1624179999782.png.JPG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # item_1.setIcon(0, icon2)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/20190512215221_wKmP4.thumb.700_0.jpeg.JPG"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        # item_1.setIcon(0, icon3)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame_7 = QtWidgets.QFrame(self.tab_2)
        self.frame_7.setGeometry(QtCore.QRect(0, 0, 401, 341))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_7.setFont(font)
        self.frame_7.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                   "border-color: rgb(230, 230, 230);")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.treeWidget = QtWidgets.QTreeWidget(self.frame_7)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 401, 331))
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setAllColumnsShowFocus(False)
        self.treeWidget.setWordWrap(False)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setExpandsOnDoubleClick(True)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon3)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/20191225154053_rxAXj.thumb.700_0.jpeg"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        item_1.setIcon(0, icon4)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/duitang_1623223793046.png.JPG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_1.setIcon(0, icon5)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/20200803190636_kwysn.jpg.JPG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_1.setIcon(0, icon6)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon4)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/20191225154056_VWLiH.thumb.700_0.jpeg"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        item_1.setIcon(0, icon7)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/QQ-3.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_1.setIcon(0, icon8)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setIcon(0, icon4)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.frame_9 = QtWidgets.QFrame(self.tab_3)
        self.frame_9.setGeometry(QtCore.QRect(0, 0, 401, 341))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_9.setFont(font)
        self.frame_9.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                   "border-color: rgb(230, 230, 230);")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.treeWidget_3 = QtWidgets.QTreeWidget(self.frame_9)
        self.treeWidget_3.setGeometry(QtCore.QRect(0, 0, 411, 351))
        self.treeWidget_3.setObjectName("treeWidget_3")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_3)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_3)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_3)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_3)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.frame_10 = QtWidgets.QFrame(self.tab_4)
        self.frame_10.setGeometry(QtCore.QRect(0, 0, 401, 341))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_10.setFont(font)
        self.frame_10.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-color: rgb(230, 230, 230);")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.treeWidget_4 = QtWidgets.QTreeWidget(self.frame_10)
        self.treeWidget_4.setGeometry(QtCore.QRect(0, 0, 411, 351))
        self.treeWidget_4.setObjectName("treeWidget_4")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_4)
        item_0.setIcon(0, icon8)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.frame_11 = QtWidgets.QFrame(self.tab_5)
        self.frame_11.setGeometry(QtCore.QRect(0, 0, 401, 341))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_11.setFont(font)
        self.frame_11.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-color: rgb(230, 230, 230);")
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.treeWidget_5 = QtWidgets.QTreeWidget(self.frame_11)
        self.treeWidget_5.setGeometry(QtCore.QRect(0, 0, 411, 351))
        self.treeWidget_5.setObjectName("treeWidget_5")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_5)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_5)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_5)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_5)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.frame_12 = QtWidgets.QFrame(self.tab_6)
        self.frame_12.setGeometry(QtCore.QRect(0, 0, 401, 341))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.frame_12.setFont(font)
        self.frame_12.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-color: rgb(230, 230, 230);")
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.tabWidget.addTab(self.tab_6, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.select_func)


    def select_func(self):
        msgBox = QMessageBox()
        msgBox.setText("请选择操作")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msgBox.button(QMessageBox.Yes).setText("添加好友")
        msgBox.button(QMessageBox.No).setText("添加群聊")
        msgBox.button(QMessageBox.Cancel).setText("创建群聊")
        msgBox.show()
        res = msgBox.exec_()
        if res == QMessageBox.Yes:
            self.searchFriend()
        elif res == QMessageBox.No:
            self.addGroup()
        elif res == QMessageBox.Cancel:
            self.createGroup()



    def showFriendsAndGroups(self):
        """
        刷新一次好友列表
        :param username:
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.treeWidget_2.clear()
        # first_item0 = self.treeWidget_2.headerItem().setText(0, _translate("Dialog", "好友"))
        first_item0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        first_item0.setText(0, _translate("Dialog", "好友"))

        first_item1 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        first_item1.setText(0, _translate("Dialog", "群聊"))

        # 初始化所有的好友
        # 发送请求拿到所有的好友
        info_dict = {"type": "searchFriend", "username": self.username}
        get_id = sendMsg(self.s, "Initiative", info_dict)

        # 循环从列表中查找有无我需要的数据,有就处理
        flag = 1
        while flag:
            for i_sub, i in enumerate(self.data_list):
                if get_id == i["id"]:
                    get_info = json_util.loads(i['info'])
                    self.friends = get_info['friends']
                    self.data_list.pop(i_sub)
                    flag = 0
                    break

        for friend in self.friends:
            item = QtWidgets.QTreeWidgetItem(first_item0)
            item.setText(0, _translate("Dialog", friend))

        # 刷新群聊
        info_dict = {"type": "searchGroupsByUser", "username": self.username}
        get_id = sendMsg(self.s, "Initiative", info_dict)

        # 循环从列表中查找有无我需要的数据,有就处理
        flag = 1
        while flag:
            for i_sub, i in enumerate(self.data_list):
                if get_id == i["id"]:
                    get_info = json_util.loads(i['info'])
                    self.groups = get_info['groups']
                    self.data_list.pop(i_sub)
                    flag = 0
                    break

        for group in self.groups:
            item = QtWidgets.QTreeWidgetItem(first_item1)
            item.setText(0, _translate("Dialog", group))

        self.treeWidget_2.clicked.connect(self.treeWidgetClicked)

    def treeWidgetClicked(self, item):
        # item = QtWidgets.QTreeWidgetItem()

        if item.data() != '好友' and item.data() != "群聊":
            from chat import UiChat
            from chat import WidgetChat
            # QQ界面的widget
            friendUsername = item.data()
            self.widget_dict[friendUsername] = WidgetChat(self, friendUsername)
            isGroup = True if item.parent().data() == "群聊" else False
            self.ui_dict[friendUsername] = (UiChat(self.s, friendUsername, self.username, self.data_list, isGroup))
            self.ui_dict[friendUsername].setupUi(self.widget_dict[friendUsername])
            self.widget_dict[friendUsername].show()

        else:
            pass

    def searchFriend(self):
        self.widget3.show()

    def addGroup(self):
        self.widget_groupSearch.show()

    def createGroup(self):
        self.widget_create_group.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; color:#ffffff;\">联系人</span></p></body></html>"))
        self.label_2.setText(
            _translate("Dialog", "<html><head/><body><p><img src=\"./images/QQ-3.jpg\"/></p></body></html>"))
        self.pushButton_2.setText(_translate("Dialog", "搜索"))
        self.toolButton.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.toolButton.setText(_translate("Dialog", "新朋友"))
        self.toolButton_2.setText(_translate("Dialog", "群通知"))

        # treeWidget 1
        __sortingEnabled = self.treeWidget_2.isSortingEnabled()
        self.treeWidget_2.setSortingEnabled(False)


        self.treeWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "好友"))
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "分组"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Dialog", "特别关心"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Dialog", "小明"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("Dialog", "小红"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Dialog", "我的好友"))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("Dialog", "小郑"))
        self.treeWidget.topLevelItem(1).child(1).setText(0, _translate("Dialog", "小邵"))
        self.treeWidget.topLevelItem(1).child(2).setText(0, _translate("Dialog", "小马"))
        self.treeWidget.topLevelItem(1).child(3).setText(0, _translate("Dialog", "小罗"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("Dialog", "同学"))
        self.treeWidget.topLevelItem(2).child(0).setText(0, _translate("Dialog", "小杨"))
        self.treeWidget.topLevelItem(2).child(1).setText(0, _translate("Dialog", "小秋"))
        self.treeWidget.topLevelItem(2).child(2).setText(0, _translate("Dialog", "小李"))
        self.treeWidget.topLevelItem(3).setText(0, _translate("Dialog", "家人"))
        self.treeWidget.topLevelItem(3).child(0).setText(0, _translate("Dialog", "爷爷"))
        self.treeWidget.topLevelItem(3).child(1).setText(0, _translate("Dialog", "奶奶"))
        self.treeWidget.topLevelItem(3).child(2).setText(0, _translate("Dialog", "妈妈"))
        self.treeWidget.topLevelItem(3).child(3).setText(0, _translate("Dialog", "哥哥"))
        self.treeWidget.topLevelItem(3).child(4).setText(0, _translate("Dialog", "爸爸"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "分组"))
        self.treeWidget_3.headerItem().setText(0, _translate("Dialog", "群聊"))
        __sortingEnabled = self.treeWidget_3.isSortingEnabled()
        self.treeWidget_3.setSortingEnabled(False)
        self.treeWidget_3.topLevelItem(0).setText(0, _translate("Dialog", "置顶群聊"))
        self.treeWidget_3.topLevelItem(0).child(0).setText(0, _translate("Dialog", "111"))
        self.treeWidget_3.topLevelItem(1).setText(0, _translate("Dialog", "未命名群聊"))
        self.treeWidget_3.topLevelItem(1).child(0).setText(0, _translate("Dialog", "222"))
        self.treeWidget_3.topLevelItem(2).setText(0, _translate("Dialog", "我创建的群聊"))
        self.treeWidget_3.topLevelItem(2).child(0).setText(0, _translate("Dialog", "333"))
        self.treeWidget_3.topLevelItem(3).setText(0, _translate("Dialog", "我管理的群聊"))
        self.treeWidget_3.topLevelItem(3).child(0).setText(0, _translate("Dialog", "444"))
        self.treeWidget_3.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "群聊"))
        self.treeWidget_4.headerItem().setText(0, _translate("Dialog", "设备"))
        __sortingEnabled = self.treeWidget_4.isSortingEnabled()
        self.treeWidget_4.setSortingEnabled(False)
        self.treeWidget_4.topLevelItem(0).setText(0, _translate("Dialog", "我的电脑"))
        self.treeWidget_4.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "设备"))
        self.treeWidget_5.headerItem().setText(0, _translate("Dialog", "通讯录"))
        __sortingEnabled = self.treeWidget_5.isSortingEnabled()
        self.treeWidget_5.setSortingEnabled(False)
        self.treeWidget_5.topLevelItem(0).setText(0, _translate("Dialog", "小李"))
        self.treeWidget_5.topLevelItem(1).setText(0, _translate("Dialog", "小丽"))
        self.treeWidget_5.topLevelItem(2).setText(0, _translate("Dialog", "小康"))
        self.treeWidget_5.topLevelItem(3).setText(0, _translate("Dialog", "小红"))
        self.treeWidget_5.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", "通讯录"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Dialog", "订阅号"))

        # start msg receive thread
        self.msgRecvThread.start()

        # 刷新好友列表
        self.showFriendsAndGroups()