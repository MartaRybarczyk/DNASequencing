from src.constants import acid_map, dummy_oligo
from src.usefullFunctions import max_common_part
import numpy as np

class Solution():

    def __init__(self, ):
        super().__init__()
        self.path_len = 0                       # current path length
        self.path = [[dummy_oligo]]             # current path, ordered set of oligonucleotides
        self.commons = []                       # list of values, i-th value of the list indicates 
                                                # length of max length of common part of suffix in i-th oligo and i-th +1 oligo in the path
                                                # size of the commons list is equal to length(path) - 1
        self.graph_path = [dummy_oligo]         # path in graph

    def clear(self):
        self.path_len = 0
        self.path = [[dummy_oligo]]
        self.commons = []
        self.graph_path = []

    def add_oligo(self, oligo, vertex_no):
        self.path.append(oligo)
        comLen = max_common_part(self.path[-2], self.path[-1])
        self.commons.append(comLen)
        self.path_len += (len(self.path[-1]) - comLen)
        self.graph_path.append(vertex_no)

    def pop_back_oligo(self):
        self.path_len -= (len(self.path[-1]) - self.commons.pop())
        self.path.pop(-1)
        self.graph_path.pop()

    def get_path_len(self):
        return len(self.path) - 1

    def __str__(self):
        out = ''
        for i in range(1,len(self.path)):
            out += ''.join([acid_map[c] for c in self.path[i][self.commons[i - 1]:]])

        return out

if __name__ == "__main__":
    pass