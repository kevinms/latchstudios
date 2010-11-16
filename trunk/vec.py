from math import *

def add(x1, y1, x2, y2):
    x = x1 + x2
    y = y1 + y2
    return x, y

def subtract(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    return x, y

def length(x, y):
    return float(sqrt(x * x + y * y))

def unitdir(x1, y1, x2, y2, tol):
    x, y = subtract(x1, y1, x2, y2)
    leng = length(x, y)
    if (leng < tol):
        return 0, 0
    x = float(x / leng)
    y = float(y / leng)
    return x, y
