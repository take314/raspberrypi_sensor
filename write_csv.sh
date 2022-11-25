#!/bin/sh

current_date=$(date +"%Y-%m-%d")
if [ ! -f data/"$current_date".csv ] ; then
  touch data/"$current_date".csv
  echo "creating data/$current_date.csv..."
  echo "timestamp co2_ppm" >> data/"$current_date".csv
fi

timestamp=$(date +%s)
co2_ppm=$(bash sampling.sh)
echo "$timestamp $co2_ppm" >> data/"$current_date".csv