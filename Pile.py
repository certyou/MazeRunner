class Pile:
    def __init__(self):
        self.size = 0
        self.elem = []

    def add(self, item):
        self.size += 1
        self.elem.append(item)

    def depile(self):
        self.size -= 1
        return self.elem.pop()
    
    def get_size(self):
        return self.size