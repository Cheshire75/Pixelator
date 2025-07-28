import tkinter as tk
from PIL import Image, ImageTk
import pixelator as px
import os

def OnButtonClick():
    px.BatchPixelate(fileDirList=filePathList)

root = tk.Tk()

filePathList = px.open_images()

originImageDisplay=False
originalImage = tk.Label(root)
if filePathList[0]:
    imgPil = Image.open(filePathList[0])
    img = ImageTk.PhotoImage(imgPil)
    
    originalImage.config(image=img)
    originImageDisplay=True
originalImage.pack(side='left')

frame = tk.Frame()
frame.pack(side = 'left')
paletteDisplay=False
palettePath = 'palette.png'
if os.path.exists(palettePath):
    palettePil = Image.open(palettePath)
    width = 200
    height = width/16*palettePil.size[1]
    palettePil=palettePil.resize((width, int(height)))

    paletteImage = ImageTk.PhotoImage(palettePil)
    paletteLabel = tk.Label(frame)
    paletteLabel.config(image=paletteImage)
    paletteLabel.pack()
    paletteDisplay=True

pixelDisplay = False
if paletteDisplay&originImageDisplay:
    pixelImagePil = px.pixelate_image(filePathList[0],palettePath,64)
    pixelImagePil = pixelImagePil.resize((320,320),resample=Image.NEAREST)
    pixelImage = ImageTk.PhotoImage(pixelImagePil)

    pixelLabel = tk.Label(root,image=pixelImage)
    pixelLabel.pack(side='left')
    pixelDisplay=True

if pixelDisplay:
    button = tk.Button(frame, text='pixelate', command=OnButtonClick)
    button.pack()

root.mainloop()

