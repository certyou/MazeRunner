import math
import sys
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from PIL import Image
from Pile import Pile


class Maze:
    """
    Classe représentant un labyrinthe carré de taille n x n.
    """
    def __init__(self, n:int):
        """ constructeur de Maze
        initialise un labyrinthe et définit un start aléatoire

        Args:
            n (int): taille du labyrinthe (n x n)
        """
        sys.setrecursionlimit(n*n*n)
        self.size = n
        self.pile = Pile()
        self.maze = np.zeros((n, n, 3), dtype=np.uint8) # matrice représentant le labyrinthe (au depart que des murs)
        self.empty_maze = None
        self.map = np.full((self.size, self.size), self.size**2, dtype=np.int64) # matrice des distances Dijkstra
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
        # start aléatoire
        rand_x = rd.randint(0, self.size-1)
        rand_y = rd.randint(0, self.size-1)
        while self.map[rand_x][rand_y] == -1:
            rand_x = rd.randint(0, self.size-1)
            rand_y = rd.randint(0, self.size-1)
        self.start = (rand_x, rand_y)
        self.change_color(rand_x, rand_y, [255,0,0])
        self.goal = (0, 0)
    
    def solve_from_random_coordonnates(self):
        """
        créer une arrivée aléatoire
        et résout le labyrinthe en utilsant dijkstra
        """
        # arrivée aléatoire
        rand_x = rd.randint(0, self.size-1)
        rand_y = rd.randint(0, self.size-1)
        dist_from_start = math.sqrt((rand_x - self.start[0])**2 + (rand_y - self.start[1])**2) # on s'assure que l'arrivée n'est pas trop proche du départ
        while self.map[rand_x][rand_y] == -1 and dist_from_start < self.size*2/3:
            rand_x = rd.randint(0, self.size-1)
            rand_y = rd.randint(0, self.size-1)
        self.goal = (rand_x, rand_y)
        self.change_color(rand_x, rand_y, [255,0,0])
        self.dijkstra()
        self.solve(self.start[0], self.start[1])
        self.change_color(self.start[0], self.start[1], [0,255,0]) # départ en vert (pour l'affichage dijkstra)
        self.change_color(self.goal[0], self.goal[1], [0,255,0]) # arrivée en vert (pour l'affichage dijkstra)

    def solve(self, x:int, y:int):
        """
        résout le labyrinthe en suivant les distances Dijkstra
        (en coloriant le chemin en rouge)
        Args:
            x (int): coordonnées en x
            y (int): coordonnées en y
        """
        min_i, min_j = x, y
        self.change_color(x, y, [255,0,0])
        for direction in self.cardinal:
            i = x+self.cardinal[direction][0]
            j = y+self.cardinal[direction][1]
            # tant qu'on est dans le labyrinthe
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                # on cherche la cellule voisine avec la plus petite distance de l'arrivée
                if 0 <= self.map[i][j] < self.map[min_i][min_j]:
                    min_i = i
                    min_j = j
        # on continue la résolution tant qu'on n'est pas arrivé
        if (x!=self.goal[0] or y!=self.goal[1]) and (x!=min_i or y!=min_j):
            self.solve(min_i, min_j)

    def dijkstra(self):
        """
        calcule les distances Dijkstra de chaque cellule par rapport à l'arrivée
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j][0] == 0:
                    self.map[i][j] = -1 # mur
        # l'arrivée a forcément une distance de 0
        self.map[self.goal[0]][self.goal[1]] = 0
        # on incrémente à partir de l'arrivée
        self.increment_neighbours(self.goal[0], self.goal[1], 1)

    def increment_neighbours(self, x:int, y:int, cpt:int):
        """
        incrémente les distances de Dijkstra des cellules voisines récursivement
        Args:
            x (int): coordonnées en x
            y (int): coordonnées en y
            cpt (int): compteur de distance
        """
        for direction in self.cardinal:
            i = x+self.cardinal[direction][0]
            j = y+self.cardinal[direction][1]
            # tant qu'on est dans le labyrinthe
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                # et que la voisine à une distance plus grande
                if self.map[i][j] > cpt:
                    self.map[i][j] = cpt
                    self.increment_neighbours(i,j,cpt+1)
    
    def generate(self):
        """
        génère le labyrinthe en utilisant l'algo décrit dans le tp
        """
        self.change_color(self.start[0], self.start[1])
        next_cell = (self.start[0], self.start[1]) # on commence par le départ
        self.pile.add(next_cell)
        while self.pile.get_size() > 0: # tant que la pile n'est pas vide
            # on cherche une cellule voisine éligible
            next_cell = self.check_neighbours(next_cell[0], next_cell[1])
            if next_cell: # si on en trouve une
                self.pile.add(next_cell) # on l'ajoute à la pile
                self.change_color(next_cell[0], next_cell[1]) # on la marque comme chemin
            else: # sinon on dépile
                next_cell = self.pile.depile()
        self.empty_maze = self.maze.copy()

    def check_neighbours(self, x:int, y:int):
        """
        renvoie aléatoirement une cellule voisine éligible
        Args:
            x (int): coordonnées en x
            y (int): coordonnées en y
        Returns:
            tuple (int, int): coordonnées de la cellule éligible, None sinon
        """
        cardinal = self.cardinal.copy()
        for k in range(8): # on essaye les 8 directions
            direction = rd.choice(list(cardinal.keys())) # on prend une direction aléatoire
            i = x+cardinal[direction][0]
            j = y+cardinal[direction][1]
            # tant qu'on est dans le labyrinthe
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                # et si la cellule est éligible
                if self.check_elegibility(i, j):
                    return i, j
                else:
                    del(cardinal[direction])
        return None
    
    def check_elegibility(self, x:int, y:int):
        """
        vérifie si la cellule est éligible (possède exactement un voisin non mur)
        Args:
            x (int): coordonnées en x
            y (int): coordonnées en y
        Returns:
            bool: True si la cellule est éligible, False sinon
        """
        cpt = 0
        for direction in self.cardinal:
            i = x+self.cardinal[direction][0]
            j = y+self.cardinal[direction][1]
            # tant qu'on est dans le labyrinthe
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if self.maze[i][j][0] == 255:
                    cpt += 1
        # la cellule est éligible si elle a exactement un voisin non mur
        return cpt == 1
    
    def is_dead_end(self, x:int, y:int):
        """
        vérifie si la cellule est une impasse (possède au plus un voisin non mur)
        Args:
            x (int): coordonnées en x
            y (int): coordonnées en y
        Returns:
            bool: True si la cellule est une impasse, False sinon
        """
        cpt = 0
        for direction in self.cardinal:
            i = x+self.cardinal[direction][0]
            j = y+self.cardinal[direction][1]
            # tant qu'on est dans le labyrinthe
            if (i>=0 and i<self.size) and (j>=0 and j<self.size):
                if self.maze[i][j][0] == 255:
                    cpt += 1
            if (i, j) == self.start or (i, j) == self.goal:
                return False
        return cpt <= 1
    
    def set_pheromone(self, x, y):
        if (x, y) != self.start and (x, y) != self.goal:
            self.map[x][y] = -1
            self.change_color(x, y, [100, 100, 100]) 
    
    def change_color(self, x:int, y:int, color:list=[255, 255, 255]):
        """
        change la couleur d'une cellule avec la couleur donnée
        Args:
            x (int): coordonnées en x
            y (int): coordonnées en y
            color (list): couleur à appliquer
        """
        self.maze[x][y] = color

    def get_cardinal(self):
        """
        renvoie les directions cardinales

        Returns:
            dict: directions cardinales
        """
        return self.cardinal
    
    def get_size(self):
        """
        renvoie la taille du labyrinthe

        Returns:
            int: taille du labyrinthe
        """
        return self.size
    
    def get_start(self):
        """
        renvoie les coordonnées du départ

        Returns:
            tuple (int, int): coordonnées du départ
        """
        return self.start
    
    def get_goal(self):
        """
        renvoie les coordonnées de l'arrivée

        Returns:
            tuple (int, int): coordonnées de l'arrivée
        """
        return self.goal
    
    def get_dijkstra_distance(self, x:int, y:int):
        """
        renvoie la distance Dijkstra d'une cellule
        Args:
            x (int): coordonnées en x
            y (int): coordonnées en y
        Returns:
            int: distance Dijkstra
        """
        return self.map[x][y]
    
    def is_valid(self, postion:tuple, move:tuple):
        """
        vérifie si un mouvement est valide
        Args:
            position (tuple (int, int)): position actuelle
            move (tuple (int, int)): mouvement voulu
        Returns:
            bool: True si le mouvement est valide (dans le labyrinthe et pas un mur), False sinon
        """
        i = postion[0]+move[0]
        j = postion[1]+move[1]
        # tant qu'on est dans le labyrinthe
        if (i>=0 and i<self.size) and (j>=0 and j<self.size):
            # et que ce n'est pas un mur
            if self.map[i][j] != -1:
                return True
        return False

    def display_soluce(self):
        """
        affiche le labyrinthe avec la solution dijkstra (en rouge)
        """
        img = Image.fromarray(self.maze)
        img.show()
    
    def display_map(self):
        """
        affiche la matrice des distances Dijkstra par rapport à l'arrivée
        """
        plt.matshow(self.map)
        plt.show()

    def display_maze(self):
        """
        affiche le labyrinthe
        """
        img = Image.fromarray(self.maze)
        img.show()

    def display_runner(self, runner):
        """
        affiche le labyrinthe avec le runner (en vert)
        le départ en bleu et l'arrivée en rouge et le chemin optimisé en rouge (dijkstra, uniquement si le runner n'a pas atteint le but)
        Args:
            runner (Runner): le runner à afficher
        """
        runner_on_maze = self.maze.copy()
        cell = list(runner.get_start()) # position de départ
        path = runner.get_path()
        for direction in path:
            if direction >=0: # si le mouvement n'est pas dans un mur ou en dehors du labyrinthe
                move = self.cardinal[direction]
                runner_on_maze[cell[0]][cell[1]] = [0,255,0] # on colorie la cellule en vert
                cell[0] += move[0]
                cell[1] += move[1]
        # on colorie l'arrivée en rouge et le départ en bleu
        runner_on_maze[self.goal[0]][self.goal[1]] = [255,0,0]
        runner_on_maze[self.start[0]][self.start[1]] = [0,0,255]
        img = Image.fromarray(runner_on_maze)
        img.show()

    def display_all(self):
        """
        affihe tous les labyrinthes 
        """
        self.display_maze()
        self.display_map()
        self.display_soluce()