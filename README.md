nupic.kaggle-eeg
================

Using NuPIC on EEG data to identify seizures - team entry for the Kaggle competition.

Data set generating
-------------------



dataFeeder.py - generats csv ready to use with OPF

extracts Patient_n_*.mat from tar.file then generate single csv formated for NuPic OPF. 
Fields names replaced to PN to be unified across any Patient_n. Number of columns takes from first Patient_n_*.mat file 

csv header example:

timestamp,P0,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15
datatime,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float
T,,,,,,,,,,,,,,,,


Usage varianst

dataFeeder.py Patient2.tar.gz Patient_2 ictal
dataFeeder.py Patient2.tar.gz Patient_2 interictal







