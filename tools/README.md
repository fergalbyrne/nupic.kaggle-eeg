nupic.kaggle-eeg
================

Tools that may be helpful:  

`dataExaminer.py`: makes (sorta) pretty charts from the data. Arguments as follows:  

```
dataExaminer.py textfile electrode
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



