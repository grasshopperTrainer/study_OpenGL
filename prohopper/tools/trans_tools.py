import numpy as np
import copy
from tools import *

def move(obj: Geometry, vec: Vector):

    trans = np.eye(4)
    trans[:,3] = vec.get_data()
    new = copy.deepcopy(obj)
    new.set_data(np.dot(trans,obj.get_data()))

    return new

