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

for model_name in "${model_names[@]}"; do
  curl -X DELETE "localhost:8081/models/${model_name}"
done

