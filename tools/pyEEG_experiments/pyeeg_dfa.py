import pyeeg
import csv

filename = 'dataAggOutput.csv'
reader = csv.reader(open(filename,'rb'),delimiter=',')

data = []

for line in reader:
	values = []
	for value in line[4:]:
		values.append(float(value))
	data.append( [float(line[0]) , float(line[1]), line[2], line[3], values] )


'''
now values data has:
data[0] = sampling frequency
data[1] = ictal state
data[2] = channel 
data[3] = time series values
'''

dfaResult = []

for record in data:
	dfaResult.append([ str(record[0]), str(record[1]), record[2], record[3], str(pyeeg.dfa(record[4])) ])

outputFile = open('dfaOutput.csv','wb')
outputWriter = csv.writer(outputFile)

for record in dfaResult:
	outputWriter.writerow( record )

outputFile.close()