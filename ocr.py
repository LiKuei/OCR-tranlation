import pytesseract

def ocr(image):
	text = pytesseract.image_to_string(image, lang="jpn+jpn_vert")
	print(text)

	return text