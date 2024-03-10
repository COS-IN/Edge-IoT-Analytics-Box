import torch
from torch import nn
from DataAnalyzerARIMA import DataAnalyzerARIMA

class DeepNNArima(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.daa = DataAnalyzerARIMA()
   
    def forward( self, x ):
        xp = self.daa.analyze( x )
        return xp 

def save_model(model):
    torch.save(model.state_dict(), "model_arima.pt")

def main():
    model = DeepNNArima()
    save_model(model)

if __name__ == "__main__":
    main()


