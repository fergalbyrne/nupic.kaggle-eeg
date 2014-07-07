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

KMAX = 9

inputFile = open('dataAggOutput.csv','rb')
reader = csv.reader(inputFile,delimiter=',')

result = []

counter=0
for line in reader:
	values = []
	for value in line[4:]:
		values.append(float(value))
	record = [float(line[0]) , float(line[1]), line[2], line[3], values]

	result.append( [ str(record[0]), str(record[1]), record[2], record[3], str(pyeeg.hfd(record[4], KMAX)) ] )

	counter+=1
	if counter%1000 == 0:
		print "%d records processed" % counter

outputFile = open('hfdOutput_kmax_'+str(KMAX)+'.csv','wb')
outputWriter = csv.writer(outputFile)
for record in result:
	outputWriter.writerow( record )
outputFile.close()

inputFile.close()