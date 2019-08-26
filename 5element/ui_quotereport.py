# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/quotereport.ui',
# licensing of 'ui/quotereport.ui' applies.
#
# Created: Tue Aug 20 00:19:34 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_QouteReport(object):
    def setupUi(self, QouteReport):
        QouteReport.setObjectName("QouteReport")
        QouteReport.resize(732, 535)
        self.quotereport = QtWidgets.QTableView(QouteReport)
        self.quotereport.setGeometry(QtCore.QRect(0, 0, 740, 540))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quotereport.sizePolicy().hasHeightForWidth())
        self.quotereport.setSizePolicy(sizePolicy)
        self.quotereport.setObjectName("quotereport")

        self.retranslateUi(QouteReport)
        QtCore.QMetaObject.connectSlotsByName(QouteReport)

    def retranslateUi(self, QouteReport):
        QouteReport.setWindowTitle(QtWidgets.QApplication.translate("QouteReport", "Form", None, -1))

