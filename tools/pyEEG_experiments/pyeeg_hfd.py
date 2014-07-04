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
data[x][0] = sampling frequency
data[x][1] = ictal state
data[x][2] = channel 
data[x][3] = time series values
'''


hfd_result = []
K_MAX = 9
for record in data:
	hfd_result.append( [ str(record[0]), str(record[1]), record[2], record[3], str(pyeeg.hfd(record[4],K_MAX)) ] )
outputFile = open('hfdOutput_kmax_9.csv','wb')
outputWriter = csv.writer(outputFile)
for record in hfd_result:
	outputWriter.writerow( record )
outputFile.close()


hfd_result = []
K_MAX = 25
for record in data:
	hfd_result.append( [ str(record[0]), str(record[1]), record[2], record[3], str(pyeeg.hfd(record[4],K_MAX)) ] )
outputFile = open('hfdOutput_kmax_25.csv','wb')
outputWriter = csv.writer(outputFile)
for record in hfd_result:
	outputWriter.writerow( record )
outputFile.close()


hfd_result = []
K_MAX = 50
for record in data:
	hfd_result.append( [ str(record[0]), str(record[1]), record[2], record[3], str(pyeeg.hfd(record[4],K_MAX)) ] )
outputFile = open('hfdOutput_kmax_50.csv','wb')
outputWriter = csv.writer(outputFile)
for record in hfd_result:
	outputWriter.writerow( record )
outputFile.close()