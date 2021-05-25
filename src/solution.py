from src.constants import acid_map, dummy_oligo
from src.usefullFunctions import max_common_part, levenshteinDistance
import numpy as np
import copy

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

def is_valid(solution, S):
    """
    Checks if solution is valid.
    - solution: Solution class object
    - S: set of oligo, data of the problem
    """
    copyS = copy.deepcopy(S)

    path_len = len(copyS[solution.graph_path[1]])

    for i in range(2, len(solution.graph_path)):

        try:
            temp = max_common_part(copyS[solution.graph_path[i - 1]], copyS[solution.graph_path[i]])
        except KeyError:
            return False

        if solution.commons[i - 1] != temp:
            return False
        
        path_len += temp

        copyS.pop(solution.graph_path[i - 1])


    return True

def solutionQuality(solution, origin_seq, n, l, name='lev'):

    if name == 'lev':
        found_seq = str(solution)
        max_dist = max(len(found_seq), len(origin_seq))
        return 1 - levenshteinDistance(found_seq, origin_seq) / max_dist
    if name == 'oligo used':
        return solution.get_path_len() / n

    return None

if __name__ == "__main__":
    pass