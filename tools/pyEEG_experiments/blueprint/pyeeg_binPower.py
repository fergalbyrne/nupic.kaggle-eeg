import pyeeg
import csv
from operator import itemgetter

inputFile = open('dataAggOutput.csv','rb')
reader = csv.reader(inputFile,delimiter=',')

outputFile = open('binPowerOutput.csv','wb')
writer = csv.writer(outputFile)


binPowerResult = []
counter = 0
for line in reader:
	values = []
	for value in line[4:]:
		values.append(float(value))
	record = [float(line[0]) , line[1], line[2], line[3], values]
	binPowerResult.append([record[0], record[1], record[2], record[3], pyeeg.bin_power(record[4], range(3, 20), int(record[0])) ])
	counter+=1
	if counter%1000 == 0:
		print "%d rows have been processed" % counter

inputFile.close()


binPowerResult = sorted(binPowerResult, key=itemgetter(3))

for result in binPowerResult:
	row = [str(result[0]), str(result[1]), result[2], result[3]]
	row.extend(str(value) for value in result[4][1])
	writer.writerow(row)

outputFile.close()