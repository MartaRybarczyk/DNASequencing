import unittest
import numpy as np
import sys
import os

from src.sequenceFactory import generateSampleOligo
from src.sequenceFactory import get_data_from_file

class sequenceFactoryTest(unittest.TestCase):

    def test_generateSampleOligo(self):

        initial, last, oligos = generateSampleOligo(10, 100)
        self.assertEqual(initial, 0)
        self.assertEqual(last, None)
        self.assertEqual(len(oligos), 91)

        initial, last, oligos = generateSampleOligo(last_oligo=True)

        self.assertEqual(initial, 0)
        self.assertEqual(last, 1)
        self.assertEqual(len(oligos), 491)

    def test_data_from_file(self):

        work_path = os.path.dirname(os.path.realpath(__file__))
        file = '/../testFiles/benchmark/error_rate_5/stand5/5/200_01'

        n, l, S = get_data_from_file(work_path + file)

        self.assertEqual(n, 200)
        self.assertEqual(l, 10)
        self.assertEqual(len(S), 191)

if __name__ == "__main__":

    unittest.main()