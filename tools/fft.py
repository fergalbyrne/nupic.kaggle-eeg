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
  dt = 1.0

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
      buf[i,:] = l_row
      row = np.zeros((l_row.shape[0]+3))
      row[0] = time
      row[1] = np.mean(abs(buf[i]-np.mean(buf[i,:]))) #Mean Absolute Difference
      row[2] = sap(buf,75)-sap(buf,25) #Interquartile Difference (All channels)
      row[3:] = l_row
      time_array.append(row[0])
      mad.append(row[1])
      idc.append(row[2])
      #print "%s,%s,%s" % ( str(row[1]) , str(row[2]) , str(row[3]))
      time += dt
      i = (i+1)%BUF_SIZE

      for element in l_row:
        if ylimMax < element:
          ylimMax = element
        if ylimMin > element:
          ylimMin = element

  print "ylim: " +  ylimMax + " : " + ylimMin

  colors = ['r', 'g', 'b', 'y', 'c', 'm', 'y', 'k',
            'a', 'd', 'e', 'f', 'h', 'i', 'n', 'p']

  plt.subplot(2, 1, 1)
  #left side
  plt.plot(time_array,data['data'][int(0)], 'b', color=colors[0])
  plt.plot(time_array,data['data'][int(1)], 'b', color=colors[1])
  plt.plot(time_array,data['data'][int(2)], 'b', color=colors[2])
  plt.plot(time_array,data['data'][int(3)], 'b', color=colors[3])

  plt.plot(time_array,data['data'][int(4)], 'b', color=colors[4])
  plt.plot(time_array,data['data'][int(5)], 'b', color=colors[5])
  plt.plot(time_array,data['data'][int(6)], 'b', color=colors[6])
  plt.plot(time_array,data['data'][int(7)], 'b', color=colors[7])

  #right side
  plt.subplot(2, 1, 2)
  plt.plot(time_array,data['data'][int(8)], 'b', color=colors[0])
  plt.plot(time_array,data['data'][int(9)], 'b', color=colors[1])
  plt.plot(time_array,data['data'][int(10)], 'b', color=colors[2])
  plt.plot(time_array,data['data'][int(11)], 'b', color=colors[3])

  plt.plot(time_array,data['data'][int(12)], 'b', color=colors[4])
  plt.plot(time_array,data['data'][int(13)], 'b', color=colors[5])
  plt.plot(time_array,data['data'][int(14)], 'b', color=colors[6])
  plt.plot(time_array,data['data'][int(15)], 'b', color=colors[7])

  plt.ylim(ylimMin, ylimMax)

  plt.title('all channels')
  plt.show()



  plt.subplot(2, 1, 1)
  plt.plot(time_array, mad, 'ko-')
  plt.title('A MAD/IDC comparison')
  plt.ylabel('MAD')

  plt.subplot(2, 1, 2)
  plt.plot(time_array, idc, 'r.-')
  plt.xlabel('time (s)')
  plt.ylabel('IDC')

  plt.show()


#  plt.plot(data['data'][int(electrode)], 'b')
#  plt.plot(mad, 'r')
#  plt.plot(idc, 'g')
#  plt.title(str(data['channels'][0][0][int(electrode)]))
#  plt.show()

  fourier = np.fft.fft(mad)

  freq = np.fft.fftfreq(len(mad))
  
  #print fourier.size

  #plt.plot(freq, fourier.real, freq, fourier.imag)
  #plt.show()



if __name__ == "__main__":
  parser = OptionParser("dataExaminer textfile")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.print_help()
    print
    raise(Exception("dataExaminer.py textfile"))

  show_numpy(args[0])

