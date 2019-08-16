import sys
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtCore import QObject, Signal, Slot, QFile
from ui_mainWindow import Ui_MainWindow
from ui_trade import Ui_Form
import json
import shioaji as sj


class Communicate(QObject):
    # create two new signals on the fly: one will handle
    # int type, the other will handle strings
    speak = Signal((list,))


class mainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainUI, self).__init__(parent)
        self.setupUi(self)
        self.trade = trade_widget()
        self.horizontalLayout.addWidget(self.trade)
        self.horizontalLayout.addWidget(self.logo())
        self.setWindowIcon(QtGui.QIcon("img/shioaji.png"))
        # event
        self.trade.login_button.clicked.connect(self.login)
        self.someone = Communicate()
        self.someone.speak.connect(self.say_something)
        self.api = sj.Shioaji()

    def logo(self):
        pixmap = QtGui.QPixmap("img/shioaji.png")
        lbl = QtWidgets.QLabel()
        lbl.setAlignment(QtCore.Qt.AlignRight)
        lbl.setPixmap(pixmap)
        return lbl

    def quote_msg(self, topic, msg):
        print(topic, msg)
        lst = [
            msg["Code"],
            msg["Close"][0],
            msg["DiffPrice"][0],
            msg["Volume"][0],
            msg["VolSum"][0],
        ]
        self.someone.speak.emit(lst)

    @Slot(list)
    def say_something(self, lst):
        self.trade.code_edit.setText(lst[0])
        self.trade.curr_price.display(lst[1])
        self.trade.diff_price.display(lst[2])
        self.trade.tick_vol.display(lst[3])
        self.trade.total_vol.display(lst[4])
        print(lst)

    @Slot()
    def login(self):
        with open("user.json") as json_file:
            user = json.load(json_file)
        self.api.login(user["uid"], user["password"])
        self.trade.login_button.setText("已登入")
        self.api.quote.subscribe(self.api.Contracts.Futures["TXFH9"])
        self.api.quote.set_callback(self.quote_msg)


class trade_widget(QWidget, Ui_Form):
    def __init__(self):
        super(trade_widget, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = mainUI()
    window.show()
    sys.exit(app.exec_())
