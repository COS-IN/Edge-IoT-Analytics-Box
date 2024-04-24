# Performance Analysis 

## End goal / Deliverable (Reason)

  Measure inference times, energy cost, utilization of a single experiment. 
  Perform experiments for multiple sensor count. 

## Next Actions (Planning)

  * [x] setup for single experiment  
    * [x] measuring inference time 
      * [x] update analytics to spit out inference time
    * [x] setting up jetson for the experiment 
    * [x] measuring metrices 
    * [x] cleaning up afterwards 
   
  * [x] repeat the experiments for following set  
    * [x] arima, arnn, both  
   
  * [x] post process a single experiment 
    * create a csv and df of 
      * inference times
        * config_name, inferences with index of timestamps
    * [x] plot csv for single exp 
    
  * [x] post process collective results  
    * [x] plot results  
      * [x] voilin plot for inference times 
    
  * [x] update report 
  
  * Updates 
    * single experiment 
      * measuring energy cost 
        * capturing tegrastats output 
        * post processing logs 
          * to get total power for each timestamp
        * post processing inference logs to get 
          * total requests for each instance 
        * calculate energy cost for each inference

## Worklog (Doing) 

  r ! date


## Review (Reading)
  How much time did it take? 
  What could I have done differently? 
  What worked really well? 
  What are the key lessons? 
