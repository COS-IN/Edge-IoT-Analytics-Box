import time
import datetime

from Coupler import Coupler 
from dataanalyzer.DataAnalyzer import DataAnalyzer
from dataanalyzer.DataAnalyzerTServe import DataAnalyzerTServe
from dataanalyzer.DataAnalyzerDump import DataAnalyzerDump

from helper_funcs import *

class HistoricProcessor: 

    def __init__(self, coupler, t_start, t_end, window_size, stride = 1):
        """
            coupler -> processes a window of measurements producing a window 
            window_size -> input window size to process in seconds  
            stride -> number of seconds to wait before moving the window 
        """
        self.coupler = coupler
        self.window_size = window_size
        self.stride = stride
        self.t_start = convert_to_isodatetime( t_start )
        self.t_end = convert_to_isodatetime( t_end )

    def event_loop(self):
        
        coupler = self.coupler
        t_start = self.t_start
        t_end = self.t_end

        delta = datetime.timedelta(seconds = int(self.window_size))
        stride = datetime.timedelta(seconds = int(self.stride))

        t_cur = t_start + delta 

        total_time = t_end - t_start
        total_time = total_time.total_seconds()

        passed = 0
        while t_cur < t_end:
            
            coupler.process_window( t_cur, delta )

            t_cur += stride 

            # TODO:  <09-10-23, abrehman>  wait for an event from db
            time.sleep( 0.01 ) # seconds 

            passed += 1
            print("Total {} Passed {} %{} remaining".format(total_time, passed, (total_time-passed)*100/total_time), end='\r')

if __name__ == "__main__":
    
    measurements = [
        "M00/PhA_Current_Arms",
        "M00/PhA_Frequency_Hz",
        "M00/PhA_HarmonicTruePower_W",
    ]
    
    bucket = 'testing'
    bucket = 'testing2'

    if True:
    #if False:
        da = DataAnalyzerTServe()
        coupler = Coupler( measurements, da, 'tserve_test', bucket )
    elif True:
        da = DataAnalyzerDump()
        coupler = Coupler( measurements, da, 'dump_test', bucket )
    else: 
        da = DataAnalyzer()
        coupler = Coupler( measurements, da, 'plus_one', bucket )
  
    t_start = '2023-10-06 11:30:00'
    t_end = '2023-10-06 12:00:00'
    window_size = 60

    htp = HistoricProcessor( coupler=coupler, t_start = t_start, t_end = t_end, window_size = window_size )
    htp.event_loop()


