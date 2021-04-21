import unittest
import numpy as np
import sys

sys.path.insert(1, '..')
from src.initialSolution import max_common_part

class initialSolutionTest(unittest.TestCase):
    def test_max_common_part(self):

        max_len = max_common_part(np.array([1,2,3,1]), np.array([1,3,1,2]))
        self.assertEqual(max_len, 2)

        max_len = max_common_part(np.array([1,2]), np.array([1,3,1,2]))
        self.assertEqual(max_len, 0)

        max_len = max_common_part(np.array([1,1,1,1,1,3,1]), np.array([1,3,1,2]))
        self.assertEqual(max_len, 3)


if __name__ == "__main__":

    unittest.main()