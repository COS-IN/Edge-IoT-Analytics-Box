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
trap kill_children SIGINT SIGTERM

PROG=
USAGE="Usage: ${PROG} -  \
--capture_inference  \
--dir '<result_directory>'" 
# Parse arguments
capture_inference="false"
results_dir="./"
while [[ "$#" -gt 0 ]]; do case $1 in
  -ci|--capture_inference) capture_inference="true"; shift;;
  -d|--dir) results_dir="$2"; shift 2;;
  -h|-help) echo "$USAGE"; exit 0;;
  *) echo "Unknown parameter passed: $1"; echo "${USAGE}"; exit 1;;
esac; done

export DATAANALYZER_PROFILE=0
export DATAANALYZER_TSERVE_IP="$jetson_ip"
export DATAANALYZER_TSERVE_PORT=8080

for config in ./configs/*.json; do 
    if [ $capture_inference ]; then
        export DATAANALYZER_PROFILE=1
        python3 ./run_config_v10.py \
            --config $config  \
            &> $results_dir/$(basename $config).log &
    else
        python3 ./run_config_v10.py --config $config &
    fi
done

wait $(jobs -p)


