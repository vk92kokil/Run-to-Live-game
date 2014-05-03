from direct.gui.DirectGui import *
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from health import Health
class Effect(ShowBase):
	def __init__(self,ex):
		#ShowBase.__init__(self)
		#self.obj = Health()
		self.hbar = DirectWaitBar(text = "",range = 50,value = 0,barColor = (1,1,0,1) )
		self.frame = DirectFrame(pos = (0.3,0,0.4),frameColor = (0,0,255,1),parent = base.a2dBottomLeft,relief = None)
		self.hbar.reparentTo(self.frame)
		self.hbar.setHpr(0,0,270)
		
		self.hbar.setSx(0.17)
		self.hbar.setSz(0.5)
		self.ps = base.loader.loadSfx("media/")
		self.ps.setLoop(True)
		
	def setspeed(self,sp):
		self.ps.play()
		fl = sp * 1.0
		fl = fl/10.0
		self.hbar['value'] = fl
		self.playrate(fl)
	def playrate(self,sp):
		f2 = sp
		f2 = f2/5.0
		self.ps.setPlayRate(f2)
	def setVol(self,vol):
		self.ps.setVolume(vol)