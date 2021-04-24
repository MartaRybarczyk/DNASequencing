import unittest
import numpy as np
import sys
import os
from pathlib import Path

from src.usefullFunctions import max_common_part, choose_next_oligo, getStringSequence
from src.constants import acid_map

class initialSolutionTest(unittest.TestCase):
    def test_max_common_part(self):

        max_len = max_common_part([1,2,3,1], [1,3,1,2])
        self.assertEqual(max_len, 1)

        max_len = max_common_part([1,2], [1,3,1,2])
        self.assertEqual(max_len, 0)

        max_len = max_common_part([1,1,1,1,1,3,1], [1,3,1,2])
        self.assertEqual(max_len, 3)

    def test_choose_next_oligo_greedy(self):

        S = [
            [1,2,3],
            [1,2,3],
            [0,3,2],
            [2,3,3]
        ]

        oligo_prec = [2,2,3]

        index = choose_next_oligo(oligo_prec, S, alg='greedy')
        self.assertEqual(index, 3)

        oligo_prec = [2,1,3]

        index = choose_next_oligo(oligo_prec, S, alg='greedy')
        self.assertEqual(index, 0)

    def test_choose_next_oligo_greedy_lag(self):

        S = [
            [1,2,0],
            [1,2,3],
            [0,3,2],
            [2,3,3]
        ]

        oligo_prec = [1,1,2]

        index = choose_next_oligo(oligo_prec, S, alg='greedy_lag')
        self.assertEqual(index, 1)

    def test_get_string_sequence(self):

        path = [
            [1,2,3,0],
            [2,3,0,1],
            [0,1,1,1]
        ]

        score = ''.join(acid_map[i] for i in [1,2,3,0, 1,1,1])

        self.assertEqual(score, getStringSequence(path))

if __name__ == "__main__":

    unittest.main()