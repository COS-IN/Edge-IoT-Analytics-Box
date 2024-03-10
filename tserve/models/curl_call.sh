#!/bin/bash

# curl http://127.0.0.1:8080/predictions/avg --data "something"
#curl http://127.0.0.1:8080/predictions/avg --data-raw "something"

# -T examples/image_classifier/mnist/test_data/0.png

get_real_path() {
    script_path=$(dirname $1)
    script_path=$(realpath $script_path)
}
if [[ $0 != $BASH_SOURCE ]]; then
    get_real_path $BASH_SOURCE
else
    get_real_path $0
fi

source $script_path/config.sh

for model_name in "${model_names[@]}"; do
  curl -X POST http://127.0.0.1:8080/predictions/$model_name \
       -H "Content-Type: application/json" \
       -d "just the data"
done



