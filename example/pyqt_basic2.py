import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TestForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Pyqt Test")
        self.setGeometry(800,400,500,300)

        btn1 = QPushButton("Click1",self)
        btn2 = QPushButton("Click2",self)
        btn3 = QPushButton("Click3",self)

        btn1.move(20,20)
        btn2.move(20,60)
        btn3.move(20,100)

        btn1.clicked.connect(self.btn_1_clicked)
        btn2.clicked.connect(self.btn_2_clicked)
        btn3.clicked.connect(QCoreApplication.instance().quit) # QCoreApplication 현재 실행되고 있는 app

    def btn_1_clicked(self):
        QMessageBox.about(self,'message','clicked')
    def btn_2_clicked(self):
        print('clicked')

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = TestForm()
    window.show()
    app.exec_()
