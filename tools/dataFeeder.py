#!/usr/bin/env python

import tarfile, os, glob, csv
from optparse import OptionParser


import numpy as np
from scipy import io
from optparse import OptionParser
import  datetime,time

current_time = datetime.datetime.now()

class dataFeeder:
	
	tar_file = str()
	tar = tarfile
	patient_name = str()
	clips_label = str()
	data_work_dir = 'data'

	#csv header for OPF
	h_chanels = ['timestamp']
	h_field_t = ['datatime']
	h_delimer = ['T']

	outputWriter = csv.writer
	outputFile = file

	def __init__(self,tar_file, patient, lable):
		self.tar_file = tar_file
		self.tar = tarfile.open(tar_file)
		self.patient_name = patient
		self.clips_label = lable

		if not os.path.exists(self.data_work_dir):
			os.makedirs(self.data_work_dir)

	def initCSV(self, ref_file_name):

		print ref_file_name
		memb=self.tar.getmember(ref_file_name)
		memb.name = os.path.basename(ref_file_name)
		self.tar.extract(memb,path=self.data_work_dir)

		data = io.loadmat(self.data_work_dir+'/'+memb.name)
  		np.set_printoptions(threshold=np.nan)

  		print "freq: " + str(data['freq'])
  		
  		parNum = 0 
  		for l_channel in data['channels'][0][0]:
  			self.h_chanels.append('P'+str(parNum))
  			self.h_field_t.append('float')
  			self.h_delimer.append ('')
  			parNum +=1
  		
  		self.outputFile = open(self.data_work_dir+'/'+self.patient_name+'_'+self.clips_label+'.csv', "w")
  		self.outputWriter = csv.writer(self.outputFile)

  		self.outputWriter.writerow(self.h_chanels)
  		self.outputWriter.writerow(self.h_field_t)
  		self.outputWriter.writerow(self.h_delimer)

  		#os.remove(self.data_work_dir+'/'+memb.name)



	def appendToCSV(self,mat_file_name):

		memb=self.tar.getmember(mat_file_name)
		memb.name = os.path.basename(mat_file_name)
		self.tar.extract(memb,path=self.data_work_dir)

		data = io.loadmat(self.data_work_dir+'/'+memb.name)
  		np.set_printoptions(threshold=np.nan)

  		for l_row in np.transpose(data['data']):    
		    ttime = current_time + datetime.timedelta(microseconds=float(0.0001) )
		    res = [ttime.strftime("%Y-%m-%d %H:%M:%S.%f").strip()] + list(l_row)
		    self.outputWriter.writerow(res)


  		os.remove(self.data_work_dir+'/'+memb.name)


	def run(self):

		fn_list = []
		tik_num = []
		for item in self.tar.getnames():
			if any(self.patient_name in s for s in  item.split('/') ) and any( self.clips_label in s for s in  item.split('/') ) :
				fn_list.append(item)
				tik_num.append( int( item.split('/')[-1].split('_')[-1].split('.')[0])-1 )
				
		tik_num = sorted(range(len(tik_num)), key=lambda k: tik_num[k])
		
		self.initCSV(fn_list[tik_num[0]])

		for i in tik_num:
			print fn_list[i].split('/')[-1]
			self.appendToCSV(fn_list[tik_num[i]])

		print 'done!'
		 	


if __name__ == "__main__":
  parser = OptionParser("dataFeader.py clip.tar.gz")

  (options, args) = parser.parse_args()

  print args

  if len(args) != 3:
    parser.print_help()
    print
    raise(Exception("dataFeader.py clip.tar.gz Patient_8 ictal"))

  df = dataFeeder(args[0], args[1], args[2])
  df.run()
  
  



  