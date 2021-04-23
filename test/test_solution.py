import unittest

from src.solution import Solution
from src.constants import dummy_oligo
import numpy as np

class test_solution(unittest.TestCase):
    def test_methods(self):

        solution = Solution(l=4)

        self.assertEqual(solution.path_len, 0)
        self.assertEqual(solution.path[0][0], dummy_oligo)
        self.assertEqual(len(solution.commons), 0)

        print(solution.path)
        oligo_list = [[1,2,2,1], [1,0,0,1]]

        # solution.add_oligo(oligo=oligo_list[0])

        # self.assertEqual(solution.path_len, 4)
        # self.assertEqual(solution.commons[0], 0)
        # self.assertEqual(len(solution.path), 2)

if __name__ == "__main__":

    unittest.main()