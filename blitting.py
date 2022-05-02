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
canvas.create_polygon(0, 0, 0, 100, 100, 100, 0, 100, 0, 0, fill = 'red', outline = 'red')
canvas.pack()

i = 0
x = 0
y = 0
img_width = image.size[0]/24
img_height = image.size[1]/12
number_of_frames = 6
image_sprite = None

cache = dict()

def run_animation(offset, key, pos):

    global i, canvas, image, cache, image_sprite
    i = i + 1
    i = i%number_of_frames
    print(i)
    print("does this ever gets executed")

    if not key in cache.keys():
        cache[key] = dict()

    if i in cache[key].keys():
        img = cache[key][i]
    else:
        dimensions = (      i*img_width + offset[0], 0          + offset[1],\
                    (i + 1)*img_width + offset[0]  , img_height + offset[1])
        cropped = image.crop(dimensions)
        img= ImageTk.PhotoImage(cropped)
        cache[key][i] = img

    
    if not image_sprite is None:
        #canvas.delete('all')
        canvas.delete(image_sprite)
    image_sprite = canvas.create_image(100 + pos[0], 100 + pos[1], image = img)

    root.update()
    time.sleep(1/12)

    

def move(evnt):
    global x, y

    if "Left" == evnt.keysym:
        x = x - img_width/4
        run_animation(offset = (0, img_height), key = evnt.keysym, pos = (x, y))
    elif "Right" == evnt.keysym:
        x = x + img_width/4
        run_animation(offset = (0,0), key = evnt.keysym, pos = (x, y))
    elif "Down" == evnt.keysym:
        y = y + img_height/4
        run_animation(offset = (3 * number_of_frames * img_width,img_height), key = evnt.keysym, pos = (x, y))
    elif "Up" == evnt.keysym:
        y = y - img_height/4
        run_animation(offset = (2 * number_of_frames * img_width,0), key = evnt.keysym, pos = (x, y))


canvas.bind_all('<Key>', move)


root.mainloop()

