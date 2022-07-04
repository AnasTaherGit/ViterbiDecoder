import unittest
import numpy as np
from bitarray import bitarray
###############################
from src.viterbi import Bitarray2Array
##############################


class TestArray2Bitarray(unittest.TestCase):
    def test_Array2Bitarray(self):
        signal=bitarray('10010111001')
        np.testing.assert_equal(Bitarray2Array(signal),np.array([1,0,0,1,0,1,1,1,0,0,1]))