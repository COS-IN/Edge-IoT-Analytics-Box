import torch
from torch import nn


class DeepNNAvg(nn.Module):
    
    def __init__(self, input_dim=60, output_dim=1, layercount=1, h_dim=1):
        super().__init__()
        for i in range(0,layercount):
            if i == 0:
                layer = nn.Linear( 
                                    input_dim, 
                                    output_dim,
                                    dtype=torch.float64,
                                )
            elif i < layercount - 1: 
                 layer = nn.Linear( 
                                    h_dim, 
                                    h_dim,
                                    dtype=torch.float64,
                                )               
            elif i == layercount - 1: 
                 layer = nn.Linear( 
                                    h_dim, 
                                    output_dim,
                                    dtype=torch.float64,
                                )               
            blayer = nn.BatchNorm1d(num_features=h_dim)
            if i < layercount - 1:
                setattr(self, 'blayer'+str(i), blayer)
            setattr(self, 'layer'+str(i), layer)
        self.activation = nn.ReLU()
        self.softmax = nn.Softmax(dim=1) 
        self.layercount = layercount
    
    def forward( self, x ):
        H = x.T
        act = self.activation
        for i in range(0, self.layercount):
            layer = getattr(self, 'layer'+str(i))
            H = layer( H )
            H = act( H )
            if i < self.layercount -1:
                blayer = getattr(self, 'blayer'+str(i))
                H = blayer( H ) 
        #yp = self.softmax( H )
        return H 

def save_model(model):
    torch.save(model.state_dict(), "model_avg.pt")

def main():
    model = DeepNNAvg(input_dim=60, output_dim=1, layercount=1)
    save_model(model)

if __name__ == "__main__":
    main()


