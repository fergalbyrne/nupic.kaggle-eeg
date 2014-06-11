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
import os
import glob
import csv
from scipy import io
from optparse import OptionParser

def analyze(filename):
  minVal,maxVal=100000.0,-100000.0

  data = io.loadmat(filename)
  np.set_printoptions(threshold=np.nan)

  #the actual data:
  for channelData in data['data']:
    minVal = min(channelData) if min(channelData) < minVal else minVal
    maxVal = max(channelData) if max(channelData) > maxVal else maxVal

  return minVal,maxVal


if __name__ == "__main__":
  parser = OptionParser("min_maxValue.py datafile [datafile...]")

  (options, args) = parser.parse_args()

  if len(args) < 1:
    parser.print_help()
    print
    raise(Exception("min_maxValue.py datafile [datafile...]"))

  filelist=[]
  if os.path.isdir(args[0]):
    DIR = args[0]
    if DIR[-1] != '/':
      DIR = DIR + '/'
    filelist.extend(glob.glob(DIR+"*.mat"))
  else:
    filelist.extend(args[:])

  minVal = 100000.0
  maxVal = -100000.0

  for matFile in filelist:
    result = analyze(matFile)
    minVal = result[0] if result[0] < minVal else minVal
    maxVal = result[1] if result[1] > maxVal else maxVal

  print "Min Value = ",minVal
  print "Max Value = ",maxVal
