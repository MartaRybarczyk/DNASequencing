import unittest
import numpy as np
import sys

from src.sequenceFactory import generateSampleOligo

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

if __name__ == "__main__":

    unittest.main()