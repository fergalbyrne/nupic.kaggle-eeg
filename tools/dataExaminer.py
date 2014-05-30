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
from scipy import io
from optparse import OptionParser
import matplotlib.pyplot as plt

def show_numpy(filename, electrode):
#  data = io.loadmat("data/Patient_1/Patient_1_interictal_segment_42.mat")

  print "filename: " + filename
  print "electrode: " + electrode

  data = io.loadmat(filename)
  np.set_printoptions(threshold=np.nan)

  print data['data']

  #But also on metadata, like the headers:
  print
  print data['__header__']
  print

  print "shape: " + repr(data['data'].shape)
  print

  print "channels: " + repr(data['channels'])
  print

  print "freq: " + str(data['freq'])
  print

  if "_ictal" in filename:
    print "latency: " + str(data['latency'])
    print

  print "data[" + str(data['channels'][0][0][int(electrode)]) + "]: ", data['data'][int(electrode)]

  plt.plot(data['data'][int(electrode)], 'b')
  plt.title(str(data['channels'][0][0][int(electrode)]))
  plt.show()

if __name__ == "__main__":
  parser = OptionParser("dataExaminer textfile electrode")

  (options, args) = parser.parse_args()

  if len(args) != 2:
    parser.print_help()
    print
    raise(Exception("dataExaminer.py textfile electrode"))

  show_numpy(args[0], args[1])


