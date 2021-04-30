import numpy as np
import random

def generateSampleOligo(l=10, n=500, initial_oligo=True, last_oligo=False):
    """
    Simple DNA sequence generator.\n
    - n: size of the output sequence\n
    - l: length of the oligonucleotide
    - initial_oligo: boolean parameter, if true function returns also index to first oligo in set S
    - back_oligo: same as initial_oligo, but returns index to last oligo in set S

    Returns pair:
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

if __name__ == "__main__":

    print(generateSampleOligo(3, 6))