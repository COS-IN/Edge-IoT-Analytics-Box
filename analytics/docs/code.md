# Class Dependencies  

```text
  DataReformatter -> none 
  DataAnalyzer -> none 
  Coupler -> DataReformatter, DataAnalyzer, InfluxDB 
  RealTime-Processor -> Coupler
  Historic-Processor -> Coupler
```

# Implicit Abstractions 
 
```text
  data exchange
    
    list of dfs - from db, to db 
    single df representing a window 
      with measurements as column name 
      rows with values 
  
  window based analysis 
    to generate window based output 
```


# Class Descriptions 

## DataReformatter

  * merge
    * convert list of dfs into a singular df 
      * each df 
        * is window long 
        * has different measurements 
        * use timestamps from single df   
  * divide
    * convert single df into a list of dfs 
      * inverse to break each measurement column to individual df  

## Data Analyzer 

  * performs analysis on a window of data 
  * generating 
    * a window  
 
## Coupler  

  * functionality 
    * fetch and put data on window basis after processing using data anayzler 
    * use datareformater to have it reformatted before being given to DataAnalyzer 
  * instantiates 
    * DataReformatter
    * DataAnalyzer 
    * list of measurements to process 
  * process a window
    * fetchdata - make calls to db to fetch one window 
      * end time 
      * delta - given as input - delta is window size 
      * list of dfs 
    * call reformatter  
      * with list of dfs
      * producing a singular df of window 
    * Call DataAnalyzer to produce a window of data 
    * call reformatter 
      * to divide into list of dfs again 
    * putdata
      * make calls to db to write list of dfs 

## RealTime Processor  

  * instantiates 
    * Coupler
  * waits for new data to arrive in the db 
  * calls process a window of Coupler 

## Historic Processor 

  * instantiates 
    * Coupler
  * for each unit of time in given range of history - incremented by stride
    * calls process a window of Coupler 


