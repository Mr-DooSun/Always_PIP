# On the back window shot
import win32gui, win32ui, win32con, winxpgui
from ctypes import windll

from PIL import Image # HPND

import cv2 # MIT
import numpy # BSD

import os

# GPL v3
from PyQt5.QtWidgets import QMenuBar, QApplication, QWidget, QLabel, QPushButton, QMainWindow, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt,QRect,QMetaObject,QCoreApplication
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap, QImage, QFont, QFontDatabase, QIcon

import sys
import threading
from time import sleep

Choose_Window = ""
width = None
height = None
Start_pip = True

class Main_MainWindow(QWidget):
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle("PIP")
        QApplication.setWindowIcon(QIcon('pip.ico'))
        MainWindow.setFixedSize(200, 320)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        # 배달의 민족 연성체
        self.new_font = QFontDatabase()
        self.new_font.addApplicationFont('BMYEONSUNG.ttf')

        #Title_Label
        self.Title_label = QLabel(self.centralwidget)
        self.Title_label.setGeometry(QRect(40, 15, 150, 40))
        self.Title_label.setObjectName("Title_label")
        self.Title_label.setText('Always PIP')
        self.Title_label.setFont(QFont('배달의민족 연성',20))

        # 프로세스 확인 라벨
        self.Process_check_label = QLabel(self.centralwidget)
        self.Process_check_label.setGeometry(QRect(25,75, 100,20))
        self.Process_check_label.setObjectName('Process_check_label')
        self.Process_check_label.setText('Choose Process')
        self.Process_check_label.setFont(QFont('배달의민족 연성',12))

        # Qombo box 프로세스 확인
        output = self.getWindowList()
        process_list = []
        for window_name,pid in output :
            process_list.append(window_name)
        self.qb = QComboBox(self.centralwidget)
        self.qb.addItems(process_list)  # 다수 아이템 추가시
        self.qb.setGeometry(QRect(25, 100, 150, 25))

        # Width 라벨
        self.Width_label = QLabel(self.centralwidget)
        self.Width_label.setGeometry(QRect(25,145, 100,20))
        self.Width_label.setObjectName('Width_label')
        self.Width_label.setText('Width')
        self.Width_label.setFont(QFont('배달의민족 연성',12))

        # Width 입력칸
        self.Width_text_edit = QLineEdit(self.centralwidget)
        self.Width_text_edit.setGeometry(QRect(25, 170, 50, 25))
        self.Width_text_edit.setObjectName("Width_text_edit")
        self.Width_text_edit.setText("640")

        # X 라벨
        self.X_label = QLabel(self.centralwidget)
        self.X_label.setGeometry(QRect(95,175, 100,20))
        self.X_label.setObjectName('X_label')
        self.X_label.setText('X')
        self.X_label.setFont(QFont('배달의민족 연성',12))

        # Height 라벨
        self.Height_label = QLabel(self.centralwidget)
        self.Height_label.setGeometry(QRect(125,145, 100,20))
        self.Height_label.setObjectName('Height_label')
        self.Height_label.setText('Height')
        self.Height_label.setFont(QFont('배달의민족 연성',12))

        # Height 입력 칸
        self.Height_text_edit = QLineEdit(self.centralwidget)
        self.Height_text_edit.setGeometry(QRect(125, 170, 50, 25))
        self.Height_text_edit.setObjectName("Height_text_edit")
        self.Height_text_edit.setText("360")

        # 안내 라벨
        self.comment_label = QLabel(self.centralwidget)
        self.comment_label.setGeometry(QRect(35,190, 150,40))
        self.comment_label.setObjectName('comment_label')
        self.comment_label.setText('값을 조정 할 수 있습니다')
        self.comment_label.setFont(QFont('배달의민족 연성',12))

        # 도움말
        self.Help_button = QPushButton(self.centralwidget)
        self.Help_button.setGeometry(QRect(90, 230, 20, 20))
        self.Help_button.setObjectName("Help_button")
        self.Help_button.setText('?')
        self.Help_button.clicked.connect(self.Help_notice)

        # Start_button
        self.Start_button = QPushButton(self.centralwidget)
        self.Start_button.setGeometry(QRect(30, 265, 75, 30))
        self.Start_button.setObjectName("Start_button")
        self.Start_button.setText('START')
        self.Start_button.setFont(QFont('배달의민족 연성',12))
        self.Start_button.clicked.connect(self.start_click)

        # 후원 버튼
        self.Sponsor_button = QPushButton(self.centralwidget)
        self.Sponsor_button.setGeometry(QRect(120, 265, 50, 30))
        self.Sponsor_button.setObjectName("Sponsor_button")
        self.Sponsor_button.setText('후원')
        self.Sponsor_button.setFont(QFont('배달의민족 연성',12))
        self.Sponsor_button.clicked.connect(self.Sponsor_notice)

        # 출처
        self.comment_label = QLabel(self.centralwidget)
        self.comment_label.setGeometry(QRect(25,300, 150,20))
        self.comment_label.setObjectName('comment_label')
        self.comment_label.setText('mr-doosun.tistory.com')
        self.comment_label.setFont(QFont('배달의민족 연성',12))

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def getWindowList(self):
        def callback(hwnd, hwnd_list: list):
            title = win32gui.GetWindowText(hwnd)

            if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
                hwnd_list.append((title, hwnd))
            return True

        output = []
        win32gui.EnumWindows(callback, output)
        
        return output

    def start_click(self,MainWindow):
        global Start_pip

        if Start_pip :
            Start_pip = False
            global Choose_Window, width, height
            Choose_Window = self.qb.currentText()
            width = int(self.Width_text_edit.text())
            height = int(self.Height_text_edit.text())

            Sub_Window()
    
    def Help_notice(self,Main_MainWindow):
        os.system('explorer http://mr-doosun.tistory.com')

    def Sponsor_notice(self,Main_MainWindow):
        QMessageBox.about(self,'후원','(기업) 579-036026-01-013 [ㅇㄷㅎ]')

