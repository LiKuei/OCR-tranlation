import pytesseract

def ocr(image):
	text = pytesseract.image_to_string(image, lang="eng+jpn+jpn_vert")
	print(text)

	return text