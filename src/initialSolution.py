import numpy as np
import random
import copy

def max_common_part(oligo_prec, oligo_succ):

    common_len = 0

    for o1, o2 in zip(oligo_succ, np.flip(oligo_prec)):
        print(o1, o2)
        if o1 == o2:
            common_len += 1
        else:
            break
    
    return common_len

def choose_next_oligo(oligo_prec, S, type='greedy'):
    """
    Return index of set S, which corresponds to best oligo
    """
    for oligo in S:
        print(oligo_prec, np.flip(oligo))
        
    # print([max_common_part(oligo_prec, oligo) for oligo in S])
    return np.argmax([max_common_part(oligo_prec, S[i]) for i in range(len(S))])

def greedyHeuristic(S, initial_oligo, n, l):

    copyS = copy.deepcopy(S)
    solution_l = 0
    solution_c = 0

    solution = [initial_oligo]
    solution_c = l
    solution_l = 1

    while solution_c < n:
        index = choose_next_oligo(solution[-1], copyS, 'greedy')
        solution.append(copyS[index])

        np.delete(copyS, index, axis=0)

    return solution


if __name__ == "__main__":

    