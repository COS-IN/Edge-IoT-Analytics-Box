import pandas as pd

def mergedfs( a, b, nearest_sec=1 ):
    sw_est = pd.merge_asof( a,  \
      b,  \
      left_on='_time', \
      right_on='_time',  \
      direction='nearest',  \
      tolerance=pd.Timedelta(nearest_sec,unit='sec') )
    return sw_est

class DataReformatter(object):

    """
        Reformats list of dfs to a df with a base timeindex 
        divides a df into list of dfs 
    """

    def __init__(self):
        pass

    def merge(self, dfs):
        dfs = sorted(dfs, key=lambda x: 1/(1+len(x)))
        mdf = dfs[0] 
        for df in dfs[1:]:
            if len(df) == 0:
                col = df.columns[0]
                mdf[col] = 0.0
                continue
            mdf = mergedfs( mdf, df )
        mdf = mdf.ffill()
        mdf = mdf.bfill()
        mdf = mdf.ffill()
        return mdf

    def divide(self, df):
        cols = df.columns 
        tagi = '_time'
        dfs = []
        for col in cols:
            if col == tagi:
                continue 
            colsel = [tagi, col]
            dfsep = df[colsel] 
            dfsep = dfsep.copy()
            dfs.append( dfsep )
        return dfs

    

        
