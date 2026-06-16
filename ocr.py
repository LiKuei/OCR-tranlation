def ocr(image, ocr_engine):
	text = ocr_engine(image)

	return "\n".join(text.txts)