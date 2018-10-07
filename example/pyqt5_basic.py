import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

label = QLabel("first test")
label.show()

print('before')
app.exec_()
print('after')
