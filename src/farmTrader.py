import sys
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QObject, Signal, Slot,QFile

def set_init(MainWindow):
    pixmap = QtGui.QPixmap("img/shioaji.png")
    lbl = QtWidgets.QLabel()
    lbl.setAlignment(QtCore.Qt.AlignRight)
    lbl.setPixmap(pixmap)
    MainWindow.horizontalLayout.addWidget(lbl)
    MainWindow.setWindowIcon(QtGui.QIcon('img/shioaji.png')) 
        
if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    ui_file = QFile("ui/farmtrade.ui")
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file)
    set_init(window)
    ui_file.close()
    window.show()
    sys.exit(app.exec_())