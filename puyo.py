from material import Material
import numpy as np


class Puyo:
    color_num = 4
    DIR_UP = (0, -1)
    DIR_DOWN = (0, 1)
    DIR_LEFT = (-1, 0)
    DIR_RIGHT = (1, 0)
    DIRECTIONS = (DIR_UP, DIR_LEFT, DIR_DOWN, DIR_RIGHT)

    def __init__(self, x, y):
        self.color_axis = self.get_new_color()
        self.pos_x = x
        self.pos_y = y
        self.color_son = self.get_new_color()
        self.dir = 0

    def get_new_color(self):
        return int(np.random.randint(Material.R_PUYO,  Material.R_PUYO + self.color_num, 1))

    def copy(self, src):
        self.color_axis = src.color_axis
        self.color_son = src.color_son
        self.dir = 0

    def set_blank(self):
        self.color_axis = Material.BLANK
        self.color_son = Material.BLANK

    def __str__(self):
        return "Puyo <axis:{0}, son:{1}, (x, y)=({2}, {3}), dir:{4}>".format\
            (self.color_axis, self.color_son, self.pos_x, self.pos_y, self.DIRECTIONS[self.dir])

if __name__ == "__main__":
    p1 = Puyo(2, 3)
    p2 = Puyo(5, 6)
    print(p1)
    print(p2)
