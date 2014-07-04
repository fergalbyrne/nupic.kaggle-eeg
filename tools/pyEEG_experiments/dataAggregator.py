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
specified.
USAGE:
	CSVHelper_Amplitudes.py csvfile file1.mat file2.mat ...
	or
	CSVHelper_Amplitudes.py csvfile directory

"""

import numpy as np
import os
import glob
import csv
from scipy import io
from optparse import OptionParser

DEBUG = False

def convertNumpyToCsv(outputWriter,filename):
  data = io.loadmat(filename)
  np.set_printoptions(threshold=np.nan)

  #list of channels
  channels = []
  for channel in data['channels'][0][0]:
    channels.append(str(channel[0]))
  print "channels: " + str(channels) 
  
  #associated data information
  print "freq: " + str(data['freq'][0])

  latency =0
  seizure=0  # False
  if "_ictal" in filename:
    latency = data['latency'][0]
    seizure=1
  print "latency: " + str(latency)

  channelIndex = 0
  for channelData in data['data']:
    state = 'ictal' if seizure == 1 else 'interictal'
    row = [ str(data['freq'][0]), str(latency), state , str(channels[channelIndex]) ]
    row.extend(channelData)
    if DEBUG:
      print row
    outputWriter.writerow( row )
    channelIndex = channelIndex +1


if __name__ == "__main__":
  parser = OptionParser("CSVHelper_Amplitudes.py csvfile datafile [datafile...]")

  (options, args) = parser.parse_args()

  if len(args) < 2:
    parser.print_help()
    print
    raise(Exception("CSVHelper_Amplitudes.py csvfile datafile [datafile...]"))

  filelist=[]
  if os.path.isdir(args[1]):
    DIR = args[1]
    if DIR[-1] != '/':
      DIR = DIR + '/'
    filelist.extend(glob.glob(DIR+"*.mat"))
  else:
    filelist.extend(args[1:])

  outputFile = open(args[0], "w")

  outputWriter = csv.writer(outputFile)

  for matFile in filelist:
    print "Preparing to output %s data to %s" % (matFile, args[0])
    convertNumpyToCsv(outputWriter, matFile)

  outputFile.close()