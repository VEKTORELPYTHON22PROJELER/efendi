import sys
from  PyQt5.QtWidgets import QApplication,QMainWindow
from  PyQt5.QtGui import QIcon
from PyQt5 import uic 

class ListOfPeople(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
       

    def initUI(self):
        uic.loadUi(r"UI\Listofpeople.ui",self)
        # self.show()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ListOfPeople()
    ex.show()
    sys.exit(app.exec_())
        