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


message "capture power"
./ssh_remote.sh "cd $dst_dir; ./performance_analysis/capture_power.sh"

message "start requests"
../analytics/run.sh





