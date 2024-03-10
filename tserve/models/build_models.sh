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

mkdir -p $store_path

i=0
for model_name in "${model_names[@]}"; do
  model_mar="$model_name.mar"
  extra_files=${extra_files_s[$i]}

  cd "$model_name" || exit 1 
  if [ -z "$model_pt" ]; then 
      torch-model-archiver  \
         --model-name "$model_name"  \
         --version 1.0  \
         --model-file "$model_py"  \
         --handler "$model_handler" \
         --extra-files "$extra_files"
  else
      torch-model-archiver  \
         --model-name "$model_name"  \
         --version 1.0  \
         --model-file "$model_py"  \
         --handler "$model_handler" \
         --serialized-file "$model_pt"  \
         --extra-files "$extra_files"
  fi
  mv "$model_mar" "$store_path/" 
  cd .. 

  i=$((i+1))
done

ls -all -h "$store_path"

