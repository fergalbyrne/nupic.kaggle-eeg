#!/usr/bin/env python

import tarfile, os
from optparse import OptionParser
import dataToCsv

patient_name = "Patient_8"
data_work_dir = "data"
clips_label = "ictal"

class dataFeeder:
	tar_file = str()
	tar = tarfile

	def __init__(self,tar_file, patient, lable):
		self.tar_file = tar_file
		self.tar = tarfile.open(tar_file)
		patient_name = patient
		clips_label = lable

	def next(self):
		next_item = tarfile.TarInfo
		for tarinfo in self.tar:
			next_item = self.tar.next()
			if any(patient_name in s for s in  next_item.name.split('/') ) and any( clips_label in s for s in  next_item.name.split('/') ) :
				break

		next_item.name = os.path.basename(next_item.name)
		self.tar.extract(next_item,path=data_work_dir)
		dataToCsv.convertNumpyToCsv(data_work_dir+'/'+next_item.name, data_work_dir+'/'+next_item.name+'.csv')
		#os.remove(data_work_dir+'/'+next_item.name) 
		
		return data_work_dir+'/'+next_item.name+'.csv'


if __name__ == "__main__":
  parser = OptionParser("dataFeader.py clip.tar.gz")

  (options, args) = parser.parse_args()

  if len(args) != 3:
    parser.print_help()
    print
    raise(Exception("dataFeader.py clip.tar.gz Patient_8 interictal"))

  df = dataFeeder(args[0], args[1], args[2])
  print df.next()
  
  



  