from src.constants import acid_map, acid_rev_map
from src.sequenceFactory import get_data_from_file
from src.usefullFunctions import max_common_part

import numpy as np
import os

def find_error_oligo(S,l, origin_seq):

    seq = []
    if type(origin_seq) == str:
        seq = origin_seq
        # print(seq)
    elif type(origin_seq) == list:
        seq = ''.join([acid_map[key] for key in origin_seq])
        # print(seq)

    #the keys are oligo and values are numbers of occurences in DNA strand
    count_dict = {}

    for index in S:
        tmp = ''
        if type(S[index]) == list:
            tmp = ''.join([acid_map[key] for key in S[index]])
        elif type(S[index]) == str:
            tmp = S[index]
        
        if tmp in count_dict:
            count_dict[tmp] += 1
        else:
            count_dict[tmp] = 1

    err_list = []

    for i in range(len(seq) - l + 1):
        if seq[i:i + l] in count_dict:
            count_dict[seq[i: i + l]] -= 1
            if count_dict[seq[i : i + l]] < 0:
                err_list.append(seq[i : i + l])
        else:
            err_list.append(seq[i : i + l])

    return err_list

if __name__=="__main__":
    
    work_path = os.path.dirname(os.path.realpath(__file__))
    absolute_benchmark_path = os.path.dirname(os.path.realpath(__file__)) + '/../testFiles/benchmark'

    e_rate = '5'
    file = '200_01'
    file_sequence = file + '.seq'
    

    relative_path_oligo = '/error_rate_{}/stand{}/{}'.format(e_rate, e_rate, e_rate)
    relative_path_sequence = '/error_rate_{}/sequence'.format(e_rate)
    
    with open(absolute_benchmark_path + relative_path_sequence + '/' + file_sequence, 'r') as f:
        origin_seq = f.read()

    n, l, S = get_data_from_file(absolute_benchmark_path + relative_path_oligo + '/' + file)

    err_list = find_error_oligo(S, l, origin_seq)

    com_matrix = np.zeros((len(S), len(S)), dtype=int)

    for i in range(com_matrix.shape[0]):
        for j in range(com_matrix.shape[1]):
            com_matrix[i][j] = max_common_part(S[i], S[j])

    test_vec = [(i, np.sum(com_matrix[i]) + np.sum(com_matrix[:,i])) for i in S]

    test_vec = sorted(test_vec, key=lambda it: it[1])

    for i in range(20):
        print(''.join([acid_map[a] for a in S[test_vec[i][0]]]))


    print('===========================')
    print(err_list)