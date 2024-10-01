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

kill_children () {
    pkill -P $$
    exit 0
}
trap kill_children SIGINT SIGTERM 

cat <<EOF
##############################################

This script will update the analytics/configs
based on the experiment configuration and
run the ./run_single.sh script to actually 
run the experiment.

After the experiment is done, it will move the results 
directory to the appropriate experiment directory.

###########
EOF

##############################################
# Functions 

copy_configs() {
    sensor_count=$1
    model_dir=$2
    no_clean_dir=$3

    model_name=$(basename $model_dir)

    if [ -z "$no_clean_dir" ]; then
        rm $configs_dir/*.json 
    fi
    for i in $(seq 0 $sensor_count); do
        cp "$model_dir/config_tserve_$i.json" $configs_dir/config_tserve_${i}_${model_name}.json
    done
}

# Experiment configuration 
#   Requirements 
#     run single exp with different number of sensors 
#       only for arnn model 
#       only for arima model 
#       both arnn and arima model 


# Experiment configuration 
#   Requirements 
#     run single exp with different number of sensors 
#       only for arnn model 

# copy configs from arnn folder to configs folder
# sensor range 0 to 53


configs_dir=$(realpath $script_path/../analytics/configs)

sensor_set=(
    10
    15
    20
    25
    30
    35
    40
    45
    50
)

run_series() {
    model_name=$1
    model_dir=$(realpath $script_path/../analytics/configs/${model_name})
    all_results_dir="$script_path/${model_name}_only"
    mkdir -p $all_results_dir

    for scount in ${sensor_set[@]}; do
        echo "Running experiment with $scount sensors"
        copy_configs $scount $model_dir
        ./run_single.sh
        mv $results_dir $all_results_dir/${model_name}_$scount
    done
}

run_series arima 
run_series arnn

model_dir0=$(realpath $script_path/../analytics/configs/arima)
model_dir1=$(realpath $script_path/../analytics/configs/arnn)
all_results_dir="$script_path/both_models"
mkdir -p $all_results_dir

for scount in ${sensor_set[@]}; do
    echo "Running experiment with $scount sensors"
    copy_configs $scount $model_dir0 
    copy_configs $scount $model_dir1 "no_clean"
    ./run_single.sh
    mv $results_dir $all_results_dir/both_$scount
done


