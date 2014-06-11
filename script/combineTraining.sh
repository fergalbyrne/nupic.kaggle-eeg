#!/bin/bash

#Usage: ./combineTraining.sh TARGET_FOLDER OUTPUT_FOLDER

find $1 -name "*_ictal_*.csv" | sort -t'_' -n -k6 | xargs -n 1 tail -n +2 > $2/$(basename $1)_ictal.csv
echo "Finished Ictal"
find $1 -name "*_interictal_*.csv" | sort -t'_' -n -k6 | xargs -n 1 tail -n +2 > $2/$(basename $1)_interictal.csv
echo "Finished Interictal"
