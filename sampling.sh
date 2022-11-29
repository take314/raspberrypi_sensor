#!/bin/sh

result=$(sudo python -m mh_z19 | jq .co2)

if [ -z "$result" ]; then
  echo "None"
else
  echo "$result"
fi
