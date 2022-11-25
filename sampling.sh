#!/bin/sh

result=$(sudo python -m mh_z19 | cut -d " " -f 2 | sed 's/[^0-9]//g')

if [ -z "$result" ]; then
  echo "None"
else
  echo "$result"
fi