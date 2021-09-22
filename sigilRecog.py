from tkinter import *
import PIL
from PIL import Image, ImageDraw
from numpy import asarray
import sys
import math

def points(x):
    p = math.exp(x/255) - 1.3
    #p = math.tan(x/math.pi - math.pi/2)
    return p

def test():
    dataCompare = asarray(imageCompare)
    info = dataCompare.shape
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    d = 0
    for i in range(info[0]):
        for j in range(info[1]):
            if (dataCompare[i][j][0] == 0):
                d += 1
                score1 += points(abs(255-meteorData[i][j][0]))
    for i in range(info[0]):
        for j in range(info[1]):
            if (dataCompare[i][j][0] == 0):
                score2 += points(abs(255-waterData[i][j][0]))
    for i in range(info[0]):
        for j in range(info[1]):
            if (dataCompare[i][j][0] == 0):
                score3 += points(abs(255-iceData[i][j][0]))
    for i in range(info[0]):
        for j in range(info[1]):
            if (dataCompare[i][j][0] == 0):
                score4 += points(abs(255-thunderData[i][j][0]))

    l = [(30.0, "No se"),(score1,"Meteor"),(score2,"water"),(score3,"ice"),(score4,"thunder")] 
    l.sort(key=lambda x:x[0], reverse=True)

    
    
    print("--->", l[0][1], l[0][0])

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




# load the image
meteor = PIL.Image.open('sigils/1.png')
water = PIL.Image.open('sigils/2.png')
ice = PIL.Image.open('sigils/3.png')
thunder = PIL.Image.open('sigils/4.png')


# convert image to numpy array
meteorData = asarray(meteor)
waterData = asarray(water)
iceData = asarray(ice)
thunderData = asarray(thunder)

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
