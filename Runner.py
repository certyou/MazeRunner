from Maze import Maze
import random as rd
import time


rd.seed()

class Runner:
    def __init__(self, maze:Maze, length:int, path=None):
        self.maze = maze
        self.start = maze.get_start()
        self.length = length
        self.last_cell = list(self.start)
        self.cardinal = {
            0:[0, 1],
            1: [-1, 1],
            2: [-1, 0],
            3: [-1, -1],
            4:[0, -1],
            5: [1, -1],
            6:[1, 0],
            7: [1, 1],
        }
        self.path = []
        if not path:
            self.generate()
        else:
            self.set_path(path)

    def generate(self):
        for i in range(self.length):
            direction = rd.choice(list(self.cardinal.keys()))
            move = self.cardinal[direction]
            new_x = self.last_cell[0] + move[0]
            new_y = self.last_cell[1] + move[1]
            if self.maze.is_valid([new_x, new_y], move):
                self.last_cell = [new_x, new_y]
                self.path.append(direction)
            else: # illegal move, stay in place
                self.path.append(-direction)

    def set_path(self, path):
        self.path = path
        self.last_cell = list(self.start)
        for i in range(len(path)):
            direction = abs(path[i])
            move = self.cardinal[direction]
            new_x = self.last_cell[0] + move[0]
            new_y = self.last_cell[1] + move[1]
            if self.maze.is_valid([new_x, new_y], move):
                self.last_cell = [new_x, new_y]
            else: # illegal move, stay in place
                self.path[i] = -direction
            if self.last_cell == list(self.maze.get_goal()):
                break

    def get_last_cell(self):
        return self.last_cell
    
    def get_start(self):
        return self.start
    
    def get_length(self):
        return self.length
    
    def get_path(self):
        return self.path
    
    def __str__(self):
        return str(self.path)