# On the back window shot
import win32gui, win32ui, win32con, winxpgui
from ctypes import windll
from PIL import Image
import cv2
import numpy

import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap, QImage
import sys

import threading

from time import sleep

ASADMIN = 'asadmin'

class MainWiondw(QWidget):
	def __init__(self):
		super().__init__()
		
		self.Running = True

		self.width = 640
		self.height = 360
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.resize(self.width, self.height)
		self.centralwidget = QWidget(self)
		self.centralwidget.setObjectName("centralwidget")

		self.label = QLabel(self.centralwidget)
		self.label.setGeometry(QRect(0, 0, self.width, self.height))
		self.label.setObjectName("label")
		self.label.setPixmap(QPixmap("im_opencv.png")) #image path

		self.Exit_button = QPushButton('Ｘ',self.centralwidget,)
		self.Exit_button.setGeometry(QRect(self.width-30,30,20,20))
		self.Exit_button.setStyleSheet("background-color : rgba(0, 0, 0, 50)") 
		self.Exit_button.setObjectName('Exit_button')
		self.Exit_button.clicked.connect(self.Exit_button_click)


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
		self.m_flag=False
		self.setCursor(QCursor(Qt.ArrowCursor))
		hWnd = win32gui.FindWindow(None,"MapleStory")
		win32gui.SetForegroundWindow(hWnd)
		
#=============================================================
# Exit Button click event
	def Exit_button_click(self,MainWindow):
		self.Running = False
		
		sys.exit(app.exec_())
		

#============================================================
	def run(self,MainWindow):
		# Get a handle to the background of the window, pay attention to the background window can not be minimized
		hWnd = win32gui.FindWindow(None,"MapleStory") # Window class name can get the SPY ++ using Visual Studio Tools
		
		win32gui.SetWindowLong (hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hWnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
		winxpgui.SetLayeredWindowAttributes(hWnd, 0, 0, win32con.LWA_ALPHA)
		
		while self.Running:
			# Get a handle to the window size information
			win32gui.MoveWindow(hWnd,0,0,self.width,self.height,0)

			left, top, right, bot = win32gui.GetWindowRect(hWnd)
			width = right - left
			height = bot - (top)
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
				saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
				# Will save the screenshot to the saveBitMap
				saveDC.SelectObject(saveBitMap)
				# Save the bitmap into the memory device context
				saveDC.BitBlt((0, 0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
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
				im_opencv.shape = (height, width, 4)

				self.rgbImage = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
				self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0], QImage.Format_RGB888)
				self.pixmap = QPixmap(self.convertToQtFormat)
				self.p = self.pixmap.scaled(640, 360, Qt.IgnoreAspectRatio)   

				self.label.setPixmap(self.p)
				self.label.update()

			except Exception as e:
				print(e)

		win32gui.SetWindowLong (hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hWnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
		winxpgui.SetLayeredWindowAttributes(hWnd, 0, 255, win32con.LWA_ALPHA)

	def video_thread(self,):
		thread=threading.Thread(target=self.run,args=(self,))
		thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
		thread.start()
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	w = MainWiondw()

	w.video_thread()
	w.show()
	
	sys.exit(app.exec_())