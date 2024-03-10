#!/bin/bash 

influx query '
from(bucket: "energy_OptoMMP/Modules/Channels")
  |> range(start: 2022-01-01T08:00:00Z, stop: 2022-01-17T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "M00/PhA_Voltage_Vrms")
  |> filter(fn: (r) => r["_field"] == "val")
'

#    |> filter(fn: (r) => r._measurement == "home")
#    |> filter(fn: (r) => r._field== "co" or r._field == "hum" or r._field == "temp")


