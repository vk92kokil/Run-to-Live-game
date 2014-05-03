from direct.gui.DirectGui import *
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from health import Health
class Effect(ShowBase):
	def __init__(self):
		#ShowBase.__init__(self)
		#self.obj = Health()
		self.hbar = DirectWaitBar(text = "Speed",range = 50,value = 0,barColor = (1,1,0,1))
		self.frame = DirectFrame(pos = (0.3,0,0.8),frameColor = (0,0,255,1),parent = base.a2dBottomLeft,relief = None)
		self.hbar.reparentTo(self.frame)
		self.hbar.setHpr(0,0,270)
		
		self.hbar.setSx(0.5)
		self.hbar.setSz(0.5)
		self.ps = base.loader.loadSfx("media/foot1.mp3")
		self.copter = base.loader.loadSfx("media/aeroplane.mp3")
		self.police = base.loader.loadSfx("media/police.wav")
		self.win = base.loader.loadSfx("media/win.ogg")
		self.ps.setLoop(True)
		self.police.setLoop(True)
		self.copter.setLoop(True)
	def setspeed(self,sp):
		#self.ps.play()
		fl = sp * 1.0
		fl = fl/6.0
		self.hbar['value'] = fl
		self.playrate(fl)
	def playrate(self,sp):
		f2 = sp
		f2 = f2/5.0
		#self.ps.setPlayRate(f2)
	def setVol(self,vol):
		self.ps.setVolume(vol)
		print 234
	def playplane(self,flag,vol):
		if(flag == 1):
			if self.copter.status() != self.copter.PLAYING:
				self.copter.play()
		elif(flag == 2):
			self.copter.stop()
		elif(flag == 3):
			self.copter.setVolume(vol)
	def playpolice(self,flag,vol):
		if(flag == 1):
			if self.police.status() != self.police.PLAYING:
				self.police.play()
		elif(flag == 2):
			self.police.stop()
		elif(flag == 3):
			self.police.setVolume(vol)
	def playwin(self,flag,vol):
		if(flag == 1):
			self.win.play()
		elif(flag == 2):
			self.win.stop()
		elif(flag == 3):
			self.win.setVolume(vol)