<h1 align="center"  style="border-bottom: none">
    <a href="//localhost" target="_blank"><img width="50%" alt="Edge-IoT-Analytics-Box" src="./artifacts/einsights_logo.jpg"></a>
</h1>

<h1  align="center" >Extensible Data Analytics System</h1>
<h2 align="center">Abdul Rehman</h2>
<h3 align="center">Advisor: Prateek Sharma</h2>
<h3 align="center">Indiana University, Bloomington</h3>

# Table of Contents
<!-- vim-markdown-toc Marked -->

* [Overview](#overview)
* [Architecture](#architecture)
* [Presentation](#presentation)
* [Performance Results](#performance-results)
* [Repository Layout](#repository-layout)
* [Getting Started](#getting-started)

<!-- vim-markdown-toc -->


## Overview 

Edge-IoT-Analytics-Box is a data analytics system that can be used to capture and analyze data in real time. 
The system is designed to be deployed on edge devices like Jetson Orin with following design goals.

  * extensibility 
  * ease of research 
  * minimum overhead from development to production 

## Architecture 

<h1 align="center"  style="border-bottom: none">
    <a href="//localhost" target="_blank"><img width="90%" alt="Architecture" src="./artifacts/architecture.drawio.png"></a>
</h1>

## Presentation 

<h1 align="center"  style="border-bottom: none">
    <a href="https://youtu.be/hBaTD35PA04?t=2421" target="_blank"><img width="90%" alt="Presentation" src="./artifacts/video_screenshot.jpg"></a>
</h1>

## Performance Results  

For 54 sensors being predicted using arima model and RNN model

  * Network bandwidth consumption on Jetson ~800 Kbytes per sec
  * CPU utilization on Jetson ~25 %
  * GPU utilization ~40 %
  * InfluxDB storage increases by ~7 Kbytes per second
    * it would take 866 days to fill up 500 Gb of space which is ~2.3 years

## Repository Layout    

For details of each module, please refer to the README.md in the respective directory.

* tserve 
  * Contains code to deploy torch serve on Jetson Orin along with scripts for building and delploying models. 
* analytics 
  * Framework to setup the pipeline for data analytics using models deployed on torch serve. 
* streaming_service  
  * Contains code to setup data streaming from sensors to InfluxDB, including scripts to setup InfluxDB.

## Getting Started 

  * setup InfluxDB on a server using the instructions in **streaming_service/README.md**
  * once data is streaming to the DB 
    * setup torch serve on a Jetson Orin using the instructions in **tserve/README.md**
    * setup an analytics pipeline using the instructions in **analytics/README.md** 

  


