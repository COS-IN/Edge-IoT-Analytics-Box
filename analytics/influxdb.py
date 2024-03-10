import pandas as pd
import warnings
import influxdb_client
from threading import Thread, Lock

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.warnings import MissingPivotFunction
warnings.simplefilter("ignore", MissingPivotFunction)

import datetime
from dateutil import parser 

from helper_funcs import *
from config import *

DEBUGPRINTS = True 
DEBUGPRINTS = False

class InfluxDB:
    def __init__(self, token, url = idb_ip, org=idb_org):
        self.token = token
        self.url = url
        self.org = org
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org, debug=False)

    def __del__(self):
        self.client.close()

    def __fetch_influx(self, query):
        """
        This function fetches dataframe for given flux query
        """

        return self.client.query_api().query_data_frame(org=self.org, query=query)

    def __dump_influx(self, df, bucket_name, time_column, measurement_name):
        """
        This function dumps data to influxDB based on given parameters
        """
        df.set_index(time_column,inplace=True)
        points = self.client.write_api(bucket=bucket_name,write_options=SYNCHRONOUS)
        points.write(bucket=bucket_name, org=self.org, record=df, data_frame_measurement_name=measurement_name)

    def get_measurements(self, bucket):
        """
        This function fetches all the tables for given bucket
        """

        query = f"""
        import \"influxdata/influxdb/schema\"
    
        schema.measurements(bucket: \"{bucket}\")
        """

        query_api = self.client.query_api()
        tables = query_api.query(query=query, org=self.org)

        # Flatten output tables into list of measurements
        measurements = [row.values["_value"] for table in tables for row in table]

        return measurements


    def read(self, bucket, measurement, query=None, delta=None, start=None, end=None):
        """
        This creates flux query for given timestamp and then returns output as a dataframe.

        Priority of parameters, query > delta > start,end > last
        """
        flux_query = query
        
        if end:
          end = convert_to_iso( end )
        if start: 
          start = convert_to_iso( start )
        
        win_size = '60s'

        if end and delta:
            start = apply_delta( end, delta )
            flux_query = f"""
                  import "interpolate"
                  from(bucket: "{bucket}")
                  |> range(start:{start}, stop: {end})
                  |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                  |> filter(fn: (r) => r["_field"] == "val")
                  |> toFloat()
                  |> interpolate.linear(every: {win_size})
                  |> aggregateWindow(every: {win_size}, fn: median, createEmpty: true)
                  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
        elif delta:
            flux_query = f"""
                  import "interpolate"
                    from(bucket: "{bucket}")
                  |> range(start:-{delta}, stop: now())
                  |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                  |> filter(fn: (r) => r["_field"] == "val")
                  |> toFloat()
                  |> interpolate.linear(every: {win_size})
                  |> aggregateWindow(every: {win_size}, fn: mean, createEmpty: true)
                  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
        elif start and end:
            flux_query = f"""
                  import "interpolate"
                  from(bucket: "{bucket}")
                  |> range(start:{start}, stop: {end})
                  |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                  |> filter(fn: (r) => r["_field"] == "val")
                  |> toFloat()
                  |> interpolate.linear(every: {win_size})
                  |> aggregateWindow(every: {win_size}, fn: mean, createEmpty: true)
                  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
        else:
            flux_query = f"""
            from(bucket: "{bucket}")
                  import "interpolate"
                  |> range(start: 0)
                  |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                  |> filter(fn: (r) => r["_field"] == "val")
                  |> toFloat()
                  |> interpolate.linear(every: {win_size})
                  |> aggregateWindow(every: {win_size}, fn: mean, createEmpty: true)
                  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
        if DEBUGPRINTS:
          print("|"*10)
          print(flux_query)
        try:
            return self.__fetch_influx(flux_query)
        except influxdb_client.rest.ApiException as e:
            print("Query: ", flux_query )
            print("Exception: ", e )
            exit(-1)

    def write(self, df, bucket, field_columns, time="_time", measurement="_measurement"):
        """
        Formats the dataframe and then writes it to influxDB
        """
        columns = field_columns
        columns.append(time)
        columns.append(measurement)

        write_df = df[columns]

        write_df.set_index(measurement, inplace = True)

        measurements = write_df.index.unique(measurement)

        for measurement_idx in measurements:
            chunk_df = write_df.loc[measurement_idx]
            if isinstance(chunk_df, pd.Series):
                chunk_df = pd.DataFrame(chunk_df).T
                chunk_df.reset_index(inplace=True)
                chunk_df.rename(columns={'index':measurement},inplace=True)
            else:
                chunk_df.reset_index(inplace=True)
            chunk_df.drop(columns=measurement,inplace = True)
            self.__dump_influx(chunk_df, bucket, time, measurement_idx)

# def test_func(conn, measure):
#     df = conn.read(bucket="energy_OptoMMP/Modules/Channels",measurement=measure, delta="1h")
#     print(len(df.index))
#     return df

def example_idf():
    idb = InfluxDB( idb_write_token )
    return idb

def example_read(): 
    idb = example_idf() 

    print('#'*20)
    print('# Last 30 mins from present')
    idf = idb.read(bucket="testing", measurement="M00/PhA_Current_Arms",  delta="30m")
    print(idf)

    print('#'*20)
    print('# Last 30 mins from 2023-10-06 16:10:20+00:00')
    t = '2023-10-06 12:00:00'
    idf = idb.read(bucket="testing", measurement="M00/PhA_Current_Arms",  delta="30m", end=t)
    print(idf)

    print('#'*20)
    print('# All the data')
    idf = idb.read(bucket="testing", measurement="M00/PhA_Current_Arms" )
    print(idf)

def example_write():
    idb = example_idf() 
    t = '2023-10-06 12:00:00'
    idf = idb.read(bucket="testing", measurement="M00/PhA_Current_Arms",  delta="30m", end=t)
    idf['predicted'] = idf['val'] + 1
    idb.write(idf, bucket="testing", field_columns=["predicted"])

    print('#'*20)
    print('# Predicted values written for last 30 mins from 2023-10-06 16:10:20+00:00')
    print(idf)

if __name__ == "__main__":
    
    example_read()
    example_write()


