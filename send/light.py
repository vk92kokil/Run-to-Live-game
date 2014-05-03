
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from panda3d.core import TextNode
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import Point3,Vec3,Vec4
from panda3d.core import Filename
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
import sys
from direct.showbase.ShowBase import ShowBase


class Light(ShowBase):
    def __init__(self):
        #Standard title and instruction text
		#ShowBase.__init__(self)
        #More standard initialization
        #self.accept('escape', sys.exit)
        #self.accept('1', self.loadParticleConfig , ['steam.ptf'])
        #self.accept('2', self.loadParticleConfig , ['dust.ptf'])
        #self.accept('3', self.loadParticleConfig , ['fountain.ptf'])
        #self.accept('4', self.loadParticleConfig , ['smoke.ptf'])
        #self.accept('5', self.loadParticleConfig , ['smokering.ptf'])
        #self.accept('6', self.loadParticleConfig , ['fireish.ptf'])
        
        #self.accept('escape', sys.exit)
        
		
		#camera.setPos(0,-20,2)
		#base.setBackgroundColor( 0, 0, 0 )

        #This command is required for Panda to render particles
		#base.disableMouse()
		base.enableParticles()
		
		#loader.loadModel("Models/models/ralph")
		#self.t.setPos(0,20,0)
		#self.t.reparentTo(render)
		self.txt = ""
		self.p = ParticleEffect()
		#self.loadchar('','')
		
    def loadchar(self,main_char,txt):
		self.txt = txt
		if(txt == 'blood'):
			self.t = main_char#loader.loadModel("Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve")
			#self.t.setPos(0,20,0)
			#self.t.reparentTo(render)
			self.setupLights()
			self.loadParticleConfig('fountain.ptf')
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
        
        #Sets particles to birth relative to the teapot, but to render at toplevel
        
        
        if(self.txt == 'blood'):
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
	#Setup lighting
    def setupLights(self):
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.4, .4, .35, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3( 0, 8, -2.5 ) )
        directionalLight.setColor(Vec4( 0.9, 0.8, 0.9, 1 ) )
		
        self.t.setLight(self.t.attachNewNode(directionalLight))
        self.t.setLight(self.t.attachNewNode(ambientLight))
#w = Light()
#run()