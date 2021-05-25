import numpy as np
import random
import copy

from src.constants import acid_map, det_rate, rcl_card
from src.sequenceFactory import generateSampleOligo
# import src.phermone_interface as phermone

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

def choose_init_oligo(S, alg='random'):

    return random.randint(0, len(S) - 1)

def choose_next_oligo(oligo_prec, S, alg='greedy', use_phermone=False, phermone_model=None):
    """
    Return index / key of set S, which corresponds to best oligo
    """ 
    if len(S) == 0:
        return None
    if len(S) == 1:
        for key in S:
            return key


    phermone_values = phermone_model
    if use_phermone == True:
        # utilize phermone model
        # construct restricted candidate list

        # simplest version
        temp = np.zeros((np.size(phermone_values), 2))
        for key in S:
            temp[key][0] = max_common_part(oligo_prec, S[key]) / (len(S[key]) - 1)
            temp[key][1] = key

        temp[:,0] = phermone_values * (temp[:, 0] ** 5)
        temp = np.array(sorted(temp, key=lambda it: it[0]))
        restricted_list = temp[-min(temp.shape[0], rcl_card):]
        if(random.random() < det_rate):
            # return best oligo
            return int(restricted_list[np.argmax(restricted_list[:, 1])][1])

        # roulette-wheel selection
        prob = restricted_list[:,0] / sum(restricted_list[:,0])
        for i in range(1, len(prob)):
            prob[i] += prob[i - 1]
        r = random.random()
        it = 0
        while(prob[it] < r):
            it += 1
        return int(restricted_list[it][1])

    if alg == 'greedy':
        return np.argmax([max_common_part(oligo_prec, S[key]) for key in S])
    elif alg == 'greedy_lag':
        # 
        return np.argmax([max_common_part(oligo_prec, S[i]) + max([max_common_part(S[i], S[j]) for j in S if j != i]) for i in S])

def objective_function(solution):
    """
    Returns signle value -> evaluation of solution.\n
    Parameters:
    - solution: Solution object
    """

    # now its only number of oligo in sequence
    return solution.get_path_len()

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

def roundFloat(floatNumber, decimalPlaces):
    return int(floatNumber * (10 ** decimalPlaces)) / (10 ** decimalPlaces)

def levenshteinDistance(a, b):
    if len(b) == 0:
        return len(a)
    if len(a) == 0:
        return len(b)
    if a[0] == b[0]:
        return levenshteinDistance(a[1:], b[1:])
    return 1 + min(
        levenshteinDistance(a[1:], b),
        levenshteinDistance(a, b[1:]),
        levenshteinDistance(a[1:], b[1:])
    )

if __name__ == "__main__":
    pass
