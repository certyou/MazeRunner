from Maze import Maze
from Runner import Runner
import random as rd
import math


# parameters for maze
MAZE_SIZE = 50
# parameters for genetic algorithm
POPULATION_SIZE = 200
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.1
SELECTION_RATE = 0.4
RUNNER_LENGTH = MAZE_SIZE ** 2
# fitness penalties
WALL_PENALTY = 20
BACKTRACK_PENALTY = 5
DISTANCE_PENALTY = 10
LENGTH_PENALTY = 1

class GeneticAlgo:
    def __init__(self, maze, runner_length, pop_size=100, max_generations=1000, mutation_rate=0.1, selection_rate=0.5):
        self.maze = maze
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.selection_rate = selection_rate
        self.max_generations = max_generations
        self.runner_length = runner_length
        self.population = [Runner(maze.get_start(), self.runner_length) for i in range(pop_size)]

    def fitness(self, runner):
        fitness = 0

        visited = set()
        current_x, current_y = runner.get_start()[0], runner.get_start()[1]
        visited.add((current_x, current_y))
        for move in runner.get_path():
            if move == -1:
                fitness += WALL_PENALTY
            else:
                current_x, current_y = current_x + self.maze.get_cardinal()[move][0], current_y + self.maze.get_cardinal()[move][1]
                if (current_x, current_y) in visited:
                    fitness += BACKTRACK_PENALTY
                else:
                    visited.add((current_x, current_y))
        
        goal = self.maze.get_goal()
        last_cell = runner.get_last_cell()
        dist = math.sqrt((last_cell[0] - goal[0])**2 + (last_cell[1] - goal[1])**2)
        fitness += dist * DISTANCE_PENALTY

        fitness += len(runner.get_path()) * LENGTH_PENALTY
        runner.set_fitness(fitness)

    def run_generation(self):
        for runner in self.population:
            runner.journey(self.maze)
            self.fitness(runner)
        self.population.sort(key=lambda runner: runner.get_fitness())
        if self.population[0].get_fitness() == 0:
            self.population[0].set_reached_goal(True)
            return self.population[0]
        return self.population[0]
    
    def selection(self):
        self.population.sort(key=lambda runner: runner.get_fitness())
        self.population = self.population[:round(self.pop_size*self.selection_rate)]
    
    def reproduction(self):
        elite = self.population.copy()
        while len(self.population) < self.pop_size:
            parent1 = rd.choice(elite)
            parent2 = rd.choice(elite)
            child = self.crossover(parent1, parent2)
            self.mutation(child)
            self.population.append(child)

    def crossover(self, parent1, parent2):
        cut = rd.randint(1, self.runner_length - 1)
        child = Runner(self.maze.get_start(), self.runner_length)
        child.set_dna(parent1.get_dna()[:cut] + parent2.get_dna()[cut:])
        return child

    def mutation(self, runner):
        for i in range(self.runner_length):
            if rd.random() < self.mutation_rate:
                runner.mutate(rd.randint(0, 7), i)


if __name__ == "__main__":
    maze = Maze(MAZE_SIZE)
    maze.generate()
    maze.solve_from_random_coordonnates()
    print(f"Départ: {maze.get_start()} -> Objectif: {maze.get_goal()}")

    world = GeneticAlgo(maze, RUNNER_LENGTH, POPULATION_SIZE, MAX_GENERATIONS, MUTATION_RATE, SELECTION_RATE)    
    best_runner = None
    
    for i in range(MAX_GENERATIONS):
        best_runner = world.run_generation()
        world.selection()
        world.reproduction()
        if (i+1) % 200 == 0:
            print(f"generation n°{i+1}: {best_runner.get_fitness()} fitness")
            maze.display_runner(best_runner)
            print(best_runner.get_dna())
            print(best_runner.get_path())
    
    if not best_runner.is_goal_reached():
        print("goal not reached.")