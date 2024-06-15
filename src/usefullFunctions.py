import numpy as np
import random
import copy
import os

from src.constants import acid_map, det_rate, rcl_card
from src.sequenceFactory import generateSampleOligo
from src.constants import MAX_OLIGO_LEN, init_det_rate, init_crd, det_rate, kib, kbs, krb, NF, NB, rcl_card, MAX_DURATION, rho
from src import constants
# import src.phermone_interface as phermone

def max_common_part(oligo_prec, oligo_succ):

    n1 = len(oligo_prec)
    n2 = len(oligo_succ)
    
    for i in range(min(n1, n2) - 1, -1, -1):
        if (oligo_prec[n1 - i:] == oligo_succ[:i]) == True:
            return i

    
    return 0

def find_best_subpath(solution, n):
    """
    Returns solution with c(path)  <= n
    In other words, searches for longest (in terms of number of oligo) subpath in a given path
    """
    pass

def choose_init_oligo(S, alg='random', com_matrix=None):

    if alg=='worst_best':
        best_succ_prec = {}

        if com_matrix is not None:
            best_succ_prec = np.zeros((len(S), 3), int)
            for i in range(np.shape(best_succ_prec)[0]):
                best_succ_prec[i][1] = np.max(com_matrix[i])
                best_succ_prec[i][0] = np.max(com_matrix[:, i])
                best_succ_prec[i][2] = i

            best_succ_prec = sorted(best_succ_prec, key=lambda item: -(1000 * -item[0] + item[1]))
            # print(best_succ_prec[:10])

            r = random.random()
            # print(init_det_rate)
            if r < init_det_rate:
                # print('fast',best_succ_prec[0][2])
                return best_succ_prec[0][2]
            else:
                # print('random')
                return best_succ_prec[random.randint(0, init_crd - 1)][2]

        for oligo1 in S:
            best_succ_prec[oligo1] = [-1, -1]
            for oligo2 in S:
                if oligo1 == oligo2:
                    continue
                best_succ_prec[oligo1][0] = max(
                    best_succ_prec[oligo1][0],
                    max_common_part(S[oligo2], S[oligo1])
                )
                best_succ_prec[oligo1][1] = max(
                    best_succ_prec[oligo1][1],
                    max_common_part(S[oligo1], S[oligo2])
                )
        
        key = 0
        min_max = [1e10, -1]
        
        for oligo in S:
            if best_succ_prec[oligo][1] >= min_max[1]:
                if best_succ_prec[oligo][0] < min_max[0]:
                    min_max[0] = best_succ_prec[oligo][0]
                    min_max[1] = best_succ_prec[oligo][1]

                    key = oligo
        print('slow',key)
        return key

    return random.randint(0, len(S) - 1)

