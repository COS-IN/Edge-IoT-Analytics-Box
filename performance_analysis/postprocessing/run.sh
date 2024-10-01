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

# Combine for each single experiment  
for expgroup in $script_path/../series_results/*; do
    csvs=()
    pcsvs=()
    for singleexp in $expgroup/*; do
        if [ -d $singleexp ]; then
            echo "Combining $singleexp"
            #python3 \
            #    $script_path/combine_single.py \
            #    $singleexp  \
            #    $singleexp/config*.log

            #python3 \
            #    $script_path/plot_single_csv.py \
            #    $singleexp.csv &> /dev/null 
            #
            #python3 \
            #    $script_path/process_tegralogs.py \
            #    $singleexp/tegrastats.log 
            csvs+=($singleexp.csv)
            pcsvs+=($singleexp/tegrastats.log.power.csv)
        fi
    done
    python3 \
        $script_path/plot_multi_csv.py \
        $expgroup/cplot \
        ${csvs[@]} &> /dev/null
    python3 \
        $script_path/plot_multi_csv_power.py \
        $expgroup/pplot \
        ${pcsvs[@]} #&> /dev/null
done





