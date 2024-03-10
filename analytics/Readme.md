# Analytics Framework 

  It is a framework to setup a pipeline and perform analytics on time series data - realtime or historic - using models deployed on torch serve.  
  For each new pipeline, setup a configuration file and execute run.sh.  

## Configuration 
  
  It is defined as a json file. See example below and it's description. 

```json
  {
     "version": 10,
      "sensor": [
          "Power_Meters/CNC_Machines/ST10_old/PhB-TruePowerWatts/Value"
      ],
      "models": [
        "arima"
      ],

      "dataanalyzer": "tserve",
      "influxdb_bucket": "einsights_bucket",

      "window_size": 121,
      "time_step": 1,
      "processor": "historic",
      "t_start": "2023-12-20 04:44:00",
      "t_end": "2023-12-20 15:54:24"
  }
```

  Positioning in the sensor and models fields specify their correspondence.

  * **sensor:** Measurement field in InfluxDB. 
  * **models:** Model in torch serve.

  Specify data analyzer. Specialized data analyzers can be created for custom use cases. 

  * **dataanalyzer:** tserve, dump
    * tserve: requests the model deployed on torch serve to perform analysis on the window of data 
    * dump: dumps the window of data to a file 

  InfluxDb Configurations. 

  * **influxdb_bucket:**  influxdb bucket to fetch data from
  
  Window size and time step.

  * **window_size:** Window span in seconds. 
  * **time_step:** Time step for the window in seconds. 

  Processor type and time range.

  * **processor:** historic, realtime
    * historic: process data from t_start to t_end 
    * realtime: process data as it arrives

## run.sh 

  It executes a new process for each configuration found at the base of configs folder. 





