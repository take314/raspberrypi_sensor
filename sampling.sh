#!/bin/sh

if [ ! -f ./latest.csv ] ; then
  touch latest.csv
  echo "creating latest.csv..."
  echo "timestamp co2_ppm" >> latest.csv
fi

current_date=$(date +"%Y-%m-%d")
if [ ! -f ./"$current_date".csv ] ; then
  touch "$current_date".csv
  echo "creating $current_date.csv..."
  echo "timestamp co2_ppm" >> "$current_date".csv
fi

timestamp=$(date +%s)
co2_ppm=$(sudo python -m mh_z19 | cut -d " " -f 2 | sed 's/[^0-9]//g')
echo "$timestamp $co2_ppm" >> "$current_date".csv