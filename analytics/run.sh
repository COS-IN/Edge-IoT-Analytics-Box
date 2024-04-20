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

kill_children () {
    pkill -P $$
    exit 0
}
trap kill_children SIGINT SIGTERM EXIT

export DATAANALYZER_PROFILE=1
export DATAANALYZER_TSERVE_IP="$jetson_ip"
export DATAANALYZER_TSERVE_PORT=8080

for config in ./configs/*.json; do 
    python3 ./run_config_v10.py --config  $config &
done

wait $(jobs -p)


