#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
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
"""
Groups together code used for creating a NuPIC model and dealing with IO.
(This is a component of the One Hot Gym Prediction Tutorial.)
"""
import importlib
import sys
import csv
import datetime
import os
from collections import deque
from optparse import OptionParser
from os import listdir
from os.path import isfile, join

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

from scipy import io
import numpy as np

#pretty graphs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.dates import date2num



BUF_SIZE = 256 #Number of samples in ring buffer for computing stats
WINDOW=60
SECONDS_PER_STEP = 1

DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the input into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
MODEL_PARAMS_DIR = "model_params"
# '7/2/10 0:00'

#plot setup
plt.ion()
fig = plt.figure()
plt.ylabel('mad')
plt.xlabel('seconds')



def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "mad"})
  return model


def getModelParamsFromName(fileName):
  name = os.path.splitext(os.path.basename(fileName))[0]
  print "name: " + name
  importName = "model_params.%s_model_params" % (
    #fileName.replace(" ", "_").replace("-", "_")
    name.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % fileName)
  return importedModelParams



def runIoThroughNupic(model, dirName, plot):
  onlyfiles = [ f for f in listdir(dirName) if (isfile(join(dirName,f)) and "interictal" in f) ]
  #print onlyfiles

  outputFile = open('./foo.csv', "w")
  outputWriter = csv.writer(outputFile)


  actHistory = deque([0.0] * WINDOW, maxlen=60)
  predHistory = deque([0.0] * WINDOW, maxlen=60)

  actline, = plt.plot(range(WINDOW), actHistory)
  predline, = plt.plot(range(WINDOW), predHistory)

  actline.axes.set_ylim(0, 50)
  predline.axes.set_ylim(0, 50)


#    plotHeight = max(plotCount * 3, 6)
#    fig = plt.figure(figsize=(14, plotHeight))
#    gs = gridspec.GridSpec(plotCount, 1)
#    for index in range(len(self.names)):
#      self.graphs.append(fig.add_subplot(gs[index, 0]))
#      plt.title(self.names[index])
#      plt.ylabel('KW Energy Consumption')
#      plt.xlabel('Date')
#    plt.tight_layout()
#ax.plot([3.1, 2.2])

  plt.show()


  time = 0
  mad = []
  pred = []
  anomaly= []
  for f in onlyfiles:
    #open file
    data = io.loadmat(join(dirName, f))
    np.set_printoptions(threshold=np.nan)

    buf = np.zeros((BUF_SIZE,np.transpose(data['data']).shape[1]))

    i = 0
    for l_row in np.transpose(data['data']):
      buf[i,:] = l_row
      mad_row = np.mean(abs(buf[i]-np.mean(buf[i,:])))   #Mean Absolute Difference
      mad.append(mad_row)
      result = model.run({
        "mad": mad_row
      })

      print "result: " + repr(result)
      #pred.append(result.inferences["multiStepBestPredictions"][5])
      inference = (result.inferences["multiStepBestPredictions"][25])
      #anomaly.append( result.inferences['anomalyScore'])
      time+=1

      print time, repr(mad_row)
      print time, repr(result.inferences["multiStepBestPredictions"][25])
      print
      outputWriter.writerow([time, mad_row, inference, f])

      if inference is not None:
        actHistory.append(mad_row)
        predHistory.append(inference)

      actline.set_ydata(actHistory)  # update the data
      predline.set_ydata(predHistory)  # update the data


      plt.draw()
      plt.legend( ('actual','predicted') )

      i = (i+1)%BUF_SIZE
#      try:
#        plt.pause(SECONDS_PER_STEP)
#      except:
#        pass



    #plt.ioff()
  plt.show()
  outputFile.close()

def runModel(dirName, plot=False):
  print "Creating model from %s..." % dirName
  model = createModel(getModelParamsFromName("Universal"))
  runIoThroughNupic(model, dirName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]
  parser = OptionParser("%prog textfile [options]")
  if "--plot" in args:
    plot = True

  if not len(args):
    parser.print_help()
    print
    raise(Exception("textfile required"))

  runModel(args[0], plot=True)

#  runModel(GYM_NAME, plot=plot)

