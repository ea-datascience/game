# This follows the instructions in this tutorial
# - https://www.pythontutorial.net/tkinter/tkinter-window/
# - https://zetcode.com/tkinter/drawing/


from cmath import sqrt
#from functools import cache
#from ftplib import parse150
import tkinter as tk
from PIL import Image, ImageTk
import time
#from turtle import color


def convert2DTo3D(position_2d):
    pass

def convert3Dto2D(position_3d):
    sqrt_2 = sqrt(2)

    x, y, z = position_3d
    x_ =     x/sqrt_2 +    y/sqrt_2
    y_ = -.5*x/sqrt_2 + .5*y/sqrt_2 - .5*z

    return x_.real, y_.real

def viewport_transform(p):
    window_width = 800
    window_height = 600

    x_ =  p[0]  + window_width/2
    y_ =  p[1]  + window_height/2
    
    return x_, y_

def transform(position_3d):
    p = convert3Dto2D(position_3d)
    p = viewport_transform(p)

    return p


def move_transform(position_3d):
    p = convert3Dto2D(position_3d)

    return p



    return p[0], p[1]

class Hero(object):
    def __init__(self, container = None, **kwargs):
        super().__init__()
        self.container = container 

        self.x = kwargs['x']
        self.y = kwargs['y']

        self.image = Image.open("images/spaghetti_atlas.png")
        self.frame_counter = 0
        self.img_width = self.image.size[0]/24
        self.img_height = self.image.size[1]/12
        self.number_of_frames = 6
        self.cache = {
            "Idle":dict(),
            "Up": dict(),
            "Down": dict(),
            "Left": dict(),
            "Right": dict()
        }
        self.image_sprite = None

    def initialize(self):
        coord = transform((self.x,self.y,0))
        dimensions = (self.frame_counter * self.img_width, 0,\
                (self.frame_counter + 1) * self.img_width, self.img_height)
        cropped = self.image.crop(dimensions)           
        img = ImageTk.PhotoImage(cropped)
        self.cache["Idle"][0] = img
        self.image_sprite = self.container.create_image(coord[0], coord[1], image = img)
        self.container.update()


    def animate(self, offset, key, pos):
        self.frame_counter = self.frame_counter + 1
        self.frame_counter = self.frame_counter % self.number_of_frames

        if self.frame_counter in self.cache[key].keys():
            img = self.cache[key][self.frame_counter]
        else:
            dimensions = (      self.frame_counter * self.img_width + offset[0], 0               + offset[1],\
                          (self.frame_counter + 1) * self.img_width + offset[0], self.img_height + offset[1]) 
            cropped = self.image.crop(dimensions)           
            img = ImageTk.PhotoImage(cropped)
            self.cache[key][self.frame_counter] = img

        if not self.image_sprite is None:
            self.container.delete(self.image_sprite)

        self.image_sprite = self.container.create_image(pos[0], pos[1], image = img)
        print(r"{0}, {1}".format(pos[0], pos[1]))        

        self.container.update()
        time.sleep(1/12)

    def move(self, evnt):
        print(r"{0} - {1}".format(evnt.keysym, evnt.keycode))        
        step = 10
        
        if "Left" == evnt.keysym:
            self.x = self.x
            self.y = self.y - step
            coord = transform((self.x,self.y,0))
            self.animate(offset = (3 * self.number_of_frames * self.img_width, 0 * self.img_height), key = evnt.keysym, pos = coord)
        elif "Right" == evnt.keysym:
            self.x = self.x
            self.y = self.y + step            
            coord = transform((self.x,self.y,0))
            self.animate(offset = (2 * self.number_of_frames * self.img_width, 1 * self.img_height), key = evnt.keysym, pos = coord)
        elif "Down" == evnt.keysym:
            self.x = self.x - step
            self.y = self.y            
            coord = transform((self.x,self.y,0))
            self.animate(offset = (1 * self.number_of_frames * self.img_width, 1 * self.img_height), key = evnt.keysym, pos = coord)
        elif "Up" == evnt.keysym:
            self.x = self.x + step
            self.y = self.y           
            coord = transform((self.x, self.y,0))
            self.animate(offset = (1 * self.number_of_frames * self.img_width, 0 * self.img_height), key = evnt.keysym, pos = coord)


        

    

