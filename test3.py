import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # 创建一个线程实例并设置名称 变量 信号与槽
        self.thread = MyThread()
        self.thread.sinOut.connect(self.outText)
        self.thread.setVal(6)

    # 打印输出文本
    def outText(self, text):
        print(text)


class MyThread(QThread):
    # 自定义信号参数为str类型
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def setVal(self, val):
        # 接受数据，运行多线程
        self.times = int(val)

        self.run()

    def run(self):
        # 当次数大于0以及名称不为空时执行代码
        while self.times > 0:
            # 发射信号，触发打印函数，次数-1
            self.sinOut.emit(self.identity + '==>' + str(self.times))
            self.times -= 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
