# This follows the instructions in this tutorial
# - https://www.pythontutorial.net/tkinter/tkinter-window/
# - https://zetcode.com/tkinter/drawing/


from cmath import sqrt
from ftplib import parse150
import tkinter as tk
from turtle import color


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






class Map(tk.Canvas):

    def __init__(self, master = None):
        super().__init__(master = master)

        self.initUI()

    def initUI(self):

        #self.pack(fill = tk.BOTH, expand = 1)

        # Drawing the tiles on the map
        # ------------------------------------------------------------

        for col in range(-5, 5):
            for row in range(-5, 5):
                tile = Tile(self, col = col, row = row)
                tile.draw()





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
    sprite = Sprite(container = map, x = 0, y = 0)
    sprite.draw()

    map.bind_all('<Key>', sprite.move)


    root.mainloop()


def main():
    create_window()



if __name__ == '__main__':
    main()