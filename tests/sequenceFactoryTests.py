import unittest
import numpy as np
import sys

sys.path.insert(1, '..')
from src.sequenceFactory import generateSampleOligo

class sequenceFactoryTest(unittest.TestCase):

    def test_generateSampleOligo(self):

        oligo = generateSampleOligo(10, 100)
        self.assertEqual(np.shape(oligo), (91, 10))

        oligo = generateSampleOligo()

        self.assertEqual(np.shape(oligo), (491, 10))
        
        oligo = generateSampleOligo(10, 1)

        self.assertEqual(np.shape(oligo), (0,))

if __name__ == "__main__":

    unittest.main()