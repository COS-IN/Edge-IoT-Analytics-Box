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

log_dir=/data/redundant_logging
log_file=mqtt.log

# Loops forever
python3 $script_path/upload.py --log_to_file $log_dir/$log_file
