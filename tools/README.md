nupic.kaggle-eeg
================

Tools that may be helpful:  

`dataExaminer.py`: makes (sorta) pretty charts from the data. Arguments as follows:  

```
dataExaminer.py textfile makes a 3d graph of all electrodes, and then a graph of the total MAD score

```

`dataToCsv.py`: turns it into a csv. Arguments as follows: 

```
dataToCsv.py datafile csvfile
```

In both cases, the code is pretty simple.  Both scripts writes the data's numpy header information to `stdout`.


CSVHelper_Amplitudes.py
-------------------------

Aggregates all the mat files specified or the files contained in the directory 
specified.
USAGE:
```
CSVHelper_Amplitudes.py csvfile file1.mat file2.mat ...
```
        or
```
CSVHelper_Amplitudes.py csvfile directory
```

min_maxValue.py
---------------

Finds the minimum and maximum value of amplitude in given file list or all files in the directory.

```
min_maxValue.py datafile [datafile...]
```
or
```
min_maxValue.py directory
```


dataFeeder.py
-------------
Extract Patient_n data from tar file and store segment by segment into single CSV 


```
dataFeeder.py  ~/Downloads/clips.tar.gz Patient_8 ictal
```
or

```
dataFeeder.py  ~/Downloads/clips.tar.gz Patient_8 interictal
```


processDir.py
-------------
point at an dir containing ictals, interictals, and training data.  It does 3 loops.  First loop it
goes through every interictal (in order) and calculates averages/standard deviations.  Second loop it goes through
each ictal file (again in order) and calculates how far each value is from the average on a variety of metrics, and
remembers the top 10 most different column and statistical metrics (by comparing the percentage it was off from the 
interictal files).  Finally, it goes through every file in the dir, and calculates how each of the 10 most interesting 
columns were, and saves those into a csv file with the following format:

filename, latency, column 1, column 2, ... column 9, column 10

It uses the following params

```
processDir.py inputDir outputbase

where inputDir is a dir described above.  outputbase is the base of the csv files it will create.  For example, if you
use "patient1_output", it will create two files, patient1_output_base.csv and patient1_output_perc.csv.  The base contains
the raw statistical values.  The perc contains how far off file results were from the average interictal values

