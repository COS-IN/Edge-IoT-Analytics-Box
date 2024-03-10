#!/bin/bash

source ../config.sh

#####################################
# Array of model names to register 
# and use 
model_names=(
              "arima" \
              "arnn_truepower"  \
              "arnn_powerfactor"\
              "arnn_aparentpower"\
            )

#####################################
# Array of extra_files
# Each line corresponds to a model
extra_files_s+=("./DataAnalyzerARIMA.py,./DataAnalyzer.py")
extra_files_s+=("./arnn.py,./DataAnalyzer.py,./HyperparameterVariables.py,./TruePowerW.pth,./DataAnalyzerARNNPredict.py,./DataVariables.py")
extra_files_s+=("./arnn.py,./DataAnalyzer.py,./HyperparameterVariables.py,./PowerFactor.pth,./DataAnalyzerARNNPredict.py,./DataVariables.py")
extra_files_s+=("./arnn.py,./DataAnalyzer.py,./HyperparameterVariables.py,./ApparentPowerVA.pth,./DataAnalyzerARNNPredict.py,./DataVariables.py")

model_py="model_da.py"
model_pt=""
model_handler="df_handler.py"

