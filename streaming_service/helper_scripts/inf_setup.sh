#!/bin/bash 

source config.sh 

influx config create -n default \
  -u http://localhost:8086 \
  -o $ORG \
  -t Be7aNDGX-koozEmHn3VRhqZ0VWOD8LTvu4JRwUu7hLnWdsxXd4d9tOBSKHRJgZJzSAoO8Nnam4hbKRNsKvS51Q== \
  -a

