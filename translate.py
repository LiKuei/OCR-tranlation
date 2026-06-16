from deep_translator import GoogleTranslator

def translate(text):
	if not text or not text.strip():
		return ""
	try:
		return GoogleTranslator(source='auto', target='zh-TW').translate(text)
	except Exception as e:
		return f"翻譯出錯: {e}"