class Sprite(object):
    def __init__(self, container = None, **kwargs):
        super().__init__()
        self.container = container

        self.x = kwargs['x']
        self.y = kwargs['y']

        self.parts = list()

    def draw(self):
        coords = None

        # Building the contour of the bounding box
        p0 = transform((0, 0, 0))
        p1 = transform((0, 50, 0))
        coords = p0 + p1

        p0= p1
        p1 = transform((50, 50, 0))
        coords += p0 + p1        

        p0= p1
        p1 = transform((50, 50, 100))
        coords += p0 + p1        

        p0= p1
        p1 = transform((50, 0, 100))
        coords += p0 + p1        

        p0= p1
        p1 = transform((0, 0, 100))
        coords += p0 + p1        

        self.parts.append(self.container.create_polygon(list(coords), fill = '#ffaaaa', outline = '#ff0000'))

        # Building the facing edge of the bounding box
        p0= p1
        p1 = transform((0, 50, 100))
        coords += p0 + p1        
        self.parts.append(self.container.create_line(p0[0], p0[1], p1[0], p1[1], fill = 'red'))

        p0= p1
        p1 = transform((50, 50, 100))
        coords += p0 + p1        
        self.parts.append(self.container.create_line(p0[0], p0[1], p1[0], p1[1], fill = 'red')) 

        p0= transform((0, 50, 100))
        p1 = transform((0, 50, 0))
        coords += p0 + p1        
        self.parts.append(self.container.create_line(p0[0], p0[1], p1[0], p1[1], fill = 'red')) 

        self.container.pack(fill = tk.BOTH, expand = 1)
        #pass

    def move(self, evnt):
        print(r"{0} - {1}".format(evnt.keysym, evnt.keycode))        
        step = 10
        for p in self.parts:
            if "Left" == evnt.keysym:
                coord = move_transform((0,-step,0))
                self.container.move(p, coord[0], coord[1])
            elif "Right" == evnt.keysym:
                coord = move_transform((0,step,0))
                self.container.move(p, coord[0], coord[1])
            elif "Down" == evnt.keysym:
                coord = move_transform((-step,0,0))
                self.container.move(p, coord[0], coord[1])
            elif "Up" == evnt.keysym:
                coord = move_transform((step,0,0))
                self.container.move(p, coord[0], coord[1])

        



class Tile(object):
    
    def __init__(self, container = None, **kwargs):
        super().__init__()
        self.container = container
        self.side_length = 50

        self.col = kwargs["col"]
        self.row = kwargs["row"]

        


    def draw(self):
        coords = None

        p0 = transform((self.col * self.side_length, self.row * self.side_length, 0))
        p1 = transform((self.col * self.side_length, self.row * self.side_length + self.side_length, 0))
        coords = p0 + p1
        
        p0 = p1
        p1 = transform((self.col * self.side_length + self.side_length, self.row * self.side_length + self.side_length, 0))
        coords += p0 + p1

        
        p0 = p1
        p1 = transform((self.col * self.side_length + self.side_length, self.row * self.side_length, 0))
        coords += p0 + p1


        p0 = p1
        p1 = transform((self.col * self.side_length, self.row * self.side_length, 0))
        coords += p0 + p1

        self.container.create_polygon(list(coords), outline='#cccccc', fill='#dddddd', width = 1)

def texturize(self):
    pass






class Map(tk.Canvas):

    def __init__(self, master = None):
        super().__init__(master = master)

        self.initUI()

        self.image = Image.open("images/isometric_pixel_0056.png")
        self.tiles = list()

        self.number_of_columns = 20
        self.number_of_rows = 20

        self.tiles = list()        

    def initUI(self):

        #self.pack(fill = tk.BOTH, expand = 1)

        # Drawing the tiles on the map
        # ------------------------------------------------------------

        
        for col in range(-5, 5):
            for row in range(-5, 5):
                tile = Tile(self, col = col, row = row)
                tile.draw()
                #tile.texturize(texture = self.image)

    def draw(self):
        min_range_col = -int(self.number_of_columns/2)
        max_range_col = int(self.number_of_columns/2)

        min_range_row = -int(self.number_of_rows/2)
        max_range_row = int(self.number_of_rows/2)

        for col in range(max_range_col, min_range_col, -1):
            for row in range(min_range_row,max_range_row,1):
                p = transform((col * 37, row * 37, 0))
                print(p)
                img = ImageTk.PhotoImage(self.image)
                self.tiles.append(img)
                self.create_image(p[0], p[1], image = img)

        self.pack(fill = tk.BOTH, expand = 1)        





def create_window():
    root = tk.Tk()

    window_width = 800
    window_height = 600

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height/2)

    root.title("Game")
    root.geometry('{0}x{1}+{2}+{3}'.format(window_width, window_height, center_x, center_y))
    root.resizable(False, False)

    map = Map(master = root)
    map.draw()
    sprite = Sprite(container = map, x = 0, y = 0)
    #sprite.draw()

    hero = Hero(container = map, x = 0, y = 0)
    hero.initialize()

    #map.bind_all('<Key>', sprite.move)
    map.bind_all('<Key>', hero.move)


    root.mainloop()


def main():
    create_window()



if __name__ == '__main__':
    main()