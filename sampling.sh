#!/bin/sh

result_mh_z19=$(sudo python -m mh_z19 | jq .co2)
result_bme280=$(sudo python bme280_sample.py)
echo "$result_mh_z19 $result_bme280"