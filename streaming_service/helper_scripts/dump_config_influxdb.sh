#!/bin/bash 

# db_dir=./db_dir/
db_dir=/data/influx_db

mkdir -p $db_dir
db_dir=$(realpath $db_dir)
cur_dir=$(realpath ./)

docker run  \
         --rm \
         --expose 8086  \
         -p 8086:8086  \
         -v $db_dir:/var/lib/influxdb2/  \
         -v $cur_dir:/workspace  \
         --name influxdb_0  \
         influxdb \
         influxd \
         print-config > config.yml

docker container ls 
