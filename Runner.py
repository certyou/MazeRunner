import random as rd

class Runner:
    def __init__(self, start, length):
        self.start = list(start)
        self.length = length
        self.cardinal = {
            "north":[-1, 0],
            "south":[1, 0],
            "west":[0, -1],
            "east":[0, 1],
            "north-east": [-1, 1],
            "north-west": [-1, -1],
            "south-east": [1, 1],
            "south-west": [1, -1]
        }
        self.path = [rd.choice(self.cardinal) for x in range(length)]
        self.last_cell = self.start
        for step in self.path:
            self.last_cell[0], self.last_cell[1] += step[0], step[1]

    def get_last_cell(self):
        return self.last_cell
    
    def get_start(self):
        return self.start
    
    def get_length(self):
        return self.length
    
    def get_path(self):
        return self.path