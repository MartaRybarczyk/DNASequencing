import unittest
import numpy as np
import sys
import os
from pathlib import Path

# sys.path.insert(1, Path(__file__).resolve().parent.parent)
sys.path.insert(1, '..')
from src.initialSolution import max_common_part, choose_next_oligo

class initialSolutionTest(unittest.TestCase):
    def test_max_common_part(self):

        max_len = max_common_part(np.array([1,2,3,1]), np.array([1,3,1,2]))
        self.assertEqual(max_len, 1)

        max_len = max_common_part(np.array([1,2]), np.array([1,3,1,2]))
        self.assertEqual(max_len, 0)

        max_len = max_common_part(np.array([1,1,1,1,1,3,1]), np.array([1,3,1,2]))
        self.assertEqual(max_len, 3)

    def test_choose_next_oligo_greedy(self):

        S = np.array([
            [1,2,3],
            [1,2,3],
            [0,3,2],
            [2,3,3]
        ])

        oligo_prec = np.array([2,2,3])

        index = choose_next_oligo(oligo_prec, S, type='greedy')
        self.assertEqual(index, 3)

        oligo_prec = np.array([2,1,3])

        index = choose_next_oligo(oligo_prec, S, type='greedy')
        self.assertEqual(index, 0)

if __name__ == "__main__":

    unittest.main()