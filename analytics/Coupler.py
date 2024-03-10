from helper_funcs import *

from DataReformatter import DataReformatter
from influxdb import InfluxDB

class Coupler(object):

    """
        Couples DataReformatter and DataAnalyzer
        to process a window of measurements. 
    """

    def __init__(self, measurements, analyzer, tag_save, bucket):
        self.mlist = measurements
        self.reform = DataReformatter()
        self.analyzer = analyzer 
        self.tag_save = tag_save
        self.idb = InfluxDB('Be7aNDGX-koozEmHn3VRhqZ0VWOD8LTvu4JRwUu7hLnWdsxXd4d9tOBSKHRJgZJzSAoO8Nnam4hbKRNsKvS51Q==')
        self.bucket = bucket 
    
    def fetch_data(self, t_start, t_end ):
        dfs = []
        mlist = self.mlist 
        idb = self.idb

        col_sel = [
            '_time', 
            'val', 
            # '_measurement',
        ]
        
        for m in mlist:
            df = idb.read(bucket=self.bucket, measurement=m,  start=t_start, end=t_end)
            if len(df) != 0:
                df = df[col_sel]
                df = df.set_index(col_sel[0])
                df = df.rename(columns={'val':m})
            else:
                df[m] = 0.0
                print("Warning: There is no data in range {} - {} for {}".format(t_start, t_end, m))
            dfs.append( df )
        return dfs 
    
    def put_data(self, dfs, name):
        tagi = '_time' 
        idb = self.idb
        for df in dfs:
            cols = df.columns
            df.loc[:,'_measurement'] = cols[1]
            rd = {cols[1]:name}
            df = df.rename(columns=rd)
            idb.write(df, bucket=self.bucket, field_columns=[name])

    def process_window(self, t_end, delta):
        reform = self.reform 
        analyzer = self.analyzer

        t_start = t_end - delta

        dfs = self.fetch_data( t_start, t_end )

        df = reform.merge( dfs )
        adf = analyzer.analyze( df )

        # TODO:  <09-10-23, abrehman> # window merger based on historic windows if needed 

        adfs = reform.divide( adf )
        
        # TODO:  <09-10-23, abrehman> # define a way to pass measurements / fields for saving each column 
        self.put_data( adfs, self.tag_save )



