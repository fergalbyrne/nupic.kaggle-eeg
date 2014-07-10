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

# to run:
# tools/processFile.py ../kaggleData/Patient_1/Patient_1_ictal_segment_40.mat

import os
import numpy as np
from scipy import io, stats
from optparse import OptionParser
import pyeeg



def minimum(l_np):
#  print "min:  " + repr(np.amin(l_np, axis=1))
  return np.amin(l_np, axis=1)

def maximum(l_np):
#  print "max:  " + repr(np.amax(l_np, axis=1))
  return np.amax(l_np, axis=1)

def median(l_np):
#  print "median:  " + repr(np.median(l_np, axis=1))
  return np.median(l_np, axis=1)

def average(l_np):
#  print "avg:  " + repr(np.average(l_np, axis=1))
  return np.average(l_np, axis=1)

def mean(l_np):
#  print "mean:  " + repr(np.mean(l_np, axis=1))
  return np.mean(l_np, axis=1)

def variance(l_np):
#  print "variance:  " + repr(np.var(l_np, axis=1))
  return  np.var(l_np, axis=1)

def stdDev(l_np):
#  print "stdDev:  " + repr(np.std(l_np, axis=1))
  return np.std(l_np, axis=1)

def kurtosis(l_np):
#  print "kurtosis:  " + repr(stats.skew(l_np, axis=1))
  return stats.kurtosis(l_np, axis=1)

def skewness(l_np):
#  print "skewness:  " + repr(stats.kurtosis(l_np, axis=1))
  return stats.skew(l_np, axis=1)

def summation(l_np):
#  print "sum:  " + repr(np.sum(l_np, axis=1))
  return np.sum(l_np, axis=1)

def meanAbs(l_np):
#  print "meanAbs:  " + repr(np.mean(np.absolute(l_np),axis=1))
  return np.mean(np.absolute(l_np),axis=1)


def hfd(l_np):
  hfd_ret = np.zeros(l_np.shape[0])
  #print "size: " + repr(l_np.shape[0])
  #print
  for i in range(0,l_np.shape[0]):
    hfd_ret[i] = pyeeg.hfd(l_np[i], 9)
  return hfd_ret


def processFileMin(data, ow):
  ow.writerow(minimum(np.absolute(data['data'])))

def processFileMax(data, ow):
  ow.writerow(maximum(np.absolute(data['data'])))

def processFileKur(data, ow):
  ow.writerow(kurtosis(data['data']))

def processFileSkew(data, ow):
  ow.writerow(skewness(data['data']))

def processFileStdDev(data, ow):
  ow.writerow(stdDev(np.absolute(data['data'])))

def processFileVariance(data, ow):
  ow.writerow(variance(np.absolute(data['data'])))

def processFileHFD(data, ow):
  ow.writerow(hfd(data['data']))

def processFileBinPower(data, owDelta, owTheta, owAlpha, owBeta, freq):
  hfdDelta = np.zeros(data['data'].shape[0])
  hfdTheta = np.zeros(data['data'].shape[0])
  hfdAlpha = np.zeros(data['data'].shape[0])
  hfdBeta = np.zeros(data['data'].shape[0])
  #print "size: " + repr(l_np.shape[0])
  #print
  for i in range(0,data['data'].shape[0]):
    binPowerArray = pyeeg.bin_power(data['data'][i], [0.5,4,7,12,30], freq)
    hfdDelta[i]=(binPowerArray[1][0])
    hfdTheta[i]=(binPowerArray[1][1])
    hfdAlpha[i]=(binPowerArray[1][2])
    hfdBeta[i]=(binPowerArray[1][3])

  owDelta.writerow(hfdDelta)
  owTheta.writerow(hfdTheta)
  owAlpha.writerow(hfdAlpha)
  owBeta.writerow(hfdBeta)


def processFileStdDev(data, ow):
  ow.writerow(stdDev(np.absolute(data['data'])))

def processFileMeanAbs(data, ow):
  ow.writerow(meanAbs(data['data']))

def printProcessFile(filename, ow):

    print "filename: %s" % (filename)
  #full_list.append(os.path.join(filename, filename))
    data = io.loadmat(filename)
    np.set_printoptions(threshold=np.nan)

    print repr(np.mean(np.absolute(data['data']), axis=1))
    print repr(stdDev(np.absolute(data['data'])))
    print repr(hfd(data['data']))




if __name__ == "__main__":
  parser = OptionParser("dataExaminer filename")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.print_help()
    raise(Exception("dataExaminer.py filename"))

  printProcessFile(args[0], "na")

