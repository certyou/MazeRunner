from Maze import Maze
from Runner import Runner
import random as rd
import math
import time

# parameters
mutation_rate = 0.2
selection_rate = 0.4
# fitness penalties
wall_penalty = 10
backtrack_penalty = 10
distance_penalty = 10

class GeneticAlgo:
    def __init__(self, maze_size, pop_size, runner_length):
        self.maze = Maze(maze_size)
        self.maze.generate()
        self.goal = self.maze.get_goal()
        self.population = []
        for x in range(pop_size):
            runner = Runner(self.maze, runner_length)
            self.population.append(runner)

    def evolve(self, generations):
        for gen in range(generations):
            self.selection(selection_rate)
            self.reproduction()
            print(f"Generation {gen+1} best fitness: {self.fitness(self.get_best_runner(), self.goal)}")
    
    def fitness(self, runner, goal):
        path = runner.get_path()
        last_cell = runner.get_last_cell()
        # start with 0
        res = 0
        # distance to goal
        distance = math.sqrt((last_cell[0]-goal[0])**2 + (last_cell[1]-goal[1])**2)
        if distance == 0:
            res += 1000  # big reward for reaching the goal
        else:
            res -= distance_penalty * distance
        # penalty for backtracking and for staying in place
        for i in range(1, len(path)):
            if path[i] < 0:
                res -= wall_penalty
            elif abs(path[i] - path[i-1]) == 4 and path[i-1] >= 0:
                res -= backtrack_penalty
        return res
    
    def selection(self, ts):
        ranked_population = sorted(
            self.population,
            key=lambda runner: self.fitness(runner, self.goal),
            reverse=True
        )
        retain_length = int(len(ranked_population)*ts)
        self.population = ranked_population[:retain_length]

    def crossover(self, parent1, parent2):
        cut = rd.randint(0, parent1.get_length()-1)
        child_path = parent1.get_path()[:cut] + parent2.get_path()[cut:]
        child = Runner(self.maze, parent1.get_length(), path=child_path)
        return child
    
    def reproduction(self):
        for i in range(len(self.population), 20):  # assuming we want a population size of 20
            parent1 = rd.choice(self.population)
            parent2 = rd.choice(self.population)
            child = self.crossover(parent1, parent2)
            if rd.random() < 0.1:  # mutation probability
                self.mutate(child)
            self.population.append(child)
    
    def mutate(self, runner):
        path = runner.get_path()
        i = rd.randint(0, runner.get_length()-1)
        path[i] = rd.randint(0, 7)
        runner.set_path(path)

    def get_best_runner(self):
        return self.population[0]
    
    def display_best_runner(self):
        best_runner = self.get_best_runner()
        self.maze.display_runner(best_runner)
        #self.maze.display_soluce()

    def __str__(self):
        string = """"""
        for runner in self.population:
            string += str(runner) + '\n'
        return string