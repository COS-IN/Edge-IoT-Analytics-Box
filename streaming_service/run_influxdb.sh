#!/bin/bash 

get_real_path() {
    script_path=$(dirname $1)
    script_path=$(realpath $script_path)
}
if [[ $0 != $BASH_SOURCE ]]; then
    get_real_path $BASH_SOURCE
else
    get_real_path $0
fi
cd $script_path                                      
source ./config.sh

mkdir -p $db_dir
db_dir=$(realpath $db_dir)

docker container stop influxdb_0
sleep 1 
docker run  \
         --rm \
         --expose 8086  \
         -p 8086:8086  \
         -v $db_dir:/var/lib/influxdb2/  \
         -v $script_path:/workspace  \
         -v $script_path/setup/config.yml:/etc/influxdb2/config.yml  \
         -v $script_path/setup/root/:/root/  \
         --name influxdb_0  \
         -d $db_version 
         # influxdb_cus:latest \
         # influxd > ./temp.log &

docker container ls 
