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
from processFile import processFileHFD, processFileMin, processFileMax, processFileVariance, processFileMeanAbs, processFileKur, processFileVariance, processFileSkew



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

  #outputFileHFD = open(os.path.join(outputCsv, "hfd.csv"), "w")
  #outputWriterHFD = csv.writer(outputFileHFD)

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
      processFileVariance(data, outputWriterVariance)
      processFileMeanAbs(data, outputWriterMeanAbs)
      #processFileHFD(data, outputWriterHFD)

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
      processFileVariance(data, outputWriterVariance)
      processFileMeanAbs(data, outputWriterMeanAbs)
      #processFileHFD(data, outputWriterHFD)

  #outputFileMin.close()
  outputFileMax.close()
  outputFileKur.close()
  outputFileSkew.close()
  outputFileVariance.close()
  outputFileMeanAbs.close()
  #outputFileFileHFD.close()
  return

if __name__ == "__main__":
  parser = OptionParser("dataExaminer inputDir outputDir")

  (options, args) = parser.parse_args()

  if len(args) != 2:
    parser.print_help()
    print
    raise(Exception("dataExaminer.py inputDir outputDir"))

  processDir(args[0], args[1])

