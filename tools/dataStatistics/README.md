#Data Statistics

###Data Aggregation
This piece of code aggregates all the .mat files to create a single csv file of the format:
```
Frequency, Seizure State, Channel, Values . . .

```

To aggregate files use the Python script 
```
python dataAggregator.py file [file...]
```

In case the file is a directory, all the ictal/interictal .mat files are combined.

###Data Analysis
Because of performance issues Pyhton was not used for this purpose.

Compile the Java file DataStatisticsHelper.java and run it on the aggregated file generated above.
```
javac DataStatisticsHelper.java
java DataStatisticsHelper AggregatedFile.csv [MAX THREADS]
```

By default the program uses 4 concurrent threads. The resultant file created is [CSV filename]_stats.csv