# On the back window shot
import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2
import numpy

hWnd = win32gui.FindWindow(None,"MapleStory") # Window class name can get the SPY ++ using Visual Studio Tools

while True:
    # Get a handle to the window size information
    win32gui.MoveWindow(hWnd,1250,600,640,360,0)
    
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
        im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)
        
        cv2.imshow("im_opencv",im_opencv) #display
    
    except Exception as e:
        print(e)

    if cv2.waitKey(1) & 0xFF == ord('q'):
    	cv2.destroyAllWindows()
    	break