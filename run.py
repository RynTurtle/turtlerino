import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg 
from gui.main_window import *
import sys

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon("static/icon.ico"))
    mainwindow = main_window()
    mainwindow.show() 
    app.exec_()
    