import time
import datetime

from Coupler import Coupler 
from dataanalyzer.DataAnalyzer import DataAnalyzer
from dataanalyzer.DataAnalyzerTServe import DataAnalyzerTServe
from dataanalyzer.DataAnalyzerDump import DataAnalyzerDump

from helper_funcs import *

class RealTimeProcessor: 

    def __init__(self, coupler: Coupler, window_size, stride = 1):
        """
            coupler -> processes a window of measurements producing a window 
            window_size -> input window size to process in seconds  
            stride -> number of seconds to wait before moving the window 
        """
        self.coupler = coupler
        self.window_size = window_size
        self.stride = stride

    def event_loop(self):
        
        coupler = self.coupler
        delta = datetime.timedelta(seconds = int(self.window_size))

        delta_bootstrap = datetime.timedelta(seconds = int(self.window_size))
        t = datetime.datetime.now()
        coupler.process_window( t, delta_bootstrap )
       
        while True:
            
            t = datetime.datetime.now()
            coupler.process_window( t, delta )

            # TODO:  <09-10-23, abrehman>  wait for an event from db
            time.sleep( 1 ) # seconds 

if __name__ == "__main__":
    
    import argparse
    argparser = argparse.ArgumentParser( description="Realtime processor" )
    argparser.add_argument( "--analyzer", help="Type of analyzer to use", required=True, type=str, choices=["arima","avg"], default="arima"  )
    args = argparser.parse_args()

    measurements = [
        "M00/PhA_Current_Arms",
        "M00/PhA_Frequency_Hz",
        "M00/PhA_HarmonicTruePower_W",
    ]

    bucket = 'testing'
    bucket = 'testing2'
    bucket = "energy_OptoMMP/Modules/Channels"

    if args.analyzer == "tserve":
        da = DataAnalyzerTServe()
        coupler = Coupler( measurements, da, 'tserve_test', bucket )
    elif args.analyzer == "dump":
        da = DataAnalyzerDump()
        coupler = Coupler( measurements, da, 'dump_test', bucket )
    else: 
        print("Error: Unknown Analyzer")
        exit(0)
  
    window_size = 60

    rtp = RealTimeProcessor( coupler=coupler, window_size = window_size )
    rtp.event_loop()


