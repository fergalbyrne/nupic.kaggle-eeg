from __future__ import division

import csv
import numpy as np
import matplotlib.pyplot as plt
import pylab

KMAX=9
inputFile = open('hfdOutput_kmax_'+str(KMAX)+'.csv', 'rb')
csvreader = csv.reader(inputFile, delimiter=',')

'''
data
|------- latency
			|--------channel = [values...]

'''

data = {}
channels = []

for row in csvreader:
	#print row
	if row[2] == 'ictal':
		latency = float(row[1])
		channel = row[3]
		if channel not in channels:
			channels.append(channel)
		value = float(row[4])
		if latency in data.keys():
			if channel in data[latency].keys():
				data[latency][channel].append(value)
			else:
				data[latency][channel] = [value]
		else:
			data[latency] = {channel:[value]}

#print data
inputFile.close()

def plotChart(ch):
	y=[]
	x=[]
	plt.clf()
	for latency in data.keys():
		x.append(latency)
		values = data[latency][ch]
		y.append(sum(values)/len(values))

	plt.plot(x,y)
	plt.title('HFD avg. values vs latency, channel='+ ch+" at K max= "+str(KMAX))
	plt.xlabel('Latency')
	plt.ylabel('average HFD')
	plt.grid(True)
	pylab.savefig("HFD_"+ch+"_kmax"+str(KMAX)+".jpg",bbox_inches='tight')
	
def plotAllTogether(channelList):
	for ch in channelList:
		y=[]
		x=[]
		for latency in data.keys():
			x.append(latency)
			values = data[latency][ch]
			y.append(sum(values)/len(values))

		plt.plot(x,y)
	plt.title('HFD avg. values vs latency, all channel at K max= '+str(KMAX))
	plt.xlabel('Latency')
	plt.ylabel('average HFD')
	plt.grid(True)
	pylab.savefig("HFD_all_channels_kmax"+str(KMAX)+".jpg",bbox_inches='tight')
	plt.clf()

for ch in channels:
	plotChart(ch)

plotAllTogether(channels)