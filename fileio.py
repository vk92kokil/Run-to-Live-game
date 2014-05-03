import base64
import sys
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
file_name = "hs.txt"
class File_Scorer():
	def check_file(self,pscore):
		flag = 0
		global file_name
		try:
			f1 = open(file_name,'r')
			self.enc_str = f1.read(64)
			f1.close()
			if(self.enc_str == ''):
				self.EMPTY_FILE = 1
				print self.enc_str
			else:
				try:
					self.hscore = int(base64.b64decode(self.enc_str))
					print "decoded"
				except:
					self.hscore = 0
				print "current high score is :"
				print self.hscore
				if(self.hscore < pscore):
					f3 = open(file_name,'w')
					f3.write(base64.b64encode(str(pscore)))
					f3.close()
					flag = 1
					print "written successfuly new high score"
				else:
					flag = -1
					print "your score is poor"
		except IOError:
			print "Error file not found"
			f2 = open(file_name,'w')
			f2.write('MA==')
			f2.close()
			print "new file created"
			self.check_file(pscore)
		return flag
	def get_high_score(self):
		try:
			f4 = open(file_name,'r')
			enc_str = f4.read(64)
			hscore = int(base64.b64decode(enc_str))
		except:
			hscore = 0
		self.check_file(-1)
		return self.hscore
	