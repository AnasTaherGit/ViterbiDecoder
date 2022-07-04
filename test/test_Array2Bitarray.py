import unittest
import numpy as np
from bitarray import bitarray
###############################
from src.viterbi import Array2Bitarray
##############################


class TestArray2Bitarray(unittest.TestCase):
    def test_Array2Bitarray(self):
        signal=np.array([1,0,0,1,0,1,1,1,0,0,1],dtype=np.uint8)
        expectedResult=bitarray('10010111001')
        self.assertEqual(Array2Bitarray(signal),expectedResult)