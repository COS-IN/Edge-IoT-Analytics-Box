#!/bin/bash 

# set -x 

source ./config.sh

influx delete --bucket $BUCKET \
  --start '2023-02-10T00:00:00Z' \
  --stop $(date +"%Y-%m-%dT%H:%M:%SZ") 
