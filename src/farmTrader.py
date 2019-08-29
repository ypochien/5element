import sys
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from PySide2.QtCore import QObject, Signal, Slot, QFile
from shioaji.constant import *
import shioaji as sj
import asyncio
import platform
from ui.ui_mainWindow import Ui_MainWindow
from ui.ui_quotereport import Ui_QouteReport
from ui.ui_trade import Ui_Form
from dataclasses import dataclass


class RTUpdate(QObject):
    caller = Signal((str, dict))
    placeorder = Signal((sj.contracts.Contract, sj.order.Order))


class mainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainUI, self).__init__(parent)
        self.setupUi(self)
        self.trade = trade_widget(self)
        self.quote_report = quote_report_widget(self)
        self.trade.login = self.login
        self.grid_layout.addWidget(self.trade, 0, 0)
        self.grid_layout.addWidget(self.logo(), 0, 1)
        self.grid_layout.addWidget(self.quote_report, 1, 0, 1, 2)
        self.setWindowIcon(QtGui.QIcon("img/shioaji.png"))
        # event
        self.rtUpdate = RTUpdate()
        self.rtUpdate.caller.connect(self.rt_worker)
        self.rtUpdate.placeorder.connect(self.placeorder_worker)
        self.api = sj.Shioaji()

    @Slot(sj.contracts.Contract, sj.order.Order)
    def placeorder_worker(self, contract, order):
        print(self.api.place_order(contract, order))

    @Slot(str, dict)
    def rt_worker(self, topic, msg):
        """"""
        topic_type = topic.split("/")[0]
        code = topic.split("/")[-1]
        {"MKT": self.proc_mkt, "QUT": self.proc_qut, "Q": self.proc_q, "L": self.proc_l}[topic_type](code, msg)

    def proc_mkt(self, code, msg):
        """
         MKT/idcdmzpcr01/TSE/2330
         {'Close': [252.5], 'Time': '13:06:24.674650', 'VolSum': [17280], 'Volume': [1]}
        """

        msg["Code"] = code
        msg["CodeName"] = f"{code} {self.api.Contracts.Stocks[code]['name']}"
        msg["DiffPrice"] = [0]
        self.trade.update_quote(code, msg)
        self.quote_report.update_quote(code, msg)

    def proc_qut(self, code, msg):
        """
          QUT/idcdmzpcr01/TSE/2330
         {'AskPrice': [253.0, 253.5, 254.0, 254.5, 255.0], 'AskVolume': [2429, 2818, 1266, 624, 2313], 'BidPrice': [252.5, 252.0, 251.5, 251.0, 250.5], 'BidVolume': [377, 809, 712, 1607, 883], 'Date': '2019/08/19', 'Time': '13:06:24.674650'}
        """
        msg["Code"] = f"{code}"
        msg["CodeName"] = f"{code} {self.api.Contracts.Stocks[code]['name']}"
        self.trade.update_bidask(code, msg)

    def proc_q(self, code, msg):
        """
        Q/TFE/TXFH9 
         {'AskPrice': [10481.0, 10482.0, 10483.0, 10484.0, 10485.0], 'AskVolSum': 321, 'AskVolume': [14, 38, 46, 86, 137], 'BidPrice': [10480.0, 10479.0, 10478.0, 10477.0, 10476.0], 'BidVolSum': 309, 'BidVolume': [27, 65, 71, 62, 84], 'Code': 'TXFH9', 'Date': '2019/08/19', 'DiffAskVol': [0, 0, 0, 0, 0], 'DiffAskVolSum': 0, 'DiffBidVol': [1, 0, 0, 0, 0], 'DiffBidVolSum': 1, 'FirstDerivedAskPrice': 10482.0, 'FirstDerivedAskVolume': 5, 'FirstDerivedBidPrice': 10479.0, 'FirstDerivedBidVolume': 9, 'TargetKindPrice': 10502.04, 'Time': '13:06:24.491000'}
        """
        msg["Code"] = f"{code}"
        msg["CodeName"] = f"{code} {self.api.Contracts.Futures[code]['name']}"
        self.trade.update_bidask(code, msg)

    def proc_l(self, code, msg):
        """
        L/TFE/TXFH9
         {'Amount': [10480.0], 'AmountSum': [804564419.0], 'AvgPrice': [10477.736352034171], 'Close': [10480.0], 'Code': 'TXFH9', 'Date': '2019/08/19', 'DiffPrice': [68.0], 'DiffRate': [0.6530925854782943], 'DiffType': [2], 'High': [10489.0], 'Low': [10419.0], 'Open': 10436.0, 'TargetKindPrice': 10502.04, 'TickType': [2], 'Time': '13:06:24.513000', 'TradeAskVolSum': 42629, 'TradeBidVolSum': 40982, 'VolSum': [76788], 'Volume': [1]}
        """
        msg["Code"] = f"{code}"
        msg["CodeName"] = f"{code} {self.api.Contracts.Futures[code]['name']}"

        self.trade.update_quote(code, msg)
        self.quote_report.update_quote(code, msg)

    def logo(self):
        pixmap = QtGui.QPixmap("img/shioaji.png")
        lbl = QtWidgets.QLabel()
        lbl.setAlignment(QtCore.Qt.AlignRight)
        lbl.setPixmap(pixmap)
        return lbl

    def quote_msg(self, topic, msg):
        self.rtUpdate.caller.emit(topic, msg)
        # self.rt_worker(topic, msg)

    def login(self):
        user = {"uid": self.trade.id_edit.text(), "password": self.trade.password_edit.text()}
        try:
            self.api.login(user["uid"], user["password"])
        except asyncio.TimeoutError:
            self.trade.code_edit.setText("目前暫停服務")
            self.trade.code_edit.repaint()
            return

        if "Darwin" != platform.system():
            print("Darwin", platform.system())
            self.api.activate_ca(f"C:/ekey/551/{user['uid']}/SinoPac.pfx", user["uid"], user["uid"])

        self.trade.login_button.setText("已登入")
        self.trade.login_button.repaint()
        api = self.api
        api.quote.set_callback(self.quote_msg)
        api.quote.subscribe(self.api.Contracts.Futures["TXFI9"])
        api.quote.subscribe(self.api.Contracts.Futures["TXFI9"], quote_type="bidask")
        api.quote.subscribe(self.api.Contracts.Futures["MXFI9"])
        api.quote.subscribe(self.api.Contracts.Futures["MXFI9"], quote_type="bidask")
        api.get_stock_account_unreal_profitloss().update()
        for item in api.get_stock_account_unreal_profitloss().data()["summary"]:
            if api.Contracts.Stocks[item["stock"]] == None:
                print(f'已下市{item["stock"]}')
                continue
            api.quote.subscribe(api.Contracts.Stocks[item["stock"]])
            api.quote.subscribe(api.Contracts.Stocks[item["stock"]], quote_type="bidask")


