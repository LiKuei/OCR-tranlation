import ctypes
from tkinter.font import Font
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter.ttk import *
from PIL import Image
from screenshot import screenshot_window

# (限Windows) 讓程式變得DPI Aware。解決不同螢幕解析度所造成
# 的文字模糊和Fraction Scaling帶來的錯誤螢幕解析度
#
# See https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows#display-scale-factor--dpi
# https://learn.microsoft.com/en-us/windows/win32/hidpi/setting-the-default-dpi-awareness-for-a-process
def fix_dpi_awareness_for_windows():
	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(2) # Per-monitor DPI aware
	except Exception:
		try:
			ctypes.windll.user32.SetProcessDPIAware() # For Windows 10以下
		except Exception:
			pass

def open_image(parent):
	f = askopenfilename(parent=parent, title="選擇圖片")
	if f == '':
		return None
	
	return Image.open(f)

def main_window():
	root = Tk()
	root.title("截圖翻譯器")
	root.resizable(False, False)
	font = Font(family="Microsoft JhengHei", size=10)
	Style().configure("TButton", font=font)
	frm = Frame(root, padding=10)
	frm.grid()
	Label(frm, text="開始翻譯你看到的文字！", font=font).grid(column=0, row=0)
	Button(frm, text="翻譯", command=lambda: screenshot_window(root)).grid(column=1, row=0)
	Button(frm, text="開啟圖片", command=lambda: open_image(root)).grid(column=1, row=1)
		
	root.mainloop()

fix_dpi_awareness_for_windows()
main_window()