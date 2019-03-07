import numpy as np
import copy
from tools import *


def translation(vector: Vector):
    trans = np.eye(4)
    trans[:3, 3] = vector()[:3, 0]
    return trans


def scaling():
    pass


def rotation():
    pass
