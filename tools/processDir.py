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

# to build data dir
# cp ../../kaggleData/Patient_1/Patient_1_*ictal*1* .


import os
import re
import csv
import numpy as np
from scipy import io
from optparse import OptionParser
from processFile import processFileHFD, processFileMin, processFileMax, processFileVariance, processFileMeanAbs, processFileKur, processFileVariance, processFileSkew, processFileBinPower
from processFile import maximum, mean, variance, hfd, binAlpha, binTheta, calcPerc



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

# why wait when i've already done it once:
#  #for each file, determine values for each algorithm
#  for filename in sorted(os.listdir (dirname), key=numericSort):
#    if "interictal" in filename:
#    #if "ictal" in filename:
#      print filename
#      data = io.loadmat(os.path.join(dirname, filename))
#      dataArrays = dataSplit(data['data'])
#      for i in range(0,10):
#        #print dataArrays[i].shape
#        maxArrayInterictal.append(maximum(np.absolute(dataArrays[i])))
#        meanArrayInterictal.append(mean(np.absolute(dataArrays[i])))
#        varArrayInterictal.append(variance(np.absolute(dataArrays[i])))
#        binAlphaArrayInterictal.append(binAlpha(dataArrays[i]))
#        binThetaArrayInterictal.append(binTheta(dataArrays[i]))
#        hfdArrayInterictal.append(hfd(dataArrays[i]))
#  interictalMax = repr(np.mean(maxArrayInterictal, axis=0))

  interictalMax = np.array([ 67.23762215,  73.48412301,  78.72853492,  68.86516637,
        54.70924147,  54.99514071,  60.59178654,  66.31650694,
        63.49467156,  82.19440027,  93.59124468,  75.15144114,
        62.74507536,  60.92095094,  62.24432559,  67.71792745])

  interictalMean = np.array([ 37.16170678,  39.86769196,  42.35656258,  37.15786066,
        29.33104384,  29.54007121,  32.99456758,  35.2581569 ,
        33.58022655,  44.35939825,  50.56035168,  43.02818189,
        33.01072935,  33.04674063,  33.15804139,  35.92467463])

  interictalVar = np.array([  390.82835292,   624.39043594,   715.77588938,   509.53096321,
         330.38851062,   343.07151699,   468.75966705,   615.82016453,
         321.18559878,   588.59305353,  1956.83318584,   694.96988964,
        1162.08335223,   525.87184165,   551.90237667,   790.69314864])

  interictalhfd = np.array([ 0.38882288,  0.37844547,  0.3480522 ,  0.35324316,  0.41821515,
        0.42897122,  0.44744992,  0.41847166,  0.35695054,  0.31923773,
        0.31175519,  0.3685185 ,  0.4024031 ,  0.4180439 ,  0.42729752,
        0.36643096])

  interictalBinAlpha = np.array([ 0.08689593,  0.08301133,  0.08140082,  0.08450645,  0.08688833,
        0.08384274,  0.08022712,  0.07711098,  0.09240069,  0.08264787,
        0.07764484,  0.07913176,  0.0839855 ,  0.08165858,  0.078732  ,
        0.07762398])

  interictalBinTheta = np.array([ 0.09243302,  0.09349234,  0.09432516,  0.09658505,  0.09281038,
        0.08843714,  0.08573612,  0.0838762 ,  0.10311281,  0.09507699,
        0.08978231,  0.1043497 ,  0.09215534,  0.08825326,  0.08342628,
        0.08533456])


  print
  #print "Max interictal mean/std: \n%s\n%s" %( repr(np.mean(maxArrayInterictal, axis=0)),  repr(np.std(maxArrayInterictal, axis=0)))
  print "Max interictal mean/std: \n%s" %(repr(interictalMax))
  print
  print "meanAbs interictal mean/std: \n%s" %(repr(interictalMean))
  print
  print "Var interictal mean/std: \n%s" %(repr(interictalVar))
  print
  print "hfd interictal mean/std: \n%s" %(repr(interictalhfd))
  print
  print "binAlpha interictal mean/std: \n%s" %(repr(interictalBinAlpha))
  print
  print "binTheta interictal mean/std: \n%s" %(repr(interictalBinTheta))

  #now for ictal (seizure)
  for filename in sorted(os.listdir (dirname), key=numericSort):
    #if "interictal" in filename:
    if "_ictal" in filename:
      print
      print filename
      print "###############"
      data = io.loadmat(os.path.join(dirname, filename))
      dataArrays = dataSplit(data['data'])

      #array for determining best 5 sensors
      sensorsPerc = np.zeros([6,dataArrays[0].shape[0]])

      #maxSensorsPerc = np.zeros(dataArrays[0].shape[0])
      #meanSensorsPerc = np.zeros(dataArrays[0].shape[0])
      #varSensorsPerc = np.zeros(dataArrays[0].shape[0])
      #hfdSensorsPerc = np.zeros(dataArrays[0].shape[0])
      #binAlphaSensorsPerc = np.zeros(dataArrays[0].shape[0])
      #binThetaSensorsPerc = np.zeros(dataArrays[0].shape[0])

      #for each 10th of the file
      for i in range(0,10):
        #print dataArrays[i].shape
        ictalMax = maximum(np.absolute(dataArrays[i]))
        ictalMean = mean(np.absolute(dataArrays[i]))
        ictalVar = variance(np.absolute(dataArrays[i]))
        ictalhfd = hfd(np.absolute(dataArrays[i]))
        ictalBinAlpha = binAlpha(np.absolute(dataArrays[i]))
        ictalBinTheta = binTheta(np.absolute(dataArrays[i]))

        maxPerc = calcPerc(ictalMax, interictalMax).clip(min=0)
        meanPerc = calcPerc(ictalMean, interictalMean).clip(min=0)
        varPerc = calcPerc(ictalVar, interictalVar).clip(min=0)
        #hfdPerc = calcPerc(ictalhfd, interictalhfd).clip(min=0)
        hfdPerc = calcPerc(ictalVar, interictalVar).clip(min=0)
        binAlphaPerc = calcPerc(ictalBinAlpha, interictalBinAlpha).clip(min=0)
        binThetaPerc = calcPerc(ictalBinTheta, interictalBinTheta).clip(min=0)

        #print "maxPerc: " + repr(maxPerc)
        #print "maxPerc: " + repr(maxPerc.clip(min=0))
        #print "meanPerc: " + repr(meanPerc)
        #print "varPerc: " + repr(varPerc)
        #print "hfdPerc: " + repr(varPerc)
        #print "binAlphaPerc: " + repr(varPerc)
        #print "binThetaPerc: " + repr(varPerc)
        #print

        sensorsPerc[0] = np.add(sensorsPerc[0], maxPerc)
        sensorsPerc[1] = np.add(sensorsPerc[1], meanPerc)
        sensorsPerc[2] = np.add(sensorsPerc[2], varPerc)
        sensorsPerc[3] = np.add(sensorsPerc[3], hfdPerc)
        sensorsPerc[4] = np.add(sensorsPerc[4], binAlphaPerc)
        sensorsPerc[5] = np.add(sensorsPerc[5], binThetaPerc)

        #maxSensorsPerc = np.add(maxSensorsPerc, maxPerc)
        #meanSensorsPerc = np.add(meanSensorsPerc, meanPerc)
        #varSensorsPerc = np.add(varSensorsPerc, varPerc)
        #hfdSensorsPerc = np.add(hfdSensorsPerc, hfdPerc)
        #binAlphaSensorsPerc = np.add(binAlphaSensorsPerc, binAlphaPerc)
        #binThetaSensorsPerc = np.add(binThetaSensorsPerc, binThetaPerc)

        #print "maxes; " + repr(np.argmax(maxPerc))
        #print "argsort; " + repr(np.argsort(maxPerc))

        #a winner
        #print "argsort; " + repr(np.argsort(maxPerc)[-1:-4:-1])
        #top5 = np.argsort(maxPerc)[-1:-6:-1]
        #print "top5: " + repr(top5)

        #bestSensorsMax[top5[0]] += 1
        #bestSensorsMax[top5[1]] += 1
        #bestSensorsMax[top5[2]] += 1
        #bestSensorsMax[top5[3]] += 1
        #bestSensorsMax[top5[4]] += 1

      #print maxSensorsPerc
      #print meanSensorsPerc
      #print varSensorsPerc
      #print "HFD" + repr(hfdSensorsPerc)
      #print binAlphaSensorsPerc
      #print binThetaSensorsPerc
      print sensorsPerc

      print "argsort: " + repr(np.argsort(sensorsPerc))

      print
        

        #determine Top 3 metrics for those 5 sensors
        #print "mean " + repr(mean(np.absolute(dataArrays[i])))
        #print "var " + repr(variance(np.absolute(dataArrays[i])))
        #print "binAlpha: " + repr(binAlpha(dataArrays[i]))
        #print "binTheta: " + repr(binTheta(dataArrays[i]))
        #print "hfd: " + repr(hfd(dataArrays[i]))

        #biggest_max = 0

  #
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

