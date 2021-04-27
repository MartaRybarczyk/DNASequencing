import numpy as np
import random
import copy

from src.constants import acid_map
from src.sequenceFactory import generateSampleOligo

def max_common_part(oligo_prec, oligo_succ):

    n1 = len(oligo_prec)
    n2 = len(oligo_succ)
    
    for i in range(min(n1, n2), -1, -1):
        if (oligo_prec[n1 - i:] == oligo_succ[:i]) == True:
            return i

    
    return 0

def find_best_subpath(path, n):
    """
    Returns solution with c(path)  <= n
    In other words, searches for longest (in terms of number of oligo) subpath in a given path
    """
    #to do
    pass

def choose_next_oligo(oligo_prec, S, alg='greedy', use_phermone=False, phermone_model=None):
    """
    Return index of set S, which corresponds to best oligo
    """ 

    phermone_matrix, last_oligo_index, bitmap = phermone_model
    if use_phermone == True and phermone_matrix != None and bitmap != None:
        # utilize phermone model
        # construct restricted candidate list
        # S_restricted = sorted(S, )
        pass

    if alg == 'greedy':
        return np.argmax([max_common_part(oligo_prec, S[i]) for i in range(len(S))])
    elif alg == 'greedy_lag':
        # 
        return np.argmax([max_common_part(oligo_prec, S[i]) + max([max_common_part(S[i], S[j]) for j in range(len(S)) if j != i]) for i in range(len(S))])

def objective_function(solution):
    """
    Returns signle value -> evaluation of solution.\n
    Parameters:
    - solution: Solution object
    """

    # now its only length of the path
    return len(solution.path)

def getStringSequence(path):
    """
    Returns sequence of letters: A, C, G, T, which represents DNA sequence
    Parameters:
    - path: ordered set of oligonucleotides, solution path
    """
    out = ''.join([acid_map[i] for i in path[0]])

    for i in range(1, len(path)):
        commonLen = max_common_part(oligo_prec=path[i - 1], oligo_succ=path[i])
        tail = ''.join([acid_map[i] for i in path[i][commonLen : ]])
        out += tail

    return out

if __name__ == "__main__":
    pass
