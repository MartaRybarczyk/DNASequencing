import numpy as np
import random
import copy

from src.constants import acid_map
from src.sequenceFactory import generateSampleOligo

def max_common_part(oligo_prec, oligo_succ):

    n1 = len(oligo_prec)
    n2 = len(oligo_succ)
    
    for i in range(min(n1, n2), -1, -1):
        if (oligo_prec[n1 - i:] == oligo_succ[:i]).all() == True:
            return i

    
    return 0

def find_best_subpath(path, n):
    """
    Returns solution with c(path)  <= n
    In other words searches for longest (in terms of number of oligo) subpath in path
    """
    #to do
    return None

def choose_next_oligo(oligo_prec, S, type='greedy'):
    """
    Return index of set S, which corresponds to best oligo
    """ 
    return np.argmax([max_common_part(oligo_prec, S[i]) for i in range(len(S))])

def greedyHeuristic(S, initial_oligo, n, l):

    copyS = copy.deepcopy(S)
    print(copyS)
    solution_l = 0
    solution_c = 0

    solution = [initial_oligo]
    solution_c = l
    solution_l = 1

    while solution_c < n and solution_l < n - l + 1:

        index = choose_next_oligo(solution[-1], copyS, 'greedy')

        solution_c += (l - max_common_part(solution[-1], copyS[index]))
        solution_l += 1
        solution.append(copyS[index])
        copyS = np.delete(copyS, index, axis=0)

    return solution

def getStringSequence(path):
    """
    Returns sequence of letters: A, C, G, T, which represents DNA sequence
    Parameters:
    - path: ordered set of oligonucleotides, which represents solution sequence
    """
    out = ''.join([acid_map[i] for i in path[0]])

    for i in range(1, len(path)):
        commonLen = max_common_part(oligo_prec=path[i - 1], oligo_succ=path[i])
        tail = ''.join([acid_map[i] for i in path[i][commonLen : ]])
        out += tail

    return out

if __name__ == "__main__":

    initial_oligo, S = generateSampleOligo(4, 15)
    solution = greedyHeuristic(S, initial_oligo, 15, 4)
    print(solution)
