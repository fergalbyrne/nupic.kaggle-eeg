#!/bin/bash

find $1 -name "*_ictal_*.csv" | sort -t'_' -n -k6 | xargs -n 1 tail -n +2 > $2/"$1"_ictal.csv
find $1 -name "*_interictal_*.csv" | sort -t'_' -n -k6 | xargs -n 1 tail -n +2 > $2/"$1"_interictal.csv
