#!/usr/bin/env python
# coding: utf-8

import argparse

import paho 
import paho.mqtt.client as mqtt
import google.protobuf
import google.protobuf.json_format
import sparkplug_b_pb2

from influxdb_client import InfluxDBClient, Point
from influxdb_client import InfluxDBClient as i_cli
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.domain.write_precision import WritePrecision
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client import WriteOptions

from datetime import datetime
from threading import Thread
import concurrent.futures
import json
import socket
import pickle
import struct
import time
import ast
import os

import logging
from logging.handlers import RotatingFileHandler

from config import *

log_file_max_size=1024*1024*1 # 1 MB
log_file_max_size=1024*1024*100 # 100 MB

class LoggerWriteAPI:

    def __init__(self, filename):
        my_handler = RotatingFileHandler( filename, mode='a', maxBytes=log_file_max_size,
                                 backupCount=100000, encoding=None, delay=True)
        my_handler.setLevel(logging.INFO)
        app_log = logging.getLogger('root')
        app_log.setLevel(logging.INFO)
        app_log.addHandler(my_handler)

        self.app_log = app_log
        self.my_handler = my_handler

    def write( self, bucket, idb_org, point ):
        self.app_log.info( point.to_line_protocol() )

metric_value_type = {
    3: "intValue",
    4: "longValue",
    9 : "floatValue"
}

def log( priority, msg ):
    print("{}: ".format(priority)+str(msg))

def log_warn( msg ):
    log( "Warn", msg )
    pass

def log_info( msg ):
    log( "Info", msg )


def dump_using_writeapi(record_key, record_value, record_time):
    # print("Parsing: [\"{}\",{},{}]".format( record_key, record_value, record_time ))
    try:
        okey = record_key.rsplit('/',1)[0]
        okey = okey.rsplit('/',1)

        base_name = okey[0]

        sensor = okey[1]
        sensor = sensor.split('_',1)
        sensor = sensor[0]+'/'+sensor[1]

        bucket = "energy_"+base_name

        record_time = int(record_time)
        m_time = datetime.fromtimestamp( record_time/1000.0 )
        m_time = m_time.astimezone( tz=None )

        point = Point.measurement( sensor ).field( 'val', record_value ).time( m_time, write_precision=WritePrecision.MS )
        write_api.write( bucket, idb_org, point )

    except IndexError:
        log_warn( "dump_using_writeapi: IndexError: record_key {}".format( record_key ) )

def prase_and_dump(messages):
    for message in messages:
        # print( message )
        key = message['name']
        dtype = message['datatype']

        metric_data_type = metric_value_type[dtype] 
        if metric_data_type == 'longValue':
            log_warn( "Ignoring key {}".format( key ) )
            continue

        value = message[metric_data_type]
        timestamp = message['timestamp']
        dump_using_writeapi(key, value, timestamp)

def read_from_file( filename, wait_time, batch_size ):
    
    wait_time = wait_time / 1000.0

    file_size = os.path.getsize( filename )
    bytes_processed = 0

    with open(filename) as f:
        i = 0 
        for line in f:
            line = ast.literal_eval( line )
            prase_and_dump([line])

            bytes_processed += 8*len(line)
            i += 1
            if i == batch_size:
                print("Processed {:.9}% of file".format( bytes_processed*100.0/file_size ), end='\r' )
                time.sleep( wait_time )
                i = 0

def parse_spkplug_pbuf(wire_raw):
    """ wire_raw is message_tuple"""

    payload_message = sparkplug_b_pb2.Payload()
    mlen = payload_message.ParseFromString(wire_raw[1])
    parsed_msg=google.protobuf.json_format.MessageToDict(payload_message)

    all_sensor_data = parsed_msg['metrics']

    prase_and_dump( all_sensor_data )

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    tup = (msg.topic, msg.payload)
    parse_spkplug_pbuf(tup)


def mqtt_connection():
    host = mqtt_ip 
    username = mqtt_user 
    password = mqtt_pass 

    client=mqtt.Client(paho.mqtt.enums.CallbackAPIVersion(1))
    client.username_pw_set(username,password)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host)

    return client

def mqtt_thread():
    conn = mqtt_connection()
    conn.loop_forever()

if __name__ == "__main__":

    argparser = argparse.ArgumentParser( description="Script that listens to MQTT Broker" )
    argparser.add_argument( "--log_to_file", '-f', help="Path to log file.", type=str)
    argparser.add_argument( "--read_from_file", '-r', help="Path to log file with rows of parsed_msg['metrics']", type=str)
    argparser.add_argument( "--sleep", '-s', help="sleep duration milliseconds", type=int)
    argparser.add_argument( "--sleep_after", '-a', help="sleep after reading this number of files", type=int)

    args = argparser.parse_args()

    if args.log_to_file is not None:
        write_api = LoggerWriteAPI( args.log_to_file )
    else:
        try:
            db_conn = InfluxDBClient(url="http://"+idb_ip+":"+idb_port, token=idb_write_token,org=idb_org, debug=False)
        except ValueError:
            print("Error: Couldn't connect to influxDB")
            exit(-1)

        class BatchingCallback(object):
            def success(self, conf: (str, str, str), data: str):
                print(f"Written batch: {conf}, data: {data}")
            def error(self, conf: (str, str, str), data: str, exception: InfluxDBError):
                print(f"Cannot write batch: {conf}, data: {data} due: {exception}")
            def retry(self, conf: (str, str, str), data: str, exception: InfluxDBError):
                print(f"Retryable error occurs for batch: {conf}, data: {data} retry: {exception}")
        callback = BatchingCallback()
        write_api = db_conn.write_api(success_callback=callback.success,
                                  error_callback=callback.error,
                                  retry_callback=callback.retry,
                                  write_options=WriteOptions(batch_size=1)
                                  )
        write_api = db_conn.write_api(write_options=WriteOptions(batch_size=100))

    # following calls require write_api object to be set appropriately 
    if args.read_from_file is not None:
        read_from_file( args.read_from_file, args.sleep, args.sleep_after )
    else:
        mqtt_thread()

