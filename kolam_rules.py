import math

def distance(p1, p2):
    return math.dist(p1, p2)

def valid_move(curr, nxt, visited, max_len=3.0):
    if nxt in visited:
        return False
    if distance(curr, nxt) > max_len:
        return False
    return True
