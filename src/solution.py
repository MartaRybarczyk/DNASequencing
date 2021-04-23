from src.constants import acid_map, dummy_oligo
from src.initialSolution import max_common_part
import numpy as np

class Solution():
    pass
    """
    In constructor you have to pass length of the oligonucleotide
    """
    def __init__(self, l):
        super().__init__()
        self.path_len = 0                       # current path length
        self.path = [[dummy_oligo]]             # current path, ordered set of oligonucleotides
        self.commons = []                       # list of values, i-th value of the list indicates 
                                                # length of max length of common part of suffix in i-th oligo and i-th +1 oligo in the path
                                                # size of the commons list is equal to length(path) - 1

    def clear(self):
        self.path_len = 0
        self.path = [[dummy_oligo]]
        self.commons = []

    def add_oligo(self, oligo):
        self.path.append(oligo)
        comLen = max_common_part(self.path[-2], self.path[-1])
        self.commons.append(comLen)
        self.path_len += comLen

    def pop_back_oligo(self):
        self.path_len -= self.commons.pop()
        self.path.pop(-1)

    def __str__(self):
        out = ''
        for i in range(len(path)):
            out += ''.join(path[i][self.commons[i]])

        return out