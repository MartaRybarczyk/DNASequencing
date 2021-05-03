import unittest

from src.solution import Solution, is_valid
from src.constants import dummy_oligo, acid_map
import numpy as np

class test_solution(unittest.TestCase):
    def test_methods(self):

        solution = Solution()

        self.assertEqual(solution.path_len, 0)
        self.assertEqual(solution.path[0][0], dummy_oligo)
        self.assertEqual(len(solution.commons), 0)
        self.assertEqual(len(solution.graph_path), 1)

        oligo_list = [[1,2,2,1], [1,0,0,1]]

        solution.add_oligo(oligo=oligo_list[0], vertex_no=0)

        self.assertEqual(solution.path_len, 4)
        self.assertEqual(solution.commons[0], 0)
        self.assertEqual(len(solution.path), 2)
        self.assertEqual(solution.graph_path[1], 0)

        solution.add_oligo(oligo=oligo_list[1], vertex_no=1)

        self.assertEqual(solution.path_len, 7)
        self.assertEqual(solution.commons[1], 1)
        self.assertEqual(len(solution.path), 3)
        self.assertEqual(solution.graph_path[2], 1)

        solution.pop_back_oligo()

        self.assertEqual(solution.path_len, 4)
        self.assertEqual(solution.commons[0], 0)
        self.assertEqual(len(solution.path), 2)

        self.assertEqual(str(solution), ''.join([acid_map[i] for i in oligo_list[0]]))

    def test_is_valid_solution(self):

        S = {
            0 : [1,2,3],
            1 : [2,3,1],
            2 : [3,1,2]
        }

        solution = Solution()
        solution.add_oligo(S[0], 0)
        solution.add_oligo(S[1], 1)
        solution.add_oligo(S[2], 2)

        self.assertEqual(is_valid(solution, S), True)

        solution.add_oligo(S[0], 0)

        self.assertEqual(is_valid(solution, S), False)

if __name__ == "__main__":

    unittest.main()