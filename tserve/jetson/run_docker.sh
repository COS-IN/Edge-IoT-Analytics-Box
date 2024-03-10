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

docker run  \
         --rm  \
         -it  \
         --runtime nvidia \
         -p 127.0.0.1:8080:8080  \
         -p 127.0.0.1:8081:8081  \
         -p 127.0.0.1:8082:8082  \
         -v $store_path:/home/model-server/model-store aarehman/torchserve:latest-cpu



