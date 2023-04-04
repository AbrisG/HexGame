class Action:
    def __init__(self, r, q, dr, dq, k):
        self.r = r
        self.q = q
        self.dr = dr
        self.dq = dq
        self.k = k

    def __str__(self):
        return f"Action: {self.r, self.q}, {self.dr, self.dq}, k: {self.k}"

    def to_tuple(self):
        return self.r, self.q, self.dr, self.dq
