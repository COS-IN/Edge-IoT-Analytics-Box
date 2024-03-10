#!/bin/bash 

# set -x 

source ./config.sh

influx bucket delete --name $BUCKET 
influx bucket create --name $BUCKET 
