from PIL import ImageGrab, ImageTk, ImageEnhance
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font

class CanvasModel:
	stroke_size = 5

	def __init__(self, canvas, screenshot):
		self.inited = False
		self.rectangle_origin = (0, 0)
		self.full_screenshot = screenshot
		self.canvas = canvas
		self.in_resetting_period = False

		dim_screenshot = ImageEnhance.Brightness(screenshot).enhance(0.5)

		# https://stackoverflow.com/questions/26479728/tkinter-canvas-image-not-displaying
		canvas.background = tk_background = ImageTk.PhotoImage(dim_screenshot)
		canvas.create_image(0, 0, image=tk_background, anchor=NW)
		self.instruction = canvas.create_text(
			canvas.winfo_screenwidth() / 2, 
			canvas.winfo_screenheight() / 30, 
			text="按住滑鼠左鍵拖拉以框選欲翻譯之文字\n點擊滑鼠右鍵重新框選\n按下Esc退出", 
			anchor=N, 
			fill="white",
			font=Font(family="Microsoft JhengHei", size=20)
		)

		self.rectangle_screenshot = canvas.create_image(0, 0)
		self.rectangle = canvas.create_rectangle([-self.stroke_size] * 4, outline='white', width=self.stroke_size)

def get_minmax(a, b):
	if a < b:
		return (a, b)
	else:
		return (b, a)

def reset_region(canvas_model):
	canvas_model.canvas.delete(canvas_model.rectangle_screenshot)
	canvas_model.rectangle_screenshot = canvas_model.canvas.create_image(0, 0)
	canvas_model.canvas.coords(canvas_model.rectangle, [-canvas_model.stroke_size] * 4)
	canvas_model.in_resetting_period = True

def init_region(e, canvas_model):
	if not canvas_model.inited:
		canvas_model.canvas.delete(canvas_model.instruction)
		canvas_model.instruction = None
		canvas_model.inited = True
	
	canvas_model.rectangle_origin = (e.x, e.y)
	canvas_model.in_resetting_period = False
	canvas_model.canvas.tkraise(canvas_model.rectangle_screenshot)
	canvas_model.canvas.tkraise(canvas_model.rectangle)

def drawing_region(e, canvas_model):
	if canvas_model.in_resetting_period:
		return
	(x1, x2) = get_minmax(canvas_model.rectangle_origin[0], e.x)
	(y1, y2) = get_minmax(canvas_model.rectangle_origin[1], e.y)
	canvas_model.canvas.coords(
		canvas_model.rectangle, 
		x1 - canvas_model.stroke_size, 
		y1 - canvas_model.stroke_size, 
		x2 + canvas_model.stroke_size, 
		y2 + canvas_model.stroke_size
	)

	canvas_model.canvas.delete(canvas_model.rectangle_screenshot)
	cropped_screenshot = canvas_model.full_screenshot.crop((x1, y1, x2, y2))
	canvas_model.canvas.cropped_screenshot = tk_cropped_screenshot = ImageTk.PhotoImage(cropped_screenshot)
	canvas_model.rectangle_screenshot = canvas_model.canvas.create_image(x1, y1, image=tk_cropped_screenshot, anchor=NW)

def on_region_complete(e, window, canvas_model: CanvasModel):
	if canvas_model.in_resetting_period:
		return
	(x1, x2) = get_minmax(canvas_model.rectangle_origin[0], e.x)
	(y1, y2) = get_minmax(canvas_model.rectangle_origin[1], e.y)

	# 長寬須至少1px
	if x1 == x2 or y1 == y2:
		return
	
	cropped_screenshot = canvas_model.full_screenshot.crop((x1, y1, x2, y2))

	# TODO: Add translation here.
	cropped_screenshot.save("cropped.png")
	##
	window.master.deiconify()
	window.destroy()

def screenshot_window(root):
	root.iconify()
	window = Toplevel(root)
	window.attributes(fullscreen=True, topmost=True)
	window.focus_force()
	for sequence in ["<Escape>", "<Alt_L>", "<Alt_R>", "<Return>"]:
		window.bind(sequence, lambda _: window.destroy())

	canvas = Canvas(
		window, 
		width=root.winfo_screenwidth(), 
		height=root.winfo_screenheight(), 
		highlightthickness=0 # 移除Canvas的邊界
	)
	canvas.pack()

	screenshot = ImageGrab.grab()
	canvas_model = CanvasModel(canvas, screenshot)

	canvas.bind("<Button-1>", lambda e: init_region(e, canvas_model))
	canvas.bind("<ButtonRelease-3>", lambda _: reset_region(canvas_model))
	canvas.bind("<B1-Motion>", lambda e: drawing_region(e, canvas_model))
	canvas.bind("<ButtonRelease-1>", lambda e: on_region_complete(e, window, canvas_model))