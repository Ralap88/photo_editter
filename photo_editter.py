#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter.constants import CENTER
from tkinter.messagebox import *
import tkinter as tk
from tkinter import filedialog				#file chooser
import tkinter.colorchooser as cc 			#color chooser
from PIL import Image,ImageDraw,ImageFont               #photo

''' initialize window'''
window = tk.Tk()
window.title('rotate photo')
window.geometry('650x500')
window.resizable(False, False)


def loadFile():    
    if loadFile_en.get() is None:
        file_path = filedialog.askopenfilename(filetypes = (("png files", "*.png"), ("all files", "*.*")))	#open file, filetypes: 顯示指定的副檔名
        loadFile_en.insert(0, file_path)	                                                                #丟到旁邊的Entry中    
    else:
        file_path = filedialog.askopenfilename(filetypes = (("png files", "*.png"), ("all files", "*.*")))
        loadFile_en.delete(0, 'end')		                                                                    #若再次選擇檔案的話，要將舊檔案路徑的文字清除
        loadFile_en.insert(0, file_path)

def checkbutton_state():    
    ''' 黑白和二值化 '''    
    if black_white_checkbox.get() == 1:
        binarization_checkbutton1.config(state = 'disabled')
    elif black_white_checkbox.get() == 0:
        binarization_checkbutton1.config(state = 'normal')
    if binarization_checkbutton.get() == 1:
        black_white_checkbox1.config(state = 'disabled')
    elif binarization_checkbutton.get() == 0:
        black_white_checkbox1.config(state = 'normal')


def output():
    fileRoute = loadFile_en.get()
    imgOpen = Image.open(fileRoute)
    name = fileRoute.split('/')

    ''' 旋轉 '''
    if radioVar.get() == 0:
        new_imgOpen = imgOpen.rotate(0)
    if radioVar.get() == 1:
        new_imgOpen = imgOpen.rotate(90)
        new_imgOpenResult = new_imgOpen
    if radioVar.get() == 2:
        new_imgOpen = imgOpen.rotate(270)
        new_imgOpenResult = new_imgOpen
    if radioVar.get() == 3:
        new_imgOpen = imgOpen.rotate(180)
        new_imgOpenResult = new_imgOpen

    ''' 如果沒有旋轉，要將變數名變成new_imgOpenResult方便接下來做特殊效果'''
    if binarization_checkbutton.get()==1:
        new_imgOpenResult = new_imgOpen
        new_imgOpenResult = new_imgOpenResult.convert('1')    
    if black_white_checkbox.get()==1:
        new_imgOpenResult = new_imgOpen
        new_imgOpenResult = new_imgOpenResult.convert('L')

    ''' 上述作完就想輸出的話，就可以從這邊先存檔，檔名預設是"new_"加上剛剛用split切好的路徑的倒數第一個值(檔名) '''
    if black_white_checkbox.get()==1 or binarization_checkbutton.get()==1 or radioVar.get() != 0:
        new_imgOpenResult.save(f"new_{name[-1]}")

    ''' 先判斷是否有輸入文字，有再進入 '''
    if inputWords.get() is not None:
        w ,h = imgOpen.width, imgOpen.height
        word = inputWords.get()
        image_table = Image.new(mode = 'RGBA', size = (w,h))
        draw_table = ImageDraw.Draw(im = image_table)
        font = ImageFont.truetype('kaiu.ttf', 20)
        image_table.save("text.png")
        text = word
        color = colorPrint['bg']													#讀取顯示顏色的Label的背景參數
        draw_table.text((0, 0), text, font = font, align = "left", fill = color)	# 文字的位置固定在左上角
        image_table.save("text.png")

		# 判斷說前面有沒有做剛剛的轉向或特殊效果，有就開啟剛剛存檔的照片，沒有就開啟原圖片
        if binarization_checkbutton.get() == 1 or black_white_checkbox.get() == 1 or radioVar.get() != 0:
           imageA = Image.open(f"new_{name[-1]}")
        if radioVar.get() == 0 and binarization_checkbutton.get() == 0 and black_white_checkbox.get()==0:
           imageA = imgOpen

        imageA = imageA.convert('RGBA')
        widthA, heightA = imageA.size
        imageB = Image.open('text.png')
        imageB = imageB.convert('RGBA')
        newWidthB = int(widthA)
        newHeightB = int(heightA)
        imageB_resize = imageB.resize((newWidthB, newHeightB))
        resultPicture = Image.new('RGBA', imageA.size, (0, 0, 0, 0))
        resultPicture.paste(imageA,(0,0))
        right_bottom = (0,0)
        resultPicture.paste(imageB_resize, right_bottom, imageB_resize)
        resultPicture.save(f"new_{name[-1]}")

    name = ''																# 將name清空
    tk.messagebox.showinfo("message", "finish!") 							# 寫一個彈出視窗告訴使用者已經處理完了，並且將這個函式附加到output_btn(輸出)按鈕上

def colorChoice():
    color=cc.askcolor()
    color = color[1]
    print(str(color))
    colorPrint.config(bg=color)


''' label'''
label1 = tk.Label(text = "Chooses the phtot to rotate", bg = "grey", fg = "white", height = 1)
label1.place(x = 0, y = 0)

label2 = tk.Label(text = "Special effect", fg = "blue", height = 1)
label2.place(x = 0, y = 50)

label3 = tk.Label(text = "Add words", fg = "red", height = 1)
label3.place(x = 0, y = 120)

colorPrint = tk.Label(height = 1, width = 2)		#color Choicer setting
colorPrint.place(x=130 ,y=143)

''' Entry '''
loadFile_en = tk.Entry(width = 40)
loadFile_en.place(x = 161, y = 0)

inputWords = tk.Entry(width = 40)
inputWords.place(x = 70, y = 120)

''' RadioButton '''
radioVar = tk.IntVar()
radio1 = tk.Radiobutton(text = "Rotate clockwise 90 degree", variable = radioVar, value = 1)
radio2 = tk.Radiobutton(text = "Rotate counter-clockwise 90 degree", variable = radioVar, value = 2)
radio3 = tk.Radiobutton(text = "Rotate 180 degree", variable = radioVar, value = 3)
radio1.place(x = 0, y = 25)
radio2.place(x = 190, y = 25)
radio3.place(x = 420, y = 25)

''' Checkbutton '''
black_white_checkbox = tk.IntVar()
black_white_checkbox1 = tk.Checkbutton(text = "Black and white", variable = black_white_checkbox, command = checkbutton_state)
black_white_checkbox1.place(x = 40, y = 80)
binarization_checkbutton = tk.IntVar()
binarization_checkbutton1 = tk.Checkbutton(text = "Binarization", variable = binarization_checkbutton, command = checkbutton_state)
binarization_checkbutton1.place(x = 240, y = 80)

''' Button '''
loadFile_btn = tk.Button(text = "...", height = 1, command = loadFile) 	    #press button to run loadFile
loadFile_btn.place(x = 445, y = 0)
choiceColor_btn = tk.Button(text = "Choose Color", command = colorChoice) 	#press button to choice color
choiceColor_btn.place(x = 70, y =  140)
output_btn = tk.Button(text = "Output", height = 1, command = output)
output_btn.place(anchor = CENTER, x = 250, y = 250)

window.mainloop()



