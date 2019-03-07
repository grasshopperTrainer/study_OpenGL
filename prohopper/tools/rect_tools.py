import numpy as np
from tools import *


def con_center(center: Point, sizex, sizey):
    x = sizex / 2
    y = sizey / 2
    p1 = trans.move(center, Vector(-x, y))
    p2 = trans.move(center, Vector(-x, -y))
    p3 = trans.move(center, Vector(x, -y))
    p4 = trans.move(center, Vector(x, y))
    # print(p1())
    return Rect(p1, p2, p3, p4)
