import numpy as np
from tools import *

a = Point(0, 0, 0)
# v = Vector(1,2,0)

first = Tlist([[0, 0], [[1, 1], [2, 2]], [3, 3]])
second = Tlist([[[], []], [[[]]]])
third = Tlist([[0, 0], [[[1], [1]]]])
fourth = Tlist([[0, 0]])
fifth = Tlist([[[0], [0]], [[[10, 1]], [[11]]], [[2], [22, 222]], [[3], [33, 333, 3333]]])
six = Tlist([2, 3, 4])

fifth.pruneall()
fifth.print_data()
