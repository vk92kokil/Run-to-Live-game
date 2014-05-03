from direct.gui.DirectGui import *
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
class Health(ShowBase):
	def __init__(self):
		#ShowBase.__init__(self)
		self.hbar = DirectWaitBar(text = "HP",range = 50,value = 50)
		self.frame = DirectFrame(pos = (0.2,0,0.8),frameColor = (0,0,255,1),parent = base.a2dBottomLeft,relief = None)
		self.hbar.reparentTo(self.frame)
		
		#self.hbar.reparentTo(ex.a2dBottomLeft)
		#self.hbar.setPos(-0.8,0,-0.5)
		self.hbar['barColor'] = (0,1,0,1)
		self.hbar.setHpr(0,0,270)
		self.hbar.setSx(0.5)
		self.hbar.setSz(0.5)
	def set_value(self,value):
		f2 = value * 1.0
		f2 = f2/2
		self.hbar['value'] = f2
		if(value > 10):
			self.hbar['barColor'] = (0,1,0,1)#set green
		else:
			self.hbar['barColor'] = (1,0,0,1)##set red