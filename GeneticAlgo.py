from Maze import Maze
from Runner import Runner
import random as rd
import math


class GeneticAlgo:
    def __init__(self, maze_size, pop_size, runner_length):
        self.maze = Maze(maze_size)
        self.population = [Runner(self.maze.get_start(), runner_length) for x in range(pop_size)]

    def evolution(self):
        rank = []
        return rank
    
    def fitness(self, runner, goal):
        res = math.sqrt(
            (runner.get_last_cell()[0] - goal[0])**2 +
            (runner.get_last_cell()[1] - goal[1])**2
        )
        return res