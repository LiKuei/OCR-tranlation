from tkinter import *
from ocr import ocr
from translate import translate

def ocr_translate(root, image, ocr_engine):
	text = ocr(image, ocr_engine)
	translated_text = translate(text)
	root.result_box.config(state=NORMAL)
	root.result_box.delete("1.0", END)
	root.result_box.insert(END, translated_text)
	root.result_box.config(state=DISABLED)