def choose_next_oligo( solution_l, range_of_appearance, oligo_prec, S, alg='greedy', use_phermone=False, phermone_model=None, commons_matrix=None, index_prec=None):
    """
    Return index / key of set S, which corresponds to best oligo
    """ 

    prec_com = False
    if commons_matrix is not None and type(commons_matrix) == np.ndarray and index_prec is not None:
        prec_com = True

    phermone_values = phermone_model
    if use_phermone == True:
        # utilize phermone model
        # construct restricted candidate list

        # simplest version
        temp = np.zeros((np.size(phermone_values), 2)) - np.inf
        for key in S:
            oligo_str = "".join([acid_map[i] for i in S[key]])
            if(range_of_appearance[oligo_str][0] <= solution_l and range_of_appearance[oligo_str][1] >= solution_l):
                if prec_com:
                    temp[key][0] = commons_matrix[index_prec][key] / (len(S[key]) - 1)
                else:
                    temp[key][0] = max_common_part(oligo_prec, S[key]) / (len(S[key]) - 1)
                temp[key][1] = key 
            else:
                temp[key][0] = 0
                temp[key][1] = key 

        temp[:,0] = phermone_values * (temp[:, 0] ** 5)

        temp = np.delete(temp, np.where(temp[:,0] == -np.inf), axis=0)
        temp = np.array(sorted(temp, key=lambda it: it[0]))

        restricted_list = temp[-min(temp.shape[0], rcl_card):]
        # print("restricted list:")
        
        if(random.random() < det_rate):
            # return best oligo
            return int(restricted_list[np.argmax(restricted_list[:, 0])][1])
        
        # some safety
        if np.sum(restricted_list[:, 0]) < 0.000000001:
            return int(restricted_list[0][1])

        # roulette-wheel selection
        prob = restricted_list[:,0] / np.sum(restricted_list[:,0])
        for i in range(1, len(prob)):
            prob[i] += prob[i - 1]
        r = random.random()
        it = 0
        while(prob[it] < r):
            it += 1
        return int(restricted_list[it][1])

    if alg == 'greedy':
        m = -1
        key = 0
        for oligo in S:
            if prec_com:
                com = commons_matrix[index_prec][oligo]
            else:
                com = max_common_part(oligo_prec, S[oligo])
            if com > m:
                key = oligo
                m = com
        return key
    # elif alg == 'greedy_lag':
    #     tmp = None
    #     if prec_com == True:
    #         # print('A')
    #         # tmp = [[commons_matrix[index_prec][i] + max([commons_matrix[i][j] for j in S if j != i]), i] for i in S]
    #         tmp = commons_matrix[index_prec] + np.max(commons_matrix, axis=1)
    #         for key in S:
    #             tmp[key] += MAX_OLIGO_LEN
    #         return np.argmax(tmp)
    #     else:
    #         tmp = [[max_common_part(oligo_prec, S[i]) + max([max_common_part(S[i], S[j]) for j in S if j != i]), i] for i in S]
    #     return sorted(tmp, key=lambda it: it[0])[-1][1]

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

    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    
    n = len(a)
    m = len(b)

    d = np.zeros((n + 1, m + 1), dtype=int)
    
    for i in range(n + 1):
        d[i][0] = i
    for i in range(m + 1):
        d[0][i] = i

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 1
            if b[j - 1] == a[i - 1]:
                cost = 0
            min1 = d[i - 1][j] + 1
            min2 = d[i][j - 1] + 1
            min3 = d[i - 1][j -1] + cost
            d[i][j] = min([min1, min2, min3])

    return d[n][m]

def set_global_parameters(_max_duration=10, _crd_list=3, _nf=6, _nb=0,
        _kib=0.3, _krb=0.3, _kbs=0.3, _det_rate=0.95, _init_det_rate=0.25, _init_crd=20
    ):
    global MAX_DURATION, rcl_card, NF, NB, kib, kbs, krb, det_rate, init_det_rate, init_crd

    MAX_DURATION = _max_duration
    rcl_card = _crd_list
    NF = _nf
    NB = _nb
    kib = _kib
    krb = _krb
    kbs = _kbs
    det_rate = _det_rate
    init_det_rate = _init_det_rate
    # constants.set_init_det_rate(_init_det_rate)
    init_crd = _init_crd

def get_file_list(dna_files_paths, seq_files_paths, limit=None, shuff=False):

    files = []

    for dna_path, seq_path in zip(dna_files_paths, seq_files_paths):
        dna_files = os.listdir(dna_path)
        seq_files = os.listdir(seq_path)

        dna_files.sort()
        seq_files.sort()

        if len(dna_files) != len(seq_files):
            print('missing file')
            return None
        
        for i in range(len(dna_files)):
            files.append(
                (
                    dna_path + '/' + dna_files[i],
                    seq_path + '/' + seq_files[i]
                )
            )
    
    if shuff == True:
        random.shuffle(files)

    if limit is not None:
        files = files[: min(len(files), limit)]



    return files

if __name__ == "__main__":
    
    work_path = os.path.dirname(os.path.realpath(__file__))

    dna_files_paths = [work_path + '/../testFiles/benchmark/error_rate_5/stand5/5']
    seq_files_paths = [work_path + '/../testFiles/benchmark/error_rate_5/sequence']

    print(get_file_list(dna_files_paths, seq_files_paths, limit=2))