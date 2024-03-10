import pandas as pd
import numpy as np 

from DataAnalyzer import DataAnalyzer

from statsmodels.tsa.arima.model import ARIMA

import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tools.sm_exceptions import ValueWarning

class DataAnalyzerARIMA(DataAnalyzer):

    """
        Analyzes given window of data to generate a new window 
    """
    def __init__(self):
        self.ccount = 0
        self.predict_win = 30 # seconds 
    
    def arima_forecast(self, dfcc):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConvergenceWarning)
            warnings.simplefilter("ignore", UserWarning)
            warnings.simplefilter("ignore", ValueWarning)

            #model = ARIMA(dfcc, order=(2,1,0), missing='drop')
            #model = ARIMA(dfcc, order=(4,2,1), missing='drop')

            # simple exp smoothing
            model = ARIMA(dfcc, order=(0,1,1), missing='drop')

            model_fit = model.fit()
            output = model_fit.forecast( self.predict_win )

            freq = np.diff(dfcc.index).mean().total_seconds()
        return output, freq

    def analyze(self, df):
        tagi = '_time' 
        # df = df.set_index(tagi)

        dfm = df.mean()
        dfm = pd.DataFrame(dfm).T
        dfm[tagi] = df.iloc[-1].name

        output, freq = self.arima_forecast( df )
        tprev = df.index[-1]
        tnew = tprev + pd.Timedelta(seconds=freq)
        
        # reset index of output 
        output = output.reset_index()
        oa = output[['predicted_mean']]

        ts = [ tprev + pd.Timedelta(seconds=t) for t in oa.index ]
        oa.index = ts 
        oa = oa[['predicted_mean']]

        oa = oa.reset_index()
        cols = [ c for c in dfm.columns if c != '_time' ]
        dfm = oa.rename( columns={'index':'_time', 'predicted_mean': cols[0] } )
        
        if False: 
            # print(dfm)
            # Duplicating same point because influxdb write api requires at least two points 
            # one points leads it iterate floats as strings! 
            # TODO:  <10-10-23, abrehman> # find a proper fix  
            dfm = pd.concat([dfm,dfm])
            dfm = dfm.reset_index()
            t = dfm.loc[1,'_time']
            dfm.loc[1,'_time'] =  t 
            dfm = dfm.drop(columns=['index'])

        return dfm



