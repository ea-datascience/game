# Read and Display Image

from tkinter import Canvas, Tk, NW
import tkinter
from PIL import Image, ImageTk
import time

image = Image.open("images/spaghetti_atlas.png")
#image.show()
print(image.format)
print(image.size)
print(image.mode)
print("Image width: {0}".format(image.size[0]/24))
print("Image height: {0}".format(image.size[1]/12))

root = Tk()
root.geometry("550x300+300+150")
root.resizable(width = True, height = True)

canvas = Canvas(master = root, width=550, height=300)
canvas.pack()

i = 0
img_width = image.size[0]/24
img_height = image.size[1]/12
number_of_frames = 6

def run_animation(offset):
    

    global i, canvas, image
    i = i + 1
    i = i%number_of_frames
    print(i)
    print("does this ever gets executed")
    dimensions = ( i*img_width + offset[0], 0 + offset[1],\
                  (i + 1)*img_width + offset[0], img_height + offset[1])
    cropped = image.crop(dimensions)
    img= ImageTk.PhotoImage(cropped)

    canvas.delete('all')
    image_sprite = canvas.create_image(100, 100, image = img)

    root.update()
    time.sleep(1/12)

    

def move(evnt):
    if "Left" == evnt.keysym:
        run_animation(offset = (0, img_height))
    elif "Right" == evnt.keysym:
        run_animation(offset = (0,0))
    elif "Down" == evnt.keysym:
        run_animation(offset = (3 * number_of_frames * img_width,img_height))
    elif "Up" == evnt.keysym:
        run_animation(offset = (2 * number_of_frames * img_width,0))


canvas.bind_all('<Key>', move)

root.mainloop()


"""
#Import the required Libraries
from tkinter import Tk, Canvas, NW
from PIL import Image,ImageTk

#Create an instance of tkinter frame
win = Tk()

#Set the geometry of tkinter frame
win.geometry("750x270")

#Create a canvas
canvas= Canvas(win, width= 600, height= 400)
canvas.pack()

#Load an image in the script
img= ImageTk.PhotoImage(Image.open("images/spaghetti_atlas.png"))

#Add image to the Canvas Items
canvas.create_image(10,10,anchor=NW,image=img)

win.mainloop()
"""