import sys
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow,QWidget
from PySide2.QtCore import QObject, Signal, Slot,QFile
from ui_mainWindow import Ui_MainWindow
from ui_trade import Ui_Form

class mainUI(QMainWindow,Ui_MainWindow):
    def __init__(self,parent =None):
        super(mainUI,self).__init__(parent)
        self.setupUi(self)
        self.trade = trade_widget()
        self.horizontalLayout.addWidget(self.trade)
        self.horizontalLayout.addWidget(self.logo())
        self.setWindowIcon(QtGui.QIcon('img/shioaji.png')) 
        # event
        self.trade.login_button.clicked.connect(self.login)
    
    def logo(self):
        pixmap = QtGui.QPixmap("img/shioaji.png")
        lbl = QtWidgets.QLabel()
        lbl.setAlignment(QtCore.Qt.AlignRight)
        lbl.setPixmap(pixmap)
        return lbl

    @Slot()
    def login(self):
        self.trade.login_button.setText("已登入")

class trade_widget(QWidget,Ui_Form):
    def __init__(self):
        super(trade_widget, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = mainUI()
    window.show()
    sys.exit(app.exec_())