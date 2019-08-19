import sys
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from PySide2.QtCore import QObject, Signal, Slot, QFile
from ui_mainWindow import Ui_MainWindow
from ui_trade import Ui_Form
import shioaji as sj
import asyncio


class RTUpdate(QObject):
    # create two new signals on the fly: one will handle
    # int type, the other will handle strings
    update_price_caller = Signal((list,))
    update_bidask_caller = Signal((list,))


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
        self.rtUpdate = RTUpdate()
        self.rtUpdate.update_price_caller.connect(self.update_price_worker)
        self.rtUpdate.update_bidask_caller.connect(self.update_bidask_worker)
        self.api = sj.Shioaji()

    def logo(self):
        pixmap = QtGui.QPixmap("img/shioaji.png")
        lbl = QtWidgets.QLabel()
        lbl.setAlignment(QtCore.Qt.AlignRight)
        lbl.setPixmap(pixmap)
        return lbl

    def quote_msg(self, topic, msg):
        if topic[0] == "L":
            lst = [
                msg["Code"],
                msg["Close"][0],
                msg["DiffPrice"][0],
                msg["Volume"][0],
                msg["VolSum"][0],
            ]
            self.rtUpdate.update_price_caller.emit(lst)
        if topic[0] == "Q":
            lst = list(range(0, 20))
            # print(topic, msg)
            # Q/TFE/TXFH9
            """
            {
                "AskPrice": [10459.0, 10460.0, 10461.0, 10462.0, 10463.0],
                "AskVolSum": 302,
                "AskVolume": [6, 50, 75, 100, 71],
                "BidPrice": [10458.0, 10457.0, 10456.0, 10455.0, 10454.0],
                "BidVolSum": 183,
                "BidVolume": [25, 38, 49, 37, 34],
                "Code": "TXFH9",
                "Date": "2019/08/19",
                "DiffAskVol": [3, 0, 0, 0, 0],
                "DiffAskVolSum": 3,
                "DiffBidVol": [3, 0, 0, -1, 0],
                "DiffBidVolSum": 2,
                "FirstDerivedAskPrice": 10461.0,
                "FirstDerivedAskVolume": 10,
                "FirstDerivedBidPrice": 10457.0,
                "FirstDerivedBidVolume": 4,
                "TargetKindPrice": 10479.52,
                "Time": "10:38:30.616000",
            }
            """
            lst = (
                msg["BidPrice"] + msg["BidVolume"] + msg["AskPrice"] + msg["AskVolume"]
            )
            self.rtUpdate.update_bidask_caller.emit(lst)

    def bidask_msg(self, topic, msg):
        lst = list(range(0, 20))
        print(lst)
        self.rtUpdate.update_bidask_caller.emit(lst)

    @Slot(list)
    def update_bidask_worker(self, lst):
        tableWidget = self.trade.bidask_grid
        # item = tableWidget.item(row,column)
        for row, i in enumerate(lst[:5]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 0, item)
        for row, i in enumerate(lst[5:10]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 1, item)
        for row, i in enumerate(lst[10:15]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 2, item)
        for row, i in enumerate(lst[15:20]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 3, item)

    @Slot(list)
    def update_price_worker(self, lst):
        self.trade.code_edit.setText(lst[0])
        self.trade.curr_price.display(lst[1])
        self.trade.diff_price.display(lst[2])
        self.trade.tick_vol.display(lst[3])
        self.trade.total_vol.display(lst[4])

    @Slot()
    def login(self):
        # self.bidask_msg(None, None)
        # return
        user = {
            "uid": self.trade.id_edit.text(),
            "password": self.trade.password_edit.text(),
        }
        try:
            self.api.login(user["uid"], user["password"])
        except asyncio.TimeoutError:
            self.trade.code_edit.setText("目前暫停服務")
            self.trade.code_edit.repaint()
            return
        self.trade.login_button.setText("已登入")
        self.trade.login_button.repaint()
        self.api.quote.set_callback(self.quote_msg)
        self.api.quote.subscribe(self.api.Contracts.Futures["TXFH9"])
        self.api.quote.subscribe(
            self.api.Contracts.Futures["TXFH9"], quote_type="bidask"
        )


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
