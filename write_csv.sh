#!/bin/sh

COLUMNS="timestamp co2_ppm temperature_celsius pressure_hpa humidity_percent"
mkdir -p data

current_date=$(date +"%Y-%m-%d")
if [ ! -f data/"$current_date".csv ] ; then
  touch data/"$current_date".csv
  echo "$COLUMNS" >> data/"$current_date".csv
fi

timestamp=$(date +%s)
results=$(bash sampling.sh)
echo "$timestamp $results" >> data/"$current_date".csv
