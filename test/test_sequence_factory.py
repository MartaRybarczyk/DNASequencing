import unittest
import numpy as np
import sys

from src.sequenceFactory import generateSampleOligo

class sequenceFactoryTest(unittest.TestCase):

    def test_generateSampleOligo(self):

        initial, oligo = generateSampleOligo(10, 100)
        self.assertEqual(np.shape(oligo), (90, 10))

        initial, oligo = generateSampleOligo()

        self.assertEqual(np.shape(oligo), (490, 10))
        
        initial, oligo = generateSampleOligo(10, 1)

        self.assertEqual(np.shape(oligo), (0,))

if __name__ == "__main__":

    unittest.main()