import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from lib.YouViewerLayout import Ui_MainWindow
import re
import datetime

#웹에서 배포시 상대경로로 설정

#form_class = uic.loadUiType('C:/python/pyqt_proj/ui/you_viewer_v1.0.ui')[0] # 절대경로

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initAuthLock()

# 기본 비활성화 설정
    def initAuthLock(self):
        self.previewButton.setEnabled(False)
        self.fileNaviButton.setEnabled(False)
        self.streamCombobox.setEnabled(False)
        self.startButton.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.urlTextEdit.setEnabled(False)
        self.pathTextEdit.setEnabled(False)
        self.showStatusMsg('인증을 해주세요')

# UI 활성화
    def initAuthActive(self):
        self.previewButton.setEnabled(True)
        self.fileNaviButton.setEnabled(True)
        self.streamCombobox.setEnabled(True)
        self.calendarWidget.setEnabled(True)
        self.urlTextEdit.setEnabled(True)
        self.pathTextEdit.setEnabled(True)
        self.showStatusMsg('인증완료')

    def showStatusMsg(self,msg):
        self.statusbar.showMessage(msg)

if __name__=='__main__':
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()
