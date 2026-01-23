from Runner import Runner
import matplotlib.pyplot as plt
import random as rd
import math


# fitness penalties and reward
WALL_PENALTY = 10
BACKTRACK_PENALTY = 10
DISTANCE_PENALTY = 3
LENGTH_PENALTY = 1
GOAL_REACHED_BONUS = -100
DISCOVERY_BONUS = -2

class GeneticAlgo:
    """
    Classe représentant un algorithme génétique.
    """
    def __init__(self, maze, runner_length:int, pop_size:int, max_generations:int, mutation_rate:float, selection_rate:float):
        """ constructeur de GeneticAlgo
        Args:
            maze (Maze): labyrinthe utilisé
            runner_length (int): longueur des runners
            pop_size (int): taille de la population
            max_generations (int): nombre maximum de générations
            mutation_rate (float): taux de mutation
            selection_rate (float): taux de sélection
        """
        self.maze = maze
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.selection_rate = selection_rate
        self.max_generations = max_generations
        # initialise la population
        self.population = [Runner(maze.get_start(), runner_length) for i in range(pop_size)]
        self.explorated = set() # enregistre les cellules explorées pour les pheromones

        # pour les stats
        self.best_fitness_history = []
        self.fitness_avg_history = []
        self.length_history = []


    def fitness(self, runner:Runner):
        """
        calcule la fitness d'un runner (sa performance dans le labyrinthe)
        Args:
            runner (Runner): runner dont on veut calculer la fitness
        """
        # tout les runners commencent à 0
        fitness = 0

        # penalités pour les murs et les retours en arrière (case déjà visitée)
        visited = set()
        current_x, current_y = runner.get_start()[0], runner.get_start()[1]
        visited.add((current_x, current_y))
        for move in runner.get_path():
            if move == -1: # mouvement dans un mur -> penalité du mur + penalité d'immobilité (mm case)
                fitness += WALL_PENALTY
                fitness += BACKTRACK_PENALTY
            else:
                current_x, current_y = current_x + self.maze.get_cardinal()[move][0], current_y + self.maze.get_cardinal()[move][1]
                # si la case a déjà été visitée -> penalité de retour en arrière
                if (current_x, current_y) in visited:
                    fitness += BACKTRACK_PENALTY
                else:
                    # ajoute la case aux visitées
                    fitness += DISCOVERY_BONUS
                    visited.add((current_x, current_y))
        
        # derniere cell atteinte
        last_cell = runner.get_last_cell()
        # j'ai essayé avec la distance euclidienne mais ca marchait (bcp) moins bien qu'avec les distances de dijkstra
        # dist = math.sqrt((last_cell[0] - self.maze.get_goal()[0])**2 + (last_cell[1] - self.maze.get_goal()[1])**2)
        dist = self.maze.get_dijkstra_distance(last_cell[0], last_cell[1])
        fitness += dist * DISTANCE_PENALTY
        # longueur du chemin parcouru (on cherche le chemin le plus court)
        fitness += len(runner.get_path()) * LENGTH_PENALTY
        # bonus si le but est atteint
        if runner.is_goal_reached():
            fitness += GOAL_REACHED_BONUS

        runner.set_fitness(fitness)
        self.explorated = self.explorated.union(visited)

    def run_generation(self):
        """
        fait évoluer la population d'une génération
        Returns:
            Runner: le meilleur runner de la génération
        """
        # pour les stats (avg fitness et avg length de la gé,nération)
        avg_fitness = 0
        avg_length = 0
        for runner in self.population:
            # fait parcourir le labyrinthe au runner (via l'ADN mais en prenant en compte les obstacles)
            runner.journey(self.maze)
            self.fitness(runner)
            avg_fitness += runner.get_fitness()
            avg_length += len(runner.get_path())
        # pour les stats
        avg_fitness /= self.pop_size
        avg_length /= self.pop_size
        self.fitness_avg_history.append(avg_fitness)
        self.length_history.append(avg_length)
        self.tri_population() # tri la population par fitness
        self.best_fitness_history.append(self.population[0].get_fitness())
        # renvoie le meilleur runner
        return self.population[0]
    
    def evolution(self, resume_interval=100):
        """
        fait évoluer la population sur le nombre maximum de générations
        Returns:
            Runner: le meilleur runner de la dernière génération
        """
        for generation in range(self.max_generations):
            best_runner = self.run_generation()
            if (generation+1) % resume_interval == 0: # resume toutes les 100 générations
                print(f"Generation {generation}: best = {best_runner.get_fitness()}, avg = {self.fitness_avg_history[-1]}, avg length = {self.length_history[-1]}")
            self.selection() # sélection des meilleurs runners
            self.reproduction() # reproduction pour remplir la population
        return best_runner
    
    def selection(self):
        """
        sélectionne les meilleurs runners pour la reproduction
        """
        # garde les meilleurs selon le taux de sélection
        self.population = self.population[:round(self.pop_size*self.selection_rate)]
    
    def reproduction(self):
        """
        fait la reproduction des runners
        """
        self.apply_pheromones()
        elite = self.population.copy() # copie des meilleurs pour la reproduction
        #tant que la population n'est pas remplie
        while len(self.population) < self.pop_size:
            # sélection aléatoire de deux parents parmi les meilleurs
            parent1 = rd.choice(elite)
            parent2 = rd.choice(elite)
            child = self.crossover(parent1, parent2) # mix de l'ADN des parents
            self.mutation(child) # chance pour que l'enfant mute
            self.population.append(child)

    def crossover(self, parent1:Runner, parent2:Runner):
        """
        croisement de l'ADN de deux parents pour créer un enfant
        Args:
            parent1 (Runner): premier parent
            parent2 (Runner): second parent
        Returns:
            Runner: l'enfant
        """
        # cut au hasard dans l'ADN des parents
        dna_len = len(parent1.get_dna())
        cut = rd.randint(1, dna_len - 1)
        child = Runner(self.maze.get_start(), dna_len)
        child.set_dna(parent1.get_dna()[:cut] + parent2.get_dna()[cut:])
        return child

    def mutation(self, runner):
        """
        mutation de l'ADN d'un runner
        Args:
            runner (Runner): runner à muter
        """
        for i in range(len(runner.get_dna())):
            if rd.random() < self.mutation_rate:
                runner.mutate(rd.randint(0, 7), i)

    def tri_population(self):
        """
        trie la population par fitness dans l'ordre décroissant
        """
        n = len(self.population)
        for i in range(n):
            for j in range(i):
                if self.population[j].get_fitness() > self.population[i].get_fitness():
                    self.population[j], self.population[i] = self.population[i], self.population[j]

    def apply_pheromones(self):
        """
        Dépose des phéromones sur les impasses découvertes par les runners
        """            
        for x, y in self.explorated:
            # Si c'est une impasse
            if self.maze.is_dead_end(x, y):
                self.maze.set_pheromone(x, y) # On bouche la case

    def get_best_runner(self):
        """
        renvoie le meilleur runner de la dernière génération

        Returns:
            Runner: meilleur runner de la dernière génération
        """
        return self.population[0]

    def get_fitness_history(self):
        """
        renvoie l'historique des fitness

        Returns:
            list: historique des fitness
        """
        return self.fitness_history
    
    def get_fitness_avg(self):
        """
        renvoie l'historique de la moyenne des fitness

        Returns:
            list: historique de la moyenne des fitness
        """
        return self.fitness_avg_history
    
    def get_length_history(self):
        """
        renvoie l'historique de la longueur moyenne des runners

        Returns:
            list: historique de la longueur moyenne des runners
        """
        return self.length_history

    def plot_stats(self):
        """
        affiche les statistiques de l'évolution (fitness et longueur moyenne des runners)
        """
        # affiche les finess en fonction des générations
        plt.plot(self.best_fitness_history, label='best fitness')
        plt.plot(self.fitness_avg_history, label='average fitness')
        plt.xlabel('generations')
        plt.ylabel('fitness')
        plt.title('fitness au fil des generations')
        plt.legend()
        plt.grid(True)
        plt.show()
        # affiche la longueur moyenne des runners en fonction des générations
        plt.plot(self.length_history, label='average runner length', color='orange')
        plt.xlabel('generations')
        plt.ylabel('length')
        plt.title('longueur moyenne des runners au fil des generations')
        plt.legend()
        plt.grid(True)
        plt.show()