from torch import nn
from DataAnalyzerARNNPredict import DataAnalyzerARNNPredict
import fire
import pandas as pd 
import numpy as np 

class Model(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.daa = DataAnalyzerARNNPredict()
   
    def forward( self, x ):
        xp = self.daa.analyze( x )
        return xp 

def main( ):
    m = Model()
    
    # generate mat of 3x3 using pd
    data = pd.DataFrame( np.random.rand( 63, 3 ) )  
    r = m.forward( data )
    # print( data )
    print( r )


if __name__ == "__main__":
    fire.Fire(main)

