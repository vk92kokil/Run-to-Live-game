from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import time
import threading
l = -2.5
r = 2.5
u = 0.8
d = -0.2
pl_name = "Player"
counter = 0.0
var = 0.0
class MyApp(ShowBase):
	def __init__(self):
		#ShowBase.__init__(self)
		#self.accept('enter', self.catchKeyPressed)
		global l,r,d,u
		self.timer = DirectLabel(text = "00:00:00",scale = 0.1,frameSize = (l,r,d-1,u+1),relief = None,text_fg=(1, 1, 0, 1))
		self.score = DirectLabel(text = "Score: 00",scale = 0.1,frameSize = (l,r,d-1,u+1),relief = None,text_fg=(1, 1, 0, 1))
		f6 = DirectFrame(pos = (-0.3,0,-0.1),frameColor = (0,0,255,1),parent = base.a2dTopRight,frameSize = (-0.1,0.1,-0.1,0.1),relief = None)
		f7 = DirectFrame(pos = (-0.3,0,-0.2),frameColor = (0,0,255,1),parent = base.a2dTopRight,frameSize = (-0.1,0.1,-0.1,0.1),relief = None)
		self.timer.reparentTo(f6)
		self.score.reparentTo(f7)
		
		self.timer.setY(5)
		#taskMgr.add(self.timerTask, 'timerTask')
	def dCharstr(self,theString):
		if len(theString) != 2:
			theString = '0' + theString
		return theString
	def setvar(self,val):
		global var
		var = val
	def getvar(self):
		global var
		return var
	def timerTask(self,task):
		global counter
		var = self.getvar()
		#counter += 1
		var = var+(3.0/60)
		self.setvar(var)
		secondsTime = int(var)
		minutesTime = int(secondsTime/60)
		hoursTime = int(minutesTime/60)
		self.timer['text'] = self.dCharstr(str(hoursTime)) + ':' + self.dCharstr(str(minutesTime%60)) + ':' + self.dCharstr(str(secondsTime%60))
		return Task.cont
	def rename(self):
		global l,r,d,u
		global pl_name
		self.name = DirectEntry(text = "" , pos = (-1.4,0,-0.8), scale=.1, initialText = pl_name, numLines = 1,frameColor= Vec4(10,10,10,10),width = 5)
	def newgame(self):
		taskMgr.add(self.timerTask, 'timerTask')
	def pause(self):
		print 1
	def quit(self):
		self.dest = YesNoDialog(text = "Are you sure you want to quit?",command = self.confirm)
	def confirm(self,clickedYes):
		self.dest.cleanup()
		if clickedYes:
			self.frame.destroy()
	def catchKeyPressed(self):
		global pl_name
		pl_name = self.name.get()
		self.name.destroy()
		#self.b5["text"] = pl_name
	def killobj(self):
		global counter,var
		counter = 0.0
		var = 0.0
		taskMgr.remove('timerTask')
		self.timer.destroy()
		self.score.destroy()