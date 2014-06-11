#!/bin/bash

echo $1

for DIR in `find $1 -type d`
do
	echo $DIR
	./combineTraining.sh $DIR ../aggData
done
