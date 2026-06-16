def ocr(image_filepath, ocr_engine):
	text = ocr_engine.readtext(image_filepath, detail = 0)
	all_text = " ".join(text if text else ["無結果"])
	print(f"\"{all_text}\"")

	return all_text