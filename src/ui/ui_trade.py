# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/trade.ui',
# licensing of 'ui/trade.ui' applies.
#
# Created: Fri Aug 30 12:16:49 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(287, 399)
        Form.setMinimumSize(QtCore.QSize(287, 399))
        Form.setMaximumSize(QtCore.QSize(287, 399))
        font = QtGui.QFont()
        font.setFamily("Lantinghei TC")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        Form.setFont(font)
        self.ask_button = QtWidgets.QPushButton(Form)
        self.ask_button.setGeometry(QtCore.QRect(220, 56, 60, 25))
        self.ask_button.setObjectName("ask_button")
        self.login_button = QtWidgets.QPushButton(Form)
        self.login_button.setGeometry(QtCore.QRect(146, 10, 67, 40))
        self.login_button.setFlat(False)
        self.login_button.setObjectName("login_button")
        self.bid_button = QtWidgets.QPushButton(Form)
        self.bid_button.setGeometry(QtCore.QRect(148, 56, 65, 24))
        self.bid_button.setObjectName("bid_button")
        self.id_edit = QtWidgets.QLineEdit(Form)
        self.id_edit.setGeometry(QtCore.QRect(12, 9, 130, 21))
        self.id_edit.setMaxLength(10)
        self.id_edit.setClearButtonEnabled(False)
        self.id_edit.setObjectName("id_edit")
        self.password_edit = QtWidgets.QLineEdit(Form)
        self.password_edit.setGeometry(QtCore.QRect(12, 32, 130, 20))
        self.password_edit.setInputMask("")
        self.password_edit.setMaxLength(20)
        self.password_edit.setFrame(True)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setObjectName("password_edit")
        self.bidask_grid = QtWidgets.QTableWidget(Form)
        self.bidask_grid.setGeometry(QtCore.QRect(10, 140, 270, 256))
        self.bidask_grid.setMinimumSize(QtCore.QSize(270, 241))
        self.bidask_grid.setLineWidth(1)
        self.bidask_grid.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.bidask_grid.setTabKeyNavigation(False)
        self.bidask_grid.setTextElideMode(QtCore.Qt.ElideNone)
        self.bidask_grid.setShowGrid(True)
        self.bidask_grid.setGridStyle(QtCore.Qt.CustomDashLine)
        self.bidask_grid.setWordWrap(False)
        self.bidask_grid.setCornerButtonEnabled(False)
        self.bidask_grid.setRowCount(10)
        self.bidask_grid.setColumnCount(4)
        self.bidask_grid.setObjectName("bidask_grid")
        self.bidask_grid.setColumnCount(4)
        self.bidask_grid.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.bidask_grid.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.bidask_grid.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.bidask_grid.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.bidask_grid.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.bidask_grid.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.bidask_grid.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.bidask_grid.setItem(1, 1, item)
        self.bidask_grid.horizontalHeader().setVisible(True)
        self.bidask_grid.horizontalHeader().setDefaultSectionSize(67)
        self.bidask_grid.horizontalHeader().setHighlightSections(True)
        self.bidask_grid.horizontalHeader().setStretchLastSection(True)
        self.bidask_grid.verticalHeader().setVisible(False)
        self.bidask_grid.verticalHeader().setDefaultSectionSize(23)
        self.code_edit = QtWidgets.QLineEdit(Form)
        self.code_edit.setGeometry(QtCore.QRect(12, 53, 131, 30))
        self.code_edit.setObjectName("code_edit")
        self.unreal_profit_edit = QtWidgets.QLineEdit(Form)
        self.unreal_profit_edit.setGeometry(QtCore.QRect(10, 117, 270, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.unreal_profit_edit.setFont(font)
        self.unreal_profit_edit.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.unreal_profit_edit.setReadOnly(True)
        self.unreal_profit_edit.setPlaceholderText("")
        self.unreal_profit_edit.setObjectName("unreal_profit_edit")
        self.qty_spin = QtWidgets.QSpinBox(Form)
        self.qty_spin.setGeometry(QtCore.QRect(220, 30, 60, 22))
        self.qty_spin.setMaximum(100)
        self.qty_spin.setSingleStep(5)
        self.qty_spin.setProperty("value", 1)
        self.qty_spin.setObjectName("qty_spin")
        self.day_trading_cb = QtWidgets.QCheckBox(Form)
        self.day_trading_cb.setGeometry(QtCore.QRect(220, 10, 73, 16))
        self.day_trading_cb.setObjectName("day_trading_cb")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(10, 85, 271, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.curr_price = QtWidgets.QLCDNumber(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.curr_price.setFont(font)
        self.curr_price.setSmallDecimalPoint(False)
        self.curr_price.setDigitCount(6)
        self.curr_price.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.curr_price.setProperty("value", 0.0)
        self.curr_price.setProperty("intValue", 0)
        self.curr_price.setObjectName("curr_price")
        self.diff_price = QtWidgets.QLCDNumber(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setWeight(50)
        font.setBold(False)
        self.diff_price.setFont(font)
        self.diff_price.setSmallDecimalPoint(False)
        self.diff_price.setDigitCount(4)
        self.diff_price.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.diff_price.setProperty("intValue", 0)
        self.diff_price.setObjectName("diff_price")
        self.tick_vol = QtWidgets.QLCDNumber(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.tick_vol.setFont(font)
        self.tick_vol.setSmallDecimalPoint(False)
        self.tick_vol.setDigitCount(3)
        self.tick_vol.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.tick_vol.setProperty("intValue", 0)
        self.tick_vol.setObjectName("tick_vol")
        self.total_vol = QtWidgets.QLCDNumber(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.total_vol.setFont(font)
        self.total_vol.setSmallDecimalPoint(False)
        self.total_vol.setDigitCount(6)
        self.total_vol.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.total_vol.setProperty("intValue", 0)
        self.total_vol.setObjectName("total_vol")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.ask_button.setText(QtWidgets.QApplication.translate("Form", "賣出", None, -1))
        self.login_button.setText(QtWidgets.QApplication.translate("Form", "Login", None, -1))
        self.bid_button.setText(QtWidgets.QApplication.translate("Form", "買進", None, -1))
        self.id_edit.setPlaceholderText(QtWidgets.QApplication.translate("Form", "ID", None, -1))
        self.password_edit.setPlaceholderText(QtWidgets.QApplication.translate("Form", "Password", None, -1))
        self.bidask_grid.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("Form", "委買", None, -1))
        self.bidask_grid.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("Form", "價格", None, -1))
        self.bidask_grid.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("Form", "量", None, -1))
        self.bidask_grid.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("Form", "委賣", None, -1))
        __sortingEnabled = self.bidask_grid.isSortingEnabled()
        self.bidask_grid.setSortingEnabled(False)
        self.bidask_grid.setSortingEnabled(__sortingEnabled)
        self.code_edit.setPlaceholderText(QtWidgets.QApplication.translate("Form", "商品代碼", None, -1))
        self.day_trading_cb.setText(QtWidgets.QApplication.translate("Form", "先賣", None, -1))

