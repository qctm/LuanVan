from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class window2(object):
    def setup(self, wd2):
        wd2.setObjectName("wd")
        wd2.setFixedSize(500, 200)


class UID(object): # UI wd obj.
    def setupUi(self, wd):
        wd.setObjectName("wd")
        wd.setFixedSize(1100, 600)

        self.imgLabel_1 = QtWidgets.QLabel(wd)
        self.imgLabel_1.setGeometry(QtCore.QRect(10, 110, 852, 480))
        self.imgLabel_1.setAutoFillBackground(False)
        self.imgLabel_1.setFrameShape(QtWidgets.QFrame.Box)
        self.imgLabel_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgLabel_1.setLineWidth(2)
        self.imgLabel_1.setScaledContents(True)
        self.imgLabel_1.setObjectName("imgLabel_1")

        self.GETFILE = QtWidgets.QPushButton(wd)
        self.GETFILE.setGeometry(QtCore.QRect(10, 10, 70, 30))
        self.GETFILE.setObjectName("GETFILE")
        self.GF_le = QtWidgets.QLineEdit(wd)
        self.GF_le.setGeometry(QtCore.QRect(90, 12, 200, 27))
        self.GF_le.setEnabled(False)

        self.control_button(wd)
        self.yolo_opt(wd)
        self.tracking_opt(wd)
        # self.speedtext(wd)
        self.add_speedCal_opt_box(wd)
        self.speed_show(wd)
        # self.add_track_opt_box(wd)

        # timer = QTimer(wd)
        # timer.timeout.connect(self.speedtext(wd))
        # timer.start(1000)

        font = QtGui.QFont()
        font.setPointSize(10)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.retranslateUi(wd)
        QtCore.QMetaObject.connectSlotsByName(wd)

    def control_button(self, wd):
        x, y, w, h = 880, 110, 45, 40
        self.START = QtWidgets.QPushButton(wd)
        self.START.setGeometry(QtCore.QRect(x, y, w, h))
        self.START.setObjectName("START")

        self.PAUSE = QtWidgets.QPushButton(wd)
        self.PAUSE.setGeometry(QtCore.QRect(x+50, y, w, h))
        self.PAUSE.setObjectName("PAUSE")

        self.RESUME = QtWidgets.QPushButton(wd)
        self.RESUME.setGeometry(QtCore.QRect(x+100, y, w, h))
        self.RESUME.setObjectName("RESUME")

        self.CLOSE = QtWidgets.QPushButton(wd)
        self.CLOSE.setGeometry(QtCore.QRect(x+150, y, w, h))
        self.CLOSE.setObjectName("CLOSE")

    def speed_show(self, wd):
        self.group_box = QtWidgets.QGroupBox(wd)
        self.group_box.setGeometry(875, 200, 210, 100)
        self.group_box.setTitle("Vận Tốc Trung Bình")
        self.group_box.setFont(QFont('Arial', 13))
        self.group_box.setStyleSheet('QGroupBox:title {color: yellow; background-color: red; subcontrol-origin: margin; subcontrol-position: top center; font-size: 18px; font-weight: bold; }')
        # self.group_box.setStyleSheet('QGroupBox#MOT { border: 3px solid red;}')
        self.lable1 = QtWidgets.QLabel("", wd)
        self.lable1.setAlignment(QtCore.Qt.AlignCenter)
        self.lable1.setFont(QFont('Arial', 20))
        self.lable1.setGeometry(self.group_box.geometry())
    
    def add_speedCal_opt_box(self, wd):
        self.speedCal_opt_box = QtWidgets.QGroupBox(wd)
        self.speedCal_opt_box.setGeometry(750, 10, 340, 90)
        self.speedCal_opt_box.setTitle("Tùy chỉnh cách tính vận tốc")
        self.speedCal_opt_box.setStyleSheet('QGroupBox:title {color: yellow; background-color: red; }')
        
        self.sobt = QtWidgets.QPushButton(wd)
        self.sobt.setGeometry(QtCore.QRect(self.speedCal_opt_box.x()+10, self.speedCal_opt_box.y()+20, 60, 30))
        self.sobt.setObjectName("Add opt")

        self.speedCal_dis_lb = QtWidgets.QLabel("Khoảng cách 2 line (m): ", wd)
        self.speedCal_dis_lb.setGeometry(QtCore.QRect(self.speedCal_opt_box.x()+10, self.speedCal_opt_box.y()+52, 110, 30))
        self.speedCal_dis_le = QtWidgets.QLineEdit(wd)
        self.speedCal_dis_le.setGeometry(QtCore.QRect(self.speedCal_dis_lb.x()+self.speedCal_dis_lb.width()+10, self.speedCal_dis_lb.y(), 60, 27))
        self.speedCal_dis_le.setValidator(QIntValidator())
    
    def add_track_opt_box(self, wd):
        x, y, w, h = 400, 10, 340, 90
        self.track_opt_box = QtWidgets.QGroupBox(wd)
        self.track_opt_box.setGeometry(x, y, w, h)
        self.track_opt_box.setTitle("Tùy chỉnh tracking")
        self.track_opt_box.setStyleSheet('QGroupBox:title {color: yellow; background-color: red; }')
        
        self.track_opt_min_conf_lb = QtWidgets.QLabel("Đô chính xác tối thiểu: ", wd)
        self.track_opt_min_conf_lb.setGeometry(QtCore.QRect(x+10, y+10, 110, 30))
        self.speedCal_dis_le = QtWidgets.QLineEdit(wd)
        self.speedCal_dis_le.setGeometry(QtCore.QRect(x+self.track_opt_min_conf_lb.width()+10, self.track_opt_min_conf_lb.y() , 60, 27))
        self.speedCal_dis_le.setValidator(QIntValidator())

        self.wd2_bt = QtWidgets.QPushButton(wd)
        self.wd2_bt.setGeometry(QtCore.QRect(x+50, y+20, 60, 30))


    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.demoTEXT.setText(label_time)

    def speedtext(self, wd):
        self.speedtext = QtWidgets.QLabel("00 Km/h", wd)
        self.speedtext.setGeometry(900, 300, 100, 40)

    def yolo_opt(self, wd):
        self.yolomodelname_lb = QtWidgets.QLabel("Yolo Model:", wd)
        self.yolomodelname_lb.setGeometry(10,50,100,30)
        self.yolomodelname_box = QtWidgets.QComboBox(wd)
        self.yolomodelname_box.setGeometry(70,50,100,30)
        list = ['PTGT Việt Nam', 'Pretrain']
        self.yolomodelname_box.addItems(list)

    def tracking_opt(self, wd):
        self.tracking_mt_lb = QtWidgets.QLabel("PT Tracking:", wd)
        self.tracking_mt_lb.setGeometry(180,50,100,30)
        self.tracking_mt_box = QtWidgets.QComboBox(wd)
        self.tracking_mt_box.setGeometry(245,50,100,30)
        list = ['SORT', 'DeepSORT']
        self.tracking_mt_box.addItems(list)

    def retranslateUi(self, wd):
        _translate = QtCore.QCoreApplication.translate
        wd.setWindowTitle(_translate("wd", "Hệ Thống Ước Lượng Tốc Độ Luồng Giao Thông"))
        
        # self.imgLabel_1.setText(_translate("wd", "CHUA CO VIDEO"))
        self.START.setText(_translate("wd", "Start"))
        self.PAUSE.setText(_translate("wd", "Pause"))
        self.RESUME.setText(_translate("wd", "Resume"))
        self.CLOSE.setText(_translate("wd", "Close"))
        self.GETFILE.setText(_translate("wd", "Chọn video"))
        self.sobt.setText(_translate("wd", "Add 2 lines"))


    def find(self):
        content = self.combo_box.currentText()
        print(content)

# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QWidget
# import sys
# class MainWindow(QWidget):
#     global app
#     global start
#     # class constructor
#     def __init__(self):
#         videopath = "E:/LuanVan/Videos/th.mp4"
#         super().__init__()
#         self.baseUI = UID() # load GUI
#         self.baseUI.setupUi(self)

# app = QApplication(sys.argv)
# mainWindow = MainWindow()
# mainWindow.show()
# sys.exit(app.exec_())