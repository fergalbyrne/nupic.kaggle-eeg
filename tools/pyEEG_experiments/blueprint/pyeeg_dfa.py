import pyeeg
import csv

'''
now values data has:
data[x][0] = sampling frequency
data[x][1] = latency
data[x][2] = ictal state
data[x][3] = channel 
data[x][4] = time series values
'''

filename = 'dataAggOutput.csv'
reader = csv.reader(open(filename,'rb'),delimiter=',')

outputFile = open('dfaOutput.csv','wb')
outputWriter = csv.writer(outputFile)

counter = 0
for line in reader:
	values = []
	for value in line[4:]:
		values.append(float(value))
	record = [float(line[0]) , float(line[1]), line[2], line[3], values]
	outputWriter.writerow([ str(record[0]), str(record[1]), record[2], record[3], str(pyeeg.dfa(record[4])) ])
	counter += 1
	if counter%1000 == 0:
		print "%d rows have been processed" % counter

outputFile.close()