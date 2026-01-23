class Pile:
    """ classe simulant une Pile (FIFO)
    permettant de stocker les celulles déjà visitées
    """
    def __init__(self):
        """
        constructeur de Pile
        initialise une liste vide
        """
        self.size = 0
        self.elem = []

    def add(self, item):
        """ ajoute un element à la pile

        Args:
            item (tuple:(int,int)): coordonnée de la cellule à empiler
        """
        self.size += 1
        self.elem.append(item)

    def depile(self):
        """ renvoie le premier élément de la pile

        Returns:
            tuple(int,int): coordonnée de la cellule
        """
        self.size -= 1
        return self.elem.pop()
    
    def get_size(self):
        """renvoie la longueur de la pile

        Returns:
            int: nombre de cellule présebt dans la pile
        """
        return self.size