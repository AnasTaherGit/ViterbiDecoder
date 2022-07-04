import unittest
# import LDACS.viterbi as viterbi
################################
import src.viterbi as viterbi
################################
from bitarray import bitarray


class TestViterbi(unittest.TestCase):

    def test_HammingMetric(self):
        v=viterbi.ViterbiDecoder(Generators=(0x79,0x5B),MemoryDepth=7)
        testArray1=bitarray('10110')
        testArray2=bitarray('11110')
        self.assertEqual(v.HammingMetric(testArray1,testArray2),1)

    def test_ParityGenerator(self):
        v=viterbi.ViterbiDecoder(Generators=(0x07,0x06),MemoryDepth=3)
        Parity=v.initParityFunctions()
        # self.assertEqual(Parity[0](1,2),0)
        # self.assertEqual(Parity[0](0,2),1)
        # self.assertEqual(Parity[1](1,2),0)
        # self.assertEqual(Parity[1](1,1),1)

    def test_decode(self):
        ReceivedMessage=bitarray('1101100100010111')
        v=viterbi.ViterbiDecoder(Generators=(0x07,0x05),MemoryDepth=3)
        ExpectedDecodedMessage=bitarray('11101100')
        DecodedMessage=v.decode(ReceivedMessage)
        self.assertEqual(DecodedMessage, ExpectedDecodedMessage)