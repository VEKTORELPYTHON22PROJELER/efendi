

import sys
import os
sys.path.append(os.getcwd() + os.sep+ "DB")
from  PyQt5.QtWidgets import QApplication,QWidget
from  PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.Qt import Qt
import cv2
from DB import DBTool

class YuzTani(QWidget):
    def __init__(self):
        super().__init__()
        self.sayac = 0
        self.timer = QTimer()
        self.db = DBTool(dbAdres=r"DB\facedb.db",tabloAdi="")
        uic.loadUi(r"UI\FaceDetection.ui",self)
        self.kisilerDoldur()
        self.btOpen.clicked.connect(self.KameraAc)
        self.btClose.clicked.connect(self.Kapat)
        self.btTake.clicked.connect(self.getImage)

    
    def kisilerDoldur(self):
        self.db.tabloAdi = "FACES"
        self.kisiler = self.db.select()
        for item in self.kisiler:
            self.cmbkisiler.addItem(item[1])

    def Kapat(self):
        try:
            self.cam.release()
        except:
            pass
        self.timer.stop()
        self.close()


    def KameraAc(self):
        if not self.timer.isActive():
            self.cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            self.timer.start(3)
            os.chdir(os.getcwd()+os.sep+"DATASET")
            try:
                isim = self.cmbkisiler.currentText()
                os.mkdir(isim)
            except:
                pass
            finally:
                os.chdir(os.getcwd()+os.sep+isim)
            self.Gosterim()

        else:
            self.cam.release()
            self.timer.stop()

    def Gosterim(self):
        while True:
            ret,frame = self.cam.read()
            buyumeFaktor = 0.4
            frame = cv2.resize(frame,None,fx=buyumeFaktor,fy=buyumeFaktor,
            interpolation=cv2.INTER_AREA)

            heigth,width,channel = frame.shape
            step = channel*width
            qImg = QImage(frame.data,width,heigth,step,QImage.Format_BGR888)
            self.lbCamera.setPixmap(QPixmap.fromImage(qImg))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.cam.release()
        self.timer.stop()

    def getImage(self):
        pix = self.lbCamera.pixmap()
        import io
        from PIL import Image
        from PyQt5.QtGui import QImage
        from PyQt5.QtCore import QBuffer
        
        img = pix.toImage()
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        img.save(buffer, "JPG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        pil_im.save(f"{self.sayac}.jpg")
        self.sayac+=1
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = YuzTani()
    ex.show()
    sys.exit(app.exec_())        
