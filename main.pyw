from ast import Num
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
from lib2to3.refactor import get_fixers_from_package
import os
from PIL import Image 
import sys
import pyocr
import pyocr.builders
from googletrans import Translator

# ファイルの参照処理
def file_select():
    typ = [('画像ファイル','*')] 
    dir = os.getcwd()
    fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
    input_box.insert(tkinter.END, fle)
    
# 出力処理
def click_export_button():
    
 #OCR処理
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    
    tool = tools[0] 
    langs = tool.get_available_languages()  
    
    #英語:0  日本語:1
    lang_num = variable.get()
    if lang_num == 'jpn':
        lang_num = 1
    elif lang_num == 'eng':
        lang_num = 0
    else:
        print("OCR言語を選択してください。")
    lang_num = int(lang_num)
    #langs['eng','jpn','osd']
    lang = langs[lang_num]
    
    img = input_box.get()

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

        textBox.insert(END, txt)

root = tk.Tk() 

w = 600 # 横の長さ
h = 550 # 縦の長さ
x = 450 # 座標軸x
y = 250 # 座標軸y

# Frameの作成
frame = ttk.Frame(root, padding=10)
frame.pack()
frame.place(x=120,y=120)

# テキスト出力ボックスの作成
textboxname = StringVar()
textboxname.set('\n\n出力内容 ')
label = ttk.Label(frame, textvariable=textboxname)
label.grid(row=1, column=0)
textBox = Text(frame, width=50)
textBox.grid(row=2, column=0)

root.geometry('%dx%d+%d+%d' % (w,h, x, y))

# テキスト出力ボタンの作成
export_button = ttk.Button(frame, text='実行', command=click_export_button, width=10)
export_button.grid(row=0, column=0)



#言語選択プルダウンメニュー
lang_list= ('jpn', 'eng')
variable=StringVar()
combobox = ttk.Combobox(root, height=2,width=10, justify="center",state="readonly",values=lang_list,textvariable=variable)
combobox.pack()
combobox.place(x=480, y=40)

#ラベル
root = tkinter.Label(text='OCR言語')
root.place(x=415, y=40)

#入力欄の作成
input_box = tkinter.Entry(width=40)
input_box.place(x=200, y=100)

#ラベルの作成
input_label = tkinter.Label(text="変換するファイルを入力してください：")
input_label.place(x=20, y=100)

#ボタンの作成
button = tkinter.Button(text="参照",command=file_select)
button.place(x=445, y=97)

root.mainloop()