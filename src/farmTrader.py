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
    # update_price_caller = Signal((list,))
    # update_bidask_caller = Signal((dict,))
    caller = Signal((str, dict))


class mainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainUI, self).__init__(parent)
        self.setupUi(self)
        self.trade = trade_widget()
        self.trade.login = self.login
        self.horizontalLayout.addWidget(self.trade)
        self.horizontalLayout.addWidget(self.logo())
        self.setWindowIcon(QtGui.QIcon("img/shioaji.png"))
        # event
        self.rtUpdate = RTUpdate()
        # self.rtUpdate.update_price_caller.connect(self.update_price_worker)
        # self.rtUpdate.update_bidask_caller.connect(self.update_bidask_worker)
        self.rtUpdate.caller.connect(self.rt_worker)
        self.api = sj.Shioaji()

    @Slot(str, dict)
    def rt_worker(self, topic, msg):
        """"""
        topic_type = topic.split("/")[0]
        code = topic.split("/")[-1]
        {
            "MKT": self.proc_mkt,
            "QUT": self.proc_qut,
            "Q": self.proc_q,
            "L": self.proc_l,
        }[topic_type](code, msg)

    def proc_mkt(self, code, msg):
        """
         MKT/idcdmzpcr01/TSE/2330
         {'Close': [252.5], 'Time': '13:06:24.674650', 'VolSum': [17280], 'Volume': [1]}
        """
        self.trade.code_edit.setText(code)
        self.trade.curr_price.display(msg["Close"][0])
        self.trade.diff_price.display(0)
        self.trade.tick_vol.display(msg["Volume"][0])
        self.trade.total_vol.display(msg["VolSum"][0])

    def proc_qut(self, code, msg):
        """
          QUT/idcdmzpcr01/TSE/2330
         {'AskPrice': [253.0, 253.5, 254.0, 254.5, 255.0], 'AskVolume': [2429, 2818, 1266, 624, 2313], 'BidPrice': [252.5, 252.0, 251.5, 251.0, 250.5], 'BidVolume': [377, 809, 712, 1607, 883], 'Date': '2019/08/19', 'Time': '13:06:24.674650'}
        """
        tableWidget = self.trade.bidask_grid
        for row, i in enumerate(msg["BidPrice"]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 0, item)
        for row, i in enumerate(msg["BidVolume"]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 1, item)
        for row, i in enumerate(msg["AskPrice"]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 2, item)
        for row, i in enumerate(msg["AskVolume"]):
            item = QTableWidgetItem()
            item.setText(str(i))
            tableWidget.setItem(row, 3, item)

    def proc_q(self, code, msg):
        """
        Q/TFE/TXFH9 
         {'AskPrice': [10481.0, 10482.0, 10483.0, 10484.0, 10485.0], 'AskVolSum': 321, 'AskVolume': [14, 38, 46, 86, 137], 'BidPrice': [10480.0, 10479.0, 10478.0, 10477.0, 10476.0], 'BidVolSum': 309, 'BidVolume': [27, 65, 71, 62, 84], 'Code': 'TXFH9', 'Date': '2019/08/19', 'DiffAskVol': [0, 0, 0, 0, 0], 'DiffAskVolSum': 0, 'DiffBidVol': [1, 0, 0, 0, 0], 'DiffBidVolSum': 1, 'FirstDerivedAskPrice': 10482.0, 'FirstDerivedAskVolume': 5, 'FirstDerivedBidPrice': 10479.0, 'FirstDerivedBidVolume': 9, 'TargetKindPrice': 10502.04, 'Time': '13:06:24.491000'}
        """
        tableWidget = self.trade.bidask_grid
        for row, i in enumerate(msg["BidVolume"]):
            item = QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setText(str(i))
            tableWidget.setItem(row + 5, 0, item)
        pricelst = list(reversed(msg["AskPrice"])) + msg["BidPrice"]
        for row, i in enumerate(pricelst):
            item = QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setText(str(i))
            tableWidget.setItem(row, 1, item)
        for row, i in enumerate(reversed(msg["AskVolume"])):
            item = QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setText(str(i))
            tableWidget.setItem(row, 3, item)

    def proc_l(self, code, msg):
        """
        L/TFE/TXFH9
         {'Amount': [10480.0], 'AmountSum': [804564419.0], 'AvgPrice': [10477.736352034171], 'Close': [10480.0], 'Code': 'TXFH9', 'Date': '2019/08/19', 'DiffPrice': [68.0], 'DiffRate': [0.6530925854782943], 'DiffType': [2], 'High': [10489.0], 'Low': [10419.0], 'Open': 10436.0, 'TargetKindPrice': 10502.04, 'TickType': [2], 'Time': '13:06:24.513000', 'TradeAskVolSum': 42629, 'TradeBidVolSum': 40982, 'VolSum': [76788], 'Volume': [1]}
        """
        self.trade.code_edit.setText(msg["Code"])
        self.trade.curr_price.display(msg["Close"][0])
        self.trade.diff_price.display(msg["DiffPrice"][0])
        self.trade.tick_vol.display(msg["Volume"][0])
        self.trade.total_vol.display(msg["VolSum"][0])
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        item.setText(str(msg["Volume"][0]))
        itemClear = QTableWidgetItem()
        itemClear.setText(" ")
        tableWidget = self.trade.bidask_grid
        ask = tableWidget.item(4, 1).text()
        bid = tableWidget.item(5, 1).text()
        # print(ask, bid, msg["Close"][0])
        if str(msg["Close"][0]) == ask:
            tableWidget.setItem(4, 2, item)
            tableWidget.setItem(5, 2, itemClear)
        if str(msg["Close"][0]) == bid:
            tableWidget.setItem(4, 2, itemClear)
            tableWidget.setItem(5, 2, item)

    def logo(self):
        pixmap = QtGui.QPixmap("img/shioaji.png")
        lbl = QtWidgets.QLabel()
        lbl.setAlignment(QtCore.Qt.AlignRight)
        lbl.setPixmap(pixmap)
        return lbl

    def quote_msg(self, topic, msg):
        self.rtUpdate.caller.emit(topic, msg)

    def login(self):
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
        self.api.quote.subscribe(self.api.Contracts.Stocks["2330"])
        self.api.quote.subscribe(self.api.Contracts.Stocks["2330"], quote_type="bidask")
        self.api.quote.subscribe(self.api.Contracts.Stocks["2383"])
        self.api.quote.subscribe(self.api.Contracts.Stocks["2383"], quote_type="bidask")
        self.api.quote.subscribe(self.api.Contracts.Stocks["4947"])
        self.api.quote.subscribe(self.api.Contracts.Stocks["4947"], quote_type="bidask")
        self.api.quote.subscribe(self.api.Contracts.Stocks["4935"])
        self.api.quote.subscribe(self.api.Contracts.Stocks["4935"], quote_type="bidask")


class BidAskDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)
        self.progressbaroption = QtWidgets.QStyleOptionProgressBar()

    def paint(self, painter, option, index):
        # if index.column() == 2 and index.row() == 0:
        if index.data():
            data = int(index.data())
            self.progressbaroption.rect = option.rect.adjusted(2, 2, -2, -2)
            self.progressbaroption.minimun = 0
            self.progressbaroption.maximum = max(100, data)
            self.progressbaroption.progress = data
            self.progressbaroption.text = f"{data}"
            self.progressbaroption.textVisible = True

            QtWidgets.QApplication.style().drawControl(
                QtWidgets.QStyle.CE_ProgressBar, self.progressbaroption, painter
            )
        else:
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)


class trade_widget(QWidget, Ui_Form):
    def __init__(self):
        super(trade_widget, self).__init__()
        self.setupUi(self)
        self.login = None
        self.login_button.clicked.connect(self._login)
        delegate = BidAskDelegate(self.bidask_grid)
        self.bidask_grid.setItemDelegateForColumn(0, delegate)
        self.bidask_grid.setItemDelegateForColumn(3, delegate)

    @Slot()
    def _login(self):
        if self.login:
            self.login()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = mainUI()
    window.show()
    sys.exit(app.exec_())
