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
# tools/preprocessor.py ../kaggleData/Patient_1/


import os
import re
import csv
import numpy as np
from scipy import io
from optparse import OptionParser
from processFile import processFileHFD, processFileMin, processFileMax, processFileVariance, processFileMeanAbs, processFileKur, processFileVariance, processFileSkew, processFileBinPower
from processFile import maximum, mean, variance, hfd, binAlpha, binTheta



def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


numbers = re.compile(r'(\d+)')
def numericSort(value):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def dataSplit(data):
  splitter = data.shape[1]/10
  newData = []

  #break array into 9 sections
  for i in range(0,9):
    #print (i*splitter), ((i+1) * splitter)
    #print np.transpose((np.transpose(data))[(i*splitter):(i+1) * splitter:1]).shape
    newData.append(np.transpose((np.transpose(data))[(i*splitter):(i+1) * splitter:1]))

  #put 10th section on the end
  #print (9*splitter), "INFInITY"
  #print np.transpose((np.transpose(data))[(9*splitter)::1])
  newData.append(np.transpose((np.transpose(data))[(9*splitter)::1]))

  #print repr(len(newData))

  return newData

def pickAlgorithms(dirname, outputCsv):
  maxArrayInterictal = []
  #maxArrayIctal = []
  meanArrayInterictal = []
  varArrayInterictal = []
  hfdArrayInterictal = []
  binAlphaArrayInterictal = []
  binThetaArrayInterictal = []

  #for each file, determine values for each algorithm
  for filename in sorted(os.listdir (dirname), key=numericSort):
    if "interictal" in filename:
    #if "ictal" in filename:
      print filename
      data = io.loadmat(os.path.join(dirname, filename))
      dataArrays = dataSplit(data['data'])
      for i in range(0,10):
        #print dataArrays[i].shape
        maxArrayInterictal.append(maximum(np.absolute(dataArrays[i])))
        meanArrayInterictal.append(mean(np.absolute(dataArrays[i])))
        varArrayInterictal.append(variance(np.absolute(dataArrays[i])))
        binAlphaArrayInterictal.append(binAlpha(dataArrays[i]))
        binThetaArrayInterictal.append(binTheta(dataArrays[i]))
      #should be in for loop, but it made things SLOW
      hfdArrayInterictal.append(hfd(dataArrays[i]))

  #now for ictal (seizure)
  for filename in sorted(os.listdir (dirname), key=numericSort):
    #if "interictal" in filename:
    if "_ictal" in filename:
      print filename
      data = io.loadmat(os.path.join(dirname, filename))
      dataArrays = dataSplit(data['data'])
      #for each 10th of the file
      for i in range(0,10):
        #print dataArrays[i].shape
        tmp_max = maximum(np.absolute(dataArrays[i]))
        biggest_max = 0
        for i in range (0. data['data'].shape[0])
          print "    max: " + np.amax(subtract(tmp_max, np.mean(maxArrayInterictal, axis=0))
          print

  #
  print
  print "Max interictal mean/std: %s\n/%s" %( repr(np.mean(maxArrayInterictal, axis=0)),  repr(np.std(maxArrayInterictal, axis=0)))
  print
  print "meanAbs interictal mean/std: %s\n/%s" %( repr(np.mean(meanArrayInterictal, axis=0)),  repr(np.std(meanArrayInterictal, axis=0)))
  print
  print "Var interictal mean/std: %s\n/%s" %( repr(np.mean(varArrayInterictal, axis=0)),  repr(np.std(varArrayInterictal, axis=0)))
  print
  print "hfd interictal mean/std: %s\n/%s" %( repr(np.mean(hfdArrayInterictal, axis=0)),  repr(np.std(hfdArrayInterictal, axis=0)))
  print
  print "binAlpha interictal mean/std: %s\n/%s" %( repr(np.mean(binAlphaArrayInterictal, axis=0)),  repr(np.std(binAlphaArrayInterictal, axis=0)))
  print
  print "binTheta interictal mean/std: %s\n/%s" %( repr(np.mean(binThetaArrayInterictal, axis=0)),  repr(np.std(binThetaArrayInterictal, axis=0)))

  #


def processDir(dirname, outputCsv):
#  data = io.loadmat("data/Patient_1/Patient_1_interictal_segment_42.mat")

  """ Sort the given list in the way that humans expect.
  """
  #l.sort(key=alphanum_key)
  #print repr(os.listdir(dirname))
  #full_list = []

  #outputFileMin = open(os.path.join(outputCsv, "min.csv"), "w")
  #outputWriterMin = csv.writer(outputFileMin)

  outputFileMax = open(os.path.join(outputCsv, "max.csv"), "w")
  outputWriterMax = csv.writer(outputFileMax)

  outputFileKur = open(os.path.join(outputCsv, "kur.csv"), "w")
  outputWriterKur = csv.writer(outputFileKur)

  outputFileSkew = open(os.path.join(outputCsv, "skew.csv"), "w")
  outputWriterSkew = csv.writer(outputFileSkew)

  outputFileVariance = open(os.path.join(outputCsv, "var.csv"), "w")
  outputWriterVariance = csv.writer(outputFileVariance)

  outputFileMeanAbs = open(os.path.join(outputCsv, "meanAbs.csv"), "w")
  outputWriterMeanAbs = csv.writer(outputFileMeanAbs)

  outputFileBinPowerDelta = open(os.path.join(outputCsv, "binPowDelta.csv"), "w")
  outputWriterBinPowerDelta = csv.writer(outputFileBinPowerDelta)

  outputFileBinPowerTheta = open(os.path.join(outputCsv, "binPowTheta.csv"), "w")
  outputWriterBinPowerTheta = csv.writer(outputFileBinPowerTheta)

  outputFileBinPowerAlpha = open(os.path.join(outputCsv, "binPowAlpha.csv"), "w")
  outputWriterBinPowerAlpha = csv.writer(outputFileBinPowerAlpha)

  outputFileBinPowerBeta = open(os.path.join(outputCsv, "binPowBeta.csv"), "w")
  outputWriterBinPowerBeta = csv.writer(outputFileBinPowerBeta)

  outputFileHFD = open(os.path.join(outputCsv, "hfd.csv"), "w")
  outputWriterHFD = csv.writer(outputFileHFD)

  #outputWriter.writerow( [ 
  #               "minimum",
  #               "maximum",
  #               "median",
  #               "average",
  #               "mean",
  #               "variance",
  #               "stdDev",
  #               "kurtosis",
  #               "skewness",
  #               "summation",
  #               "meanAbs"
  #           ])

  #interictals first, kinda stupid
  for filename in sorted(os.listdir (dirname), key=numericSort):
    if "interictal" in filename:
    #if "ictal" in filename:
      print filename
      data = io.loadmat(os.path.join(dirname, filename))
      #processFileMin(data, outputWriterMin)
      processFileMax(data, outputWriterMax)
      processFileKur(data, outputWriterKur)
      processFileSkew(data, outputWriterSkew)
      processFileBinPower(data, outputWriterBinPowerDelta, outputWriterBinPowerTheta, outputWriterBinPowerAlpha, outputWriterBinPowerBeta,data['freq'][0])
      processFileVariance(data, outputWriterVariance)
      processFileMeanAbs(data, outputWriterMeanAbs)
      processFileHFD(data, outputWriterHFD)

  #now for ictal (seizure)
  for filename in sorted(os.listdir (dirname), key=numericSort):
    #if "interictal" in filename:
    if "_ictal" in filename:
      print filename
      data = io.loadmat(os.path.join(dirname, filename))
      #processFileMin(data, outputWriterMin)
      processFileMax(data, outputWriterMax)
      processFileKur(data, outputWriterKur)
      processFileSkew(data, outputWriterSkew)
      processFileBinPower(data, outputWriterBinPowerDelta, outputWriterBinPowerTheta, outputWriterBinPowerAlpha, outputWriterBinPowerBeta,data['freq'][0])
      processFileVariance(data, outputWriterVariance)
      processFileMeanAbs(data, outputWriterMeanAbs)
      processFileHFD(data, outputWriterHFD)

  #outputFileMin.close()
  outputFileMax.close()
  outputFileKur.close()
  outputFileSkew.close()
  outputFileBinPowerDelta.close()
  outputFileBinPowerTheta.close()
  outputFileBinPowerAlpha.close()
  outputFileBinPowerBeta.close()
  outputFileVariance.close()
  outputFileMeanAbs.close()
  outputFileFileHFD.close()
  return

if __name__ == "__main__":
  parser = OptionParser("dataExaminer inputDir outputDir")

  (options, args) = parser.parse_args()

  if len(args) != 2:
    parser.print_help()
    print
    raise(Exception("dataExaminer.py inputDir outputDir"))

  #processDir(args[0], args[1])
  pickAlgorithms(args[0], args[1])

