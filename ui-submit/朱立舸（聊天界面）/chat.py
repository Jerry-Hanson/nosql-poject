
import pics
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 650)
        Form.setMinimumSize(QtCore.QSize(750, 650))
        Form.setMaximumSize(QtCore.QSize(750, 650))
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 750, 650))
        self.frame.setMinimumSize(QtCore.QSize(750, 650))
        self.frame.setMaximumSize(QtCore.QSize(750, 650))
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 750, 60))
        self.label.setMinimumSize(QtCore.QSize(750, 60))
        self.label.setMaximumSize(QtCore.QSize(750, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/pics/1.png"))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QtCore.QRect(0, 110, 750, 360))
        self.textBrowser.setMinimumSize(QtCore.QSize(750, 360))
        self.textBrowser.setMaximumSize(QtCore.QSize(750, 360))
        self.textBrowser.setStyleSheet("")
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(0, 500, 750, 150))
        self.textEdit.setMinimumSize(QtCore.QSize(750, 150))
        self.textEdit.setMaximumSize(QtCore.QSize(750, 150))
        self.textEdit.setStyleSheet("border:0px;")
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(0, 470, 750, 30))
        self.label_2.setMinimumSize(QtCore.QSize(750, 30))
        self.label_2.setMaximumSize(QtCore.QSize(750, 30))
        self.label_2.setStyleSheet("border-bottom:0px;\n"
"border-top:1px solid #f4f4f4;\n"
"border-right:0px;\n"
"border-left:0px;")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/pics/4.png"))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(0, 10, 750, 40))
        self.label_3.setMinimumSize(QtCore.QSize(750, 40))
        self.label_3.setMaximumSize(QtCore.QSize(750, 40))
        font = QtGui.QFont()
        font.setFamily("Alibaba PuHuiTi")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(530, 600, 92, 37))
        self.pushButton.setStyleSheet("QPushButton{border-image: url(:/pics/guanbi.png)}\n"
"QPushButton:hover{border-image: url(:/pics/guanbi2.png)}\n"
"QPushButton:pressed{border-image: url(:/pics/guanbi3.png)}")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 600, 113, 37))
        self.pushButton_2.setStyleSheet("QPushButton{border-image: url(:/pics/fasong.png)}\n"
"QPushButton:hover{border-image: url(:/pics/fasong2.png)}\n"
"QPushButton:pressed{border-image: url(:/pics/fasong3.png)}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(0, 60, 750, 50))
        self.label_4.setMinimumSize(QtCore.QSize(750, 50))
        self.label_4.setMaximumSize(QtCore.QSize(750, 50))
        self.label_4.setStyleSheet("")
        self.label_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/pics/5.png"))
        self.label_4.setObjectName("label_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(690, 471, 28, 28))
        self.pushButton_3.setStyleSheet("QPushButton{border-image: url(:/pics/ltjl1.png)}\n"
"QPushButton:hover{border-image: url(:/pics/ltjl2.png)}\n"
"QPushButton:pressed{border-image: url(:/pics/ltjl3.png)}")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.picture = QtWidgets.QPushButton(self.frame)
        self.picture.setGeometry(QtCore.QRect(215, 473, 28, 26))
        self.picture.setMinimumSize(QtCore.QSize(28, 26))
        self.picture.setMaximumSize(QtCore.QSize(28, 26))
        self.picture.setStyleSheet("QPushButton{border-image: url(:/pics/7.png)}\n"
"QPushButton:hover{border-image: url(:/pics/7-1.png)}\n"
"QPushButton:pressed{border-image: url(:/pics/7-2.png)}")
        self.picture.setText("")
        self.picture.setObjectName("picture")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(128, 475, 28, 26))
        self.pushButton_4.setMinimumSize(QtCore.QSize(28, 26))
        self.pushButton_4.setMaximumSize(QtCore.QSize(28, 26))
        self.pushButton_4.setStyleSheet("QPushButton{border-image: url(:/pics/file1.png)}\n"
"QPushButton:hover{border-image: url(:/pics/file2.png)}\n"
"QPushButton:pressed{border-image: url(:/pics/file3.png)}")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/pics/3.png\" /></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">张丹</span></p></body></html>"))

if __name__ == "__main__":
	import sys
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

	app =  QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_Form()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
