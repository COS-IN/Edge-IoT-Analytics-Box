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

model="arnn_powerfactor"
model="arima"

sensors=(
        "Power_Meters/CNC_Machines/ST10_old/ApparentPowerVA/Value"
        "Power_Meters/CNC_Machines/ST10_v2/ApparentPowerVA/Value"
        "Power_Meters/CNC_Machines/VF5_old/ApparentPowerVA/Value"
        "Power_Meters/CNC_Machines/VF5_v2/ApparentPowerVA/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/ApparentPowerVA/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/ApparentPowerVA/Value"
        "Power_Meters/CNC_Machines/ST10_old/PhA-PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_old/PhB-PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_old/PhC-PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_old/PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_v2/PhA-PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_v2/PhB-PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_v2/PhC-PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_v2/PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_old/PhA-PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_old/PhB-PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_old/PhC-PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_old/PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_v2/PhA-PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_v2/PhB-PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_v2/PhC-PowerFactor/Value"
        "Power_Meters/CNC_Machines/VF5_v2/PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/PhA-PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/PhB-PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/PhC-PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/PhA-PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/PhB-PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/PhC-PowerFactor/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/PowerFactor/Value"
        "Power_Meters/CNC_Machines/ST10_old/PhA-TruePowerWatts/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/TruePowerWatts/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/PhC-TruePowerW/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/PhB-TruePowerWatts/Value"
        "Power_Meters/HVAC/RoofTopUnit1_v2/PhA-TruePowerWatts/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/TruePowerWatts/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/PhC-TruePowerW/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/PhB-TruePowerWatts/Value"
        "Power_Meters/HVAC/RoofTopUnit1_old/PhA-TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/VF5_v2/TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/VF5_v2/PhC-TruePowerW/Value"
        "Power_Meters/CNC_Machines/VF5_v2/PhB-TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/VF5_v2/PhA-TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/VF5_old/TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/VF5_old/PhC-TruePowerW/Value"
        "Power_Meters/CNC_Machines/VF5_old/PhB-TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/VF5_old/PhA-TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/ST10_v2/TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/ST10_v2/PhC-TruePowerW/Value"
        "Power_Meters/CNC_Machines/ST10_v2/PhB-TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/ST10_v2/PhA-TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/ST10_old/TruePowerWatts/Value"
        "Power_Meters/CNC_Machines/ST10_old/PhC-TruePowerW/Value"
        "Power_Meters/CNC_Machines/ST10_old/PhB-TruePowerWatts/Value"
)


i=0
for sensor in "${sensors[@]}"; do 
    sensor=$(echo "$sensor" | sed 's/\//\\\//gi')
    cat ./config_tserve_template.json | \
        sed "s/input_fill/$sensor/gi" | \
        sed "s/model_fill/$model/gi" > ./config_tserve_$i.json
    i=$((i+1))
done

