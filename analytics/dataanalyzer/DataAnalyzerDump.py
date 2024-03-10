import pandas as pd

from dataanalyzer.DataAnalyzer import DataAnalyzer

class DataAnalyzerDump(DataAnalyzer):

    """
        Analyzes given window of data to generate a new window 
    """

    def __init__(self):
        pass

    def analyze(self, df):
        
        df.to_csv( "./df_dump.csv" )
        dfm = df.mean()
        dfm = pd.DataFrame( dfm )

        dfmz = dfm.loc[ dfm[0] < 0.001 ]
        dfmz.to_csv('no_data.csv')
        

        dfmz = dfm.loc[ dfm[0] > 0.001 ]
        dfmz.to_csv('with_data.csv')


        dfd = df.describe()
        dfd.to_csv( "./df_dump_describe.csv" )

        print(dfd)
        exit(0)

