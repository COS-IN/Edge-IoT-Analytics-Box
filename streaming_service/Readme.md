# Streaming Service 

## Configuration 
  
  * modify config.py to 
    * specify InfluxDB Configurations like ip address, port, token and org 
    * specify MQTT Configurations like ip address, port, username and password

## Use

  * use run_influxdb.sh to start the influxdb container
  * use mqtt_to_influxdb.sh to start fetching data from mqtt sensors and uploading to influxdb


