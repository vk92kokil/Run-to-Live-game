from direct.gui.DirectGui import *
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.FunctionInterval import Func
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import *
from direct.task import Task
import time
cnt = 3000  
val = 0
class Start(ShowBase):
	def __init__(self):
		#ShowBase.__init__(self)
		l = 0.1
		r = 0.1
		self.l1 = OnscreenText(text="Ready!!", style=1, fg=(0,0,0,1), mayChange=1,pos=(0,0), align=TextNode.ALeft, scale = .3, shadow=(1,1,1,1), shadowOffset=(0.1,0.1))
		taskMgr.add(self.t1, 'timerTask')
	def t1(self,task):
		global cnt,val
		if(cnt>499):
			self.l1['text'] = str(cnt/500)
			cnt -= 40
		else:
			self.l1['text'] = "Go..."
			cnt -= 50
		if(cnt < 0):
			val = 1
			self.l1.destroy()
			taskMgr.remove('timerTask')
		print "check"+str(cnt)
		return Task.cont
	def retreat(self):
		return val