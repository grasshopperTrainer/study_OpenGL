import numpy as np
from tools import *


def wrap(tlist:Tlist, times: int = 1, _count=1):
    new_list = tlist
    for i in range(times):
        new_list = Tlist(new_list)

    return new_list

# def unwrap(self, times: int = 1):
#     for i in range(times):
#         try:
#             new_data = []
#             for i in self._data:
#                 new_data += i
#             self._data = new_data
#         except:
#             t = f'_from: {__class__.__name__}.trim - Alist already flat'
#             print(t)
#             break


def empty(structure):
    if isinstance(structure,(list,tuple)):
        print(structure)
        # for i in structure
        #     if

def fromlist(data):
    if isinstance(data,(list,tuple)):
        simples = []
        iterables = []
        for i in data:
            if isinstance(i,(list,tuple)):
                iterables.append(i)
            else:
                simples.append(i)
        simples = Tlist(*simples)

        branches = []
        for i in iterables:
            branches.append(fromlist(i))
        return Tlist(simples, *branches)

    else:
        return Tlist(data)
