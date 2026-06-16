import ctypes
from tkinter.font import Font
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter.ttk import *
from PIL import Image
from screenshot import screenshot_window
from rapidocr import *
from common import ocr_translate
import easyocr

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
			ctypes.windll.user32.SetProcessDPIAware() # For Windows 8以下
		except Exception:
			pass

def translate_image(parent, ocr_engine):
	f = askopenfilename(parent=parent, title="選擇圖片")
	if f == "":
		return None
	
	ocr_translate(parent, f, ocr_engine)

def main_window():
	root = Tk()
	root.title("截圖翻譯器")
	root.resizable(False, False)
	font = Font(family="Microsoft JhengHei", size=10)
	style = Style()
	style.configure("TButton", font=font)
	style.configure("TLabelframe.Label", font=font)

	ocr_engine = easyocr.Reader(["ja", "en"], gpu=False)
	
	frm = Frame(root, padding=10)
	frm.grid(row=0, column=0, sticky="w")
	Button(frm, text="翻譯", command=lambda: screenshot_window(root, ocr_engine)).grid(row=0, column=0, padx=2)
	Button(frm, text="開啟圖片", command=lambda: translate_image(root, ocr_engine)).grid(row=0, column=1, padx=2)
	
	frm_result = LabelFrame(root, text="翻譯結果", padding=5)
	frm_result.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
	
	root.result_box = result_box = Text(frm_result, width=45, height=6, font=font)
	result_box.insert(END, "等待翻譯結果...")
	result_box.config(state=DISABLED)
	result_box.grid(row=0, column=0, sticky="nsew")
	
	scrollbar = Scrollbar(frm_result, command=result_box.yview)
	scrollbar.grid(row=0, column=1, sticky="ns")
	result_box.config(yscrollcommand=scrollbar.set)
		
	root.mainloop()

if __name__ == "__main__":
	fix_dpi_awareness_for_windows()
	main_window()