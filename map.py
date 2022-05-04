from cmath import sqrt
import tkinter as tk
from PIL import Image, ImageTk


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


class Map(tk.Canvas):

    def __init__(self, master = None):
        super().__init__(master = master)
        
        self.image = Image.open("images/isometric_pixel_0056.png")
        self.tiles = list()

        self.number_of_columns = 20
        self.number_of_rows = 20

        self.tiles = list()

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

    root.mainloop()


def main():
    create_window()



if __name__ == '__main__':
    main()