# ==========================================================================
# ==========================================================================
# ==========================================================================

class Sub_Window(QWidget):
    def __init__(self):
        super().__init__()
        global width,height
        
        self.Running = True

        self.width = width
        self.height = height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(self.width, self.height)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.Picture = QLabel(self.centralwidget)
        self.Picture.setGeometry(QRect(0, 0, self.width, self.height))
        self.Picture.setObjectName("Picture")
        self.Picture.setPixmap(QPixmap("im_opencv.png")) #image path

        self.Exit_button = QPushButton('Ｘ',self.centralwidget,)
        self.Exit_button.setGeometry(QRect(self.width-30,10,20,20))
        self.Exit_button.setStyleSheet("background-color : rgba(255, 255, 255, 200)") 
        self.Exit_button.setObjectName('Exit_button')
        self.Exit_button.clicked.connect(self.Exit_button_click)

        self.video_thread()
        self.show()

#========================================================
# MOUSE Click drag EVENT function
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #Change mouse icon

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)#Change window position
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global Choose_Window

        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
        hWnd = win32gui.FindWindow(None,Choose_Window)
        win32gui.SetForegroundWindow(hWnd)

#=============================================================
# Exit Button click event
    def Exit_button_click(self,MainWindow):
        global Start_pip
        Start_pip = True
        self.Running = False

        self.close()
#============================================================
    def run(self,MainWindow):
        global Choose_Window
        # Get a handle to the background of the window, pay attention to the background window can not be minimized
        hWnd = win32gui.FindWindow(None,Choose_Window) # Window class name can get the SPY ++ using Visual Studio Tools
        
        win32gui.SetWindowLong (hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hWnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
        winxpgui.SetLayeredWindowAttributes(hWnd, 0, 0, win32con.LWA_ALPHA)
        
        while self.Running:
            # Get a handle to the window size information
            win32gui.MoveWindow(hWnd,0,0,self.width,self.height,0)

            left, top, right, bot = win32gui.GetWindowRect(hWnd)
            self.width = right - left
            self.height = bot - (top)
            # Returns the device context handle of the window, covering the entire window, including non-client area, title bars, menus, borders
            hWndDC = win32gui.GetWindowDC(hWnd)
            # Create a device context
            mfcDC = win32ui.CreateDCFromHandle(hWndDC)
            # Create a memory device context
            saveDC = mfcDC.CreateCompatibleDC()
            # Create a bitmap object ready to save the picture
            saveBitMap = win32ui.CreateBitmap()

            try :
                # For the bitmap open space
                saveBitMap.CreateCompatibleBitmap(mfcDC,self.width,self.height)
                # Will save the screenshot to the saveBitMap
                saveDC.SelectObject(saveBitMap)
                # Save the bitmap into the memory device context
                saveDC.BitBlt((0, 0), (self.width,self.height), mfcDC, (0, 0), win32con.SRCCOPY)
                ## three methods (first part): opencv
                ### get the bitmap information
                signedIntsArray = saveBitMap.GetBitmapBits(True)
                ## The method of tris (subsequent revolutions of the second part)

                # Memory release
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hWnd,hWndDC)

                ## The method of tris (Part II)qq: opencv
                ### PrintWindow success, saved to a file, to the screen
                im_opencv = numpy.frombuffer(signedIntsArray, dtype = 'uint8')
                im_opencv.shape = (self.height, self.width, 4)

                self.rgbImage = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0], QImage.Format_RGB888)
                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaled(640, 360, Qt.IgnoreAspectRatio)   

                self.Picture.setPixmap(self.p)
                self.Picture.update()

            except Exception as e:
                print(e)

        win32gui.SetWindowLong(hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hWnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
        winxpgui.SetLayeredWindowAttributes(hWnd, 0, 255, win32con.LWA_ALPHA)

    def video_thread(self,):
        thread=threading.Thread(target=self.run,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    ui = Main_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())