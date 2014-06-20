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
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import scoreatpercentile as sap


BUF_SIZE = 256 #Number of samples in ring buffer for computing stats


def show_numpy(filename):
#  data = io.loadmat("data/Patient_1/Patient_1_interictal_segment_42.mat")

  print "filename: " + filename

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

  #dt = 1.0/float(data['freq'])  
  dt = 1.0/float(data['freq'])


  print "dt: " + str(dt)
  print

  if "_ictal" in filename:
      print "latency: " + str(data['latency'])
      time = 0 - float(data['latency'])
  else:
      dclass = -1
      time = 0 


  buf = np.zeros((BUF_SIZE,np.transpose(data['data']).shape[1]))
  i = 0
  time_array = []
  mad = []
  idc = []
  ylimMax = 0
  ylimMin = 0
  for l_row in np.transpose(data['data']):
      #print "l_row: %s" % repr(l_row)
      buf[i,:] = l_row
      #print "buf: %s" % repr(buf)
      #print "idc: %s" % repr(sap(buf,75)-sap(buf,25))

      row = np.zeros((l_row.shape[0]+2))
      row[0] = time
      row[1] = np.mean(abs(buf[i]-np.mean(buf[i,:]))) #Mean Absolute Difference
      row[2:] = l_row
      time_array.append(row[0])
      mad.append(row[1])
      #print "%s,%s,%s" % ( str(row[1]) , str(row[2]) , str(row[3]))
      time += dt
      i = (i+1)%BUF_SIZE

      for element in l_row:
        if ylimMax < element:
          ylimMax = element
        if ylimMin > element:
          ylimMin = element

  #plot MAD and IDC
  plt.plot(time_array, mad, 'k')
  plt.ylabel('MAD')

  plt.show()

  #fun with fourier
  #fourier = np.fft.fft(data['data'][int(6)])/len(data['data'][int(6)])
  fourier = np.fft.fft(mad)/len(mad)

  #freq = np.fft.fftfreq(len(data['data'][int(6)]))
  freq = np.fft.fftfreq(len(mad))

  Fk = np.fft.fftshift(fourier)
  nu = np.fft.fftshift(freq)

  plt.subplot(2, 1, 1)
  plt.plot(nu, np.real(Fk))
  plt.subplot(2, 1, 2)
  plt.plot(nu, np.imag(Fk))

  plt.show()



if __name__ == "__main__":
  parser = OptionParser("dataExaminer textfile")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.print_help()
    print
    raise(Exception("dataExaminer.py textfile"))

  show_numpy(args[0])

