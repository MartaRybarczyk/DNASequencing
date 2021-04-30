import numpy as np
import unittest
import math

from src.metaheuristic import compute_convergence_factor

class test_ACO_metaheuristic(unittest.TestCase):

    def test_compute_convergence_factor(self):

        T = np.ones([3,3])
        T[1][1] = 3
        T[0][0] = 0

        self.assertEqual(40 / 27 - 1, compute_convergence_factor(T))


if __name__ == "__main__":

    unittest.main()