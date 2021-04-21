import numpy as np
import random

def max_common_part(oligo_prec, oligo_succ):

    common_len = 0
    temp_oligo = [i for i in np.flip(oligo_prec)]

    for o1, o2 in zip(oligo_succ, np.flip(oligo_prec)):
        if o1 == o2:
            common_len += 1
        else:
            break
    
    return common_len


def greedyHeuristic(oligo, initial_oligo, n, l):

    return None
