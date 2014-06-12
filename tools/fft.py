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
from scipy.stats import scoreatpercentile as sap


BUF_SIZE = 256 #Number of samples in ring buffer for computing stats


def show_numpy(filename, electrode):
#  data = io.loadmat("data/Patient_1/Patient_1_interictal_segment_42.mat")

  print "filename: " + filename
  print "electrode: " + electrode

  data = io.loadmat(filename)
  np.set_printoptions(threshold=np.nan)

#  print data['data']

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

  dt = 1.0/float(data['freq'])  
  if "_ictal" in filename:
      print "latency: " + str(data['latency'])
      time = float(data['latency'])
      dclass = 1
  else:
      dclass = -1
      time = -1
      dt = 0

  buf = np.zeros((BUF_SIZE,np.transpose(data['data']).shape[1]))
  i = 0
  mad = []
  idc = []
  for l_row in np.transpose(data['data']):
      buf[i,:] = l_row
      row = np.zeros((l_row.shape[0]+4))
      row[0] = dclass
      row[1] = time
      row[2] = np.mean(abs(buf[i]-np.mean(buf[i,:]))) #Mean Absolute Difference
      row[3] = sap(buf,75)-sap(buf,25) #Interquartile Difference (All channels)
      row[4:] = l_row
      #outputWriter.writerow(row)
      mad.append(row[2])
      idc.append(row[3])
      print  str(l_row[int(electrode)]) + " : " + str(row[2])
      time += dt
      i = (i+1)%BUF_SIZE


  plt.plot(data['data'][int(electrode)], 'b')
  plt.plot(mad, 'r')
  plt.plot(idc, 'g')
  plt.title(str(data['channels'][0][0][int(electrode)]))
  plt.show()

  fourier = np.fft.fft(data['data'][int(electrode)])
  freq = np.fft.fftfreq(data['data'][int(electrode)].size)
  
  print repr(fourier)

  plt.plot(freq, fourier.real, freq, fourier.imag)
  plt.show()



if __name__ == "__main__":
  parser = OptionParser("dataExaminer textfile electrode")

  (options, args) = parser.parse_args()

  if len(args) != 2:
    parser.print_help()
    print
    raise(Exception("dataExaminer.py textfile electrode"))

  show_numpy(args[0], args[1])

