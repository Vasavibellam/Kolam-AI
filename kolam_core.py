from enum import Enum

class Bond(Enum):
    CROSS = "X"
    DOUBLE = "D"
    BROKEN = "B"

class Dot:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Junction:
    def __init__(self, d1, d2, bond):
        self.d1 = d1
        self.d2 = d2
        self.bond = bond
