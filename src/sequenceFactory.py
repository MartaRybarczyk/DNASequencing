import numpy as np
import random

def generateSampleOligo(l=10, n=500):
    
    if l >= n:
        return np.array([])

    sequence = [random.randint(0, 3) for i in range(n)]
    
    return np.random.permutation(np.array([sequence[i:i + l] for i in range(n - l + 1)]))

if __name__ == "__main__":

    print(generateSampleOligo(3, 6))