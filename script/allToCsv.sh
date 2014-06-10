#!/bin/bash

for f in $(find $1 -name '*.mat')
do
	FNAME=$(basename $f)
	DIRNAME=$(basename $(dirname $f))
	filename="${FNAME%.*}"
	mkdir -p ../csvData/$DIRNAME
	./dataToCSV.py $f ../csvData/$DIRNAME/"$filename".csv
done


