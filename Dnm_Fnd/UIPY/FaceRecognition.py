

import sys
from  PyQt5.QtWidgets import QApplication,QWidget
from  PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtGui import QImage,QPixmap
import cv2

class YuzKaydet(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        uic.loadUi(r"UI\FaceRecognition.ui",self)
        self.btOpen.clicked.connect(self.KameraAc)
        self.btClose.clicked.connect(self.Kapat)
  

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
            self.Gosterim()
        else:
            self.cam.release()
            self.timer.stop()

    def Gosterim(self):
        while True:
            ret,frame = self.cam.read()
            buyumeFaktor = 0.5
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
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = YuzKaydet()
    ex.show()
    sys.exit(app.exec_())        
