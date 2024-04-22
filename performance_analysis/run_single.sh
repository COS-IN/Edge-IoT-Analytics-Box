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

This script will wait for $warmup_time seconds 
before starting inference requests by 
running the analytics/run.sh script.

It will wait for $duration seconds before
killing the analytics/run.sh script and
collecting the results.

Results will be stored in directory: $results_dir.

###########
EOF

results_dir=$(realpath $results_dir)

rotatedir $results_dir

sys_pids=()

message "capture power"
./ssh_remote.sh "sudo tegrastats --interval 1000" > $results_dir/tegrastats.log &
sys_pids+=($!)

#sleep $warmup_time
message "start requests"
../analytics/run.sh \
    --capture_inference \
    --dir $results_dir &
sys_pids+=($!)

sleep $duration

for pid in ${sys_pids[@]}; do
    kill $pid
    wait $pid
done
wait $(jobs -p)

