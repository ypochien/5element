import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow
from uifarmtrade import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        pixmap = QtGui.QPixmap("img/shioaji.png")
        lbl = QtWidgets.QLabel()
        lbl.setAlignment(QtCore.Qt.AlignRight)
        lbl.setPixmap(pixmap)
        self.ui.horizontalLayout.addWidget(lbl)
        self.setWindowIcon(QtGui.QIcon('img/shioaji.png')) 


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())