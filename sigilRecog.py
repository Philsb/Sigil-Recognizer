from tkinter import *
import PIL
from PIL import Image, ImageDraw
from numpy import asarray
import sys
import math
import os

def points(x):
    p = math.exp(x/125) - 1.3
    #p = math.tan(x/math.pi - math.pi/2)
    return p

def test():
    scores = []
    for keys in imagesData:
        myScore = [keys,0]
        dataCompare = asarray(imageCompare)
        info = dataCompare.shape
        
        #Itera por los arrays de imagenes y compara pixeles
        imageData = imagesData[keys]
        for i in range(info[0]):
            for j in range(info[1]):
                #si pega con el pixel le sube puntos, de lo contrario le baja la cantidad que devuelve points()
                if(dataCompare[i][j][0] == 0):
                    myScore[1] += points(abs(255 - imageData[i][j][0]))
                elif(dataCompare[i][j][0] < 25):
                    myScore[1] -= points(abs(255 - imageData[i][j][0]))
                    
        scores.append(myScore)

    # ordena los scores
    scores.sort(key=lambda x:x[1], reverse=True)
    print("--->", scores[0][0], ": ",scores[0][1])

def save():
    global image_number
    filename = f'image_{image_number}.png'   # image_number increments by 1 at every save
    imageCompare.save(filename)
    image_number += 1


def clear():
    cv.delete("all")
    draw.rectangle((0, 0, 32, 32), fill=(255, 255, 255, 255))

def activate_paint(e):
    global lastx, lasty
    cv.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y


def paint(e):
    global lastx, lasty
    x, y = e.x, e.y
    cv.create_line((lastx, lasty, x, y), width=1)

    #  --- PIL
    draw.line((int(lastx/16), int(lasty/16), int(x/16), int(y/16)), fill='black', width=1)
    lastx, lasty = x, y


images = {}
imagesData = {}
#Inicia programa
for files in os.listdir("sigils"):
    filename = os.path.splitext(files)[0]
    #Carga imagenes
    images[filename] = PIL.Image.open("sigils/"+files)
    imagesData[filename] = asarray(images[filename])



root = Tk()
root.resizable(False, False)

lastx, lasty = None, None
image_number = 0

cv = Canvas(root, width=512, height=512, bg='white')

# --- PIL
imageCompare = Image.new('RGB', (32, 32), 'white')
draw = ImageDraw.Draw(imageCompare)

cv.bind('<1>', activate_paint)
cv.pack(expand=YES, fill=BOTH)

btn_clear = Button(text="clear", command=clear)
btn_clear.pack()

btn_test = Button(text="test", command=test)
btn_test.pack()

root.mainloop()
