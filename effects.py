from panda3d.core import *
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from direct.task.Task import Task
from direct.directutil import Mopath
from direct.interval.MopathInterval import *
import sys
import Tkinter
offset_x = -504.0
offset_y = -86.0
offset_z = 0.0
def restrain(i, mn = -1, mx = 1): return min(max(i, mn), mx)
class Effects(ShowBase):
	def __init__(self):
		#ShowBase.__init__(self)
		
		#################fulscreen###############
		root = Tkinter.Tk()
		w = root.winfo_screenwidth()
		h = root.winfo_screenheight()
		props = WindowProperties() 
		props.setSize(w, h) 
		base.win.requestProperties(props)
		#################end####################3
		
		
		#camera.setPos(-500,-80,0)
		base.enableParticles()
		self.txt = ""
		self.p = ParticleEffect()
		
		st_x = 5.0 ####-515,-60,0
		st_y = 8.0
		st_z = 0.0
		
		
		self.c2 = Actor('Models/dancer/dancer')#Actor("Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve",{"run":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-run",	"jump":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-jump",	"offbalance":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-offbalance",	"tireroll":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-tireroll"})
		self.c2.setPos(offset_x+st_x,offset_y+st_y+7,offset_z+st_z)
		self.c2.reparentTo(render)
		self.c2.loadAnims({'win':'Models/dancer/dancer'})
		self.c2.loop('win')
		
		'''self.tex = Texture()
		self.tex.setMinfilter(Texture.FTLinear)
		base.win.addRenderTexture(self.tex, GraphicsOutput.RTMTriggeredCopyTexture)
		
		self.backcam = base.makeCamera2d(base.win, sort=-10)
		self.background = NodePath("background")
		self.backcam.reparentTo(self.background)
		self.background.setDepthTest(0)
		self.background.setDepthWrite(0)
		self.backcam.node().getDisplayRegion(0).setClearDepthActive(0)
		
		#taskMgr.add(self.takeSnapShot, "takeSnapShot")
		
		self.bcard = base.win.getTextureCard()
		self.bcard.reparentTo(self.background)
		self.bcard.setTransparency(1)
		self.fcard = base.win.getTextureCard()
		self.fcard.reparentTo(render2d)
		self.fcard.setTransparency(1)
		
		base.setBackgroundColor(0,0,0,1)
		self.bcard.hide()
		self.fcard.show()
		self.fcard.setColor(1.0,1.0,1.0,0.99)
		self.fcard.setScale(1.00)
		self.fcard.setPos(0,0,0)
		self.fcard.setR(0)
		self.clickrate = 30
		self.nextclick = 0'''
		
		self.c4 = Actor('Models/dancer/dancer')
		#self.c2.loadModel('Models/dancer/dancer')
		self.c4.setPos(offset_x-st_x,offset_y+st_y+7,offset_z+st_z)
		self.c4.reparentTo(render)
		self.c4.loadAnims({'win':'Models/dancer/dancer'})
		self.c4.loop('win')
		
		#self.c2.setR(-90)
		
		#self.c2.loop('tireroll')
		#base.setSleep(0.5)
		self.c3 = Actor("Models/cat-humans/bvw-f2004--ralph-egg/bvw-f2004--ralph/ralph")
		self.c3.setScale(2)
		self.c3.setPos(offset_x+0,offset_y+20,offset_z+(-1))
		self.c3.reparentTo(render)
		self.c3.listJoints()
		#self.c4.listJoints()
		self.actorRh = self.c3.controlJoint(None, 'modelRoot', 'RightShoulder')
		self.actorLh = self.c3.controlJoint(None, 'modelRoot', 'LeftShoulder')
		self.actorNeck = self.c3.controlJoint(None, 'modelRoot', 'Neck')
		
		self.actorNeck1 = self.c3.controlJoint(None, 'modelRoot', 'Neck')
		
		#self.actorNeck.hprInterval(3,Point3(0,90,0)).loop()
		self.actorLh.hprInterval(3,Point3(90,0,0)).loop()
		self.actorRh.hprInterval(3,Point3(0,0,-180)).loop()
		#self.actorRh.hprInterval(3,Point3(0,90,0)).loop()
		self.actorRh.setHpr(180,180,-60) # For Both hands upward
		self.actorLh.setHpr(90,-90,120)
		
		
		self.loadchar('','')
		self.duckPlane = loader.loadModel('Models/plane/plane')
		self.duckPlane.setPos(offset_x-2, offset_y+8, offset_z+10)         #set its position
		self.duckPlane.reparentTo(render)       #reparent to render
		self.duckPlane.setTransparency(1)
		self.duckTexs = self.loadTextureMovie(24, 'duck/duck_fly_left',
                                          'png', padding = 2)
		self.duckTask = taskMgr.add(self.textureMovie, "duckTask")
		self.duckTask.fps = 36
		self.duckTask.obj = self.duckPlane  
		self.duckTask.textures = self.duckTexs
		self.duckPlane.node().setEffect(BillboardEffect.makePointEye())
		
		self.expPlane = loader.loadModel('Models/plane/plane')  #load the object
		self.expPlane.setScale(18,10,10)
		self.expPlane.setPos(offset_x+0, offset_y+22, offset_z+4)                         #set the position
		self.expPlane.reparentTo(render)                      #reparent to render
		self.expPlane.setTransparency(1)                      #enable transparency

		self.expTexs = self.loadTextureMovie(50, 'explosion/def','png', padding = 4)
    #create the animation task
		self.expTask = taskMgr.add(self.textureMovie, "movieTask")
		self.expTask.fps = 30                                 #set framerate
		self.expTask.obj = self.expPlane                      #set object
		self.expTask.textures = self.expTexs                  #set texture list
		#self.expPlane.node().setEffect(BillboardEffect.makePointEye())
		
		
		self.c1 = loader.loadModel("Models/Dynamite/Dynamite")
		self.c1.setPos(offset_x-6,offset_y+10,offset_z+2)
		self.c1.reparentTo(render)
		
		self.expPlane1 = loader.loadModel('Models/plane/plane')  #load the object
		#self.expPlane1.setScale(1,10,10)
		self.expPlane1.setPos(offset_x-8, offset_y+10, offset_z+3)                         #set the position
		self.expPlane1.reparentTo(render)                      #reparent to render
		self.expPlane1.setTransparency(1)
		
		self.expTexs1 = self.loadTextureMovie(50, 'explosion1/explosion','png', padding = 4)
    #create the animation task
		self.expTask1 = taskMgr.add(self.textureExplosion, "explosionTask")
		self.expTask1.fps = 30                                 #set framerate
		self.expTask1.obj = self.expPlane1                      #set object
		self.expTask1.textures = self.expTexs1                  #set texture list
		self.expPlane1.node().setEffect(BillboardEffect.makePointEye())
		
		self.orientPlane = loader.loadModel('Models/plane/plane') #Load the object
		#self.orientPlane.setScale(1)
		self.orientTex = loader.loadTexture("Models/plane/textures/carpet.jpg")
		self.orientPlane.setTexture(self.orientTex, 1)        #Set the texture
		self.orientPlane.reparentTo(render)		#Parent to render
    #Set the position, orientation, and scale
		self.orientPlane.setPosHprScale(offset_x+0, offset_y+18, offset_z, 0, -90, 0, 20, 20, 20)

	def textureMovie(self, task):
		currentFrame = int(task.time * task.fps)
		task.obj.setTexture(task.textures[currentFrame % len(task.textures)], 1)
		return Task.cont
	def textureExplosion(self, task):
		currentFrame = int(task.time * task.fps)
		#print "curr  "
		#print currentFrame%51
		if((currentFrame%len(task.textures)) > 10):
			self.c1.hide()
		elif((currentFrame%len(task.textures)) <= 0):
			self.c1.show()
		task.obj.setTexture(task.textures[currentFrame % len(task.textures)], 1)
		return Task.cont
	def takeSnapShot(self, task):
		if (task.time > self.nextclick):
			self.nextclick += 1.0 / self.clickrate
			if (self.nextclick < task.time):
				self.nextclick = task.time
			base.win.triggerCopy()
		return Task.cont
	def loadTextureMovie(self, frames, name, suffix, padding = 1):
		return [loader.loadTexture((name+"%0"+str(padding)+"d."+suffix) % i) 
        for i in range(frames)]
	def loadchar(self,main_char,txt):
		self.txt = txt
		if(txt == ''):
			self.t = loader.loadModel("Models/DJTable/DJTable")
			self.t.setPos(offset_x+0,offset_y+20,offset_z)
			self.t.setH(180)
			self.t.reparentTo(render)
			self.setupLights()
			self.loadParticleConfig('fountain2.ptf')
		else:
			self.t = main_char#loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")#loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
			#self.t.setPos(0,20,0)
			#self.t.reparentTo(render)
			self.setupLights()
			self.loadParticleConfig('steam.ptf')
	def loadParticleConfig(self, file):
        #Start of the code from steam.ptf
		self.p.cleanup()
		self.p = ParticleEffect()
		if(self.txt == ''):
			self.txt = ''
			self.p.loadConfig(Filename(file))
			self.p.setPos(0.000, 0, 2.500)  
		elif(self.txt == 'blue'):
			self.txt = ''
			self.p.loadConfig(Filename('steam_front.ptf'))        
			self.p.setPos(0.000, -1.8, -0.800)
			
		elif(self.txt == 'red'):
			self.txt = ''
			self.p.loadConfig(Filename(file))
			self.p.setPos(0.000, 1.800, 0.250)
		self.p.start(self.t)
	def setupLights(self):
		ambientLight = AmbientLight("ambientLight")
		ambientLight.setColor(Vec4(.4, .4, .35, 1))
		directionalLight = DirectionalLight("directionalLight")
		directionalLight.setDirection(Vec3( 0, 8, -2.5 ) )
		directionalLight.setColor(Vec4( 0.9, 0.8, 0.9, 1 ) )
		
		self.t.setLight(self.t.attachNewNode(directionalLight))
		self.t.setLight(self.t.attachNewNode(ambientLight)) 
#w = Effects()
#run()