import numpy as np
import unittest
import math

from src.usefullFunctions import levenshteinDistance

class test_utils(unittest.TestCase):

    def test_levenshtein(self):

        self.assertEqual(levenshteinDistance("kitten", "sitten"), 1)
        self.assertEqual(levenshteinDistance("sitten", "sittin"), 1)
        self.assertEqual(levenshteinDistance("sittin", "sitting"), 1)

if __name__ == "__main__":

    unittest.main()