import time
import datetime

from Coupler import Coupler 
from dataanalyzer.DataAnalyzer import DataAnalyzer
from dataanalyzer.DataAnalyzerDump import DataAnalyzerDump
from dataanalyzer.DataAnalyzerTServe import DataAnalyzerTServe

from RealTimeProcessor import RealTimeProcessor
from HistoricProcessor import HistoricProcessor

from concurrent.futures import ThreadPoolExecutor

from helper_funcs import *

if __name__ == "__main__":
    
    import argparse
    argparser = argparse.ArgumentParser( description="Launch Processor based on the config" )
    argparser.add_argument( "--config", help="Configuration to use", required=True)
    args = argparser.parse_args()

    import json
    with open(args.config, "r") as f:
        config = json.load(f) 

    sensors = config["input_measurements"]
    models = config["models"]

    def launch_processor( config, sensor, model ):

        bucket = config["influxdb_bucket"]
        window_size =  config["window_size"] 
        measurements = [sensor] 
        processor_type = config["processor"]
        output_field_name = model 

        print("#"*20)
        print("bucket: {}".format(bucket))
        print("window_size: {}".format(window_size))
        print("measurements: {}".format(measurements))
        print("model: {}".format(model))
        print("processor_type: {}".format(processor_type))
        print("output_field_name: {}".format(output_field_name))
        print("#"*10)

        if config['dataanalyzer'] == "tserve":
            da = DataAnalyzerTServe(model_name=model) 
        elif config['dataanalyzer'] == "dump":
            da = DataAnalyzerDump() 
        else: 
            print("Error: Unknown Analyzer")
            exit(0)

        coupler = Coupler( measurements, da, output_field_name, bucket )

        if processor_type == 'realtime':
            rtp = RealTimeProcessor( coupler = coupler, window_size = window_size )
            rtp.event_loop()
        elif processor_type == 'historic':
            t_start = config['t_start'] 
            t_end = config['t_end'] 
            htp = HistoricProcessor( coupler=coupler, t_start = t_start, t_end = t_end, window_size = window_size )
            htp.event_loop()

    with ThreadPoolExecutor(max_workers=len(sensors)) as executor:
        tasks = [executor.submit(launch_processor, config, sensor, model) for sensor, model in zip(sensors, models)]
        for future in tasks:
            r = future.result()
            print("    {}".format(r))

