import random as rd


class Runner:
    """
    Classe représentant un individu tentant de résoudre le labyrinthe.
    """
    def __init__(self, start:tuple, runner_length:int):
        self.start = start
        # ici je fais la différence entre l'ADN du runner (self.dna) et le chemin réellement parcouru (self.path)
        # le but étant de pouvoir tracer le chemin réellement parcouru dans le labyrinthe sans compromettre l'ADN
        self.dna = [rd.randint(0, 7) for i in range(runner_length)]
        self.path = []
        self.fitness = float('inf') # fitness initiale infinie
        self.last_cell = start # dernière cellule atteinte
        self.reached_goal = False # indique si le but a été atteint

    def journey(self, maze):
        """
        Fait parcourir le labyrinthe au runner selon son ADN en prenant en compte les obstacles.
        Args:
            maze (Maze): labyrinthe parcouru
        """
        current_x, current_y = self.start[0], self.start[1]
        self.path = []
        for direction in self.dna: # pour chaque mouvement dans l'ADN
            move = maze.get_cardinal()[direction]
            # on vérifie si le mouvement est valide (dans le labyrinthe et pas un mur)
            if maze.is_valid((current_x, current_y), move):
                # si oui, on effectue le mouvement et on l'ajoute au chemin parcouru
                current_x += move[0]
                current_y += move[1]
                self.path.append(direction)
                self.last_cell = (current_x, current_y)
            else:
                # sinon, on reste sur place et on ajoute -1 au chemin parcouru
                self.path.append(-1) 
            if (current_x, current_y) == maze.get_goal():
                # si le but est atteint, on arrête le parcours et on ajuste l'ADN
                self.reached_goal = True
                self.dna = self.dna[:len(self.path)]
                break

    def mutate(self, mutation:int, index:int):
        """
        mutation de l'ADN du runner à l'index donné.
        Args:
            mutation (int): nouvelle direction pour l'ADN à l'index donné
            index (int): index dans l'ADN à muter
        """
        self.dna[index] = mutation

    def set_fitness(self, fitness:int):
        """
        définit la fitness du runner
        Args:
            fitness (int): valeur actuelle de la fitness du runner
        """
        self.fitness = fitness
    
    def set_dna(self, dna:list):
        """
        définit l'ADN du runner, (utile pour la reproduction)
        Args:
            dna (list): valeur de l'ADN du runner
        """
        self.dna = dna

    def set_reached_goal(self, reached_goal:bool):
        """
        définit si le but a été atteint
        Args:
            reached_goal (bool): True si le but a été atteint, False sinon
        """
        self.reached_goal = reached_goal

    def is_goal_reached(self):
        """
        renvoie si le but a été atteint

        Returns:
            bool: True si le but a été atteint, False sinon
        """
        return self.reached_goal

    def get_fitness(self):
        """
        renvoie la fitness du runner

        Returns:
            int: fitness du runner
        """
        return self.fitness

    def get_last_cell(self):
        """
        renvoie les coordonnées de la dernière cellule atteinte

        Returns:
            tuple (int, int): coordonnées de la dernière cellule atteinte
        """
        return self.last_cell
    
    def get_start(self):
        """
        renvoie les coordonnées du départ

        Returns:
            tuple (int, int): coordonnées du départ
        """
        return self.start
    
    def get_length(self):
        """
        renvoie la longueur du chemin parcouru

        Returns:
            int: longueur du chemin parcouru
        """
        return len(self.path)
    
    def get_path(self):
        """
        renvoie le chemin parcouru

        Returns:
            list: chemin parcouru
        """
        return self.path
    
    def get_dna(self):
        """
        renvoie l'ADN du runner

        Returns:
            list: ADN du runner
        """
        return self.dna
    
    def __str__(self):
        """
        renvoie une chaîne de caractères représentant le runner, (chemin parcouru)

        Returns:
            str: chaîne de caractères représentant le runner
        """
        return str(self.path)