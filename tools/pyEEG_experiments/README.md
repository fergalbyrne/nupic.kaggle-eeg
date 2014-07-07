#pyEEG experiments
==================================

This folder contains scripts that use the pyEEG module to process the raw data of Patient 7 and generated results and plots.

##blueprint

The folder blueprint contains all the scripts and folder constructs without any data. This will help you create experiments with different datasets. Just copy this folder and rename it to suit your need and perform the following steps.


>###Run dataAggregator.py
>>This file collects all the ictal and interictal records in the given folder or from the list of files specified to create a csv file on which all other scripts will operate.

>>```python dataAggregator.py OUTPUT_FILE [directory or file] [file...]```

>>You can use this to create samller data file for testing purpose also.

>###pyeeg.py
>>This is the modules used to generate frequency-power distribution, Detrended Fluctuation Analysis and Hjorth Fractal Dimension. There are many other properties like hurst(lenght of signal path compared to random walk) and spectral entropy. 

>>We use HFD, DFA and binPower.

>###pyeeg_binPower.py
>>This is the script that generates file binPowerOutput.csv with normalized power distributions of frequesncies from 3-18 Hz.

>###pyeeg_dfa.py
>>This is the script that generates file dfaOutput.csv with with the DFA value calculated for each time series in the dataAggOutput.csv file.

>###pyeeg_hfd.py
>>This is the script that generates file hfdOutput_kmax_<KMAX>.csv with with the HFD value calculated for each time series in the dataAggOutput.csv file.

>> The value of kmax can be changes in the python file to generate corresponding results. For this experiment we have used values 9, 25 and 50 as suggested by the research paper "Comparision of Fractal Dimension" by Polychronaki.

##Creating Plots of the processed data

To create the plots use the scripts plot.py in the folders pattern_hfd and pattern_dfa. These scripts will generate charts of latency vs value for indivisual as well as all channels.
```python plot.py```
