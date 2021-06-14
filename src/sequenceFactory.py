import numpy as np
import random
import time
from src.constants import acid_rev_map, acid_map
import os

random.seed(time.time())

def generateSampleOligo(l=10, n=500, initial_oligo=True, last_oligo=False):
    """
    Simple DNA sequence generator.\n
    - n: size of the output sequence\n
    - l: length of the oligonucleotide
    - initial_oligo: boolean parameter, if true function returns also index to first oligo in set S
    - back_oligo: same as initial_oligo, but returns index to last oligo in set S

    Return pair:
    - set of oligo (shuffled)
    """
    init_oligo_index = None
    last_oligo_index = None

    if l >= n:
        return [], []

    sequence = [random.randint(0, 3) for i in range(n)]

    begin = int(initial_oligo)
    end = 1 - int(last_oligo)

    temp = [sequence[i:i + l] for i in range(begin, n - l + end)]
    random.shuffle(temp)

    if initial_oligo==True:
        temp.insert(0, sequence[0:l])
        init_oligo_index = 0
    if last_oligo==True:
        temp.insert(1, sequence[n - l + 1: ])
        last_oligo_index = 1

    # return as dict to uniquely identify oligos when operating on set
    dic = {}
    for i in range(len(temp)):
        dic[i] = temp[i]

    return init_oligo_index, last_oligo_index, dic

def get_data_from_file(file):

    """
    ## Parse data from file
    First line of the file represents length of the DNA sequence,
    next line is the number K of oligo, which are in the next K lines as string of letters A,C,T,G each.
    ## Return:
    - n: target lenth of the sequence
    - l: length of one oligo
    - S: dictionary of oligo
    """

    S = {}
    n = 0
    l = 0

    with open(file, 'r') as f:
        
        n = int(f.readline())
        l = n - int(f.readline()) + 1

        it = 0

        oligo = f.readlines()

        for o in oligo:
            S[it] = [acid_rev_map[letter] for letter in o.strip()]
            it += 1
        
    return n, l, S

def generateData(n, l, pos_error, neg_error, initial_oligo=True):

    pos_error /= 100
    neg_error /= 100

    init_oligo_index = None

    if l >= n:
        return [], []

    sequence = [random.randint(0, 3) for i in range(n)]

    begin = int(initial_oligo)

    temp = [sequence[i:i + l] for i in range(begin, n - l)]
    random.shuffle(temp)

    if initial_oligo==True:
        temp.insert(0, sequence[0:l])
        init_oligo_index = 0

    pos_error_oligo_no = int(len(temp) * pos_error)
    neg_error_oligo_no = int(len(temp) * neg_error)

    for i in range(neg_error_oligo_no):
        
        r = random.randint(begin, len(temp) - 1)
        temp.pop(r)

    for i in range(pos_error_oligo_no):
        
        if random.random() < 0.5:
            r = random.randint(begin, len(temp) - 1)
            temp.insert(r, [random.randint(0, 3) for i in range(l)])
        else:
            tmp = [0, 1, 2, 3]
            index = random.randint(begin, len(temp) - 1)
            #number of nucleotides to be modified (mutation)
            nucl_no = max(int(l * 0.50), 1)
            for i in range(nucl_no):
                pos = random.randint(0, l - 1)
                mem = tmp.pop(tmp.index(temp[index][pos]))
                new = random.randint(0, 2)
                temp[index][pos] = new
                tmp.append(mem)

    target_seq = ''.join([acid_map[key] for key in sequence])

    data_str = ''
    data_str += str(n) + '\n' + str(len(temp)) + '\n'
    for oligo in temp:
        data_str += ''.join([acid_map[key] for key in oligo]) + '\n'

    return target_seq, data_str

def generateWholeSet(basePath, oligo_len=10, error_rate_list=[5, 10, 20], dna_lengths=[50, 100, 200, 400, 600], in_group=25):

    for error_rate in error_rate_list:
        os.mkdir(basePath + '/error_rate_' + str(error_rate))
        current_path = basePath + '/error_rate_' + str(error_rate)
        os.mkdir(current_path + '/sequence')
        os.mkdir(current_path + '/oligo')

        for dna_length in dna_lengths:
            for i in range(in_group):
                pos_error = random.randint(0, error_rate)
                neg_error = error_rate - pos_error
                target_seq, data_str = generateData(dna_length, oligo_len, pos_error, neg_error, initial_oligo=True)

                with open(current_path + '/sequence/' + str(dna_length) + '_' + str(i + 1).rjust(2, '0') + '.seq', 'w') as f:
                    f.write(target_seq)
                
                with open(current_path + '/oligo/' + str(dna_length) + '_' + str(i + 1).rjust(2, '0'), 'w') as f:
                    f.write(data_str)


if __name__ == "__main__":

    work_path = os.path.dirname(os.path.realpath(__file__))

    generateWholeSet(work_path + '/../testFiles/our_set')

    # t, d = generateData(100, 8, 0.3, 0.4)