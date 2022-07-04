import bitarray
import bitarray.util
import numpy as np
from time import time
# from numba import jit
# 171 OCT == 0x79 HEX
# 133 OCT == 0x5B HEX

class ViterbiDecoder():

    def __init__(self,Generators:tuple,MemoryDepth:int)->None:
        self.Generators=Generators
        self.MemoryDepth=MemoryDepth
        self.NbrOfState=2**(MemoryDepth-1)
        self.Parity=self.initParityFunctions()

    def decode(self,ParityBitsVector:bitarray.bitarray)->bitarray.bitarray:
        print(type(ParityBitsVector))
        if type(ParityBitsVector) is not bitarray.bitarray:
            raise TypeError("Only Bitarray supported. Please use Array2Bitarray method to convert a numpy array to Bitarray")
        n=len(ParityBitsVector)//len(self.Generators)
        PathMetric=np.ones((self.NbrOfState,n+1))*np.inf
        PredecessorsTable=np.ones((self.NbrOfState,n+1),dtype=np.int64)*-1
        PathMetric[0,0]=0
        for k in range(1,n+1):
            for s in range(self.NbrOfState):
                self.ComputePathMetric(s,PathMetric,k,ParityBitsVector,PredecessorsTable)
        print(PathMetric[0,-1])
        return self.traceback(PathMetric,PredecessorsTable)

    def ComputePathMetric(self,State,PathMetric,k,ReceivedParityBits,PredecessorsTable)-> None:
        # t=time()
        RPB=ReceivedParityBits[len(self.Generators)*(k-1):len(self.Generators)*k]
        Predecessors=((2*State)%self.NbrOfState,(2*State+1)%self.NbrOfState)
        PM=[-1]*2
        PM[0]=self.ComputeBranchMetric(StateX=Predecessors[0],
                                    StateY=State,
                                    ReceivedParityBits=RPB
                                    )+PathMetric[Predecessors[0],k-1]
        PM[1]=self.ComputeBranchMetric(StateX=Predecessors[1],
                                    StateY=State,
                                    ReceivedParityBits=RPB
                                    )+PathMetric[Predecessors[1],k-1]
        i=np.argmin(PM)
        PredecessorsTable[State,k]=Predecessors[i]
        PathMetric[State,k]=PM[i]
        # print("Branch metric exec time",time()-t)
        

    def ComputeBranchMetric(self,StateX: int, StateY: int, ReceivedParityBits: bitarray.bitarray)-> int:
        X=StateY//2**(self.MemoryDepth-2)
        ExpectedParityBits=bitarray.bitarray([self.ComputeParity(0,X,StateX),self.ComputeParity(1,X,StateX)])

        return self.HammingMetric(ExpectedParityBits,ReceivedParityBits)

    def HammingMetric(self,X: bitarray.bitarray,Y: bitarray.bitarray)-> int:

        return bitarray.util.count_xor(X, Y)

    def traceback(self,PathMetric: np.ndarray,PredecessorsTable: np.ndarray)-> bitarray.bitarray:
        # t=time()
        message=[]
        n=PathMetric.shape[1]
        s=0
        for k in range(n-1):
           message.append(s>>(self.MemoryDepth-2))
           s=PredecessorsTable[s,n-k-1]
        message.reverse()
        # print('traceback time',time()-t)
        return bitarray.bitarray(message)

    def initParityFunctions(self):
        ParityFunctionArray=[]
        for e in self.Generators:
            ComputeParity=self.ParityGenerator(e)
            ParityFunctionArray.append(ComputeParity)

        return ParityFunctionArray
    def ParityGenerator(self,e: int):
        var=self.BinaryConversion(e,self.MemoryDepth)
        
        return var  

    def ComputeParity(self,ParityBitNumber,X,State):
            var=self.Parity[ParityBitNumber]
            S=self.BinaryConversion(State,self.MemoryDepth-1)
            P=(var[0]*X+np.sum(var[1:]*S))%2           
            return P
    def BinaryConversion(self,e: int,nbrBits: int)->np.ndarray:
        return np.unpackbits(np.array([e],dtype=np.uint8))[-nbrBits:]


def Array2Bitarray(vector:np.ndarray):
    bitvector=bitarray.bitarray()
    vector_=vector.tobytes()
    bitvector.pack(vector_)

    return bitvector

def Bitarray2Array(bitvector:bitarray.bitarray)->np.ndarray:
    vectorBytes=bitvector.unpack()
    vector=np.frombuffer(vectorBytes,dtype=np.uint8).copy()
    return vector