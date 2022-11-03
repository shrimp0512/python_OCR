#!/usr/bin/env python
# coding: utf-8

# In[1]:
from PIL import Image 
import sys
import pyocr
import pyocr.builders
from googletrans import Translator

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0] 
langs = tool.get_available_languages()
#英語:0  日本語:1
lang_num = input('読み込むファイルの言語を入力してください。　英語:0 日本語:1')
lang_num = int(lang_num)
#langs['eng','jpn','osd']
lang = langs[lang_num]


# In[2]:
img = input('ファイルのパスを入力してください。')

txt = tool.image_to_string(
    Image.open(img),
    lang=lang,
    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
)


#英語翻訳(日本語→英語)
if lang_num == 1:
    txt = txt.replace(' ', '') #文字抽出時の半角スペースを消す
    tr = Translator()
    txt = tr.translate(txt,src="ja",dest="en").text
#日本語翻訳(英語→日本語)
elif lang_num == 0:
    tr = Translator()
    txt = tr.translate(txt,src="en",dest="ja").text

print(txt)
