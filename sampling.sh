#!/bin/sh

result_mh_z19=$(sudo python -m mh_z19 | jq .co2)
result_bme280=$(sudo python bme280_sample.py)

if [ -z "$result_mh_z19" ]; then
  result_mh_z19="None"
elif [ -z "$result_bme280" ]; then
  result_bme280="None None None"
fi

echo "$result_mh_z19 $result_bme280"