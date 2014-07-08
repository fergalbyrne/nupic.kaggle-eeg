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
  l_array = []
  for i in range(0,data['data'].shape[0]):
    l_array.append(pyeeg.hfd(data['data'][i], 9))
  ow.writerow(l_array)

def processFileStdDev(data, ow):
  ow.writerow(stdDev(np.absolute(data['data'])))

def processFileMeanAbs(data, ow):
  ow.writerow(meanAbs(data['data']))

def printProcessFile(filename, ow):

    print "filename: %s" % (filename)
  #full_list.append(os.path.join(filename, filename))
    data = io.loadmat(filename)
    np.set_printoptions(threshold=np.nan)
#  for l_channel in data['channels'][0][0]:
#    print repr(l_channel)

    print "freq: " + str(data['freq'])
    if "_ictal" in filename:
        print "latency: " + str(data['latency'])

#  ow.writerow(minimum(data['data']))
#  ow.writerow(maximum(data['data']))
#  ow.writerow(median(data['data']))
#  ow.writerow(average(data['data']))
#  ow.writerow(mean(data['data']))
#  ow.writerow(variance(data['data']))
 # print "stddev: " + repr(stdDev(data['data']))
 # print "mean: " + repr(mean(data['data']))
  #ow.writerow(stdDev(data['data']))
#  ow.writerow(kurtosis(data['data']))
    print "kur: " + repr(kurtosis(data['data']))
    print "skew: " + repr(skewness(data['data']))
#  ow.writerow(skewness(data['data']))
#  ow.writerow(summation(data['data']))
#  ow.writerow(meanAbs(data['data']))

    print "variance-abs: " + repr(variance(np.absolute(data['data'])))
    print "stddev-abs: " + repr(stdDev(np.absolute(data['data'])))
    print "mean-abs: " + repr(meanAbs(data['data']))
    #print "binPower: " + repr(binPower(data['data']))
    l_column = 0
    print
    print
    print "hfd 0: " + repr(pyeeg.hfd(data['data'][0], 9))
    print "hfd 6: " + repr(pyeeg.hfd(data['data'][6], 9))
    print 
    print "hfd: " + repr(hfd(data['data']))


#  for l_channel in data['channels'][0][0]:
    #print repr(l_channel)
    #print l_column
    #print minimum(data['data'])
    #print minimum(data['data'])[0]

#    ow.writerow( [ minimum(data['data'])[l_column],
#                   maximum(data['data'])[l_column],
#                   median(data['data'])[l_column],
#                   average(data['data'])[l_column],
#                   mean(data['data'])[l_column],
#                   variance(data['data'])[l_column],
#                   stdDev(data['data'])[l_column],
#                   kurtosis(data['data'])[l_column],
#                   skewness(data['data'])[l_column],
#                   summation(data['data'])[l_column],
#                   meanAbs(data['data'])[l_column]
#                 ])


#    l_column+=1



if __name__ == "__main__":
  parser = OptionParser("dataExaminer filename")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.print_help()
    raise(Exception("dataExaminer.py filename"))

  printProcessFile(args[0], "na")

