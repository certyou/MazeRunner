from Maze import Maze
import random as rd

class Runner:
    def __init__(self, start, runner_length):
        self.start = start
        self.dna = [rd.randint(0, 7) for i in range(runner_length)]
        self.fitness = float('inf')
        self.last_cell = start
        self.path = []
        self.reached_goal = False

    def journey(self, maze):
        current_x, current_y = self.start[0], self.start[1]
        self.path = []
        for direction in self.dna:
            move = maze.get_cardinal()[direction]
            if maze.is_valid((current_x, current_y), move):
                current_x += move[0]
                current_y += move[1]
                self.path.append(direction)
                self.last_cell = (current_x, current_y)
            else:
                self.path.append(-1) 
            if (current_x, current_y) == maze.get_goal():
                break

    def mutate(self, mutation, index):
        self.dna[index] = mutation

    def set_fitness(self, fitness):
        self.fitness = fitness
    
    def set_dna(self, dna):
        self.dna = dna

    def set_reached_goal(self, reached_goal):
        self.reached_goal = reached_goal

    def is_goal_reached(self):
        return self.reached_goal

    def get_fitness(self):
        return self.fitness

    def get_last_cell(self):
        return self.last_cell
    
    def get_start(self):
        return self.start
    
    def get_length(self):
        return len(self.genome)
    
    def get_path(self):
        return self.path
    
    def get_dna(self):
        return self.dna
    
    def __str__(self):
        return str(self.path)