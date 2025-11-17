from Pile import Pile
from PIL import Image
import numpy as np
import random as rd


class Maze:
    def __init__(self, n:int):
        self.size = n
        self.pile = Pile()
        self.maze = np.zeros((n, n, 3), dtype=np.uint8)
        self.cardinal = {
            "north":[-1, 0],
            "south":[1, 0],
            "west":[0, -1],
            "east":[0, 1]
        }

    def get_size(self):
        return self.size
    
    def generate(self):
        rand_x = rd.randint(0, self.size-1)
        rand_y = rd.randint(0, self.size-1)
        self.change_color(rand_x, rand_y)
        next_cell = (rand_x, rand_y)
        self.pile.add(next_cell)
        while self.pile.get_size() > 0:
            next_cell = self.check_neighbours(next_cell[0], next_cell[1])
            if next_cell:
                self.pile.add(next_cell)
                self.change_color(next_cell[0], next_cell[1])
            else:
                next_cell = self.pile.depile()
        self.change_color(0, 0, [255,0,0])

    def display(self):
        img = Image.fromarray(self.maze)
        img.show()

    def check_neighbours(self, x, y):
        cardinal = self.cardinal.copy()
        for k in range(4):
            choice = rd.choice(list(cardinal.keys()))
            i = x+self.cardinal[choice][0]
            j = y+self.cardinal[choice][1]
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if self.check_elegibility(i, j):
                    return i, j
                else:
                    del(cardinal[choice])
        return None
    
    def check_elegibility(self, x, y):
        cpt = 0
        for choice in self.cardinal:
            i = x+self.cardinal[choice][0]
            j = y+self.cardinal[choice][1]
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if self.maze[i][j][0] == 255:
                    cpt += 1
        return cpt == 1
    
    def change_color(self, x, y, color=[255, 255, 255]):
        self.maze[x][y] = color