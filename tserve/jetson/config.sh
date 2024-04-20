#!/bin/bash

source ../config.sh
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

message() {
    cat <<\EOF
#####################################
EOF
    cat <<< "# "
}

tserve_version=4a110235b334f46564d0c3d1ba8946806368b075


