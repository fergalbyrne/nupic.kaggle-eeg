import pyeeg
import csv
from operator import itemgetter

filename = 'dataAggOutput.csv'
reader = csv.reader(open(filename,'rb'),delimiter=',')

data = []

for line in reader:
	values = []
	for value in line[4:]:
		values.append(float(value))
	data.append( [float(line[0]) , line[1], line[2], line[3], values] )


'''
now values data has:
data[0] = sampling frequency
data[1] = ictal state
data[2] = channel 
data[3] = time series values
'''

binPowerResult = []

for record in data:
	binPowerResult.append([record[0], record[1], record[2], record[3], pyeeg.bin_power(record[4], range(3, 20), int(record[0])) ])

outputFile = open('binPowerOutput.csv','wb')
writer = csv.writer(outputFile)

binPowerResult = sorted(binPowerResult, key=itemgetter(3))

for result in binPowerResult:
	row = [str(result[0]), str(result[1]), result[2], result[3]]
	row.extend(str(value) for value in result[4][1])
	writer.writerow(row)

outputFile.close()