#!/usr/bin/env python

# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Aggregates all the mat files specified or the files contained in the directory 
to create a CSV of format 
frequency, ictal/interictal, channel, values...
USAGE:

dataAggregator.py OutputCSVfile PatientDirectory_or_file

"""

import numpy as np
import os
import glob
import csv
from scipy import io
from optparse import OptionParser
from scipy.stats import mode

DEBUG = False
def getData(matFile):

  data = io.loadmat(matFile)
  np.set_printoptions(threshold=np.nan)

  #list of channels
  dataset = {}
  channels = []
  for channel in data['channels'][0][0]:
    dataset[str(channel[0])] = []
    channels.append(str(channel[0]))
  if DEBUG:
    print 'channels : ',channels
    print "dataset : "
    print dataset
  
  #associated data information
  if DEBUG:
    print "freq: " + str(data['freq'])

  seizure=0  # False
  if "_ictal" in matFile:
    seizure=1

  #the actual data:
  channelIndex = 0
  for channeldata in data['data']:
    dataset[channels[channelIndex]].extend(channeldata)
    channelIndex += 1
  return {'sampleFrequency':data['freq'][0]  , 'dataset' : dataset , 'seizure' : seizure}

def initialize(outputFile, inputFile):
  filelist=[]
  if os.path.isdir(inputFile[0]):
    DIR = inputFile[0]
    if DIR[-1] != '/':
      DIR = DIR + '/'
    filelist.extend(glob.glob(DIR+"*_i*.mat"))
  else:
    filelist.extend(inputFile)

  outputFile = open(args[0], "w")

  outputWriter = csv.writer(outputFile)

  result = {} 
  print '************  ACCUMULATING DATA  *************'
  for matFile in filelist:      
    print "processing %s . . ." % (matFile)
    data = getData(matFile)
    dataset = data['dataset']
    if data['sampleFrequency'] in result:
        if data['seizure'] == 1:
            for channel in dataset.keys():
                if channel in result[data['sampleFrequency']]['ictal']:
                    result[data['sampleFrequency']]['ictal'][channel].extend(dataset[channel])
                else:
                    result[data['sampleFrequency']]['ictal'][channel] = dataset[channel]
        else:
            for channel in dataset.keys():
                if channel in result[data['sampleFrequency']]['interictal']:
                    result[data['sampleFrequency']]['interictal'][channel].extend(dataset[channel])
                else:
                    result[data['sampleFrequency']]['interictal'][channel] = dataset[channel]
    else:
        if data['seizure'] == 1:
            result[data['sampleFrequency']] = {'ictal':dataset, 'interictal':{}}
        else:
            result[data['sampleFrequency']] = {'ictal':{}, 'interictal':dataset}    

  print '************  WRITING DATA TO FILE  *************'
  for freq in result.keys():
      for ictalState in result[freq].keys():
          for channel in result[freq][ictalState].keys():
              row = [freq,ictalState, channel]
              row.extend(result[freq][ictalState][channel])
              outputWriter.writerow(row)
  
  outputFile.close()
  print '************  DATA ACCUMULATION COMPLETED  *************'

if __name__ == "__main__":
  parser = OptionParser("dataAggregator.py OutputCSVfile PatientDirectory_or_file")

  (options, args) = parser.parse_args()

  if len(args) != 2:
    parser.print_help()
    raise(Exception("dataAggregator.py OutputCSVfile PatientDirectory_or_file"))
  initialize(args[0],args[1:])