import sys
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from PIL import Image
from Pile import Pile


class Maze:
    def __init__(self, n:int):
        sys.setrecursionlimit(n*n*n)
        self.size = n
        self.pile = Pile()
        self.maze = np.zeros((n, n, 3), dtype=np.uint8)
        self.map = np.full((self.size, self.size), self.size**2, dtype=np.int64)
        self.cardinal = {
            0: [0, 1],
            1: [-1, 1],
            2: [-1, 0],
            3: [-1, -1],
            4: [0, -1],
            5: [1, -1],
            6: [1, 0],
            7: [1, 1],
        }
        rand_x = rd.randint(0, self.size-1)
        rand_y = rd.randint(0, self.size-1)
        # start
        while self.map[rand_x][rand_y] == -1:
            rand_x = rd.randint(0, self.size-1)
            rand_y = rd.randint(0, self.size-1)
        self.start = (rand_x, rand_y)
        self.change_color(rand_x, rand_y, [255,0,0])
        self.goal = (0, 0)
    
    def solve_from_random_coordonnates(self):
        # goal
        rand_x = rd.randint(0, self.size-1)
        rand_y = rd.randint(0, self.size-1)
        while self.map[rand_x][rand_y] == -1 and (rand_x, rand_y)!=self.start:
            rand_x = rd.randint(0, self.size-1)
            rand_y = rd.randint(0, self.size-1)
        self.goal = (rand_x, rand_y)
        self.change_color(rand_x, rand_y, [255,0,0])
        self.dijkstra()
        self.solve(self.start[0], self.start[1])
        self.change_color(self.start[0], self.start[1], [0,255,0])
        self.change_color(self.goal[0], self.goal[1], [0,255,0])

    def solve(self, x, y):
        min_i, min_j = x, y
        self.change_color(x, y, [255,0,0])
        for direction in self.cardinal:
            i = x+self.cardinal[direction][0]
            j = y+self.cardinal[direction][1]
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if 0 <= self.map[i][j] < self.map[min_i][min_j]:
                    min_i = i
                    min_j = j
        if (x!=self.goal[0] or y!=self.goal[1]) and (x!=min_i or y!=min_j):
            self.solve(min_i, min_j)

    def dijkstra(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j][0] == 0:
                    self.map[i][j] = -1
        self.map[self.goal[0]][self.goal[1]] = 0
        self.increment_neighbours(self.goal[0], self.goal[1], 1)

    def increment_neighbours(self, x, y, cpt):
        for direction in self.cardinal:
            i = x+self.cardinal[direction][0]
            j = y+self.cardinal[direction][1]
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if self.map[i][j] > cpt:
                    self.map[i][j] = cpt
                    self.increment_neighbours(i,j,cpt+1)
    
    def generate(self):
        self.change_color(self.start[0], self.start[1])
        next_cell = (self.start[0], self.start[1])
        self.pile.add(next_cell)
        while self.pile.get_size() > 0:
            next_cell = self.check_neighbours(next_cell[0], next_cell[1])
            if next_cell:
                self.pile.add(next_cell)
                self.change_color(next_cell[0], next_cell[1])
            else:
                next_cell = self.pile.depile()

    def check_neighbours(self, x, y):
        cardinal = self.cardinal.copy()
        for k in range(8):
            direction = rd.choice(list(cardinal.keys()))
            i = x+cardinal[direction][0]
            j = y+cardinal[direction][1]
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if self.check_elegibility(i, j):
                    return i, j
                else:
                    del(cardinal[direction])
        return None
    
    def check_elegibility(self, x, y):
        cpt = 0
        for direction in self.cardinal:
            i = x+self.cardinal[direction][0]
            j = y+self.cardinal[direction][1]
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if self.maze[i][j][0] == 255:
                    cpt += 1
        return cpt == 1
    
    def change_color(self, x, y, color=[255, 255, 255]):
        self.maze[x][y] = color

    def get_size(self):
        return self.size
    
    def get_start(self):
        return self.start
    
    def get_goal(self):
        return self.goal
    
    def is_valid(self, postion, move):
        i = postion[0]+move[0]
        j = postion[1]+move[1]
        # move in the maze
        if (i>=0 and i<self.size) and (j>=0 and j<self.size):
            # not a wall
            if self.map[i][j] != -1:
                return True
        return False

    def display_soluce(self):
        img = Image.fromarray(self.maze)
        img.show()
    
    def display_map(self):
        plt.matshow(self.map)
        plt.show()

    def display_runner(self, runner):
        runner_on_maze = self.maze.copy()
        cell = list(runner.get_start())
        path = runner.get_path()
        for direction in path:
            if direction >=0:
                move = self.cardinal[direction]
                runner_on_maze[cell[0]][cell[1]] = [0,255,0]
                cell[0] += move[0]
                cell[1] += move[1]
        img = Image.fromarray(runner_on_maze)
        img.show()