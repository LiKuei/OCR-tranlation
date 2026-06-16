import asyncio
import sys
from googletrans import Translator

def translate(text):
	translator = Translator()
	result = asyncio.run(translator.translate(text, dest='zh-tw'))
			
	return result.text