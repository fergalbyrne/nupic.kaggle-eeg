import pyeeg
import csv

filename = 'test.csv'
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

spectralEntropyResult = []

bins = range(3,50)
bins.remove(5)
bins.remove(11)
bins.remove(23)
bins.remove(28)
bins.remove(47)


for record in data:
	spectralEntropyResult.append([ str(record[0]), str(record[1]), record[2], record[3], str(pyeeg.spectral_entropy(record[4], bins, int(record[0]))) ])

outputFile = open('spectralEntropyOutput.csv','wb')
outputWriter = csv.writer(outputFile)

for result in spectralEntropyResult:
	outputWriter.writerow( result )

outputFile.close()