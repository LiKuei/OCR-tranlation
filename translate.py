import asyncio
import sys
from googletrans import Translator

def translate(text):
	translator = Translator()
	result = asyncio.run(translator.translate(text, dest='zh-tw'))
	print(result.text)
	
	# 更新 GUI
	main_module = sys.modules.get('main') or sys.modules.get('__main__')
	if main_module and hasattr(main_module, 'update_display'):
		try:
			main_module.update_display(result.text)
		except Exception:
			pass
			
	return result.text