class quote_report_widget(QWidget, Ui_QouteReport):
    def __init__(self, parent):
        super(quote_report_widget, self).__init__()
        self.setupUi(self)
        self.parent = parent
        self.raw = dict()
        self.model = QtGui.QStandardItemModel()
        self.quotereport.setModel(self.model)
        header = ["商品", "成交價", "單量", "成交量", "時間"]
        for i, v in enumerate(header):
            item = QtGui.QStandardItem(v)
            self.model.setHorizontalHeaderItem(i, item)
        self.load_data()
        model = self.quotereport.selectionModel()
        model.selectionChanged.connect(self.handleSelectionChanged)

    def handleSelectionChanged(self, selected, deselected):
        ranged = selected.indexes()
        if ranged:
            row = ranged[0].row()
            code = self.model.item(row, 0).text()
            self.parent.trade.selectedCode = code
            contract = (
                self.parent.api.Contracts.Stocks[code]
                if self.parent.api.Contracts.Stocks[code]
                else self.parent.api.Contracts.Futures[code]
            )
            codename = f"{code} {contract['name']}"
            self.parent.trade.code_edit.setText(codename)
            self.parent.trade.update_unreal(code)

    def load_data(self):
        model = self.model
        row_n = 0
        for k, v in self.raw.items():
            for coln, i in enumerate(v):
                item = QtGui.QStandardItem(i)
                model.setItem(row_n, coln, item)

            row_n += 1

    def update_quote(self, code, msg):
        self.raw[code] = [msg["Code"], str(msg["Close"][0]), str(msg["Volume"][0]), str(msg["VolSum"][0]), msg["Time"]]
        self.load_data()


