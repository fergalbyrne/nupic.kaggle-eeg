nupic.kaggle-eeg
================

swarm.py:  Does swarms on a mad.csv.  Basically, i used it to get a pretty simple model_params for run.py.
           I've tried a few variations of fields/columns to try and build the model, but the end results 
           were all similar enough to not warrant a lot of varieties.  I am contemplating a 2 column
           MAD.csv based on whether the electrodes are on left or right side of head.  This may give more
           consistent results.  More experimentation needed.

run.py     Takes a .mat file, extracts data and feeds it into nupic.  No need for intermidiatary .csv files.
           Prediction doesn't seem to work.  I plan on watching and replicating the anomoly examples to 
           see if that seems useful.

