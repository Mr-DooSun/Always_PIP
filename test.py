import win32gui
import win32con
import winxpgui
import win32api
import subprocess
import time

from time import sleep

subprocess.Popen("notepad.exe", shell=True)
time.sleep(1)
hwnd = win32gui.FindWindow(None, "제목 없음 - Windows 메모장")  ## The caption of my empty notepad (MetaPad)

win32gui.SetWindowLong (hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hwnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
winxpgui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA)

sleep(3)
