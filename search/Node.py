class Node:
    def __init__(self, coord, parent, g, h, f):
        self.coord = coord
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f