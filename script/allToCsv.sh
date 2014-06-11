#!/bin/bash

#Usage: ./allToCsv.sh DIRNAME OUTDIRNAME

for f in $(find $1 -name '*ictal_*.mat')
do
	FNAME=$(basename $f)
	DIRNAME=$(basename $(dirname $f))
	filename="${FNAME%.*}"
	mkdir -p ../csvData/$DIRNAME
	../tools/dataToCSV.py $f $2/$DIRNAME/"$filename".csv &
done