class trade_widget(QWidget, Ui_Form):
    def __init__(self, parent):
        super(trade_widget, self).__init__()
        self.setupUi(self)
        self.parent = parent
        self.selectedCode = None
        self.login = None
        self.bidprice = None
        self.askprice = None
        self.login_button.clicked.connect(self._login)
        delegate = BidAskDelegate(self.bidask_grid)
        self.bidask_grid.setItemDelegateForColumn(0, delegate)
        self.bidask_grid.setItemDelegateForColumn(3, delegate)
        self.bid_button.clicked.connect(self.bid_placeorder)
        self.ask_button.clicked.connect(self.ask_placeorder)
        self.bidask_grid.cellClicked.connect(self.hander_click)
        self.code_edit.returnPressed.connect(self.sub_new_code)

    def sub_new_code(self):
        code = self.code_edit.text()
        api = self.parent.api
        api.quote.subscribe(api.Contracts.Stocks[code])
        api.quote.subscribe(api.Contracts.Stocks[code], quote_type="bidask")

    def hander_click(self, row, col):
        price = self.bidask_grid.item(row, 1).text()
        if price and col == 0:
            self.bid_placeorder(price=price)
        if price and col == 3:
            self.ask_placeorder(price=price)

    def bid_placeorder(self, price=None):
        self.place_order("bid", price)

    def ask_placeorder(self, price=None):
        self.place_order("ask", price)

    def place_order(self, bidask, price=None):
        print(self.bidprice, self.askprice)
        selectedCode = self.selectedCode
        api = self.parent.api
        contract = (
            api.Contracts.Stocks[selectedCode]
            if api.Contracts.Stocks[selectedCode]
            else api.Contracts.Futures[selectedCode]
        )
        if contract:
            # if price == None:
            # price = self.bidprice if bidask == "ask" else self.askprice

            print(bidask, contract, price)
            if contract.security_type == "STK":
                if price:
                    sample_order = api.Order(
                        price=price,
                        quantity=self.qty_spin.value(),
                        action=ACTION_SELL if bidask == "ask" else ACTION_BUY,
                        price_type=STOCK_PRICE_TYPE_LIMITPRICE,
                        order_type=STOCK_ORDER_TYPE_COMMON,
                    )
                else:
                    sample_order = api.Order(
                        price="",
                        quantity=self.qty_spin.value(),
                        action=ACTION_SELL if bidask == "ask" else ACTION_BUY,
                        price_type=STOCK_PRICE_TYPE_LIMITDOWN if bidask == "ask" else STOCK_PRICE_TYPE_LIMITUP,
                        order_type=STOCK_ORDER_TYPE_COMMON,
                    )

            elif contract.security_type == "FUT":
                sample_order = api.Order(
                    price=price if price else 0,
                    quantity=self.qty_spin.value(),
                    action=ACTION_SELL if bidask == "ask" else ACTION_BUY,
                    price_type=FUTURES_PRICE_TYPE_LMT if price else FUTURES_PRICE_TYPE_MKP,
                    order_type=FUTURES_ORDER_TYPE_ROD if price else FUTURES_ORDER_TYPE_IOC,
                )
            elif contract.security_type == "OPT":
                pass

            self.parent.rtUpdate.placeorder.emit(contract, sample_order)
            # print(api.place_order(contract, sample_order))

    def update_bidask(self, topic, msg):
        if msg["Code"] != self.selectedCode:
            return
        tableWidget = self.bidask_grid

        for row, i in enumerate(msg["BidVolume"]):
            item = QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setText(str(i))
            tableWidget.setItem(row + 5, 0, item)
        self.bidprice = msg["BidPrice"][0]
        self.askprice = msg["AskPrice"][0]
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

    def update_quote(self, topic, msg):
        if msg["Code"] != self.selectedCode:
            return

        self.curr_price.display(msg["Close"][0])
        self.diff_price.display(msg["DiffPrice"][0])
        self.tick_vol.display(msg["Volume"][0])
        self.total_vol.display(msg["VolSum"][0])
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        item.setText(str(msg["Volume"][0]))
        itemClear = QTableWidgetItem()
        itemClear.setText(" ")
        tableWidget = self.bidask_grid
        ask = tableWidget.item(4, 1).text()
        bid = tableWidget.item(5, 1).text()
        if str(msg["Close"][0]) == ask:
            tableWidget.setItem(4, 2, item)
            tableWidget.setItem(5, 2, itemClear)
        if str(msg["Close"][0]) == bid:
            tableWidget.setItem(4, 2, itemClear)
            tableWidget.setItem(5, 2, item)

        self.update_unreal(msg["Code"])

    def update_unreal(self, code):
        api = self.parent.api
        api.get_stock_account_unreal_profitloss().update()
        unreals_summary = api.get_stock_account_unreal_profitloss().data()["summary"]
        text_unreal = ""
        for item in unreals_summary:
            if code != item["stock"]:
                continue
            text_unreal = f"均價: {item['avgprice']} / 庫存: {int(item['real_qty'])//1000} / 損益: {item['unreal']}"
            break
        self.unreal_profit_edit.setText(text_unreal)
        self.unreal_profit_edit.repaint()

    @Slot()
    def _login(self):
        if self.login:
            self.login()


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

            QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_ProgressBar, self.progressbaroption, painter)
        else:
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    sysstr = platform.system()
    print(sysstr)
    # at Windows - ['windowsvista', 'Windows', 'Fusion']
    # print(QtWidgets.QStyleFactory.keys())
    window = mainUI()
    window.show()
    sys.exit(app.exec_())
