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


import numpy as np
import csv
from scipy import io
from optparse import OptionParser

def convertNumpyToCsv(filename, csvName):
  #data = io.loadmat("data/Patient_1/Patient_1_interictal_segment_42.mat")

  
  data = io.loadmat(filename)
  np.set_printoptions(threshold=np.nan)


  print "Preparing to output %s data to %s" % (filename, csvName)
  outputFile = open(csvName, "w")

  outputWriter = csv.writer(outputFile)

  #header row on csv
  l_channels = []
  for l_channel in data['channels'][0][0]:
    l_channels.append(str(l_channel[0]))
  #print "l_channels: " + str(l_channels)
  outputWriter.writerow(l_channels)
  
  #associated data information
  print "freq: " + str(data['freq'])
  if "_ictal" in filename:
    print "latency: " + str(data['latency'])


  #the actual data:
  #print "transpose: " + repr(np.transpose(data['data']))
  for l_row in np.transpose(data['data']):
    outputWriter.writerow(l_row)
    #print (repr(l_row))

  outputFile.close()

if __name__ == "__main__":
  parser = OptionParser("datatoCsv.py datafile csvfile")

  (options, args) = parser.parse_args()

  if len(args) != 2:
    parser.print_help()
    print
    raise(Exception("dataToCsv.py datafile csvfile"))


  convertNumpyToCsv(args[0], args[1])




