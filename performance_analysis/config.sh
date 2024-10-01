#!/bin/bash

###
# Locations 
target="ar@$jetson_ip"
dst_dir="/data2/ar/workspace/Edge-IoT-Analytics-Box"
<<<<<<< HEAD
results_dir="results"
=======
>>>>>>> .

###
# Parameters  

<<<<<<< HEAD
warmup_time=10 # seconds
duration=30 # seconds
=======
warmuptime=60 # seconds
>>>>>>> .

###
# Functions 

message() {
    cat <<\EOF
#####################################
EOF
    cat <<< "# $1"
}

<<<<<<< HEAD
rotatedir(){
  if [ -d $1 ]; then
    mv $1 $1-$(date +%Y%m%d%H%M%S)
  fi
  mkdir -p $1
}

=======
>>>>>>> .
# include config from directory above if it exists
get_real_path() {
    script_path=$(dirname $1)
    script_path=$(realpath $script_path)
}
if [[ $0 != $BASH_SOURCE ]]; then
    get_real_path $BASH_SOURCE
else
    get_real_path $0
fi
if [[ -f $script_path/../config.sh ]]; then
    source $script_path/../config.sh
fi
