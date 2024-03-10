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

message "Deploying on Jetson Orin" 

cd /tmp 
if [ ! -d "serve-$tserve_version" ]; then
    wget https://github.com/pytorch/serve/archive/$tserve_version.zip
    mv $tserve_version.zip serve.zip
    unzip serve.zip
    cd serve-$tserve_version
    patch -p1 < $script_path/torch_serve.patch
fi

cd docker 
chmod a+x ./build_jetson.sh
./build_jetson.sh

chmod a+x ./build_img.sh
./build_img.sh

$script_path/run_docker.sh


