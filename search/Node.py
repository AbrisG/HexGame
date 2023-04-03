class Node:
    def __init__(self, coord, parent, g, h, k, offset, state):
        self.coord = coord
        self.parent = parent
        self.g = g
        self.h = h
        self.k = k
        self.f = g + h
        self.offset = offset
        self.state = state

    dr_dq = [
        (0, 1),  # down-right
        (-1, 1),  # down
        (-1, 0),  # down-left
        (0, -1),  # up-left
        (1, -1),  # up
        (1, 0)  # up-right
    ]

    def get_neighbours(self):
        # Grab all the neighbours according to the offsets and the power (k)
        neighbours = {key: [] for key in Node.dr_dq}
        for i in range(1, self.k + 1):
            for (dr, dq) in Node.dr_dq:
                neighbours[(dr, dq)].append(((self.coord[0] + dr * i) % 7, (self.coord[1] + dq * i) % 7))
        return neighbours

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.coord == other.coord \
            and self.parent == other.parent \
            and self.g == other.g \
            and self.h == other.h \
            and self.k == other.k \
            and self.offset == other.offset \
            and self.state == other.state

    def __str__(self):
        return f"Node: {self.coord}, g: {self.g}, h: {self.h}, f: {self.f}, k: {self.k}"
