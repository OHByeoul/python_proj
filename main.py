import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl
from PyQt5 import uic
from lib.YouViewerLayout import Ui_MainWindow
from lib.AuthDialog import AuthDialog
import re
import datetime
import pytube

#웹에서 배포시 상대경로로 설정

#form_class = uic.loadUiType('C:/python/pyqt_proj/ui/you_viewer_v1.0.ui')[0] # 절대경로

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initAuthLock()
        self.initSignal() # 시그널 초기화
        #youtube관련 작업에 사용
        self.youtb = None
        self.youtb_size = 0

        #로그인 관련 변수선언
        self.user_id = None
        self.user_pw = None
        #동영상 재생여부 flag
        self.is_play = False
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

    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)
        self.previewButton.clicked.connect(self.load_url)
        self.exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.webEngineView.loadProgress.connect(self.showProgressBroswerLoading)
        self.fileNaviButton.clicked.connect(self.selectDownPath)
        self.calendarWidget.clicked.connect(self.append_date)
        self.startButton.clicked.connect(self.downloadYouTube)

    @pyqtSlot()
    def authCheck(self):
        dlg = AuthDialog()
        dlg.exec_()
        self.user_id = dlg.user_id
        self.user_pw = dlg.user_pw

        #print('id: %s password: %s' %(self.user_id,self.user_pw))

        if True:
            self.initAuthActive()
            self.loginButton.setText('로그인 완료')
            self.loginButton.setEnabled(False)
            self.urlTextEdit.setFocus(True)
            self.append_log_msg('login Success')
        else:
            QMessageBox.about(self,'인증오류','아이디 혹은 비밀번호가 틀렸습니다')

    def load_url(self):
        url = self.urlTextEdit.text().strip() #공백제거
        v = re.compile('^https://www.youtube.com/?')
        if self.is_play:
            self.append_log_msg('Stop Click')
            self.webEngineView.load(QUrl('about:blank'))
            self.previewButton.setText('재생')
            self.is_play = False
            self.urlTextEdit.clear()
            self.urlTextEdit.setFocus(True)
            self.startButton.setEnabled(False)
            self.streamCombobox.clear()
            self.progressBar_2.setValue(0)
            self.showStatusMsg('인증완료')
        else:
            if v.match(url) is not None:
                self.append_log_msg('Play Click')
                self.webEngineView.load(QUrl(url))
                self.showStatusMsg(url+' 재생 중')
                self.previewButton.setText('중지')
                self.is_play = True
                self.startButton.setEnabled(True)
                self.initialYouWork(url)
            else :
                QMessageBox.about(self,'URL 형식오류','Youtube 주소 형식이 아닙니다')
                self.urlTextEdit.clear()
                self.urlTextEdit.setFocus(True)

    def initialYouWork(self, url):
        video_list = pytube.YouTube(url)
        #로딩바 계산
        video_list.register_on_progress_callback(self.showProgressDownloading)

        self.youtb = video_list.streams.all()
        self.streamCombobox.clear()
        for e in self.youtb:
            tmp_list, str_list = [],[]
            tmp_list.append(str(e.mime_type or '')) #mime 타입이 없으면 공백
            tmp_list.append(str(e.res or ''))
            tmp_list.append(str(e.fps or ''))
            tmp_list.append(str(e.abr or ''))

            str_list = [y for y in tmp_list if y != '']
            self.streamCombobox.addItem(','.join(str_list))


    def append_log_msg(self,msg):
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        app_msg = self.user_id+' : ' +msg+'('+nowDatetime+')'
        self.logTextEdit.appendPlainText(app_msg)

        with open('C:/python/pyqt_proj/log.txt','a') as file:
            file.write(app_msg+'\n')

    @pyqtSlot(int)
    def showProgressBroswerLoading(self,v):
        self.progressBar.setValue(v)

    @pyqtSlot()
    def selectDownPath(self):
        #파일선택 파일 불러와서 작업할때
        #fname = QFileDialog.getOpenFileName(self)
        #self.pathTextEdit.setText(fname[0])
        #경로선택
        fpath = QFileDialog.getExistingDirectory(self,'Select Directory')
        self.pathTextEdit.setText(fpath)

    @pyqtSlot()
    def append_date(self):
        selected_date = self.calendarWidget.selectedDate()
        #print('click date ', self.calendarWidget.selectedDate().toString())
        print(str(selected_date.year())+'-'+str(selected_date.month())+'-'+str(selected_date.day()))
        self.append_log_msg('Calendar Click')

    @pyqtSlot()
    def downloadYouTube(self):
        down_dir = self.pathTextEdit.text().strip()

        if down_dir is None or down_dir =='' or not down_dir:
            QMessageBox.about(self,'경로 선택','다운받을 경로를 선택하세요')
            return None

        self.youtb_fsize = self.youtb[self.streamCombobox.currentIndex()].filesize
        self.youtb[self.streamCombobox.currentIndex()].download(down_dir)
        self.append_log_msg('Download_Click')

    def showProgressDownloading(self, stream, chunk, finle_handle, bytes_remaining):
        self.progressBar_2.setValue(int(((self.youtb_fsize-bytes_remaining)/self.youtb_fsize)*100))

if __name__=='__main__':
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()
