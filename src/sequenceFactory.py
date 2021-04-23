import numpy as np
import random

def generateSampleOligo(l=10, n=500):
    """
    Simple DNA sequence generator.\n
    - n: size of the output sequence\n
    - l: length of the oligonucleotide

    Returns pair:
    - initial oligonucleotide
    - set of remaining oligo (shuffled)
    """
    if l >= n:
        return np.array([]), np.array([])

    sequence = [random.randint(0, 3) for i in range(n)]
    
    return sequence[0:l], np.random.permutation(np.array([sequence[i:i + l] for i in range(1, n - l + 1)]))

if __name__ == "__main__":

    print(generateSampleOligo(3, 6))