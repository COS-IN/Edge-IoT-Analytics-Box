import pandas as pd
import numpy as np 
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data

from DataAnalyzer import DataAnalyzer
from HyperparameterVariables import HyperparameterVariables
from DataVariables import DataVariables

import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tools.sm_exceptions import ValueWarning
from arnn import A_RNN
from arnn import TemporalMapper
from arnn import RNNCell

class DataVariables:

    def __init__(self):
        self.n_predictor = 1
        self.n_response = 1
        self.temporal_mapping = [60, 10]

class HyperparameterVariables:

    def __init__(self):
        self.hidden_size = 16
        self.rnn_kwargs = {
            "n_rnn_layers": 1,
            "rnn_layer": "RNN",
            "rnn_kwargs": {},
            "dropout": 0.0,
        }
        self.mapper_kwargs = {
            "temporal_mapper": "last",
            "temporal_mapper_kwargs": {},
        }
        self.kwargs = {}


class DataAnalyzerARNNPredict(DataAnalyzer):

    """
        Analyzes given window of data to generate a new window 
    """
    def __init__(self):
        data_var = DataVariables()
        hyp_var = HyperparameterVariables()
        self.model = A_RNN(
        data_var.n_predictor,
        data_var.n_response,
        data_var.temporal_mapping[0],
        hyp_var.hidden_size,
        hyp_var.rnn_kwargs,
        hyp_var.mapper_kwargs,
        hyp_var.kwargs
        )
        #checkpoint = torch.load('./TruePowerW.pth',map_location='cpu')
        checkpoint = torch.load('./ApparentPowerVA.pth',map_location='cpu')
        #checkpoint = torch.load('./PowerFactor.pth',map_location='cpu')
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to('cuda')
        #torch.load_state_dict(torch.load('TruePowerW.pth')) 
        
        
    def create_dataset(self, dataset, lookback):
        X, y = [], []
        for i in range(len(dataset)-lookback):
            feature = dataset[i:i+lookback]
            #target = dataset[i+1:i+lookback+1]
            X.append(feature)
            #y.append(target)
        return torch.tensor(X),i

    def analyze(self, df):
        # print(df)
        data_var = DataVariables()
        tagi = '_time' 
        Ti, To = data_var.temporal_mapping
        test = np.array(df[df.columns[0]].values.astype('float32'))  
        #print(test)
        lookback = 60
        X_test,i = self.create_dataset(test, lookback=lookback)
        # print('The shape of X_test and Y_test is' , X_test.shape, y_test.shape)
        #print("xtest=",X_test)
        for x in range(1):
            X_temp = X_test[x]
            X_temp = X_temp.reshape(1,X_test.shape[1],1,1)
            #print(X_temp.shape)
            X_temp = X_temp.to('cuda')
            y_temp = self.model(x=X_temp, n_temporal_out=To)["yhat"]
            y_temp = y_temp.to('cpu')
            y_temp = y_temp.detach().numpy()
            #y_temp = self.model(X_temp)


            #y_temp = y_temp[:, -1]
            y_temp = y_temp.reshape(10)

            #print("y_pred=",y_temp)
            ##dfm = y_pred
            dfm = y_temp
            dfm = pd.DataFrame(dfm)
            dfm[tagi] = df.iloc[-1].name 

            # print(dfm)

            dfm = dfm.rename(columns={0:df.columns[0]})
            dfm = dfm.iloc[0:2,:]
           
            return dfm
            #print('******************************',X_test.shape)
            #print(i)

        #y_pred = self.model(X_test)
        #y_pred = y_pred.detach().numpy()
        #y_temp = y_temp.detach().numpy()
        # print(dfm)
        # print('outside loop')
        # exit(0)
        return dfm

