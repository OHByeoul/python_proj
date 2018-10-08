import sys
from PyQt5.QtWidgets import *

class AuthDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setupUi()

        self.user_id = None
        self.user_pw = None


    def setupUi(self):
        self.setGeometry(900,500,300,100)
        self.setWindowTitle('Sign in')
        self.setFixedSize(300,100)

        idLabel = QLabel('ID ')
        passwordLabel = QLabel('Password ')

        self.idInput = QLineEdit()
        self.pwdInput = QLineEdit()
        self.pwdInput.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton('로그인')
        self.loginButton.clicked.connect(self.submitLogin) #click시그널에 로그인 슬롯 넣음

        layout = QGridLayout() # 행렬처럼 행과 열을 받아서 위치를 정함
        layout.addWidget(idLabel,0,0)
        layout.addWidget(self.idInput,0,1)
        layout.addWidget(self.loginButton,0,2)

        layout.addWidget(passwordLabel,1,0)
        layout.addWidget(self.pwdInput,1,1)

        self.setLayout(layout)

    def submitLogin(self):
        self.user_id = self.idInput.text()
        self.user_pw = self.pwdInput.text()

        if self.user_id is None or self.user_id == '' or not self.user_id:
            QMessageBox.about(self,'인증오류','ID를 입력하세요')
            self.idInput.setFocus(True)
            return None

        if self.user_pw is None or self.user_pw =='' or not self.user_pw:
            QMessageBox.about(self,'인증오류','PW를 입력하세요')
            self.pwdInput.setFocus(True)
            return None


        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginDialog = AuthDialog()
    loginDialog.show()
    app.exec_()
