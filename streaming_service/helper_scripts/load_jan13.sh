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

upload_script=$(realpath ../upload.py)
python3 $upload_script --read_from_file /data/mqtt/jan13_data.txt --sleep 100 --sleep_after 400

