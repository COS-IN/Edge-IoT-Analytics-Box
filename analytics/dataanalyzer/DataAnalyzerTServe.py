import pandas as pd
import requests
import pickle 
import base64
import binascii

from dataanalyzer.DataAnalyzer import DataAnalyzer

class DataAnalyzerTServe(DataAnalyzer):

    """
        Analyzes given window of data to generate a new window 
    """

    def __init__(self, server_ip="localhost", port="8080", timeout=120, model_name='arnn_truepower'):
        self.server_ip = server_ip
        self.port = port
        self.timeout = timeout
        self.model_name = model_name
        self.hist_dict = {}
        self.hist_limit = 10*60 # seconds 
    
    def gather_hist(self, measur, cur_win ):
        hist_dict = self.hist_dict
        if measur not in hist_dict:
            hist_dict[measur] = cur_win
            dfcc = cur_win
        else:
            df = hist_dict[measur]
            dfc = cur_win
            dfcc = pd.concat([df,dfc])
            dfcc = dfcc.reset_index()
            dfcc = dfcc.drop_duplicates(subset='_time')
            dfcc = dfcc.set_index('_time')
            dfcc = dfcc[measur]
            hist_limit = self.hist_limit 
            n = len(dfcc)
            if n > hist_limit:
                extra = n - hist_limit
                dfcc = dfcc.iloc[extra:]
            hist_dict[measur] = dfcc
        return dfcc

    def request( self, model_name, data):
        protocol = "http"
        host = self.server_ip
        port = self.port
        timeout = self.timeout

        url = f"{protocol}://{host}:{port}/predictions/{model_name}"
        response = requests.post(url, data=data, timeout=timeout)
        return response

    def df_to_bytes(self, df): 
        pickled = pickle.dumps(df)
        pickled_b64 = base64.b64encode(pickled)
        return pickled_b64

    def str_to_bytes(self, data):
        return data.encode()
    def bytes_to_df(self, data): 
        ss_df = pickle.loads(base64.b64decode(data))
        return ss_df 

    def analyze(self, df):
        for measur in df.columns:
            cur_win = df[measur]
            df = self.gather_hist( measur, cur_win )
            df = pd.DataFrame(df)
            data = self.df_to_bytes( df )
            r = self.request( self.model_name, data )
            try: 
                rdf = self.bytes_to_df( r.content )
            except binascii.Error:
                print(self.model_name, r, r.content )
                exit(-1)
            return rdf 



