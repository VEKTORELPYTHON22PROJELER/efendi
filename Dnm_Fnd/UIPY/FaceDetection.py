

import sys
from  PyQt5.QtWidgets import QApplication,QWidget
from  PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtGui import QImage,QPixmap
import cv2

class YuzTani(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        uic.loadUi(r"UI\FaceDetection.ui",self)
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
        
        faces_cascade=cv2.CascadeClassifier(r"UIPY\cascades\haarcascade_frontalface_default.xml")
        while True:

            ret,frame = self.cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces=faces_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
            for (x,y,w,h) in faces:
                roi_gray=gray[y:y+h,x:x+w]
                roi_color=frame[y:y+h,x:x+w]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) 
                
               
            
            buyumeFaktor = 0.5
            frame = cv2.resize(frame,None,fx=buyumeFaktor,fy=buyumeFaktor,
            interpolation=cv2.INTER_AREA)

            heigth,width,channel = frame.shape
            step = channel*width
            qImg = QImage(frame.data,width,heigth,step,QImage.Format_BGR888)
            self.lbCamera.setPixmap(QPixmap.fromImage(qImg))
            if cv2.waitKey(1) & 0xFF == ord("t"):
                    cv2.imwrite("oldumu.jpg",frame)
          
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            
            
                
        self.cam.release()
        self.timer.stop()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = YuzTani()
    ex.show()
    sys.exit(app.exec_())        
