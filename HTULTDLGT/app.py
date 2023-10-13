import sys
import cv2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QDir
from uid import UID

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import imutils
import time
from DeepSort.track_deepsort import *
from Sort.track_sort import *
from speed_calculator import *
from suport import *

global app
global start

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        self.videopath = "E:/LuanVan/Videos/th.mp4"
        self.area_speedcal = None 
        # call QWidget constructor
        super().__init__()
        self.baseUI = UID() # load GUI
        # self.model = loadmodel() # load YOLO model
        self.baseUI.setupUi(self)
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.run)
        self.baseUI.START.clicked.connect(self.start_bt)
        self.baseUI.PAUSE.clicked.connect(self.pause)
        self.baseUI.RESUME.clicked.connect(self.resume)
        self.baseUI.CLOSE.clicked.connect(self.close)
        self.baseUI.GETFILE.clicked.connect(self.getvideofile)
        self.baseUI.sobt.clicked.connect(self.add2lines)
        self.baseUI.GF_le.setText(self.videopath)
        self.baseUI.speedCal_dis_le.setText("20")
        self.area_speedcal = load_indexfromcsv(self.videopath)
        self.FPS = None

        pixmap = QPixmap('E:/LuanVan/HTULTDLGT/IMG/no-video.jpg')
        # qImg = QImage(pixmap.data, 852, 480, 3*480, QImage.Format_RGB888)
        self.baseUI.imgLabel_1.setPixmap(pixmap)
        self.setWindowIcon(QIcon('logo.png'))
    
    def pause(self):
        self.timer.stop()

    def resume(self):
        if self.logic:
            self.timer.start(30)
        else:
            print('>0')

    def close(self):
        self.timer.stop()
        self.detector = None
        self.speed_calculator = None
        
    def start_bt(self):
        tracker_name = self.baseUI.tracking_mt_box.currentText()
        if tracker_name == 'DeepSORT':
            self.detector = DeepSORT_Tracker()
        if tracker_name == 'SORT':
            self.detector = SORT_Tracker()
        self.load_area_speedcal()
        m = self.baseUI.speedCal_dis_le.text()
        self.speed_calculator = SpeedCalculator(int(m), self.y_line2 - self.y_line1)
        print('-> ')
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            # self.cap = cv2.VideoCapture(self.videopath)
            self.cap = loadVideo(self.videopath)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            # start timer
            self.timer.start(30)
            # print(self.timer.start(30))
            self.logic = True

        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()

    def run(self):
        global start
        colorR = (0,0,255)
        colorB = (255,0,0)
        offset = 10     

        ret, frame = self.cap.read()
        if not ret:
            return False
        # nhan dang va truy vet

        start_time = time.time()
        results = self.detector.update_track(frame)
        end_time = time.time()
        self.FPS = round(1.0/(end_time-start_time))

        # tinh van toc
        for result in results:
            x1, y1, x2, y2, id = result
            x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
            w, h = x2 -x1, y2-y1
            cx = (x1+x2)//2
            cy = (y1+y2)//2
            cvzone.putTextRect(frame, f' {int(id)}', (max(0, x1),max(35,y1)), 
                                    scale=1, thickness=1, offset=0)
            
            if cy < (self.y_line2 - offset) and cy > (self.y_line1 - offset) and cx < self.x2_line1 and cx > self.x1_line1 :
                self.speed_calculator.add(id, cx, cy, time.time())
            if cy < (self.y_line2 + offset) and cy > (self.y_line2 - offset) and cx < self.x2_line2 and cx > self.x1_line2:
                self.speed_calculator.calculate(id, self.FPS)
                # self.speed_calculator.test(id)
            if id in self.speed_calculator.speeds:
                cvzone.putTextRect(frame, f' {int(self.speed_calculator.speeds[id])} Km/h', (max(0, x1),max(35,y1)), 
                                    scale=1, thickness=1, offset=0)

            cv2.circle(frame, (cx, cy), 2, (255,0,0),2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), colorB, 1)
            

        # cv2.putText(frame, 'FPS: ' + str(round(vfps)), (50, 90), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255),3)
        # cv2.putText(frame, 'AVG SPEED: ' + str(round(speed.avg_speed, 2)) + "Km/h", (50, 150), cv2.FONT_HERSHEY_PLAIN, 3, colorR,3)
        # cv2.imshow('FRAME', frame)

        # image = imutils.resize(image, width=852)
        cv2.putText(frame, 'FPS: ' + str(self.FPS), (50, 90), cv2.FONT_HERSHEY_PLAIN, 3, colorR,3)
        cv2.line(frame, (self.pointA[0], self.pointA[1]), (self.pointB[0], self.pointA[1]), colorR, 2)
        cv2.line(frame, (self.pointC[0], self.pointC[1]), (self.pointD[0], self.pointC[1]), colorR, 2)
        self.baseUI.lable1.setText(str(self.speed_calculator.avg_speed)+" Km/h")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.baseUI.imgLabel_1.setPixmap(QPixmap.fromImage(qImg))
       
    def getvideofile(self):
        filter_name = 'mp4 (*.mp4*)'
        dirpath = QDir.currentPath() + "/HTULTDLGT/Videos"
        filepath = QFileDialog.getOpenFileName(self, caption='Choose Video File',
                                                    directory=dirpath,
                                                    filter=filter_name)
        print(filepath[0])
        self.baseUI.GF_le.setText(str(filepath[0]))
        self.videopath = str(filepath[0])
        self.video = 0 if self.videopath == None else self.videopath
        self.preview()

    def preview(self):
        f = get_1_frame(self.videopath)
        if self.area_speedcal:
            self.load_area_speedcal()
            cv2.putText(f, "Line 1", (self.pointA[0], self.pointA[1]), cv2.FONT_HERSHEY_PLAIN, 1.2, (0,0,255),2)
            cv2.line(f, (self.pointA[0], self.pointA[1]), (self.pointB[0], self.pointB[1]), (100, 100, 255), 2)
            #line 1
            cv2.putText(f, "Line 2", (self.pointC[0], self.pointC[1]), cv2.FONT_HERSHEY_PLAIN, 1.2, (0,0,255),2)
            cv2.line(f, (self.pointC[0], self.pointC[1]), (self.pointD[0], self.pointD[1]), (14, 200, 255), 2)
        f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        height, width, channel = f.shape
        step = channel * width
        qImg = QImage(f.data, width, height, step, QImage.Format_RGB888)
        self.baseUI.imgLabel_1.setPixmap(QPixmap.fromImage(qImg))


    def load_area_speedcal(self):
        self.area_speedcal = load_indexfromcsv(self.videopath)
        if self.area_speedcal:
            self.pointA, self.pointB, self.pointC, self.pointD = self.area_speedcal
            self.x1_line1, self.x2_line1, self.x1_line2, self.x2_line2 = self.pointA[0], self.pointB[0], self.pointC[0], self.pointD[0]
            self.y_line1, self.y_line2 = self.pointA[1], self.pointC[1]

    def add2lines(self):
        print("Ve 2 doan thang len frame")
        save_path = './HTULTDLGT/Videos/csv/'
        add_new_2lines(self.videopath, save_path)
        self.area_speedcal = load_indexfromcsv(self.videopath)
        self.preview()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # height, width, channel = frame.shape
        # step = channel * width
        # qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # self.baseUI.imgLabel_1.setPixmap(QPixmap.fromImage(qImg))
    

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()    