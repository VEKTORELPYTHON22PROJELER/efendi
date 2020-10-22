import sys
import os
sys.path.append(os.getcwd() + os.sep+ "DB")
from  PyQt5.QtWidgets import QApplication,QMainWindow
from  PyQt5.QtGui import QIcon
from PyQt5 import uic
from DB import DBTool


class ListOfPeople(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DBTool(dbAdres=r"DB\facedb.db",tabloAdi="")
        self.ilListe = []
        self.initUI()

       

    def initUI(self):
        uic.loadUi(r"UI\Listofpeople.ui",self)
        self.cmbIlDoldur()
        self.cmbil.currentIndexChanged.connect(self.cmbilceDoldur)
        
    
    def cmbIlDoldur(self):
        self.cmbil.addItem("Seçiniz")
        self.db.tabloAdi = "ST_ILLER"
        self.ilListe = self.db.select()
        for item in self.ilListe:
            self.cmbil.addItem(item[1])

    def cmbilceDoldur(self):
        self.db.tabloAdi = "ST_ILCELER"
        ilid = ""
        for item in self.ilListe:
            if item[1] == self.cmbil.currentText():
                ilid = item[0]
                break
        self.cmbilce.clear()
        self.ilceListe = self.db.select(sart=f"IL_ID={ilid}")
        for item in self.ilceListe:
            self.cmbilce.addItem(item[1])


    def Kaydet(self):
        isim =  self.isim.Text()
        soyisim = self.soyisim.Text()
        ilId = self.ilListe[self.ilListe.index(self.cmbil.currentText())][0]
        ilId = self.ilceListe[self.ilceListe.index(self.cmbilce.currentText())][0]
        self.db.tabloAdi = "FACES"
        self.db.insert(alan=["NAME", "LAST_NAME", "IL_ID", "ILCE_ID"],deger=[f"'{isim}'"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ListOfPeople()
    ex.show()
    sys.exit(app.exec_())
        