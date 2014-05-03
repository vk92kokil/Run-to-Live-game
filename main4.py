#import direct.directbase.DirectStart
#from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import sys
from panda3d.ai import *
from panda3d.core import loadPrcFileData
# Configure the parallax mapping settings (these are just the defaults)
loadPrcFileData("", "parallax-mapping-samples 3")
loadPrcFileData("", "parallax-mapping-scale 0.1")
from direct.gui.OnscreenText import OnscreenText
from direct.interval.FunctionInterval import Func
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import *
#from panda3d.core import Vec3,Vec4,BitMask32
from panda3d.core import Point3
from direct.gui.DirectGui import *
from direct.gui.DirectButton import DirectButton
from panda3d.core import WindowProperties
from panda3d.core import Filename,Shader
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.interval.ActorInterval import ActorInterval
import random
from panda3d.core import *
from pythongui import MyApp
from health import Health
from soundeffect import Effect
from start_timer import Start
from fileio import File_Scorer
from light import Light
#from gui import Menu
from pythongui import MyApp

import random, sys, os, math
score = 0
time1 = 0
click2 = 0
pauseflag = 0
l = -2.5
r = 2.5
u = 0.8
d = -0.2
click = 0
present_health = 100
toggle = True
first_time = 0
loadPrcFileData("", "audio-library-name p3openal_audio")
play_video = 0
cnt = 0
blood_cnt = 0
rules = "The Aim of this game is to collect maximum golden coins.\n"+ "You are a thief  and the Police of the city knows about you.\n"+"You have to collect those coins without getting caught from police." + "\n\nPress [Esc] for Main menu"
msg2 = "Run To Live"+"\n\n Under Professor Nitin Raje" +"\n\n Created by Vikramaditya Kokil\n Amit Agarwal \n Rajesh Kumar Gaur\n version 1.0.1"+ "\n Press [Esc] for Main menu"

class World(DirectObject):
 def __init__(self):
	#ShowBase.__init__(self)
	self.exbase = base
	global score,l,r,d,u
	#self.obj = MyApp()
	self.fileobj = File_Scorer()
	self.speed = 0
	self.throttle = 0
	self.maxSpeed = 300
	self.accel = 20
	self.handling = 30
	
	#self.focus = Vec3(55,-55,20)
	self.heading = 180
	self.pitch = 0
	self.mousex = 0
	self.mousey = 0
	self.last = 0
	self.floating=False
	self.ans = 0
	self.timeelapsed = 120
	
	base.setBackgroundColor(0.53,0.80,0.92)
	base.disableMouse()
	props = WindowProperties()
	#props.setCursorHidden(True)
	base.win.requestProperties(props)
	
	self.lm=[]
	self.aeroModel1 = []
	self.heartModel1 = []
	self.bikeModel1 = []
	self.treeModel1=[]
	self.heartCollider1=[]
	self.bikeCollider1=[]
	self.track = loader.loadModel("Models/CityTerrain/CityTerrain")
	self.track.reparentTo(render)
	self.track.setScale(1,1,1)
	self.track.setPos(0, 0, 0)
	#self.track.setP(-10)
	#######################video.py#####################################
	taskMgr.add(self.stop_movie, 'stop_movie')
	cm = CardMaker("plane")
	cm.setFrame(-1, 1, -1, 1)
	self.plane = render2d.attachNewNode(cm.generate())
	self.movie = loader.loadTexture("media/game01.avi")
	self.sound = loader.loadSfx("media/game01.avi")
	
	self.plane.setTexture(self.movie)
	self.plane.setTexScale(TextureStage.getDefault(), self.movie.getTexScale())
	self.movie.synchronizeTo(self.sound)
	self.sound.play()
	self.movie.play()
	######################end video.py##################################
	
	self.keyMap = {"w" : False,
					"s" : False,
					"a" : False,
					"d" : False,
					"cam-left":0, "cam-right":0,
					"space" : False,
					"mouse1" : False,
					"mouse3" : False}
	#taskMgr.add(self.cycleControl, "Cycle Control")
	#taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
	self.accept("w", self.setKey, ["w", True])
	self.accept("s", self.setKey, ["s", True])
	self.accept("a", self.setKey, ["a", True])
	self.accept("d", self.setKey, ["d", True])
	self.accept("w-up", self.setKey, ["w", False])
	self.accept("s-up", self.setKey, ["s", False])
	self.accept("a-up", self.setKey, ["a", False])
	self.accept("d-up", self.setKey, ["d", False])
	self.accept("arrow_left", self.setKey, ["cam-left",0])
	self.accept("arrow_right", self.setKey, ["cam-right",0])
	self.accept("arrow_left-up",self.setKey,["cam-left",1])
	self.accept("arrow_right-up",self.setKey,["cam-right",1])
	self.accept("space", self.setKey, ["space", True])
	self.accept("space-up", self.setKey, ["space", False])
	self.accept("mouse1", self.setKey, ["mouse1", True])
	self.accept("mouse1-up", self.setKey, ["mouse1", False])
	self.accept("mouse3", self.setKey, ["mouse3", True])
	self.accept("mouse3-up", self.setKey, ["mouse3", False])
	self.floater = NodePath(PandaNode("floater"))
	self.floater.reparentTo(render)
	#taskMgr.add(self.controlCamera, "Cam Control")
 def stop_movie(self, task):
		global cnt,play_video
		stop_time = 150
		if(self.sound.status() == AudioSound.PLAYING):
			print "Playing"
			cnt += 1
		if(cnt == stop_time):   #provide stop_time 
			
			print "Stopping"
			self.sound.stop()
			self.movie.stop()	
			play_video = 1
			taskMgr.remove('stop_movie')
			self.b6 = DirectButton(text = "Go!!",scale = 0.5,pos = Vec3(0,0,0),frameSize = (-4,4,-1,1),relief = None,clickSound = None,command = self.loadmenu)
			#self.loadmenu()
		return task.cont
 def loadmenu(self):
		global msg2,rules
		#self.plane.setTexture(None)
		self.imageObject = OnscreenImage(image = 'images/back.jpg', pos = (0, 0, 0),scale = (2.0,1,1))
		self.title = self.addTitle("Welcome to my Game")
		self.inst1 = self.addInstructions(0.95,"N: New Game")
		self.inst2 = self.addInstructions(0.88,"R: Rules")
		self.inst3 = self.addInstructions(0.81,"Q: Quit")
		self.inst4 = self.addInstructions(0.74,"I: About")
		self.accept('N', self.newgame1)
		self.accept('n', self.newgame1)
		self.accept('R', self.rule1,extraArgs = [rules])
		self.accept('r', self.rule1,extraArgs = [rules])
		self.accept('Q', self.quit1)
		self.accept('q', self.quit1)
		self.accept('i', self.rule1,extraArgs = [msg2])
		self.accept('I', self.rule1,extraArgs = [msg2])
		self.accept('escape', self.loadmenu)
		self.b6.destroy()
		#self.accept('escape', self.loadmenu)
 def addInstructions(self,pos, msg):
		return OnscreenText(text=msg, style=1, fg=(0,0,0,1), mayChange=1,
			pos=(0,pos-0.6), align=TextNode.ACenter, scale = .08, shadow=(1,1,1,1), shadowOffset=(0.1,0.1))
 def addTitle(self,text):
		return OnscreenText(text=text, style=1, fg=(0,0,0,1),
                        pos=(0,0.6), align=TextNode.ACenter, scale = .2, shadow=(1,1,1,1), shadowOffset=(0.05,0.05),)
 def addcontrols(self,x,z,msg):
		return OnscreenText(text=msg, style=1, fg=(0,1,1,1), mayChange=1,
			pos=(x,z), align=TextNode.ALeft, scale = .05)
 def newgame1(self):
		#print "new game start"
		self.title.hide()
		self.inst1.hide()
		self.inst2.hide()
		self.inst3.hide()
		self.inst4.hide()
		#self.imageObject.destroy()
		self.ignore('R')
		self.ignore('r')
		self.ignore('N')
		self.ignore('n')
		self.ignore('Q')
		self.ignore('q')
		self.ignore('escape')
		self.waitlabel = DirectLabel(text = "Please wait...",pos = Vec3(0,0,-0.2),relief = None,scale = 0.12,frameColor = (0,0,0,1))
		self.waitBar = DirectWaitBar(text = "",range = 100,value = 0,pos = Vec3(0, 0, -0.3),barColor = (0.3,1,0.4,2))
		
		self.waitBar.setSx(1)
		self.waitBar.setSz(0.1)
		#self.obj = MyApp()
		
		inc = Func(self.loadStep)
		show = Func(self.finishbar)
		gamecall = Func(self.gamecall)
		
		#load = Sequence(Wait(1+random.random()), inc, Wait(random.random()), inc, Wait(random.random()),			inc,Wait(random.random()), inc,Wait(random.random()),inc,Wait(random.random()),inc,Wait(random.random()),inc,Wait(random.random()),inc,inc,Wait(random.random()),inc,show)
		load = Sequence(inc,Wait(1+random.random()), inc, Wait(random.random()), inc, Wait(random.random()),inc,show)
		load.start()
		#self.finishbar()
 def loadStep(self):
		self.waitBar["value"] += 25
 def finishbar(self):
		self.waitlabel['frameColor'] = (0,0,1,1)
		print "Finished job!!"
		self.waitlabel['text'] = "Ready!!"
		self.plane.remove()
		self.imageObject.destroy()
		self.waitBar.destroy()
		self.waitlabel.destroy()
		self.chalukaro()
		
 def gamecall(self):
		self.call = Application()
		self.call.run()
 def rule1(self, m):
		global rules
		#print "show rules"
		#self.inst1.destroy()
		self.inst1['text'] = ""
		self.inst2['text'] = ""
		self.inst3['text'] = ""
		self.inst4["text"] = m
		self.accept('escape',self.showmenu)
		self.accept('m',self.showmenu)
 def showmenu(self):
		self.inst1['text'] = "N: New Game"
		self.inst2['text'] = "R: Rules"
		self.inst3['text'] = "Q: Quit"
		self.inst4['text'] = "I: About"
		
 def quit1(self):
		self.q2 = YesNoDialog(text = "Do you really want to quit",command = self.exit)
 def exit(self,clickedYes):
		self.q2.cleanup()
		if clickedYes:
			sys.exit()
	
 def setKey(self, key, value):
	self.keyMap[key] = value
 
 def check_health(self,h):
	global score
	flg = -1
	if(h <= 0):
	##DIE##
		flg = self.fileobj.check_file(score)
		if(flg == -1):
			msg = "Your score: " + str(score) +"$"
		else:
			self.speedobj.playwin(1,0)
			msg = "High score: " + str(score) +"$"
		self.gameover = OnscreenText(text= "Game Over", style=1, fg=(0,0,0,1),bg = (1,1,0,1),
                        pos=(0,0.5), align=TextNode.ARight, scale = .1, shadow=(1,1,1,1), shadowOffset=(0.05,0.05))
		self.show_score = OnscreenText(text= msg, style=1, fg=(0,0,0,1),bg = (1,1,0,1),
                        pos=(0,0.3), align=TextNode.ARight, scale = .1, shadow=(1,1,1,1), shadowOffset=(0.05,0.05))
		self.pausekaro('die')
		taskMgr.remove('scorer')
		taskMgr.remove('catch')
		self.goback = DirectButton(text = "Click here to go to Main Menu",scale = 0.06,pos = Vec3(0,0,0),frameSize = (-8,8,-0.6,1.4),command = self.clearscreen,relief = None)
 def clearscreen(self):
	global pauseflag
	self.goback.destroy()
	self.gameover['text'] = ''
	self.show_score['text'] = ''
	self.speedobj.playwin(2,0)
	self.destroy1()
	pauseflag = 0
	self.loadmenu()
#		self.loadmenu()
 def rst(self):################calls when restart
	self.pausekaro('restart')
	#self.b2['state'] = DGG.DISABLED
	self.cnf2 = YesNoDialog(text = "Do you want to restart the game anyway?",command = self.confirm2)
 def confirm2(self,ClickedYes):
	self.cnf2.cleanup()
	if(ClickedYes):
		self.destroy1()
		#self.b2['state'] = DGG.NORMAL
		self.chalukaro()
	else:
		self.resume()
		#self.b2['state'] = DGG.NORMAL
 def cycleControl(self, task):
	dt = globalClock.getDt()
	ans=1
	startpos = self.cycle.getPos()
	if( dt > .20):
		return task.cont
	if(self.keyMap["w"] == True):
		#self.cycle.setY(self.cycle, -10 * dt)
		self.throttle = 1
		print(self.cycle.getPos())
	elif(self.keyMap["s"] == True):
		self.throttle = -1
		arg = self.speed
		#print(self.speed,arg)
		#self.speed= .7*arg
	else:
		#print(self.speed)
		self.throttle = 0
		#self.cycle.loop("start")
		
	if(self.keyMap["d"] == True):
		self.turn("r", dt)
		#print(self.cycle.getPos())
	elif(self.keyMap["a"] == True):
		self.turn("l", dt)
	if(self.keyMap["space"] == True and self.cycle.getZ()==0):
		self.floating = False
		#self.cycle.loop("jump")
	elif(self.keyMap["space"] == True and self.cycle.getZ()!=0):
		self.cycle.setZ(0)
		self.floating = False
	if(self.keyMap["mouse1"] == True):
		self.cameraZoom("in", dt)
	elif(self.keyMap["mouse3"] == True):
		self.cameraZoom("out", dt)
	
	self.speedCheck(dt)
	self.move(dt)
	self.jump(dt)
	#print(dt)
	base.camera.lookAt(self.cycle)
	if (self.keyMap["cam-left"]!=0):
		base.camera.setX(base.camera, -40 * dt)
	if (self.keyMap["cam-right"]!=0):
		base.camera.setX(base.camera, +40 * dt)
	
	camvec = self.cycle.getPos() - base.camera.getPos()
	camvec.setZ(0)
	camdist = camvec.length()
	camvec.normalize()
	if (camdist > 10.0):
		base.camera.setPos(base.camera.getPos() + camvec*(camdist-30))#10
		camdist = 30.0
	if (camdist < 5.0):
		base.camera.setPos(base.camera.getPos() - camvec*(20-camdist))#5
		camdist = 20.0
	
	#startpos = self.cycle.getPos()
	
	self.cTrav.traverse(render)
	entr = []
	#for k in range(self.collisionHandler.getNumEntries()):
		#print(self.cycle.getPos())
		#entry = self.collisionHandler.getEntry(i)
		#entr.append(entry)
	
	
	entries = []
	for i in range(self.ralphGroundHandler.getNumEntries()):
		#print(self.cycle.getPos())
		entry = self.ralphGroundHandler.getEntry(i)
		entries.append(entry)
		#print(entries[i])
	entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
	if (len(entries)>0) and ((entries[0].getIntoNode().getName() == "CityTerrain") or (entries[0].getIntoNode().getName() == "wide_ramp")or (entries[0].getIntoNode().getName() == "rail_ramp") or (entries[0].getIntoNode().getName() == "bridge")):
		#print("if me")
		self.cycle.setZ(entries[0].getSurfacePoint(render).getZ())
	else:
		#print(entries[0].getIntoNode().getName())
		#entries[0].getIntoNode().getName().removeNode()
		#if((entries[0].getIntoNode().getName() == "collidera")):
			#print("maa ki chut")
		if((entries[0].getIntoNode().getName() != "collider") and (entries[0].getIntoNode().getName() != "colliderbike") and (entries[0].getIntoNode().getName() != "colliderpara") and (entries[0].getIntoNode().getName() != "collidermag") and (entries[0].getIntoNode().getName() != "collidera")):
			self.speed=0
			self.cycle.setPos(startpos)
		
	
	entries = []
	for i in range(self.camGroundHandler.getNumEntries()):
		#print("1");
		entry = self.camGroundHandler.getEntry(i)
		entries.append(entry)
	entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
	if (len(entries)>0) and ((entries[0].getIntoNode().getName() == "CityTerrain") or (entries[0].getIntoNode().getName() == "wide_ramp") or (entries[0].getIntoNode().getName() == "rail_ramp") or (entries[0].getIntoNode().getName() == "bridge") ):
		base.camera.setZ(entries[0].getSurfacePoint(self.track).getZ()+3.0)#1
		#print("idhar",entries[0].getSurfacePoint(self.track))
	if (base.camera.getZ() < self.cycle.getZ() + 4.0):#2
		base.camera.setZ(self.cycle.getZ() + 4.0)#2
		#print("udhar" )
	if (base.camera.getZ() > self.cycle.getZ() + 4.0):#2
		base.camera.setZ(self.cycle.getZ() + 4.0)#2
		#print("idhar")
	self.floater.setPos(self.cycle.getPos())
	self.floater.setZ(self.cycle.getZ() + 4.0)#2
	base.camera.lookAt(self.floater)
	return task.cont
	
 def debugTask(self, task):
	#print(taskMgr)
	taskMgr.removeTasksMatching("Cycle Move *")
	return task.again
 def speedCheck(self, dt):
	tSetting = (self.maxSpeed * self.throttle)
	self.speedobj.setspeed(self.speed)
	if(self.speed < tSetting):
		if((self.speed + (self.accel * dt)) > tSetting):
			self.speed = tSetting
		else:
			self.speed += (self.accel * dt)
	elif(self.speed > tSetting):
		if((self.speed - (self.accel * dt)) < tSetting):
			self.speed = tSetting
		else:
			self.speed -= (2*self.accel * dt)
 def move(self, dt):
	
	mps = self.speed * 1000 / 3600
	if(mps!=0):
		self.cycle.setY(self.cycle, -mps * dt)
	else:
		if(self.speed==0):
			self.cycle.setLightOff()
  
		self.cycle.loop("run")
	
 def turn(self, dir, dt):
	turnRate = self.handling * (2 -(self.speed / self.maxSpeed))
	if(dir == "r"): 
		turnRate = -turnRate
		self.cycle.setH(self.cycle.getH() - 40 *dt)
	if(dir == "l"):
		#turnRate = -turnRate
		self.cycle.setH(self.cycle.getH() + 40 * dt)
	#self.cycle.setH(self.cycle, turnRate * dt)
 def onCollision(self, entry):
	vel = random.uniform(0.01, 0.2)
	self.cycle.setPythonTag("velocity", vel)	
 def cycleMove(self, task):
	self.env10.setY(self.env10, .05)
	#print(taskMgr)
	return task.cont
 def restart1(self, task):
	self.pandaActor.setY(self.pandaActor,0.05)
	return task.cont
 def cycleMove1(self, task):
	self.pandaActor.reparentTo(self.track)
	#print(taskMgr)
	return task.done
 def makeenv(self, task):
	#ans=0
	#timeelapsed=5
	
	dt = globalClock.getDt()
	#print("self.elapsed",self.timeelapsed,dt)
	
	if(self.ans <= self.timeelapsed):
		self.env16.detachNode()
		self.env17.reparentTo(self.track)
		self.ans = self.ans+dt
		#print("if me",self.ans,dt)
		
	elif(self.ans<(self.timeelapsed+125)):
		#print("else me",self.ans,dt)
		self.env17.detachNode()
		self.env16.reparentTo(self.track)
		
		self.ans = self.ans+dt
		if(self.ans>= (self.timeelapsed+125)):
			self.ans=0
	return task.cont	
 def collideEventIn(self, entry):
  #print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
  global score
  score = score + 1
  self.pointsound()
  #self.bt["text"] = str(score)
  
  self.obj.score["text"] = "Score: "+str(score)+"$"
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  # we now may change the aspect of the two colliding objects
  colliderINTO.setColor(1,1,1,1)
  #colliderFROM.setScale(6.0045)
  #print(entry.getFromNodePath().getParent())
  self.cycle.setLight(self.ambientNP)
  colliderFROM.setY(colliderFROM,1.15)
  colliderFROM.setX(colliderFROM,1.30)
  colliderFROM.setZ(100.30)
  #print(colliderFROM.getZ())
 def bikecollideEventIn(self, entry):
  #print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
  self.cycle.setLight(self.ambientNP1)
  self.pandaActor2.setPos(self.cycle.getPos()+Vec3(40,40,0))
  self.setAI(self.pandaActor2)
  self.speed=0
  self.jump1()
  global present_health,pauseflag
  if(pauseflag == 0):
	present_health = present_health - 19
  self.healthobj.set_value(present_health)
  self.check_health(present_health)
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  if(present_health < 0):
		self.cycle.detachNode()
		self.b2.hide()
		self.b3.hide()
		self.b4.hide()
		self.b5.hide()
		self.healthobj.hbar.hide()
		self.speedobj.hbar.hide()
  # we now may change the aspect of the two colliding objects
  
 def paracollideEventIn(self, entry):
  #print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  #self.cur = score
  #taskMgr.add(self.hawame, "hawame") 
 def paracollideEventOut(self, entry):
  #print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  taskMgr.add(self.hawame, "hawame") 
 def magcollideEventIn(self, entry):
  #print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  #self.cur = score
  #taskMgr.add(self.hawame, "hawame") 
 def magcollideEventOut(self, entry):
  #print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  #print("aa gaya")
  #for i in range(len(self.heartModel1):
	#if((abs(self.cycle.getX() -self.heartModel[i].getX()) <= 20) and (abs(self.cycle.getY()-self.heartModel[i].getY())>=20)):
		#self.heartModel[i].setPos(self.cycle.getPos())
		
  #taskMgr.add(self.collectkaro, "collectkaro") 
 def collectkaro(self, task):
	global score
	for i in range(len(self.heartModel1)):
		if(score>self.cur+10):
			#print("idhar aa gaya")
			#self.heartModel1[i].detachNode()
			return task.done
		
		if(((abs(abs(self.cycle.getX())) -(abs(self.heartModel1[i].getX()))) <= 200) and ((abs((abs(self.cycle.getY()))-(abs(self.heartModel1[i].getY()))))<=200) ):
			#print("idhar collect karna chaiye",i,self.heartModel1[i].getPos())
			self.heartModel1[i].setZ(4)
			self.myParallel16 = Sequence(name="myParallel16")
			
			x = self.heartModel1[i].getX()
		
			y = self.heartModel1[i].getY()
		
			#pandaPosInterval1 = self.heartModel1[i].posInterval(7,
															#Point3(self.cycle.getX(), self.cycle.getY(), self.cycle.getZ()),
                                                        #startPos=Point3( x, y, self.heartModel1[i].getZ()))
		
			#self.myParallel16.append(pandaPosInterval1)
		
	
			#self.myParallel16.loop()
			 
			#self.heartModel1[i].detachNode()
			score = score+1
			self.obj.score["text"] = "Score: "+str(score)+"$"
			#print("idhar collect kiay aur chaiye",i,self.heartModel1[i].getPos())
			#return task.cont
		
		#else:
			#print("else me aagay")
			#return task.cont
	return task.done		
 def hawame(self, task):
  #cur = score
  #self.cycle.setPos(self.cycle.getX(),self.cycle.getY(),10)
  if( score < self.cur+5):
	#self.para1.reparentTo(self.cycle)
	#self.para1.setScale(3)
	self.cycle.setPos(self.cycle.getX(),self.cycle.getY(),5)
	base.camera.setZ(5)
  elif(score> self.cur+5):
	#print("idhar")
	#self.para1.reparentTo(self.track)
	self.cycle.setPos(self.cycle.getX(),self.cycle.getY(),0)
	base.camera.setZ(0)
	return task.done
  return task.cont
 def collideEventOut(self, entry):
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  colliderINTO.setColor(.4, .4, .4, 1)
  #colliderFROM.setScale(4.25) 
  #print(colliderFROM.getZ())
  colliderFROM.removeNode()
  #print(colliderFROM.getZ())
  #colliderFROM = None
  self.cycle.setLightOff()
 
 def bikecollideEventOut(self, entry):
  colliderFROM = entry.getFromNodePath().getParent()
  colliderINTO = entry.getIntoNodePath().getParent()
  #taskMgr.remove("AIUpdate")
  #colliderINTO.setColor(.4, .4, .4, 1)
  self.cycle.setLight(self.ambientNP1)
  self.pandaActor2.setPos(self.cycle.getPos()+Vec3(40,40,0))
  self.setAI(self.pandaActor2)
  #self.cycle.loop("tireroll",fromFrame = 24, toFrame = 26)
  #self.speed = 150
  taskMgr.add(self.blood,'bloodtask')
  self.blood1 = Light()
  self.blood1.loadchar(self.cycle,'blood')
  self.diesound()
  self.floating = False
  self.speed =0
  self.jump1()
 def blood(self,task):
	global blood_cnt
	if(blood_cnt > 50):
		blood_cnt = 0
		self.blood1.stopblood()
		taskMgr.remove('bloodtask')
	blood_cnt += 2
	return Task.cont
	
 def jump(self, dt):
	
	if not self.floating:
		self.floating=True
		lf=LerpFunc(lambda z: self.cycle.setZ(z),
		fromData = self.cycle.getZ(),
		toData = self.cycle.getZ()+4.0, duration = 0.6,
		blendType = 'easeOut'
		)
		self.seq=Sequence(lf, Wait(299.7))
		self.seq.setPlayRate(4)
		self.seq.start()
		
	elif not self.seq.isPlaying(): 
		
		self.floating=False
		
 def jump1(self):
	
	if not self.floating:
		self.floating=True
		lf=LerpFunc(lambda z: self.cycle.setPos(z),
		fromData = self.cycle.getPos(),
		toData = self.cycle.getPos()+Vec3(8.0,8.0,0.0), duration = 2.0,
		blendType = 'easeOut'
		)
		self.seq=Sequence(lf, Wait(299.7))
		self.seq.setPlayRate(4)
		self.seq.start()
		
	elif not self.seq.isPlaying(): 
		
		self.floating=False
 def createStartMenu(self):
	menu = Menu(self.menuGraphics, self.fonts, self.inputManager)
	menu.initMenu([0, None, ["Submenu", "Quit Game"],[self.createSubMenu, base.userExit],["Submenu", None]])
 def createSubMenu(self, title):
	menu = Menu(self.menuGraphics, self.fonts, self.inputManager)
	menu.initMenu([3, title, ["Submenu", "Go Back"],[self.createSubMenu, self.createStartMenu],["Another Submenu", None]])
 def makelight(self, task):
	for i in range(len(self.lm)):
		if((abs(self.cycle.getX() -self.lm[i].getX()) >= 600) and (abs(self.cycle.getY()-self.lm[i].getY())>=600)):
			#print(self.lm[i],self.lm[i].getPos())
			#self.lm[i].detachNode()
			self.lm[i].setColor(0.4,0.4,0.4,0.4)
		#else:
			#self.lm[i].reparentTo(self.track)
			
		if((abs(self.cycle.getX() -self.lm[i].getX()) <= 500) and (abs(self.cycle.getY()-self.lm[i].getY())<=500)):
			#print(self.lm[i],self.lm[i].getPos())
			#self.lm[i].reparentTo(self.track)
			self.lm[i].setColor(1.1,1.1,1.1,1.1)
		
		#else:
			#self.lm[i].setColor(0.2,0.2,0.2,0.2)
	return task.cont
 def sabdis(self ):
	for i in range(len(self.lm)):
		#if(((abs(abs(self.cycle.getX())) -(abs(self.lm[i].getX()))) >= 300) and ((abs((abs(self.cycle.getY()))-(abs(self.lm[i].getY()))))>=300) ):
			#print(self.lm[i],self.lm[i].getPos())
			self.lm[i].detachNode()	
 def setlig(self, task):
	for i in range(len(self.lm)):
		if(((abs(abs(self.cycle.getX())) -(abs(self.lm[i].getX()))) >= 150) and ((abs((abs(self.cycle.getY()))-(abs(self.lm[i].getY()))))>=150) ):
			#print(self.lm[i],self.lm[i].getPos())
			self.lm[i].detachNode()
			#self.lm[i].setColor(0.4,0.4,0.4,0.4)
		#else:
			#self.lm[i].reparentTo(self.track)
			
		if(((abs(abs(self.cycle.getX())) -(abs(self.lm[i].getX()))) < 150) and ((abs((abs(self.cycle.getY()))-(abs(self.lm[i].getY()))))<150) ):
			#print(self.lm[i],self.lm[i].getPos())
			#self.lm[i].detachNode()
			self.lm[i].reparentTo(self.track)
			#self.lm[i].setColor(1.1,1.1,1.1,1.1)
	for i in range(len(self.bikeModel1)):
		#if( self.heartModel1[i].getZ() >45):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			#self.heartModel1[i].detachNode()
			#self.lm[i].setColor(0.4,0.4,0.4,0.4)
		#else:
			#self.lm[i].reparentTo(self.track)
		if(((abs(abs(self.cycle.getX())) -(abs(self.bikeModel1[i].getX()))) > 150) and ((abs((abs(self.cycle.getY()))-(abs(self.bikeModel1[i].getY()))))>150) ):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			self.bikeModel1[i].detachNode()	
		if(((abs(abs(self.cycle.getX())) -(abs(self.bikeModel1[i].getX()))) < 150) and ((abs((abs(self.cycle.getY()))-(abs(self.bikeModel1[i].getY()))))<150) ):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			#self.bikeModel1[i].detachNode()
			self.bikeModel1[i].reparentTo(self.track)
			#self.lm[i].setColor(1.1,1.1,1.1,1.1)	
	for i in range(len(self.heartModel1)):
		 
		#if( self.heartModel1[i].getZ() >45):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			#self.heartModel1[i].detachNode()
			#self.lm[i].setColor(0.4,0.4,0.4,0.4)
		#else:
			#self.lm[i].reparentTo(self.track)
		if(((abs(abs(self.cycle.getX())) -(abs(self.heartModel1[i].getX()))) < 100) and ((abs((abs(self.cycle.getY()))-(abs(self.heartModel1[i].getY()))))<100) and self.heartModel1[i].getZ()<=2 and self.visited[i]!=0 ):
			#print(self.heartModel1[i].getZ(), self.visited[i])
			self.heartModel1[i].reparentTo(self.track)
			#self.heartModel1[i].detachNode()
		if(((abs(abs(self.cycle.getX())) -(abs(self.heartModel1[i].getX()))) > 100) and ((abs((abs(self.cycle.getY()))-(abs(self.heartModel1[i].getY()))))>100)  ):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			self.heartModel1[i].detachNode()	
		if(((abs(abs(self.cycle.getX())) -(abs(self.heartModel1[i].getX()))) < 100) and ((abs((abs(self.cycle.getY()))-(abs(self.heartModel1[i].getY()))))<100) and self.heartModel1[i].getZ()>=5  ):
			#print("idhar aaya",self.heartModel1[i].getZ())
			#self.heartModel1[i].reparentTo(self.track)
			self.heartModel1[i].detachNode()
			self.visited[i]=0
		#if(((abs(abs(self.cycle.getX())) -(abs(self.heartModel1[i].getX()))) < 100) and ((abs((abs(self.cycle.getY()))-(abs(self.heartModel1[i].getY()))))<100) and self.heartModel1[i].getZ()<=2 ):
			#print(self.heartModel1[i].getZ())
			#self.heartModel1[i].reparentTo(self.track)
	
	
	for i in range(len(self.treeModel1)):
		#if( self.heartModel1[i].getZ() >45):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			#self.heartModel1[i].detachNode()
			#self.lm[i].setColor(0.4,0.4,0.4,0.4)
		#else:
			#self.lm[i].reparentTo(self.track)
		if(((abs(abs(self.cycle.getX())) -(abs(self.treeModel1[i].getX()))) > 80) and ((abs((abs(self.cycle.getY()))-(abs(self.treeModel1[i].getY()))))>80) ):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			self.treeModel1[i].detachNode()	
		if(((abs(abs(self.cycle.getX())) -(abs(self.treeModel1[i].getX()))) < 80) and ((abs((abs(self.cycle.getY()))-(abs(self.treeModel1[i].getY()))))<80) ):
			#print(self.heartModel1[i],self.heartModel1[i].getPos())
			self.treeModel1[i].reparentTo(self.track)
		
		#else:
			#self.lm[i].setColor(0.2,0.2,0.2,0.2)
	#for i in range(len(self.heartModel1)):
		#self.heartModel1[i].detachNode()		
	return task.cont	
 def cameraZoom(self, dir, dt):
	if(dir == "in"): 
		base.camera.setY(base.camera, 30 * dt)
	else: 
		base.camera.setY(base.camera, -30 * dt)
 def chalukaro(self):
	global first_time,pauseflag
	#if (first_time == 0):
	self.createmap()
	self.addsound()
	#	first_time = -1
	#self.b2.hide()
	pauseflag = 0
	self.healthobj.hbar.hide()
	self.speedobj.hbar.hide()
	self.pbutton.hide()
	self.setnote.hide()
	self.b3.hide()
	self.b4.hide()
	self.b5.hide()
	
	taskMgr.add(self.starttimer,"starttimer")
 def starttimer(self, task):
	if(self.strt.retreat() != 1):
			print "Nothing!!"
			return Task.cont
	else:
		self.b2 = DirectButton(text = "",scale = 0.1,frameSize = (-1.0,1.0,-1,1),command = self.rst,image = "images/new4.png",relief = None)
		self.b2.setTransparency(1)
		self.b2.reparentTo(self.frm1)
		self.b2.show()
		self.b3.show()
		self.b4.show()
		self.b5.show()
		
		self.healthobj.hbar.show()
		self.speedobj.hbar.show()
		taskMgr.add(self.scorer,'scorer')
		taskMgr.remove("starttimer")
		taskMgr.add(self.cycleControl, "cycle move")
		#taskMgr.add(self.makeenv,"make env")
		#taskMgr.add(self.makelight,"make light")
		taskMgr.add(self.obj.timerTask, 'timerTask')
		taskMgr.add(self.setlig, "setlight")
		taskMgr.add(self.police,'catch')
 def pausekaro(self ,arg):
		global pauseflag
		global click
		if(arg == 'button' and click == 1):
			click = 0
			self.resume()##########resume
		elif(arg == 'button' and click == 0):
			pauseflag = 1
			click = 1############pause
			self.b3["image"] = "new3.png"
			self.snd3.setVolume(0)
			taskMgr.remove("cycle move")
			#taskMgr.remove("make light")
			taskMgr.remove("setlight")
			taskMgr.remove("timerTask")
			taskMgr.remove("AIUpdate")
		elif(arg == 'quit'):
			pauseflag = 1
			click = 1
			self.b3["image"] = "new3.png"
			self.snd3.setVolume(0)
			taskMgr.remove("cycle move")
			taskMgr.remove("setlight")
			#taskMgr.remove("make light")
			taskMgr.remove("timerTask")
			taskMgr.remove("AIUpdate")
			########quit
		elif(arg == 'die' or arg == 'options' or arg == 'restart'):
			pauseflag = 1
			self.b3['state'] = DGG.DISABLED
			self.snd3.setVolume(0)
			taskMgr.remove("cycle move")
			taskMgr.remove("setlight")
			#taskMgr.remove("make light")
			taskMgr.remove("timerTask")
			taskMgr.remove("AIUpdate")
 def resume(self):
		global pauseflag
		pauseflag = 0
		self.b3['state'] = DGG.NORMAL
		self.snd3.setVolume(1)
		taskMgr.add(self.obj.timerTask, 'timerTask')
		taskMgr.add(self.cycleControl, "cycle move")
		#taskMgr.add(self.makelight,"make light")
		taskMgr.add(self.setlig,"setlight")
		self.b3["image"] = "pause.png"
		taskMgr.add(self.AIUpdate,"AIUpdate")
 def quit(self, val, txt):
		self.pausekaro('quit')
		if txt == "":
			txt = "Are you sure you want to quit?"
		self.dest = YesNoDialog(text = txt,command = self.confirm,extraArgs = [val])
 def confirm(self,clickedYes,val):
		self.dest.cleanup()
		if clickedYes:
			if val == "quit":
				sys.exit()
			elif val == "loadmenu":
				self.loadmenu()
		else:
			self.resume()
 def options(self):
		print "show options"
		self.pausekaro('options')
		self.b5['state'] = DGG.DISABLED
		self.op_frame = DirectFrame(pos = (0,0,-0.7),frameColor = (1,1,0.6,1),parent = base.a2dTopCenter,frameSize = (-0.5,0.5,-0.5,0.5))
		self.vol_bt = DirectButton(text = "Set Volume",scale = 0.1,pos = Vec3(0,0,0.6),frameSize = (-5,5,-0.5,0.5),command = self.optionlistener,extraArgs = ["vol"],pressEffect = 1,relief = None)
		self.help_bt = DirectButton(text = "Help",scale = 0.1,pos = Vec3(0,0,0.4),frameSize = (-5,5,-0.5,0.5),command = self.optionlistener,extraArgs = ["help"],pressEffect = 1,relief = None)
		self.menu_bt = DirectButton(text = "Return To Menu",scale = 0.1,pos = Vec3(0,0,0.2),frameSize = (-5,5,-0.5,0.5),command = self.optionlistener,extraArgs = ["menu"],pressEffect = 1,relief = None)
		self.done_bt = DirectButton(text = "Done",scale = 0.1,pos = Vec3(0,0,0),frameSize = (-5,5,-0.5,0.5),command = self.optionlistener,extraArgs = ["done"],pressEffect = 1,relief = None)

 def optionlistener(self,val):
		global cnt
		if val == "vol":
			self.vol_bar = DirectSlider(text = "",scale = 0.5,pos = (1.2,0,0),value=0.50,orientation = DGG.VERTICAL, command=self.setVol)
			self.vol_bt['state'] = DGG.DISABLED
			cnt = 2
		elif val == "help":
			print 1
			#self.loadmenu()
		elif val == "done":
			print "tmp"
			self.b5['state'] = DGG.NORMAL
			self.resume()#########later
			if cnt == 2:
				self.vol_bar.hide()
			self.vol_bt.hide()
			self.help_bt.hide()
			self.menu_bt.hide()
			self.done_bt.hide()
			self.op_frame.hide()
			self.vol_bt['state'] = DGG.NORMAL
			print "end"
		elif val == "menu":
			self.quit("loadmenu","Do u want to go to main menu")
		else:
			print val
 def decsound(self):
	self.vol_bar = DirectSlider(text = "setVolume",scale = 0.3,pos = (1.2,0,0),value=0.50,orientation = DGG.VERTICAL, command=self.setVol)
	self.vol_bt['text'] = "Done"
	
 def setVol(self):
    #Simply reads the current value from the slider and sets it in the sound
	newVol = self.vol_bar.guiItem.getValue()
	self.snd1.setVolume(newVol)
	self.snd2.setVolume(newVol)
	self.snd3.setVolume(newVol)
	#self.speedobj.setVol(newVol)

 
 
 def createmap(self ):
	
	global score,l,r,d,u,present_health
	###
	lf = -0.8
	tf = 0.3
	present_health = 100
	self.strt = Start()
	self.text_controls1 = self.addcontrols(-1.2,0.80,"[W]:Move Foreward")
	self.text_controls2 = self.addcontrols(-1.2,0.75,"[S]:Move Backward")
	self.text_controls3 = self.addcontrols(-1.2,0.70,"[A]:Turn Left")
	self.text_controls4 = self.addcontrols(-1.2,0.65,"[D]:Turn Right")
	self.text_controls5 = self.addcontrols(-1.2,0.60,"[Space]:Jump")
	self.text_controls6 = self.addcontrols(-1.2,0.55,"[Left Arrow]:Turn Camera Left")
	self.text_controls7 = self.addcontrols(-1.2,0.50,"[Right Arrow]:Turn Camera Right")
	
	self.frm1 = DirectFrame(pos = (lf,0,tf),frameColor = (0,0,255,1),frameSize = (-0.1,0.1,-0.1,0.1),parent = base.a2dBottomRight,scale = 1,relief = None)
	self.frm2 = DirectFrame(pos = (lf+0.2,0,tf),frameColor = (0,0,255,1),frameSize = (-0.1,0.1,-0.1,0.1),parent = base.a2dBottomRight,scale = 1,relief = None)
	self.frm3 = DirectFrame(pos = (lf+0.4,0,tf),frameColor = (0,0,255,1),frameSize = (-0.1,0.1,-0.1,0.1),parent = base.a2dBottomRight,scale = 1,relief = None)
	self.frm4 = DirectFrame(pos = (lf+0.6,0,tf),frameColor = (0,0,255,1),frameSize = (-0.1,0.1,-0.1,0.1),parent = base.a2dBottomRight,scale = 1,relief = None)
	self.frm5 = DirectFrame(pos = (0.4,0,-0.2),frameColor = (0,0,255,1),frameSize = (-0.1,0.1,-0.1,0.1),parent = base.a2dTopLeft,scale = 1,relief = None)
	
	self.healthobj = Health()
	self.speedobj = Effect()
	self.obj = MyApp()
	
	self.snd2 = base.loader.loadSfx("media/point2.wav")
	self.snd3 = base.loader.loadSfx("media/die1.wav")
	
	
	
	
	self.b3 = DirectButton(text = "",scale = 0.1,frameSize = (l+1.5,r-1.5,-0.8,0.8),command = self.pausekaro,extraArgs = ['button'],image = "images/pause.png",relief = None)
	self.b3.setTransparency(1)
	self.b3.reparentTo(self.frm2)
	
	self.pbutton = DirectButton(text = "Pay Fine",pos = (0,0,-0.9),scale = 0.1,command = self.bhagao,frameSize = (-2,2,-1,1))
	self.setnote = self.addInstructions(0.90,"Police Caught\n10$ penalty")
	#self.b3.setPos = Vec3(lf-0.1,0,bf+0.2)
	
	self.b4 = DirectButton(text = "",scale = 0.1,frameSize = (l+1.5,r-1.5,-1,1),command = self.quit,extraArgs = ["quit",""],image = "images/quit2.png",relief = None)
	self.b4.setTransparency(1)
	self.b4.reparentTo(self.frm3)
	#self.b4.setPos = Vec3(lf,0,bf+0.2)
	
	self.b5 = DirectButton(text = "",scale = 0.1,frameSize = (l+1.5,r-1.5,-1,1),command = self.options,image = "images/options.png",relief = None)
	self.b5.setTransparency(1)
	self.b5.reparentTo(self.frm4)
	#self.b5.setPos = Vec3(lf+0.1,0,bf+0.2)
	
	sc = self.fileobj.get_high_score()
	#self.b6 = DirectLabel(text = "Max Score: "+str(sc)+"$",scale = 0.1,frameSize = (l+1.5,r-1.5,-1,1),relief = None)
	self.bscr = OnscreenText(text = "Max Score: "+str(sc)+"$",style = 1,fg = (1,1,0,1),scale = 0.1,pos = (-1.2,0.9),align=TextNode.ALeft)
	#self.b6.reparentTo(self.frm5)
	
	#self.b5.setTransparency(1)
	##############
	# Add a light to the scene.
	#self.area1= loader.loadModel("Models/volcano/volcano")
	#self.area1.reparentTo(render)
	#self.area1.setScale(0.01)
	#self.area1.setPos(-116,22,0)
	
	#self.lightpivot = render.attachNewNode("lightpivot")
	#self.lightpivot.setPos(-106,-120,15)
	#self.lightpivot.hprInterval(5,Point3(360,0,0)).loop()
	#plight = PointLight('plight')
	#plight.setColor(Vec4(1, 1, 1, 1))
	#plight.setAttenuation(Vec3(0,0,0.5))
	#plnp = self.lightpivot.attachNewNode(plight)
	#plnp.setPos(0, 0, 0)
	#self.area1.setLight(plnp)
	#self.area1.setShaderInput("light", plnp)
	
	# Add an ambient light
	#alight = AmbientLight('alight')
	#alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
	#alnp = render.attachNewNode(alight)
	#self.area1.setLight(alnp)
	# create a sphere to denote the light
	#sphere = loader.loadModel("Models/sphere")
	#sphere.reparentTo(plnp)
	#sphere.setLight(alnp)
	
	#self.myFog = Fog("Fog Name")
	#self.myFog.setColor(0.5,0.8,0.8)
	#self.myFog.setExpDensity(0.005)
	#self.render.setFog(self.myFog)
	
	#base.setBackgroundColor(0.5,0.8,0.8)
	#self.render.clearFog()
	
	
	#self.ramp = loader.loadModel("Models/wide_ramp/wide_ramp")
	#self.ramp.reparentTo(self.track)
	#self.ramp.setScale(0.15,0.15,0.15)
	#self.ramp.setPos(-68,-65,0)
	#self.lm.append(self.ramp)
	#self.env1 = loader.loadModel("Models/bird1/bird1")
	#self.env1.reparentTo(render)
	#self.env1.setScale(2.40, 2.40, 2.40)
	#self.env1.setPos(-30, 30, 30)
	#self.lm.append(self.env1)
	#self.env10 = loader.loadModel("Models/drum/DRUM_F")
	#self.env10.reparentTo(self.track)
	#self.env10.setScale(2.40, 2.40, 2.40)
	#self.env10.setPos(-50,-260,1)
	#self.lm.append(self.env10)
	#self.env2 = loader.loadModel("Models/drum/DRUM_F")
	
	
	

	self.env51 = loader.loadModel("Models/cat-buildings/alice-farm--farmhouse-egg/alice-farm--farmhouse/farmhouse")
	self.env51.reparentTo(self.track)
	self.env51.setScale(3.2,3.2,3.2)
	self.env51.setPos(-131,-358,-0.1)
	self.lm.append(self.env51)
	self.env11 = loader.loadModel("Models/cat-furniture/alice-beach--beachchair-egg/alice-beach--beachchair/beachchair")
	self.env11.reparentTo(self.track)
	
	self.env11.setScale(1.0,1.0,1.0)
	self.env11.setPos(-480,-45,0)
	self.lm.append(self.env11)
	self.env12 = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
	self.env12.reparentTo(self.track)
	self.env12.setScale(0.60,0.60,0.60)
	self.env12.setPos(-280,-45,0)
	self.lm.append(self.env12)
	self.mc12 = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--monstercar-egg/bvw-f2004--monstercar/carmonster")
	self.mc12.reparentTo(self.track)
	self.mc12.setScale(1.60,1.60,1.60)
	self.mc12.setPos(-612,-195,0)
	self.lm.append(self.mc12)
	self.ap12 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.ap12.reparentTo(self.track)
	self.ap12.setScale(0.80,0.80,0.80)
	self.ap12.setPos(-443,372.8,5)
	self.lm.append(self.ap12)
	self.ap2 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.ap2.reparentTo(self.track)
	self.ap2.setScale(0.80,0.80,0.80)
	self.ap2.setPos(-401,328.8,5)
	self.lm.append(self.ap2)
	self.ap3 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.ap3.reparentTo(self.track)
	self.ap3.setScale(0.80,0.80,0.80)
	self.ap3.setPos(-148,673.8,5)
	self.ap3.setH(180)
	self.lm.append(self.ap3)
	self.ap4 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.ap4.setH(180)
	self.ap4.reparentTo(self.track)
	self.ap4.setScale(0.80,0.80,0.80)
	self.ap4.setPos(-171.85,673.8,5)
	self.lm.append(self.ap4)
	self.ap5 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.ap5.reparentTo(self.track)
	self.ap5.setScale(0.80,0.80,0.80)
	self.ap5.setH(180)
	self.ap5.setPos(-238,670.8,5)
	self.lm.append(self.ap5)
	self.ap6 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.ap6.reparentTo(self.track)
	self.ap6.setScale(0.80,0.80,0.80)
	self.ap6.setH(180)
	self.ap6.setPos(-208,670.8,5)
	self.lm.append(self.ap6)
	self.p1 = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
	self.p1.reparentTo(self.track)
	self.p1.setScale(0.60,0.60,0.60)
	self.p1.setPos(-487,-430,0)
	self.lm.append(self.p1)
	self.p2 = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
	self.p2.reparentTo(self.track)
	self.p2.setScale(1.60,1.60,1.60)
	self.p2.setPos(-642,-214,0)
	self.lm.append(self.p2)
	self.p3 = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
	self.p3.reparentTo(self.track)
	self.p3.setScale(1.20,1.20,1.20)
	self.p3.setPos(-591.7,-80,0)
	self.lm.append(self.p3)
	self.p4 = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
	self.p4.reparentTo(self.track)
	self.p4.setScale(0.60,0.60,0.60)
	self.p4.setPos(-487,-430,0)
	self.lm.append(self.p4)
	self.env13 = loader.loadModel("Models/cat-plants/bvw-f2004--plant6-egg/bvw-f2004--plant6/plants6")
	self.env13.reparentTo(self.track)
	
	self.env13.setScale(0.40,0.40,0.40)
	self.env13.setPos(-180,-45,0)
	self.lm.append(self.env13)
	self.env14 = loader.loadModel("Models/cat-plants/bvw-f2004--plant3-egg/bvw-f2004--plant3/plants3")
	self.env14.reparentTo(self.track)
	
	self.env14.setScale(0.40,0.40,0.40)
	self.env14.setPos(-219,133,0)
	self.lm.append(self.env14)
	#self.ans = 0
	#self.timeelapsed = 120
	
	self.env16 = loader.loadModel("Models/cat-skies/alice-skies--cloudysky-egg/alice-skies--cloudysky/cloudysky")
	#self.env16.reparentTo(self.track)
	
	self.env16.setScale(1.5,1.5,1.5)
	self.env16.setPos(0,0,-2)
	#self.lm.append(self.env16)
	self.env17 = loader.loadModel("Models/cat-skies/alice-skies--stars-egg/alice-skies--stars/stars")
	#self.env17.reparentTo(self.track)
	
	self.env17.setScale(1.5,1.5,1.5)
	self.env17.setPos(0,0,-2)
	#self.lm.append(self.env17)
	#taskMgr.add(self.makeenv,"make env")
	#self.accept('collider1-into-cyclenode', self.collideEventIn)
	#self.accept('collider1-out-cyclenode', self.collideEventOut)
	#taskMgr.add(self.cycleMove, "Cycle Move")
	
	
	self.env20 = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.env20.reparentTo(self.track)
	
	self.env20.setScale(1.5,1.5,1.5)
	self.env20.setPos(120,120,0)
	self.lm.append(self.env20)
	
	
	#self.env21.setScale(0.50,0.50,0.50)
	#self.env21.setPos(-315,47,0)
	#self.env21.setH(100)
	#self.lm.append(self.env21)
	#self.env23 = loader.loadModel("Models/rail_ramp/rail_ramp")
	#self.env23.reparentTo(self.track)
	
	#self.env23.setScale(.025,.025,.025)
	#self.env23.setPos(-240,143,0)
	#self.lm.append(self.env23)
	self.env29 = loader.loadModel("Models/cat-buildings/alice-city--church-egg/alice-city--church/church")
	self.env29.reparentTo(self.track)
	self.env29.setScale(1.0,1.0,1.0)
	self.env29.setPos(-248,-318.8,0)
	self.env29.setColor(0.6,0.6,0.6,0.6)
	self.lm.append(self.env29)
	self.env30 = loader.loadModel("Models/cat-buildings/alice-japan--bridge-egg/alice-japan--bridge/bridge")
	self.env30.reparentTo(self.track)
	self.env30.setScale(0.070,0.070,0.070)
	self.env30.setH(-60)
	self.env30.setPos(-160,-162.8,20)
	self.lm.append(self.env30)
	self.env37 = loader.loadModel("Models/Windmill/Windmill")
	self.env37.reparentTo(self.track)
	self.env37.setScale(3.30,3.30,3.30)
	self.env37.setH(-60)
	self.env37.setPos(471,-315,0)
	self.lm.append(self.env37)
	self.env38 = loader.loadModel("Models/cat-buildings/alice-japan--dojo-egg/alice-japan--dojo/dojo")
	self.env38.reparentTo(self.track)
	self.env38.setScale(0.370,0.370,0.370)
	self.env38.setH(-60)
	self.env38.setPos(250,400,0)
	self.lm.append(self.env38)
	self.env85 = loader.loadModel("Models/BuildingCluster5/BuildingCluster5")
	self.env85.reparentTo(self.track)
	self.env85.setScale(1.370,1.370,1.370)
	self.env85.setH(-60)
	self.env85.setPos(357,-667,0)
	self.lm.append(self.env85)
	self.env86 = loader.loadModel("Models/cat-carnival-and-arcade/alice-amusement-park--ringtoss-egg/alice-amusement-park--ringtoss/ringtoss")
	self.env86.reparentTo(self.track)
	self.env86.setScale(3.370,3.370,3.370)
	self.env86.setH(0)
	self.env86.setPos(-409,721,0)
	self.lm.append(self.env86)
	self.env39 = loader.loadModel("Models/cat-buildings/bvw-f2004--russianbuilding/tetris-building")

	self.env39.reparentTo(self.track)
	self.env39.setScale(12.170,12.170,12.170)
	self.env39.setH(-60)
	self.env39.setPos(-278,474,0)
	self.lm.append(self.env39)
	self.env40 = loader.loadModel("Models/cat-buildings/bvw-f2004--pueblo/pueblo")

	self.env40.reparentTo(self.track)
	self.env40.setScale(0.870,0.870,0.870)
	self.env40.setH(90)
	self.env40.setPos(432,-166,-14)
	self.lm.append(self.env40)
	self.env41 = loader.loadModel("Models/cat-miscellaneous/bvw-f2004--hangglider1-egg/bvw-f2004--hangglider1/hang-glider-1")

	self.env41.reparentTo(self.track)
	self.env41.setScale(1.370,1.370,1.370)
	self.env41.setH(-100)
	self.env41.setPos(431,173,6)
	self.lm.append(self.env41)
	self.env42 = loader.loadModel("Models/rest station/rest station")

	self.env42.reparentTo(self.track)
	self.env42.setScale(0.370,0.370,0.370)
	self.env42.setH(-60)
	self.env42.setPos(-684,370,0)
	self.lm.append(self.env42)
	self.env43 = loader.loadModel("Models/cat-carnival-and-arcade/alice-amusement-park--funhouse-egg/alice-amusement-park--funhouse/funhouse")
	self.env43.reparentTo(self.track)
	self.env43.setScale(3.370,3.370,3.370)
	self.env43.setH(-60)
	self.env43.setPos(-623,-308,0)
	self.lm.append(self.env43)
	self.env44 = loader.loadModel("Models/stadium/stadium")
	self.env44.reparentTo(self.track)
	self.env44.setScale(0.370,0.370,0.370)
	self.env44.setH(0)
	self.env44.setPos(208,-435,0)
	self.lm.append(self.env44)
	self.env64 = loader.loadModel("Models/BuildingCluster4/BuildingCluster4")
	self.env64.reparentTo(self.track)
	self.env64.setScale(4.370,4.370,4.370)
	self.env64.setH(0)
	self.env64.setPos(-251,-738,0)
	self.lm.append(self.env64)
	self.env45 = loader.loadModel("Models/BuildingCluster2/BuildingCluster2")
	self.env45.reparentTo(self.track)
	self.env45.setScale(3.370,3.370,3.370)
	self.env45.setH(0)
	self.env45.setPos(411,219,0)
	self.lm.append(self.env45)
	#self.env25 = loader.loadModel("Models/gate/gate")
	#self.env25.reparentTo(self.track)
	
	#self.env25.setScale(0.025,0.025,0.025)
	#self.env25.setPos(-244,-32,0)
	#self.lm.append(self.env25)
	self.env26 = loader.loadModel("Models/CityHall/CityHall")
	self.env26.reparentTo(self.track)
	
	self.env26.setScale(0.80,0.80,0.80)
	self.env26.setPos(-310,-255,0)
	self.env26.setH(-90)
	self.lm.append(self.env26)
	#taskMgr.add(self.makeenv, "make env")
	
	self.mod6b21 = loader.loadModel("Models/Tank/Tank")
	self.mod6b21.reparentTo(self.track)
	self.mod6b21.setPos(-120,54,0.6)
	self.mod6b21.setH(90)
	self.mod6b21.setScale(0.80,0.80,0.80)
	self.lm.append(self.mod6b21)
	#self.mod6b21 = None
	self.lm.remove(self.mod6b21)
	self.mod6b21 = None
	self.cycle = Actor("Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve", 
	{"run":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-run",
	"jump":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-jump",
	"offbalance":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-offbalance",
	"tireroll":"Models/cat-humans/bvw-f2004--eve-egg/bvw-f2004--eve/eve-tireroll"})
	
	self.cycle.reparentTo(render)
	self.cycle.setPos(-257,18,2)
	self.cycle.setScale(0.35)
	
	#taskMgr.add(self.controlCamera, "Cam Control")
	
	self.mol2 = loader.loadModel("Models/highway pole/highway pole")
	self.mol2.reparentTo(self.track)
	self.mol2.setPos(-256,-312,0)
	self.mol2.setScale(0.008,0.008,0.008)
	#self.lm.append(self.model2)
	self.mol3 = loader.loadModel("Models/highway pole/highway pole")
	self.mol3.reparentTo(self.track)
	self.mol3.setPos(-276,85,0)
	self.mol3.setScale(0.008,0.008,0.008)
	self.mol4 = loader.loadModel("Models/highway pole/highway pole")
	self.mol4.reparentTo(self.track)
	self.mol4.setPos(-213,-243,0)
	self.mol4.setScale(0.008,0.008,0.008)
	self.mol4.setH(180)
	self.mol5 = loader.loadModel("Models/highway pole/highway pole")
	self.mol5.reparentTo(self.track)
	self.mol5.setPos(24,-293,0)
	self.mol5.setScale(0.008,0.008,0.008)
	self.mol6 = loader.loadModel("Models/highway pole/highway pole")
	self.mol6.reparentTo(self.track)
	self.mol6.setPos(-54,-286,0)
	self.mol4.setH(-90)
	self.mol6.setScale(0.008,0.008,0.008)
	self.mol7 = loader.loadModel("Models/highway pole/highway pole")
	self.mol7.reparentTo(self.track)
	self.mol7.setPos(296,-296,0)
	self.mol7.setScale(0.008,0.008,0.008)
	self.mol8 = loader.loadModel("Models/highway pole/highway pole")
	self.mol8.reparentTo(self.track)
	self.mol8.setPos(267,-248,0)
	self.mol8.setScale(0.008,0.008,0.008)
	self.mol9 = loader.loadModel("Models/highway pole/highway pole")
	self.mol9.reparentTo(self.track)
	self.mol9.setPos(311,-74,0)
	self.mol9.setScale(0.008,0.008,0.008)
	self.mol10 = loader.loadModel("Models/highway pole/highway pole")
	self.mol10.reparentTo(self.track)
	self.mol10.setPos(308,-7,0)
	self.mol10.setScale(0.008,0.008,0.008)
	self.mol11 = loader.loadModel("Models/highway pole/highway pole")
	self.mol11.reparentTo(self.track)
	self.mol11.setPos(267,250,0)
	self.mol11.setScale(0.008,0.008,0.008)
	self.mol12 = loader.loadModel("Models/highway pole/highway pole")
	self.mol12.reparentTo(self.track)
	self.mol12.setPos(310,307,0)
	self.mol12.setScale(0.008,0.008,0.008)
	self.mol13 = loader.loadModel("Models/highway pole/highway pole")
	self.mol13.reparentTo(self.track)
	self.mol13.setPos(321,271,0)
	self.mol13.setH(180)
	self.mol13.setScale(0.008,0.008,0.008)
	self.mol14 = loader.loadModel("Models/highway pole/highway pole")
	self.mol14.reparentTo(self.track)
	self.mol14.setPos(-244,314,0)
	self.mol14.setScale(0.008,0.008,0.008)
	self.mol15 = loader.loadModel("Models/highway pole/highway pole")
	self.mol15.reparentTo(self.track)
	self.mol15.setPos(-216.9,250,0)
	self.mol15.setScale(0.008,0.008,0.008)
	self.mol16 = loader.loadModel("Models/highway pole/highway pole")
	self.mol16.reparentTo(self.track)
	self.mol16.setPos(10,316,0)
	self.mol16.setScale(0.008,0.008,0.008)
	self.mol17 = loader.loadModel("Models/highway pole/highway pole")
	self.mol17.reparentTo(self.track)
	self.mol17.setPos(100,298,0)
	self.mol17.setScale(0.008,0.008,0.008)
	self.mol18 = loader.loadModel("Models/highway pole/highway pole")
	self.mol18.reparentTo(self.track)
	self.mol18.setPos(-570,76,0)
	self.mol18.setH(-90)
	self.mol18.setScale(0.008,0.008,0.008)
	self.mol19 = loader.loadModel("Models/highway pole/highway pole")
	self.mol19.reparentTo(self.track)
	self.mol19.setPos(-485,88,0)
	self.mol19.setH(-90)
	self.mol19.setScale(0.008,0.008,0.008)
	self.mol20 = loader.loadModel("Models/highway pole/highway pole")
	self.mol20.reparentTo(self.track)
	self.mol20.setPos(-506,-8,0)
	self.mol20.setH(-90)
	self.mol20.setScale(0.008,0.008,0.008)
	self.mol21 = loader.loadModel("Models/highway pole/highway pole")
	self.mol21.reparentTo(self.track)
	self.mol21.setH(90)
	self.mol21.setPos(-558.8,-2.29,0)
	self.mol21.setScale(0.008,0.008,0.008)
	self.mol22 = loader.loadModel("Models/highway pole/highway pole")
	self.mol22.reparentTo(self.track)
	self.mol22.setPos(-474,-516,0)
	self.mol22.setScale(0.008,0.008,0.008)
	self.mol22.setH(180)
	self.mol23 = loader.loadModel("Models/highway pole/highway pole")
	self.mol23.reparentTo(self.track)
	self.mol23.setPos(27,-532,0)
	self.mol23.setH(180)
	self.mol23.setScale(0.008,0.008,0.008)
	self.mol24 = loader.loadModel("Models/highway pole/highway pole")
	self.mol24.reparentTo(self.track)
	self.mol24.setPos(31,-583,0)
	self.mol24.setScale(0.008,0.008,0.008)
	self.mol25 = loader.loadModel("Models/highway pole/highway pole")
	self.mol25.reparentTo(self.track)
	self.mol25.setPos(-17,-587,0)
	self.mol25.setScale(0.008,0.008,0.008)
	self.mol26 = loader.loadModel("Models/highway pole/highway pole")
	self.mol26.reparentTo(self.track)
	self.mol26.setPos(-48,-515,0)
	self.mol26.setScale(0.008,0.008,0.008)
	self.mol27 = loader.loadModel("Models/highway pole/highway pole")
	self.mol27.reparentTo(self.track)
	self.mol27.setPos(-508,-453,0)
	self.mol27.setScale(0.008,0.008,0.008)
	self.lm.append(self.mol27)
	self.mol28 = loader.loadModel("Models/highway pole/highway pole")
	self.mol28.reparentTo(self.track)
	self.mol28.setPos(488,-519,0)
	self.mol28.setScale(0.008,0.008,0.008)
	self.lm.append(self.mol28)
	self.mol29 = loader.loadModel("Models/highway pole/highway pole")
	self.mol29.reparentTo(self.track)
	self.mol29.setPos(535,-492,0)
	self.mol29.setScale(0.008,0.008,0.008)
	self.lm.append(self.mol29)
	self.mol30 = loader.loadModel("Models/highway pole/highway pole")
	self.mol30.reparentTo(self.track)
	self.mol30.setPos(315,-256,0)
	self.mol30.setH(-90)
	self.mol30.setScale(0.008,0.008,0.008)
	#self.cycle.setPos(self.mol30.getPos())
	self.lm.append(self.mol30)
	self.mol31 = loader.loadModel("Models/highway pole/highway pole")
	self.mol31.reparentTo(self.track)
	self.mol31.setPos(536,447,0)
	self.mol31.setH(90)
	self.mol31.setScale(0.008,0.008,0.008)
	#self.cycle.setPos(self.mol31.getPos())
	self.lm.append(self.mol31)
	self.mol32 = loader.loadModel("Models/highway pole/highway pole")
	self.mol32.reparentTo(self.track)
	self.mol32.setPos(536,447,0)
	self.mol32.setH(0)
	self.mol32.setScale(0.008,0.008,0.008)
	#self.cycle.setPos(self.mol32.getPos())
	self.lm.append(self.mol32)
	self.mol33 = loader.loadModel("Models/highway pole/highway pole")
	self.mol33.reparentTo(self.track)
	self.mol33.setPos(544,34,0)
	self.mol33.setH(0)
	self.mol33.setScale(0.008,0.008,0.008)
	self.lm.append(self.mol33)
	#self.cycle.setPos(self.mol33.getPos())
	self.lm.append(self.mol2)
	self.lm.append(self.mol3)
	self.lm.append(self.mol4)
	self.lm.append(self.mol5)
	self.lm.append(self.mol6)
	self.lm.append(self.mol7)
	self.lm.append(self.mol8)
	self.lm.append(self.mol9)
	self.lm.append(self.mol10)
	self.lm.append(self.mol11)
	self.lm.append(self.mol12)
	self.lm.append(self.mol13)
	self.lm.append(self.mol14)
	self.lm.append(self.mol15)
	self.lm.append(self.mol16)
	self.lm.append(self.mol17)
	self.lm.append(self.mol18)
	self.lm.append(self.mol19)
	self.lm.append(self.mol20)
	self.lm.append(self.mol21)
	self.lm.append(self.mol22)
	self.lm.append(self.mol23)
	self.lm.append(self.mol24)
	self.lm.append(self.mol25)
	self.lm.append(self.mol26)
	self.mod2 = loader.loadModel("Models/Fountain/Fountain")
	self.mod2.reparentTo(self.track)
	self.mod2.setPos(-370,-108,0)
	self.mod2.setScale(0.80,0.80,0.80)
	self.lm.append(self.mod2)
	self.mod3 = loader.loadModel("Models/CityHall/CityHall")
	self.mod3.reparentTo(self.track)
	self.mod3.setPos(695,-48,-1)
	self.mod3.setH(90)
	self.mod3.setScale(3.20,3.20,3.20)
	self.lm.append(self.mod3)
	self.mod5 = loader.loadModel("Models/highway pole/highway pole")
	self.mod5.reparentTo(self.track)
	self.mod5.setPos(-268,20.5,0)
	self.mod5.setH(90)
	self.mod5.setScale(.009,.009,0.009)
	self.lm.append(self.mod5)
	self.mod6 = loader.loadModel("Models/highway pole/highway pole")
	self.mod6.reparentTo(self.track)
	self.mod6.setPos(-207,378,0)
	self.mod6.setH(90)
	self.mod6.setScale(.009,.009,0.009)
	self.lm.append(self.mod6)
	#self.followCam = FollowCam(self.cam, self.cycle)
	
	
	
	
	self.cTrav = CollisionTraverser()
	self.collisionHandler = CollisionHandlerEvent()
	LOVE_MASK=BitMask32.bit(2)
	#self.heartModel1 = []
	#self.bikeModel1 = []
	#self.heartCollider1=[]
	#self.bikeCollider1=[]
	#self.para1 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	#self.para1.reparentTo(self.track)
	#self.para1.setPos(-240,-126,1)
	#self.para1.setH(4)
	#self.paraCollider = self.para1.attachNewNode(CollisionNode('colliderpara'))
	# let's mark it as a from collider and with its distinct mask as well
	
	#self.paraCollider.node().addSolid(CollisionSphere(0, 0, 0, 4.5))
	#self.paraCollider.node().setFromCollideMask(LOVE_MASK)
	#self.cTrav.addCollider(self.paraCollider, self.collisionHandler)
	#self.para1.setScale(0.180,0.180,0.180)
	
	#self.lm.append(self.para1)
	
	#self.mag1 = loader.loadModel("Models/Magnet/Magnet")
	#self.mag1.reparentTo(self.track)
	#self.mag1.setPos(-240,-126,0)
	#self.mag1.setH(4)
	#self.mag1.setP(90)
	#self.mag1.setScale(2)
	
	#self.magCollider = self.mag1.attachNewNode(CollisionNode('collidermag'))
	# let's mark it as a from collider and with its distinct mask as well
	
	#self.magCollider.node().addSolid(CollisionSphere(0, 0, 0, 1.5))
	#self.magCollider.node().setFromCollideMask(LOVE_MASK)
	#self.cTrav.addCollider(self.magCollider, self.collisionHandler)
	#self.mag1.setScale(3.80,3.80,3.80)
	
	#self.lm.append(self.mag1)
	
	x = -240
	y = -126
	z = 0.9
	for i in range(10):
		self.heartModel = loader.loadModel("Models/coin/coin1")
	#self.heartModel.reparentTo(render)
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		y= y-7
		if(i<5):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel1 = Parallel(name="myParallel1")
	for i in range(10):
		x = self.heartModel1[i].getX()
		
		y = self.heartModel1[i].getY()
		
		pandaPosInterval1 = self.heartModel1[i].posInterval(5,
                                                        Point3(x-10, y, self.heartModel1[i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[i].getZ()))
		
		self.myParallel1.append(pandaPosInterval1)
		
		
	
	self.myParallel1.loop()
	
	
	
	x=2
	y = -268
	z=0.8
	for i in range(10):
		
		self.heartModel = loader.loadModel("Models/coin/coin1")
	#self.heartModel.reparentTo(render)
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x= x-5
		if(i<5):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	
	
	
	self.myParallel2 = Parallel(name="myParallel2")
	for i in range(10):
		x = self.heartModel1[10+i].getX()
		
		y = self.heartModel1[10+i].getY()
		
		pandaPosInterval1 = self.heartModel1[10+i].posInterval(10,
                                                        Point3(x, y-7, self.heartModel1[10+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[10+i].getZ()))
		self.myParallel2.append(pandaPosInterval1)
		
	self.myParallel2.loop()
	x=50
	y = -273
	z=1
	for i in range(10):
		self.heartModel = loader.loadModel("Models/coin/coin1")
	#self.heartModel.reparentTo(render)
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x+6
		if(i<5):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel3 = Parallel(name="myParallel3")
	for i in range(10):
		x = self.heartModel1[20+i].getX()
		
		y = self.heartModel1[20+i].getY()
		
		pandaPosInterval1 = self.heartModel1[20+i].posInterval(10,
                                                        Point3(x, y-7, self.heartModel1[20+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[20+i].getZ()))
		self.myParallel3.append(pandaPosInterval1)
		
	self.myParallel3.loop()
	
	x=284
	y = -120
	z=1
	for i in range(15):
		self.heartModel = loader.loadModel("Models/coin/coin1")
	#self.heartModel.reparentTo(render)
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		y = y+6
		if(i<7):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel4 = Parallel(name="myParallel4")
	for i in range(15):
		x = self.heartModel1[30+i].getX()
		
		y = self.heartModel1[30+i].getY()
		
		pandaPosInterval1 = self.heartModel1[30+i].posInterval(10,
                                                        Point3(x-10, y, self.heartModel1[30+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[30+i].getZ()))
		pandaPosInterval2 = self.heartModel1[30+i].posInterval(5,
                                                        Point3(x, y, self.heartModel1[30+i].getZ()),
                                                        startPos=Point3(x-6, y, self.heartModel1[30+i].getZ()))
		
		
		self.myParallel4.append(pandaPosInterval1)
			
	self.myParallel4.loop()
	
	x = -247
	y=66
	z=0
	for i in range(3):
		
		self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
	#self.heartModel.reparentTo(render)
		self.bikeModel.setPos(x, y, z)
		self.bikeModel.reparentTo(self.track)
		self.lightobj = Light()
		self.lightobj.loadchar(self.bikeModel,'red')
		
		y= y-80
		x = x-3
		self.bikeModel.setH(180)
		#self.model12.setPos(-240,-126,1)
		self.bikeModel.setScale(1.818)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel1 = Parallel(name="carParallel1")
	for i in range(3):
		x = self.bikeModel1[i].getX()
		
		y = self.bikeModel1[i].getY()
		
		#pandaPosInterval1 = self.bikeModel1[i].posInterval(6.5,
                                                        #Point3(x, y-460, self.bikeModel1[i].getZ()),
                                                        #startPos=Point3( x, y, self.bikeModel1[i].getZ()))
		pandaPosInterval2 = self.bikeModel1[i].posInterval(9.5,
                                                        Point3(x, y+150, self.bikeModel1[i].getZ()),
                                                        startPos=Point3(x, y-60, self.bikeModel1[i].getZ()))
		
		
																
		#self.carParallel1.append(pandaPosInterval1)
		self.carParallel1.append(pandaPosInterval2)
	
	self.carParallel1.loop()
	
	
	
	x = 10
	y=-260
	z=0
	for i in range(3):
		
		#self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
		#self.heartModel.reparentTo(render)
		#self.bikeModel.setPos(x, y, z)
		
		if(i%2==0):
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
	#self.heartModel.reparentTo(render)
			self.bikeModel.setH(-90)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setPos(x, y, z)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'red')
		else:
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")
			self.bikeModel.setPos(x, y, z+2.0)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setH(90)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'blue')
		
		
		x= x-150
		y = y-3
		#self.bikeModel.setH(-90)
		#self.model12.setPos(-240,-126,1)
		self.bikeModel.setScale(1.618)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel2 = Parallel(name="carParallel2")
	for i in range(3):
		x = self.bikeModel1[3+i].getX()
		
		y = self.bikeModel1[3+i].getY()
		
		#pandaPosInterval1 = self.bikeModel1[3+i].posInterval(22.5,
                                                        #Point3(x+660, y, self.bikeModel1[3+i].getZ()),
                                                        #startPos=Point3( x+200, y, self.bikeModel1[3+i].getZ()))
		pandaPosInterval2 = self.bikeModel1[3+i].posInterval(12.5,
                                                        Point3(x, y, self.bikeModel1[3+i].getZ()),
                                                        startPos=Point3(x+460, y, self.bikeModel1[3+i].getZ()))
		
		
																
		#self.carParallel2.append(pandaPosInterval1)
		self.carParallel2.append(pandaPosInterval2)
		
	
	self.carParallel2.loop()
	
	
	x = 288
	y=260
	z=0
	for i in range(3):
		
		if(i%2==0):
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
	#self.heartModel.reparentTo(render)
			self.bikeModel.setH(0)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setPos(x, y, z)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'red')
		else:
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")
			self.bikeModel.setPos(x, y, z+2.0)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setH(180)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'blue')
		y= y+150
		x = x-3
		#self.bikeModel.setH(0)
		#self.model12.setPos(-240,-126,1)
		self.bikeModel.setScale(1.518)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel3 = Parallel(name="carParallel3")
	for i in range(3):
		x = self.bikeModel1[6+i].getX()
		
		y = self.bikeModel1[6+i].getY()
		
		pandaPosInterval1 = self.bikeModel1[6+i].posInterval(9.5,
                                                        Point3(x, y-760, self.bikeModel1[6+i].getZ()),
                                                        startPos=Point3( x, y, self.bikeModel1[6+i].getZ()))
		#pandaPosInterval2 = self.bikeModel1[6+i].posInterval(13.5,
                                                        #Point3(x, y+20, self.bikeModel1[6+i].getZ()),
                                                        #startPos=Point3(x, y-260, self.bikeModel1[6+i].getZ()))
		
		
																
		self.carParallel3.append(pandaPosInterval1)
		#self.carParallel3.append(pandaPosInterval2)
	
	self.carParallel3.loop()
	
	
	x=-525
	k = -525
	y=100
	z=0
	for i in range(3):
		
		if(i%2==0):
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
	#self.heartModel.reparentTo(render)
			self.bikeModel.setH(0)
			self.bikeModel.setPos(x, y, z)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setScale(1.38)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'red')
		else:
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")
			self.bikeModel.setPos(x, y, z+2.0)
			self.bikeModel.setH(180)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setScale(1.38)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'blue')
		y= y+150
		if(i%2==0):
			x = k+6
		else:
			x = k-12
		self.bikeModel.setH(0)
		#self.model12.setPos(-240,-126,1)
		#self.bikeModel.setScale(0.38)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel4 = Parallel(name="carParallel4")
	for i in range(3):
		x = self.bikeModel1[9+i].getX()
		
		y = self.bikeModel1[9+i].getY()
		
		pandaPosInterval1 = self.bikeModel1[9+i].posInterval(13.5,
                                                        Point3(x, y-300, self.bikeModel1[9+i].getZ()),
                                                        startPos=Point3( x, y+60, self.bikeModel1[9+i].getZ()))
		#pandaPosInterval2 = self.bikeModel1[9+i].posInterval(13.5,
                                                        #Point3(x, y+20, self.bikeModel1[6+i].getZ()),
                                                        #startPos=Point3(x, y-260, self.bikeModel1[6+i].getZ()))
		
		
																
		self.carParallel4.append(pandaPosInterval1)
		#self.carParallel3.append(pandaPosInterval2)
	
	
	x = -71
	y=262
	k=262
	z=0
	#self.cycle.setPos(x,y,z)
	for i in range(8):
		
		self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--jeep-egg/bvw-f2004--jeep/jeep")
	#self.heartModel.reparentTo(render)
		self.bikeModel.setPos(x, y, z)
		self.lightobj = Light()
		self.lightobj.loadchar(self.bikeModel,'red')
		if(i%2==0):
			y= k+6
		else:	
			y= k-6
		x = x+150
		self.bikeModel.setH(-90)
		#self.model12.setPos(-240,-126,1)
		self.bikeModel.setScale(0.28)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel5 = Parallel(name="carParallel5")
	for i in range(8):
		x = self.bikeModel1[12+i].getX()
		
		y = self.bikeModel1[12+i].getY()
		
		pandaPosInterval1 = self.bikeModel1[12+i].posInterval(7.5,
                                                        Point3(x-400, y, self.bikeModel1[12+i].getZ()),
                                                        startPos=Point3( x, y, self.bikeModel1[12+i].getZ()))
		
		
		
																
		self.carParallel5.append(pandaPosInterval1)
		#self.carParallel3.append(pandaPosInterval2)
	self.carParallel5.loop()
	
	x = -390
	y=-560
	k=-560
	z=0
	#self.cycle.setPos(x,y,z)
	for i in range(7):
		
		if(i%2==0):
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
			#self.heartModel.reparentTo(self.track)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setH(90)
			self.bikeModel.setPos(x, y, z)
			self.bikeModel.setScale(1.38)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'red')
		else:
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")
			self.bikeModel.setPos(x, y, z+2.0)
			self.bikeModel.setH(-90)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setScale(1.38)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'blue')
		#elif(i%3==2):
			#self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--policecar-egg/bvw-f2004--policecar/policecar")
			#self.bikeModel.setPos(x, y, z)
			#self.bikeModel.setH(180)
			#self.bikeModel.setScale(1.38)
		#game/game/Models/cat-vehicles-road/bvw-f2004--policecar-egg/bvw-f2004--policecar/policecar
		#Models/cat-vehicles-road/bvw-f2004--fordcar-egg/bvw-f2004--fordcar/ford
		#self.bikeModel = loader.loadModel("Models/cat-vehicles-land/alice-vehicles--trolley-egg/alice-vehicles--trolley/trolley")
	#self.heartModel.reparentTo(render)
		#self.bikeModel.setPos(x, y, z)
		if(i%2==0):
			y= k+5
		else:	
			y= k-5
		x = x+200
		#self.bikeModel.setH(90)
		#self.model12.setPos(-240,-126,1)
		#self.bikeModel.setScale(0.38)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel6 = Parallel(name="carParallel6")
	for i in range(7):
		x = self.bikeModel1[20+i].getX()
		
		y = self.bikeModel1[20+i].getY()
		
		pandaPosInterval1 = self.bikeModel1[20+i].posInterval(14.5,
                                                        Point3(x+700, y, self.bikeModel1[20+i].getZ()),
                                                        startPos=Point3( x-400, y, self.bikeModel1[20+i].getZ()))
		
		
		
																
		self.carParallel6.append(pandaPosInterval1)
	
	self.carParallel6.loop()
	
	
	x=572
	k = 572
	y=-220
	z=0
	#self.cycle.setPos(k,y,z)
	for i in range(10):
		
		#if(i%2==0):
			#self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
	#self.heartModel.reparentTo(render)
			#self.bikeModel.setH(0)
			#self.bikeModel.setPos(x, y, z)
			#self.bikeModel.setScale(1.38)
		#elif(i%4==1):
			#self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")
			#self.bikeModel.setPos(x, y, z+2.0)
			#self.bikeModel.setH(180)
			#self.bikeModel.setScale(1.38)
		if(i%2==0):
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
			self.bikeModel.setPos(x, y, z+2)
			self.bikeModel.setH(0)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setScale(1.7)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'red')
		elif(i%2==1):
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")
			self.bikeModel.setPos(x, y, z)
			self.bikeModel.setH(0)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setScale(1.38)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'blue')
		#self.bikeModel = loader.loadModel("Models/cat-vehicles-land/alice-vehicles--trolley-egg/alice-vehicles--trolley/trolley")
	#self.heartModel.reparentTo(render)
		#self.bikeModel.setPos(x, y, z)
		if(i%2==0):
			x= k+5
		else:	
			x= k-5
		y = y+100
		#self.bikeModel.setH(0)
		#self.model12.setPos(-240,-126,1)
		#self.bikeModel.setScale(0.38)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel8 = Parallel(name="carParallel8")
	for i in range(10):
		x = self.bikeModel1[27+i].getX()
		
		y = self.bikeModel1[27+i].getY()
		
		pandaPosInterval1 = self.bikeModel1[27+i].posInterval(20.5,
                                                        Point3(x, self.bikeModel1[27+i].getY()+400, self.bikeModel1[26+i].getZ()),
                                                        startPos=Point3( x, self.bikeModel1[27+i].getY()-700, self.bikeModel1[26+i].getZ()))
		
		
		
																
		self.carParallel8.append(pandaPosInterval1)
	
	self.carParallel8.loop()
	
	
	
	x= -531
	k = -531
	y=-220
	z=0
	#self.cycle.setPos(x,y,z)
	for i in range(4):
		if(i%2==0):
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--carnsx-egg/bvw-f2004--carnsx/carnsx")
	#self.heartModel.reparentTo(render)
			self.bikeModel.setH(0)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setPos(x, y, z)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'red')
		else:
			self.bikeModel = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--girlscar-egg/bvw-f2004--girlscar/girlcar")
			self.bikeModel.setPos(x, y, z+2.0)
			self.bikeModel.reparentTo(self.track)
			self.bikeModel.setH(180)
			self.lightobj = Light()
			self.lightobj.loadchar(self.bikeModel,'blue')
		if(i%2==0):
			x= k+10
		else:	
			x= k-10
		y = y-200
		#self.bikeModel.setH(180)
		#self.model12.setPos(-240,-126,1)
		#if(i%2==0)
		self.bikeModel.setScale(1.4)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		self.bikeCollider = self.bikeModel.attachNewNode(CollisionNode('colliderbike'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.bikeCollider.node().addSolid(CollisionSphere(0, 0, 0, 2.1))
		self.bikeCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.bikeCollider, self.collisionHandler)
		self.bikeModel1.append(self.bikeModel)
		self.bikeCollider1.append(self.bikeCollider)	
	
	self.carParallel9 = Parallel(name="carParallel9")
	for i in range(4):
		x = self.bikeModel1[37+i].getX()
		
		y = self.bikeModel1[37+i].getY()
		
		pandaPosInterval1 = self.bikeModel1[37+i].posInterval(12.5,
                                                        Point3(x, y, self.bikeModel1[37+i].getZ()),
                                                        startPos=Point3( x, y+500, self.bikeModel1[37+i].getZ()))
		
		
		
																
		self.carParallel9.append(pandaPosInterval1)
	
	self.carParallel9.loop()
	
	
	x=294
	y = 10
	z=1
	for i in range(15):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		y = y+6
		if(i<8):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel5 = Parallel(name="myParallel5")
	for i in range(15):
		x = self.heartModel1[45+i].getX()
		
		y = self.heartModel1[45+i].getY()
		
		pandaPosInterval1 = self.heartModel1[45+i].posInterval(10,
                                                        Point3(x-10, y, self.heartModel1[45+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[45+i].getZ()))
		
		self.myParallel5.append(pandaPosInterval1)
		
	
	self.myParallel5.loop()
	
	x=277.5
	y = 176
	z=1
	for i in range(15):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		y = y+5
		if(i<8):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel6 = Parallel(name="myParallel6")
	for i in range(15):
		x = self.heartModel1[60+i].getX()
		
		y = self.heartModel1[60+i].getY()
		
		pandaPosInterval1 = self.heartModel1[60+i].posInterval(10,
                                                        Point3(x+10, y, self.heartModel1[60+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[60+i].getZ()))
		
		self.myParallel6.append(pandaPosInterval1)
		
	
	self.myParallel6.loop()
	
	x= -130
	y = 276
	z= 1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x+5
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		#self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel7 = Parallel(name="myParallel7")
	for i in range(25):
		x = self.heartModel1[75+i].getX()
		
		y = self.heartModel1[75+i].getY()
		
		pandaPosInterval1 = self.heartModel1[75+i].posInterval(10,
                                                        Point3(x, y-8, self.heartModel1[75+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[75+i].getZ()))
		
		self.myParallel7.append(pandaPosInterval1)
		
	
	self.myParallel7.loop()
	
	x=-21
	y = 272
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x+5
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel8 = Parallel(name="myParallel8")
	for i in range(25):
		x = self.heartModel1[100+i].getX()
		
		y = self.heartModel1[100+i].getY()
		
		pandaPosInterval1 = self.heartModel1[100+i].posInterval(10,
                                                        Point3(x, y-9, self.heartModel1[100+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[100+i].getZ()))
		
		self.myParallel8.append(pandaPosInterval1)
		
	
	self.myParallel8.loop()
	
	x=-370
	y = 429
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(30)
		x = x-3
		y = y+3
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel9 = Parallel(name="myParallel9")
	for i in range(25):
		x = self.heartModel1[125+i].getX()
		
		y = self.heartModel1[125+i].getY()
		
		pandaPosInterval1 = self.heartModel1[125+i].posInterval(10,
                                                        Point3(x-7, y, self.heartModel1[125+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[125+i].getZ()))
		
		self.myParallel9.append(pandaPosInterval1)
		
	
	self.myParallel9.loop()
	
	
	x=-260
	y = 46
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x-2.5
		y = y+0.2
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel10 = Parallel(name="myParallel10")
	for i in range(25):
		x = self.heartModel1[150+i].getX()
		
		y = self.heartModel1[150+i].getY()
		
		pandaPosInterval1 = self.heartModel1[150+i].posInterval(10,
                                                        Point3(x-5, y, self.heartModel1[150+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[150+i].getZ()))
		
		self.myParallel10.append(pandaPosInterval1)
		
	
	self.myParallel10.loop()
	
	x=-526
	y = 58
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x+2.5
		y = y-1
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel11 = Parallel(name="myParallel11")
	for i in range(25):
		x = self.heartModel1[175+i].getX()
		
		y = self.heartModel1[175+i].getY()
		
		pandaPosInterval1 = self.heartModel1[175+i].posInterval(10,
                                                        Point3(x-5, y, self.heartModel1[175+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[175+i].getZ()))
		
		self.myParallel11.append(pandaPosInterval1)
		
	
	self.myParallel11.loop()
	
	x=-516
	y = 230
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		x = x
		y = y+4
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel12 = Parallel(name="myParallel12")
	for i in range(25):
		x = self.heartModel1[200+i].getX()
		
		y = self.heartModel1[200+i].getY()
		
		pandaPosInterval1 = self.heartModel1[200+i].posInterval(10,
                                                        Point3(x-5, y, self.heartModel1[200+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[200+i].getZ()))
		
		self.myParallel12.append(pandaPosInterval1)
		
	
	self.myParallel12.loop()
	
	x=-521
	y = 331
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		x = x
		y = y+4
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel13 = Parallel(name="myParallel13")
	for i in range(25):
		x = self.heartModel1[225+i].getX()
		
		y = self.heartModel1[225+i].getY()
		
		pandaPosInterval1 = self.heartModel1[225+i].posInterval(10,
                                                        Point3(x-5, y, self.heartModel1[225+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[225+i].getZ()))
		
		self.myParallel13.append(pandaPosInterval1)
		
	
	self.myParallel13.loop()
	
	
	
	x=569
	y = -145
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		x = x
		y = y-4
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel14 = Parallel(name="myParallel14")
	for i in range(25):
		x = self.heartModel1[250+i].getX()
		
		y = self.heartModel1[250+i].getY()
		
		pandaPosInterval1 = self.heartModel1[250+i].posInterval(10,
                                                        Point3(x-5, y, self.heartModel1[250+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[250+i].getZ()))
		
		self.myParallel13.append(pandaPosInterval1)
		
	
	self.myParallel14.loop()
	
	x=360
	y = -561
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x-5
		#y = y+8
		if(i<14):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel15 = Parallel(name="myParallel15")
	for i in range(25):
		x = self.heartModel1[275+i].getX()
		
		y = self.heartModel1[275+i].getY()
		
		pandaPosInterval1 = self.heartModel1[275+i].posInterval(8,
                                                        Point3(x, y-4, self.heartModel1[275+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[275+i].getZ()))
		
		self.myParallel15.append(pandaPosInterval1)
		
	
	self.myParallel15.loop()
	
	x=56
	y = -548
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x+5
		#y = y+8
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel16 = Parallel(name="myParallel16")
	for i in range(25):
		x = self.heartModel1[300+i].getX()
		
		y = self.heartModel1[300+i].getY()
		
		pandaPosInterval1 = self.heartModel1[300+i].posInterval(8,
                                                        Point3(x, y-4, self.heartModel1[300+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[300+i].getZ()))
		
		self.myParallel16.append(pandaPosInterval1)
		
	
	self.myParallel16.loop()
	
	x=3.5
	y = -477
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		#x = x+10
		y = y+4
		if(i<13):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel17 = Parallel(name="myParallel17")
	for i in range(25):
		x = self.heartModel1[325+i].getX()
		
		y = self.heartModel1[325+i].getY()
		
		pandaPosInterval1 = self.heartModel1[325+i].posInterval(10,
                                                        Point3(x-5, y, self.heartModel1[325+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[325+i].getZ()))
		
		self.myParallel17.append(pandaPosInterval1)
		
	
	self.myParallel17.loop()
	
	x=-144
	y = -547
	z=1
	for i in range(25):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		self.heartModel.setH(90)
		x = x-4
		#y = y+8
		if(i<14):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel18 = Parallel(name="myParallel18")
	for i in range(25):
		x = self.heartModel1[350+i].getX()
		
		y = self.heartModel1[350+i].getY()
		
		pandaPosInterval1 = self.heartModel1[350+i].posInterval(10,
                                                        Point3(x, y+5, self.heartModel1[350+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[350+i].getZ()))
		
		self.myParallel18.append(pandaPosInterval1)
		
	
	self.myParallel18.loop()
	
	
	x=-530
	y = -388
	z=1
	for i in range(35):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		#x = x+10
		y = y+4
		if(i<17):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel19 = Parallel(name="myParallel19")
	for i in range(35):
		x = self.heartModel1[375+i].getX()
		
		y = self.heartModel1[375+i].getY()
		
		pandaPosInterval1 = self.heartModel1[375+i].posInterval(10,
                                                        Point3(x+4, y, self.heartModel1[375+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[375+i].getZ()))
		
		self.myParallel19.append(pandaPosInterval1)
		
	
	self.myParallel19.loop()
	
	x=581
	y = 284
	z=1
	for i in range(35):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		#x = x+10
		y = y-4
		if(i<17):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel20 = Parallel(name="myParallel20")
	for i in range(35):
		x = self.heartModel1[410+i].getX()
		
		y = self.heartModel1[410+i].getY()
		
		pandaPosInterval1 = self.heartModel1[410+i].posInterval(10,
                                                        Point3(x-4, y, self.heartModel1[410+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[410+i].getZ()))
		
		self.myParallel20.append(pandaPosInterval1)
		
	
	self.myParallel20.loop()
	
	x=55
	y = 340
	z=1
	for i in range(20):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		#x = x+10
		y = y+4
		if(i<10):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel21 = Parallel(name="myParallel21")
	for i in range(20):
		x = self.heartModel1[445+i].getX()
		
		y = self.heartModel1[445+i].getY()
		
		pandaPosInterval1 = self.heartModel1[445+i].posInterval(10,
                                                        Point3(x-4, y, self.heartModel1[445+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[445+i].getZ()))
		
		self.myParallel21.append(pandaPosInterval1)
		
	
	self.myParallel21.loop()
	
	x=162
	y = 555
	z=1
	for i in range(40):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		x = x+4
		#y = y+10
		if(i<20):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel22 = Parallel(name="myParallel22")
	for i in range(40):
		x = self.heartModel1[465+i].getX()
		
		y = self.heartModel1[465+i].getY()
		
		pandaPosInterval1 = self.heartModel1[465+i].posInterval(10,
                                                        Point3(x, y-4, self.heartModel1[465+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[465+i].getZ()))
		
		self.myParallel22.append(pandaPosInterval1)
		
	
	self.myParallel22.loop()
	
	x=162
	y = 555
	z=1
	for i in range(30):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		x = x-4
		#y = y+10
		if(i<15):
			z = z+0.07
		else:
			z = z-0.07
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel23 = Parallel(name="myParallel23")
	for i in range(30):
		x = self.heartModel1[505+i].getX()
		
		y = self.heartModel1[505+i].getY()
		
		pandaPosInterval1 = self.heartModel1[505+i].posInterval(10,
                                                        Point3(x, y-4, self.heartModel1[505+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[505+i].getZ()))
		
		self.myParallel23.append(pandaPosInterval1)
		
	
	self.myParallel23.loop()
	
	self.carParallel4.loop()
	#BROKEN_LOVE_MASK=BitMask32.bit(2)
	
	
	x=570
	y = -471
	z=0.8
	for i in range(30):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		#x = x-10
		y = y+4
		if(i<15):
			z = z+0.16;
		else:
			z = z-0.16;
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel24 = Parallel(name="myParallel24")
	for i in range(30):
		x = self.heartModel1[535+i].getX()
		
		y = self.heartModel1[535+i].getY()
		
		pandaPosInterval1 = self.heartModel1[535+i].posInterval(5,
                                                        Point3(x, y, self.heartModel1[535+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[535+i].getZ()))
		
		self.myParallel24.append(pandaPosInterval1)
		
	
	self.myParallel24.loop()
	
	
	x=490
	y = -32.6
	z=0.8
	for i in range(20):
		self.heartModel = loader.loadModel("Models/coin/coin1")
		self.heartModel.setPos(x, y, z)
		self.heartModel.setP(90)
		x = x-10
		#y = y+10
		if(i<10):
			z = z+0.16;
		else:
			z = z-0.16;
		#self.model12.setPos(-240,-126,1)
		self.heartModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.heartModel.reparentTo(self.track)
		self.heartCollider = self.heartModel.attachNewNode(CollisionNode('collider'))
	# let's mark it as a from collider and with its distinct mask as well
	
		self.heartCollider.node().addSolid(CollisionSphere(0, 0, 0, 3.5))
		self.heartCollider.node().setFromCollideMask(LOVE_MASK)
		self.cTrav.addCollider(self.heartCollider, self.collisionHandler)
		self.heartModel1.append(self.heartModel)
		self.heartCollider1.append(self.heartCollider)
	self.myParallel25 = Parallel(name="myParallel25")
	for i in range(20):
		x = self.heartModel1[565+i].getX()
		
		y = self.heartModel1[565+i].getY()
		
		pandaPosInterval1 = self.heartModel1[565+i].posInterval(5,
                                                        Point3(x, y, self.heartModel1[535+i].getZ()),
                                                        startPos=Point3( x, y, self.heartModel1[535+i].getZ()))
		
		self.myParallel25.append(pandaPosInterval1)
		
	
	self.myParallel25.loop()
	
	self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
	
	self.bikeModel.setH(0)
	self.bikeModel.setPos(-438,-497,0)
	self.bikeModel.setScale(1.58)
	# this is just to move the heart - never mind it
	self.bikeModel.reparentTo(self.track)
	self.treeModel1.append(self.bikeModel)
	
	self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
	
	self.bikeModel.setH(0)
	self.bikeModel.setPos(145,409,0)
	self.bikeModel.setScale(4.58)
	# this is just to move the heart - never mind it
	self.bikeModel.reparentTo(self.track)
	self.treeModel1.append(self.bikeModel)
	
	self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
	
	self.bikeModel.setH(0)
	self.bikeModel.setPos(69,-437,0)
	self.bikeModel.setScale(1.58)
	# this is just to move the heart - never mind it
	self.bikeModel.reparentTo(self.track)
	self.treeModel1.append(self.bikeModel)
	
	self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
	
	self.bikeModel.setH(0)
	self.bikeModel.setPos(114,-498,0)
	self.bikeModel.setScale(1.58)
	# this is just to move the heart - never mind it
	self.bikeModel.reparentTo(self.track)
	self.treeModel1.append(self.bikeModel)
	
	
	x= -636
	k = -636
	y=-594
	z=0
	for i in range(20):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		x = x+30
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.88)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 33
	k = -378
	y=-378
	z=0
	for i in range(6):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		y = y+10
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 536
	k = -378
	y=15
	z=0
	for i in range(20):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		y = y+20
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 528
	k = -492
	y=-492
	z=0
	for i in range(16):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		y = y+25
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 606
	k = -492
	y=599
	z=0
	for i in range(13):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		y = y-25
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	#x= 490
	#k = -492
	#y=509
	#z=0
	#for i in range(13):
	
		#self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		#y = y-25
		#self.bikeModel.setH(0)
		#self.bikeModel.setPos(x,y,z)
		#self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		#self.treeModel1.append(self.bikeModel)
	
	#x= 265
	#k = -492
	#y=57
	#z=0
	#for i in range(13):
	
		#self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		#y = y+25
		#self.bikeModel.setH(0)
		#self.bikeModel.setPos(x,y,z)
		#self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		#self.treeModel1.append(self.bikeModel)
	
	x= 268
	k = 246
	y=246
	z=0
	for i in range(8):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		x = x-25
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 260
	
	y=240
	z=0
	for i in range(8):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		
		y = y-25
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	#x= -429
	
	#y=455
	#z=0
	#for i in range(17):
	
		#self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		#x = x+4
		#y = y-4
		#self.bikeModel.setH(0)
		#self.bikeModel.setPos(x,y,z)
		#self.bikeModel.setScale(0.58)
	# this is just to move the heart - never mind it
		#self.bikeModel.reparentTo(self.track)
		#self.treeModel1.append(self.bikeModel)
	
	x= -657
	
	y=528
	z=0
	for i in range(4):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		x = x+6
		y = y-8
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(1.58)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 382
	
	y=11.96
	z=0
	for i in range(10):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		x = x+14
		y = y-0.8
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.8)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 308
	
	y=257
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(20):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		#x = x+14
		y = y-20
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.4)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 497
	
	y=502
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(19):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		x = x-15
		y = y-0.2
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 495
	
	y=500
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(19):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		x = x-10
		y = y-10
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.5)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 10
	
	y=550
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(12):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/alice-nature--shrubbery-egg/alice-nature--shrubbery/shrubbery")
		
		x = x-0.4
		y = y-20
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.15)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= -430
	
	y=551
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(12):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/alice-nature--shrubbery-egg/alice-nature--shrubbery/shrubbery")
		
		x = x+20
		#y = y-20
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.15)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= -413
	
	y=550
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(4):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/alice-nature--shrubbery-egg/alice-nature--shrubbery/shrubbery")
		
		x = x-5
		y = y-6
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.15)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	
	
	x= -480
	
	y=510
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(15):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		
		x = x+14
		y = y-14
		self.bikeModel.setH(0)
		self.bikeModel.setPos(x,y,z)
		self.bikeModel.setScale(0.35)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	
	x= -482
	
	y=521
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(22):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		self.bikeModel.setPos(x,y,z)
		#x = x+8
		y = y-20
		self.bikeModel.setH(0)
		
		self.bikeModel.setScale(0.15)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= -527
	
	y=571
	z=0
	#self.cycle.setPos(x+500,y+2,0)
	
	for i in range(9):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		self.bikeModel.setPos(x,y,z)
		
		y = y-12
		x= x-7
		self.bikeModel.setH(0)
		
		self.bikeModel.setScale(0.55)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= 424
	
	y=-312
	z=0
	#self.cycle.setPos(x+24,y,0)
	
	for i in range(4):
	
		self.bikeModel = loader.loadModel("Models/cat-plants/bvw-f2004--plant1-egg/bvw-f2004--plant1/plants1")
		self.bikeModel.setPos(x,y,z)
		
		y = y+25
		x= x-30
		self.bikeModel.setH(0)
		
		self.bikeModel.setScale(0.55)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= -269
	
	y=88
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(21):
	
		self.bikeModel = loader.loadModel("Models/ChristmasTree/ChristmasTree")
		self.bikeModel.setPos(x,y,z)
		
		y = y+0.02
		x= x-10
		self.bikeModel.setH(0)
		
		self.bikeModel.setScale(0.8)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	x= -268
	
	y=88
	z=0
	#self.cycle.setPos(x,y,0)
	
	for i in range(14):
	
		self.bikeModel = loader.loadModel("Models/ChristmasTree/ChristmasTree")
		self.bikeModel.setPos(x,y,z)
		
		y = y+15
		#x= x-10
		self.bikeModel.setH(0)
		
		self.bikeModel.setScale(0.8)
	# this is just to move the heart - never mind it
		self.bikeModel.reparentTo(self.track)
		self.treeModel1.append(self.bikeModel)
	
	
	
	self.mod4gg1 = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--firetruck-egg/bvw-f2004--firetruck/firetruck")
	self.mod4gg1.reparentTo(self.track)
	#self.gardenCollider = self.heartModel.attachNewNode(CollisionNode('collider1'))
	#self.gardenCollider.node().addSolid(CollisionSphere(100, 100, 0, 19999))
	#self.gardenCollider.node().setFromCollideMask(LOVE_MASK)
	#self.cTrav.addCollider(self.gardenCollider, self.collisionHandler)
	self.mod4gg1.setPos(483,-400,0)
	self.mod4gg1.setH(80)
	self.mod4gg1.setScale(0.83)
	self.lm.append(self.mod4gg1)
	#self.cycle.setPos(self.mod4gg1.getPos())
	self.mod4gg = loader.loadModel("Models/garden/garden")
	self.mod4gg.reparentTo(self.track)
	#self.gardenCollider = self.heartModel.attachNewNode(CollisionNode('collider1'))
	#self.gardenCollider.node().addSolid(CollisionSphere(100, 100, 0, 19999))
	#self.gardenCollider.node().setFromCollideMask(LOVE_MASK)
	#self.cTrav.addCollider(self.gardenCollider, self.collisionHandler)
	self.mod4gg.setPos(-387,189,-0.1)
	self.mod4gg.setH(0)
	self.mod4gg.setScale(1.23,1.230,1.230)
	self.lm.append(self.mod4gg)
	self.g4 = loader.loadModel("Models/garden/garden")
	self.g4.reparentTo(self.track)
	#self.gardenCollider = self.heartModel.attachNewNode(CollisionNode('collider1'))
	#self.gardenCollider.node().addSolid(CollisionSphere(100, 100, 0, 19999))
	#self.gardenCollider.node().setFromCollideMask(LOVE_MASK)
	#self.cTrav.addCollider(self.gardenCollider, self.collisionHandler)
	self.g4.setPos(168,728,-0.1)
	self.g4.setH(0)
	self.g4.setScale(1.20,1.20,1.20)
	self.lm.append(self.g4)
	self.mod5gg = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.mod5gg.reparentTo(self.track)
	self.mod5gg.setPos(-612,-129,-0.1)
	self.mod5gg.setH(-90)
	self.mod5gg.setScale(2.80,2.80,2.80)
	self.lm.append(self.mod5gg)
	self.t1 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t1.reparentTo(self.track)
	self.t1.setPos(-321,-33,-0.1)
	self.t1.setH(-90)
	self.t1.setScale(2.30,2.30,2.30)
	self.lm.append(self.t1)
	self.t2 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t2.reparentTo(self.track)
	self.t2.setPos(-295,-66,-0.1)
	self.t2.setH(-90)
	self.t2.setScale(2.30,2.30,2.30)
	self.lm.append(self.t2)
	self.t3 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t3.reparentTo(self.track)
	self.t3.setPos(-294.6,-110,-0.1)
	self.t3.setH(-90)
	self.t3.setScale(2.30,2.30,2.30)
	self.lm.append(self.t3)
	self.t4 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t4.reparentTo(self.track)
	self.t4.setPos(-294.5,-151,-0.1)
	self.t4.setH(-90)
	self.t4.setScale(2.30,2.30,2.30)
	self.lm.append(self.t4)
	self.t5 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t5.reparentTo(self.track)
	self.t5.setPos(-125,-210,-0.1)
	self.t5.setH(-180)
	self.t5.setScale(2.30,2.30,2.30)
	self.lm.append(self.t5)
	self.t6 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t6.reparentTo(self.track)
	self.t6.setPos(-104.7,-210.3,-0.1)
	#self.t6.setPos(-104.7,-230.3,-0.1)
	self.t6.setH(-180)
	self.t6.setScale(2.30,2.30,2.30)
	self.lm.append(self.t6)
	self.t7 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t7.reparentTo(self.track)
	self.t7.setPos(-81,-210,-0.1)
	self.t7.setH(-180)
	self.t7.setScale(2.30,2.30,2.30)
	self.lm.append(self.t7)
	self.t8 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t8.reparentTo(self.track)
	self.t8.setPos(-61,-210.1,-0.1)
	self.t8.setH(-180)
	self.t8.setScale(2.30,2.30,2.30)
	self.lm.append(self.t8)
	self.t9 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t9.reparentTo(self.track)
	self.t9.setPos(-1.87,-210,-0.1)
	self.t9.setH(-180)
	self.t9.setScale(2.30,2.30,2.30)
	self.lm.append(self.t9)
	#self.lm.append(self.t6)
	self.t10 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t10.reparentTo(self.track)
	self.t10.setPos(35,-210,-0.1)
	self.t10.setH(-180)
	self.t10.setScale(2.30,2.30,2.30)
	self.lm.append(self.t10)
	self.t11 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t11.reparentTo(self.track)
	self.t11.setPos(76,-210,-0.1)
	self.t11.setH(-180)
	self.t11.setScale(2.30,2.30,2.30)
	self.lm.append(self.t11)
	self.t12 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t12.reparentTo(self.track)
	self.t12.setPos(153,-210,-0.1)
	self.t12.setH(-180)
	self.t12.setScale(2.30,2.30,2.30)
	self.lm.append(self.t12)
	self.t13 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t13.reparentTo(self.track)
	self.t13.setPos(153,-210,-0.1)
	self.t13.setH(-180)
	self.t13.setScale(2.30,2.30,2.30)
	self.lm.append(self.t13)
	self.t14 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t14.reparentTo(self.track)
	self.t14.setPos(-185,216,-0.1)
	self.t14.setH(0)
	self.t14.setScale(2.30,2.30,2.30)
	self.lm.append(self.t14)
	self.t15 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t15.reparentTo(self.track)
	self.t15.setPos(-145,216,-0.1)
	self.t15.setH(0)
	self.t15.setScale(2.30,2.30,2.30)
	self.lm.append(self.t15)
	self.t16 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t16.reparentTo(self.track)
	self.t16.setPos(-100,216,-0.1)
	self.t16.setH(0)
	self.t16.setScale(2.30,2.30,2.30)
	self.lm.append(self.t16)
	self.t17 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t17.reparentTo(self.track)
	self.t17.setPos(-60,216,-0.1)
	self.t17.setH(0)
	self.t17.setScale(2.30,2.30,2.30)
	self.lm.append(self.t17)
	self.t18 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t18.reparentTo(self.track)
	self.t18.setPos(-20,216,-0.1)
	self.t18.setH(0)
	self.t18.setScale(2.30,2.30,2.30)
	self.lm.append(self.t18)
	self.t19 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t19.reparentTo(self.track)
	self.t19.setPos(20,216,-0.1)
	self.t19.setH(0)
	self.t19.setScale(2.30,2.30,2.30)
	self.lm.append(self.t19)
	self.t20 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t20.reparentTo(self.track)
	self.t20.setPos(60,216,-0.1)
	self.t20.setH(0)
	self.t20.setScale(2.30,2.30,2.30)
	self.lm.append(self.t20)
	self.t21 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t21.reparentTo(self.track)
	self.t21.setPos(100,216,-0.1)
	self.t21.setH(0)
	self.t21.setScale(2.30,2.30,2.30)
	self.lm.append(self.t21)
	self.t22 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t22.reparentTo(self.track)
	self.t22.setPos(140,216,-0.1)
	self.t22.setH(0)
	self.t22.setScale(2.30,2.30,2.30)
	self.lm.append(self.t22)
	self.t23 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t23.reparentTo(self.track)
	self.t23.setPos(669,-400,-0.1)
	self.t23.setH(90)
	self.t23.setScale(3.40,3.40,3.40)
	self.lm.append(self.t23)
	self.t24 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t24.reparentTo(self.track)
	self.t24.setPos(669,-300,-0.1)
	self.t24.setH(90)
	self.t24.setScale(3.40,3.40,3.40)
	self.lm.append(self.t24)
	self.t25 = loader.loadModel("Models/Townhouse1/Townhouse1")
	self.t25.reparentTo(self.track)
	self.t25.setPos(669,-200,-0.1)
	self.t25.setH(90)
	self.t25.setScale(3.40,3.40,3.40)
	self.lm.append(self.t25)
	self.t23a = loader.loadModel("Models/CityHall/CityHall")
	self.t23a.reparentTo(self.track)
	self.t23a.setPos(145,342,-0.6)
	self.t23a.setH(180)
	self.t23a.setScale(1.30,1.30,1.30)
	self.lm.append(self.t23a)
	self.b1 = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.b1.reparentTo(self.track)
	self.b1.setPos(-80,411.527,0)
	self.b1.setH(0)
	self.b1.setScale(1.90,1.90,1.90)
	self.lm.append(self.b1)
	self.b2s = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.b2s = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.b2s.reparentTo(self.track)
	self.b2s.setPos(685,80.527,0)
	self.b2s.setH(0)
	self.b2s.setScale(1.90,1.90,1.90)
	self.lm.append(self.b2s)
	self.b1e = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.b1e.reparentTo(self.track)
	self.b1e.setPos(-602,648.527,0)
	self.b1e.setH(0)
	self.b1e.setScale(2.40,2.40,2.40)
	self.lm.append(self.b1e)
	self.b2e = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.b2e.reparentTo(self.track)
	self.b2e.setPos(-668,158.527,0)
	self.b2e.setH(0)
	self.b2e.setScale(2.40,2.40,2.40)
	self.lm.append(self.b2e)
	self.b3e = loader.loadModel("Models/cat-buildings/alice-city--church-egg/alice-city--church/church")
	self.b3e.reparentTo(self.track)
	self.b3e.setPos(-680,5.527,0)
	self.b3e.setH(0)
	self.b3e.setScale(3.90,3.90,3.90)
	self.lm.append(self.b3e)
	
	self.b3e1 = loader.loadModel("Models/cat-buildings/alice-city--church-egg/alice-city--church/church")
	self.b3e1.reparentTo(self.track)
	self.b3e1.setPos(-115,-446,-1)
	self.b3e1.setH(0)
	self.b3e1.setScale(2.60,2.60,2.60)
	self.lm.append(self.b3e1)
	#self.cycle.setPos(self.b3e1.getPos())
	self.b4e = loader.loadModel("Models/stadium/stadium")
	self.b4e.reparentTo(self.track)
	self.b4e.setPos(-748,-704.527,0)
	self.b4e.setH(0)
	self.b4e.setScale(0.70,0.70,0.70)
	self.lm.append(self.b4e)
	self.b5e = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.b5e.reparentTo(self.track)
	self.b5e.setPos(689,-604.527,0)
	self.b5e.setH(0)
	self.b5e.setScale(3.00,3.00,3.00)
	self.lm.append(self.b5e)
	self.b5x = loader.loadModel("Models/BuildingCluster5/BuildingCluster5")
	self.b5x.reparentTo(self.track)
	self.b5x.setPos(368,689.527,0)
	self.b5x.setH(0)
	self.b5x.setScale(3.00,3.00,3.00)
	self.lm.append(self.b5x)
	self.b6e = loader.loadModel("Models/cat-buildings/alice-farm--farmhouse-egg/alice-farm--farmhouse/farmhouse")
	self.b6e.reparentTo(self.track)
	self.b6e.setPos(494.6,-667,-0.1)
	self.b6e.setH(0)
	self.b6e.setScale(2.70,2.70,2.70)
	self.lm.append(self.b6e)
	self.b6e1 = loader.loadModel("Models/cat-buildings/alice-farm--farmhouse-egg/alice-farm--farmhouse/farmhouse")
	self.b6e1.reparentTo(self.track)
	self.b6e1.setPos(360,-464,-0.1)
	self.b6e1.setH(0)
	self.b6e1.setScale(2.60,2.60,2.60)
	self.lm.append(self.b6e1)
	self.b3k = loader.loadModel("Models/cat-buildings/alice-city--church-egg/alice-city--church/church")
	self.b3k.reparentTo(self.track)
	self.b3k.setPos(685,280.527,0)
	self.b3k.setH(90)
	self.b3k.setScale(2.90,2.90,2.90)
	self.lm.append(self.b3k)
	self.b7e = loader.loadModel("Models/BuildingCluster2/BuildingCluster2")
	self.b7e.reparentTo(self.track)
	self.b7e.setPos(-299,-439.527,0)
	self.b7e.setH(90)
	self.b7e.setScale(2.40,2.40,2.40)
	self.lm.append(self.b7e)
	self.b8e = loader.loadModel("Models/cat-buildings/bvw-f2004--russianbuilding/tetris-building")

	self.b8e.reparentTo(self.track)
	self.b8e.setScale(12.170,12.170,12.170)
	self.b8e.setH(0)
	self.b8e.setPos(217,-648,-0.6)
	self.lm.append(self.b8e)
	self.b9e = loader.loadModel("Models/BuildingCluster2/BuildingCluster2")

	self.b9e.reparentTo(self.track)
	self.b9e.setScale(6.370,6.370,6.370)
	self.b9e.setH(0)
	self.b9e.setPos(12,-748,-0.6)
	self.lm.append(self.b9e)
	self.b9a = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")

	self.b9a.reparentTo(self.track)
	self.b9a.setScale(1.470,1.470,1.470)
	self.b9a.setH(0)
	self.b9a.setPos(-372,-251,-0.6)
	self.lm.append(self.b9a)
	self.b1a = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")
	self.b1a.reparentTo(self.track)
	self.b1a.setScale(2.370,2.370,2.370)
	self.b1a.setH(0)
	self.b1a.setPos(9,725,-0.6)
	self.lm.append(self.b1a)
	self.b9f = loader.loadModel("Models/BuildingCluster2/BuildingCluster2")

	self.b9f.reparentTo(self.track)
	self.b9f.setScale(3.870,3.870,3.870)
	self.b9f.setH(0)
	self.b9f.setPos(524,668,-0.6)
	self.lm.append(self.b9f)
	self.b1f = loader.loadModel("Models/BuildingCluster2/BuildingCluster2")

	self.b1f.reparentTo(self.track)
	self.b1f.setScale(6.570,6.570,6.570)
	self.b1f.setH(0)
	self.b1f.setPos(-80,38,-0.6)
	self.lm.append(self.b1f)
	self.b1z = loader.loadModel("Models/BuildingCluster3/BuildingCluster3")

	self.b1z.reparentTo(self.track)
	self.b1z.setScale(1.470,1.470,1.470)
	self.b1z.setH(0)
	self.b1z.setPos(-457,-230,-0.6)
	self.lm.append(self.b1z)
	self.env43a = loader.loadModel("Models/cat-carnival-and-arcade/alice-amusement-park--funhouse-egg/alice-amusement-park--funhouse/funhouse")
	self.env43a.reparentTo(self.track)
	self.env43a.setScale(4.370,4.370,4.370)
	self.env43a.setH(-60)
	self.env43a.setPos(729,475,0)
	self.lm.append(self.env43a)
	self.gaz1 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz1.reparentTo(self.track)
	self.gaz1.setScale(4.50,4.50,4.50)
	self.gaz1.setPos(73,-634,0)
	self.lm.append(self.gaz1)
	
	self.gaz1a = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz1a.reparentTo(self.track)
	self.gaz1a.setScale(5.50,5.50,5.50)
	self.gaz1a.setPos(217,205,0)
	self.lm.append(self.gaz1a)
	
	self.gaz2a = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz2a.reparentTo(self.track)
	self.gaz2a.setScale(4.50,4.50,4.50)
	self.gaz2a.setPos(152,453,0)
	self.lm.append(self.gaz2a)
	
	self.gaz2 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz2.reparentTo(self.track)
	self.gaz2.setScale(4.50,4.50,4.50)
	self.gaz2.setPos(265,-337,0)
	self.lm.append(self.gaz2)
	self.gaz3 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz3.reparentTo(self.track)
	self.gaz3.setScale(4.50,4.50,4.50)
	self.gaz3.setPos(404,48,0)
	self.lm.append(self.gaz3)
	self.gaz4 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz4.reparentTo(self.track)
	self.gaz4.setScale(4.50,4.50,4.50)
	self.gaz4.setPos(486,364,0)
	self.lm.append(self.gaz4)
	self.gaz5 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz5.reparentTo(self.track)
	self.gaz5.setScale(4.50,4.50,4.50)
	self.gaz5.setPos(225,-211,0)
	self.lm.append(self.gaz5)
	self.gaz6 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz6.reparentTo(self.track)
	self.gaz6.setScale(4.50,4.50,4.50)
	self.gaz6.setPos(-460,-364,0)
	self.lm.append(self.gaz6)
	self.gaz7 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz7.reparentTo(self.track)
	self.gaz7.setScale(2.50,2.50,2.50)
	self.gaz7.setPos(-394,-475,0)
	self.lm.append(self.gaz7)
	self.gaz8 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz8.reparentTo(self.track)
	self.gaz8.setScale(3.0,3.0,3.0)
	self.gaz8.setPos(79.54,-340.54,0)
	self.lm.append(self.gaz8)
	self.gaz9 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz9.reparentTo(self.track)
	self.gaz9.setScale(3.0,3.0,3.0)
	self.gaz9.setPos(67.54,-479.54,0)
	self.lm.append(self.gaz9)
	self.gaz9a = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaz9a.reparentTo(self.track)
	self.gaz9a.setScale(3.0,3.0,3.0)
	self.gaz9a.setPos(-381.54,502.54,0)
	self.lm.append(self.gaz9a)
	self.gaza = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaza.reparentTo(self.track)
	self.gaza.setScale(3.0,3.0,3.0)
	self.gaza.setPos(-191.54,502.54,0)
	self.lm.append(self.gaza)
	
	self.gaza1 = loader.loadModel("Models/Gazebo/Gazebo")
	self.gaza1.reparentTo(self.track)
	self.gaza1.setScale(3.0,3.0,3.0)
	self.gaza1.setPos(-453,-32,0)
	self.lm.append(self.gaza1)
	#self.cycle.setPos(self.gaza1.getPos())
	self.mod6 = loader.loadModel("Models/cat-buildings/alice-farm--farmhouse-egg/alice-farm--farmhouse/farmhouse")
	self.mod6.reparentTo(self.track)
	self.mod6.setPos(78,-391,-0.1)
	self.mod6.setH(0)
	self.mod6.setScale(1.70,1.70,1.70)
	self.lm.append(self.mod6)
	self.mod61 = loader.loadModel("Models/cat-buildings/alice-farm--farmhouse-egg/alice-farm--farmhouse/farmhouse")
	self.mod61.reparentTo(self.track)
	self.mod61.setPos(-209,361,-0.1)
	self.mod61.setH(180)
	self.mod61.setScale(1.70,1.70,1.70)
	self.lm.append(self.mod61)
	self.mod6a = loader.loadModel("Models/cat-buildings/alice-farm--farmhouse-egg/alice-farm--farmhouse/farmhouse")
	self.mod6a.reparentTo(self.track)
	self.mod6a.setPos(-473,-307,-0.6)
	self.mod6a.setH(180)
	self.mod6a.setScale(1.30,1.30,1.30)
	self.lm.append(self.mod6a)
	self.mod6c = loader.loadModel("Models/cat-buildings/alice-farm--farmhouse-egg/alice-farm--farmhouse/farmhouse")
	self.mod6c.reparentTo(self.track)
	self.mod6c.setPos(-415,-342.062,-0.6)
	self.mod6c.setH(180)
	self.mod6c.setScale(1.30,1.30,1.30)
	self.lm.append(self.mod6c)
	self.amb6c = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--firetruck-egg/bvw-f2004--firetruck/firetruck")
	self.amb6c.reparentTo(self.track)
	self.amb6c.setPos(-687,-366.062,-0.6)
	self.amb6c.setH(0)
	self.amb6c.setScale(1.30,1.30,1.30)
	self.lm.append(self.amb6c)
	self.pc6c = loader.loadModel("Models/cat-vehicles-road/bvw-f2004--policecar-egg/bvw-f2004--policecar/policecar")
	self.pc6c.reparentTo(self.track)
	self.pc6c.setPos(-627,-496.062,0.0)
	self.pc6c.setH(0)
	self.pc6c.setScale(1.30,1.30,1.30)
	self.lm.append(self.pc6c)
	
	self.mod4g = loader.loadModel("Models/garden/garden")
	self.mod4g.reparentTo(self.track)
	#self.gardenCollider = self.heartModel.attachNewNode(CollisionNode('collider1'))
	#self.gardenCollider.node().addSolid(CollisionSphere(100, 100, 0, 19999))
	#self.gardenCollider.node().setFromCollideMask(LOVE_MASK)
	#self.cTrav.addCollider(self.gardenCollider, self.collisionHandler)
	self.mod4g.setPos(177,-51,-0.1)
	self.mod4g.setH(0)
	self.mod4g.setScale(1.30,1.30,1.30)
	self.lm.append(self.mod4g)
	self.mod6b1 = loader.loadModel("Models/cat-buildings/alice-city--church-egg/alice-city--church/church")
	self.mod6b1.reparentTo(self.track)
	self.mod6b1.setPos(-463.27,-115,-0.6)
	self.mod6b1.setH(90)
	self.mod6b1.setScale(1.90,1.90,1.90)
	self.lm.append(self.mod6b1)
	self.mod6b2 = loader.loadModel("Models/Tank/Tank")
	self.mod6b2.reparentTo(self.track)
	self.mod6b2.setPos(358.27,65.4,-0.6)
	self.mod6b2.setH(90)
	self.mod6b2.setScale(1.90,1.90,1.90)
	self.lm.append(self.mod6b2)
	
	
	#self.lm.append(self.cycle)
	self.cycleCollider = self.cycle.attachNewNode(CollisionNode('cyclenode'))
	self.cycleCollider.node().addSolid(CollisionSphere(0, 0, 0, 3))
	# ...with the proper mask on...
	self.cycleCollider.node().setIntoCollideMask(LOVE_MASK)
	base.camera.setPos(self.cycle.getX(),self.cycle.getY()+10,2)
	#self.notifier = CollisionHandlerEvent()
	#self.notifier.addInPattern("%fn-in-%in")
	#self.accept("cycle-in-track", self.onCollision)
	#self.cycleFloorHandler = CollisionHandlerGravity()
	#self.cycleFloorHandler.setGravity(9.81+25)
	#self.cycleFloorHandler.setMaxVelocity(100)
	
	self.h1 = loader.loadModel("Models/cat-x1-not-yet-classified/alice-food--banana-egg/alice-food--banana/banana")
	self.h1.reparentTo(self.track)
	self.h1.setScale(6,6,6)
	self.h1.setPos(-250,-223,2)
	#self.h1.setP(90)
	#self.asd = self.h1.hprInterval(1,Vec3(0,360,0))
	#self.asd.loop()
	#self.lm.append(self.h1)
	self.targCollider = self.h1.attachNewNode(CollisionNode('colliderh'))
	self.targCollider.node().addSolid(CollisionSphere(0,0,0,0.02))
	self.targCollider.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider, self.collisionHandler)
	
	self.h1 = loader.loadModel("Models/cat-x1-not-yet-classified/alice-food--banana-egg/alice-food--banana/banana")
	self.h1.reparentTo(self.track)
	self.h1.setScale(6,6,6)
	self.h1.setPos(136,-280,2)
	#self.h1.setP(90)
	#self.asd = self.h1.hprInterval(1,Vec3(0,360,0))
	#self.asd.loop()
	#self.lm.append(self.h1)
	self.targCollider = self.h1.attachNewNode(CollisionNode('colliderh'))
	self.targCollider.node().addSolid(CollisionSphere(0,0,0,0.02))
	self.targCollider.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider, self.collisionHandler)
	
	
	self.h1 = loader.loadModel("Models/cat-x1-not-yet-classified/alice-food--banana-egg/alice-food--banana/banana")
	self.h1.reparentTo(self.track)
	self.h1.setScale(6,6,6)
	self.h1.setPos(288,4,2)
	#self.h1.setP(90)
	#self.asd = self.h1.hprInterval(1,Vec3(0,360,0))
	#self.asd.loop()
	#self.lm.append(self.h1)
	self.targCollider = self.h1.attachNewNode(CollisionNode('colliderh'))
	self.targCollider.node().addSolid(CollisionSphere(0,0,0,0.02))
	self.targCollider.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider, self.collisionHandler)
	
	
	self.h1 = loader.loadModel("Models/cat-x1-not-yet-classified/alice-food--banana-egg/alice-food--banana/banana")
	self.h1.reparentTo(self.track)
	self.h1.setScale(6,6,6)
	self.h1.setPos(-380,-4,2)
	#self.h1.setP(90)
	#self.asd = self.h1.hprInterval(1,Vec3(0,360,0))
	#self.asd.loop()
	#self.lm.append(self.h1)
	self.targCollider = self.h1.attachNewNode(CollisionNode('colliderh'))
	self.targCollider.node().addSolid(CollisionSphere(0,0,0,0.02))
	self.targCollider.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider, self.collisionHandler)
	
	
	self.h1 = loader.loadModel("Models/cat-x1-not-yet-classified/alice-food--banana-egg/alice-food--banana/banana")
	self.h1.reparentTo(self.track)
	self.h1.setScale(6,6,6)
	self.h1.setPos(-517,535,2)
	#self.h1.setP(90)
	#self.asd = self.h1.hprInterval(1,Vec3(0,360,0))
	#self.asd.loop()
	#self.lm.append(self.h1)
	self.targCollider = self.h1.attachNewNode(CollisionNode('colliderh'))
	self.targCollider.node().addSolid(CollisionSphere(0,0,0,0.02))
	self.targCollider.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider, self.collisionHandler)
	
	
	self.h1 = loader.loadModel("Models/cat-x1-not-yet-classified/alice-food--banana-egg/alice-food--banana/banana")
	self.h1.reparentTo(self.track)
	self.h1.setScale(6,6,6)
	self.h1.setPos(583,478,2)
	#self.h1.setP(90)
	#self.asd = self.h1.hprInterval(1,Vec3(0,360,0))
	#self.asd.loop()
	#self.lm.append(self.h1)
	self.targCollider = self.h1.attachNewNode(CollisionNode('colliderh'))
	self.targCollider.node().addSolid(CollisionSphere(0,0,0,0.02))
	self.targCollider.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider, self.collisionHandler)
	
	
	self.env31 = loader.loadModel("Models/Gazebo/Gazebo")
	self.env31.reparentTo(self.track)
	self.env31.setScale(4.50,4.50,4.50)
	self.env31.setPos(73,-634,0)
	self.lm.append(self.env31)
	
	
	self.pandaActor1 = Actor("Models/cat-vehicles-road/bvw-f2004--policecar-egg/bvw-f2004--policecar/policecar")
	self.pandaActor1.reparentTo(self.track)
	#self.pandaActor1.loop("run")
	self.pandaActor1.setScale(0.4)
	#self.lm.append(self.pandaActor1)
	self.pandaActor1.setPos(self.cycle.getPos()+Point3(200,200,0))
	self.targCollider = self.pandaActor1.attachNewNode(CollisionNode('collidera'))
	self.targCollider.node().addSolid(CollisionSphere(0,0,0,1.5))
	self.targCollider.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider, self.collisionHandler)
	self.pandaActor2 = Actor("Models/cat-vehicles-road/bvw-f2004--firetruck-egg/bvw-f2004--firetruck/firetruck")
	self.pandaActor2.reparentTo(self.track)
	#self.pandaActor1.loop("run")
	self.pandaActor2.setScale(0.1)
	#self.lm.append(self.pandaActor1)
	self.pandaActor2.setPos(self.cycle.getPos()+Point3(200,200,0))
	self.targCollider1 = self.pandaActor2.attachNewNode(CollisionNode('colliderb'))
	self.targCollider1.node().addSolid(CollisionSphere(0,0,0,1.5))
	self.targCollider1.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider1, self.collisionHandler)
	self.ralphGroundRay = CollisionRay()
	self.ralphGroundRay.setOrigin(0,0,1000)
	self.ralphGroundRay.setDirection(0,0,-1)
	self.ralphGroundCol = CollisionNode('ralphRay')
	self.ralphGroundCol.addSolid(self.ralphGroundRay)
	#col = self.cycle.attachNewNode(CollisionNode("cycle"))
	#col.node().addSolid(CollisionSphere(0, 0, 0, 1.1))
	#col.show()
	#self.cTrav.addCollider(col, self.notifier)
	
	#self.cnode.setTag("shipid", str(self.id))
	self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
	self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
	self.ralphGroundColNp = self.cycle.attachNewNode(self.ralphGroundCol)
	self.ralphGroundHandler = CollisionHandlerQueue()
	
	#self.cTrav.addCollider(self.cnode, self.raplhGroundHandler)
	#self.cTrav.addCollider(self.ralphGroundColNp, self.cycleFloorHandler)
	
	self.camGroundRay = CollisionRay()
	self.camGroundRay.setOrigin(0,0,1000)
	self.camGroundRay.setDirection(0,0,-1)
	self.camGroundCol = CollisionNode('camRay')
	self.camGroundCol.addSolid(self.camGroundRay)
	self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
	self.camGroundCol.setIntoCollideMask(BitMask32.allOff())
	self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
	self.camGroundHandler = CollisionHandlerQueue()
	self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)
	self.collisionHandler.addInPattern('%fn-into-%in')
	self.collisionHandler.addOutPattern('%fn-out-%in')
	self.collisionHandler.addOutPattern('%in-out-%in')
	self.collisionHandler.addOutPattern('%in-in-%in')
	ambientLight = AmbientLight("ambientLight")
	ambientLight.setColor(Vec4(.3, .3, .3, 1))
	directionalLight = DirectionalLight("directionalLight")
	directionalLight.setDirection(Vec3(-5, -5, -5))
	directionalLight.setColor(Vec4(1, 1, 1, 1))
	directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
	render.setLight(render.attachNewNode(ambientLight))
	render.setLight(render.attachNewNode(directionalLight))
	
	self.ambient = AmbientLight('ambient')
	self.ambient.setColor(Vec4(0.5, 1, 0.5, 1))
	self.ambientNP = self.cycle.attachNewNode(self.ambient)
	self.cycle.setLightOff()
	self.ambient1 = AmbientLight('ambient1')
	self.ambient1.setColor(Vec4(1,0 , 0, 1))
	self.ambientNP1 = self.cycle.attachNewNode(self.ambient1)
	self.cycle.setLightOff()
	#self.cycle.setLight(ambientNP)
	self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)	
	self.accept('collider-into-cyclenode', self.collideEventIn)
	#self.accept('colliderpara-into-cyclenode', self.paracollideEventIn)
	#self.accept('collidermag-into-cyclenode', self.magcollideEventIn)
	self.accept('colliderbike-into-cyclenode', self.bikecollideEventIn)
	self.accept('collider-out-cyclenode', self.collideEventOut)
	#self.accept('colliderpara-out-cyclenode', self.paracollideEventOut)
	self.accept('colliderbike-out-cyclenode', self.bikecollideEventOut)
	#self.accept('collidermag-out-cyclenode', self.magcollideEventOut)
	self.accept('collidera-in-cyclenode', self.collideEventIn1)
	self.accept('collidera-out-cyclenode', self.collideEventOut1)
	self.accept('colliderb-in-cyclenode', self.collideEventIn2)
	self.accept('colliderb-out-cyclenode', self.collideEventOut2)
	#self.setAI(self.pandaActor2)
	#taskMgr.add(self.makelight,"make light")
	#self.sabdis()
	
	#self.lightpivot = render.attachNewNode("lightpivot")
	#self.lightpivot.setPos(0,0,45)
	#self.lightpivot.hprInterval(1000,Point3(360,0,0)).loop()
	self.lightpivot1 = render.attachNewNode("lightpivot1")
	self.lightpivot1.setPos(0,0,45)
	self.lightpivot1.hprInterval(20,Point3(360,0,0)).loop()
	
	
	x= 400
	k = 20
	y=50
	z=15
	
	self.lightpivot2 = render.attachNewNode("lightpivot2")
	self.lightpivot2.setPos(0,0,25)
	self.lightpivot2.hprInterval(k,Point3(360,0,0)).loop()
	k = k+4
	plight2 = PointLight('plight2')
	plight2.setColor(Vec4(1, 1, 1, 1))
	plight2.setAttenuation(Vec3(0.7,0.05,0))
	plnp2 = self.lightpivot2.attachNewNode(plight2)
	plnp2.setPos(x,y,z)
	x = x+200
	y = y+100
	z = z+5
	self.track.setLight(plnp2)
		#sphere = loader.loadModel("Models/cat-shapes/alice-shapes--circle-egg/alice-shapes--circle/circle")
		#sphere.reparentTo(plnp2)
		#sphere.setScale(4.015)
		#sphere.setP(90)
	self.para13 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	#self.para1.reparentTo(self.track)
	#self.para1.setPos(0,0,0)
	self.para13.setH(4)
	self.para13.setScale(0.60)
	self.para13.reparentTo(plnp2)
	self.aeroModel1.append(self.para13)
	self.lightpivot3 = render.attachNewNode("lightpivot3")
	self.lightpivot3.setPos(0,0,25)
	self.lightpivot3.hprInterval(k,Point3(360,0,0)).loop()
	k = k+10
	plight3 = PointLight('plight3')
	plight3.setColor(Vec4(1, 1, 1, 1))
	plight3.setAttenuation(Vec3(0.7,0.05,0))
	plnp3 = self.lightpivot3.attachNewNode(plight3)
	plnp3.setPos(x,y,z)
	x = x+500
	
	z = z+10
	self.track.setLight(plnp3)
		#sphere = loader.loadModel("Models/cat-shapes/alice-shapes--circle-egg/alice-shapes--circle/circle")
		#sphere.reparentTo(plnp2)
		#sphere.setScale(4.015)
		#sphere.setP(90)
	self.sphere = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.sphere.reparentTo(self.track)
	self.sphere.setScale(0.06)
	self.sphere.setH(4)
	self.sphere.setPos(self.cycle.getPos()+Vec3(3,3,2))
	
	self.aeroModel1.append(self.sphere)
	self.lightpivot4 = render.attachNewNode("lightpivot4")
	self.lightpivot4.setPos(0,0,3)
	self.lightpivot4.hprInterval(5,Point3(360,0,0)).loop()
	self.sphere.reparentTo(self.lightpivot4)
	self.para1 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	self.aeroModel1.append(self.para1)
	#self.para1.setPos(0,0,0)
	self.para1.setH(4)
	self.para1.setScale(0.60)
	self.para1.reparentTo(plnp3)
	#self.lm.append(self.para1)
	
	
	plight1 = PointLight('plight1')
	plight1.setColor(Vec4(1, 1, 1, 1))
	plight1.setAttenuation(Vec3(0.7,0.05,0))
	plnp1 = self.lightpivot1.attachNewNode(plight1)
	plnp1.setPos(500,75,25)
	self.track.setLight(plnp1)
	
	alight = AmbientLight('alight')
	alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
	alnp = render.attachNewNode(alight)
	self.track.setLight(alnp)
	#self.sphere = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	#self.sphere.reparentTo(plnp)
	#self.sphere.setScale(6.015)
	#self.sphere.setP(90)
	#self.sphere.setPos(self.cycle.getPos()+Vec3(0,0,3))
	#self.sphere.

	self.para1 = loader.loadModel("Models/cat-vehicles-air/alice-vehicles--boeing707-egg/alice-vehicles--boeing707/boeing707")
	#self.para1.reparentTo(self.track)
	#self.para1.setPos(0,0,0)
	self.para1.setH(4)
	self.para1.setScale(0.80)
	self.para1.reparentTo(plnp1)
	self.aeroModel1.append(self.para1)
	self.track.setShaderAuto()
	self.shaderenable = 1
	
	self.gate1 = loader.loadModel("Models/gate/gate")
	#self.para1.reparentTo(self.track)
	self.gate1.setPos(-243,-53,0)
	#self.gate1.setH(4)
	self.gate1.setScale(0.05)
	self.gate1.reparentTo(self.track)
	
	self.para1a = loader.loadModel("Models/Lever2/Lever2")
	#self.para1.reparentTo(self.track)
	self.para1a.setPos(-229.939,-3.26,1)
	self.para1a.setH(4)
	self.para1a.setScale(3.80)
	self.para1a.reparentTo(self.track)
	self.targCollider1 = self.para1a.attachNewNode(CollisionNode('colliderc'))
	self.targCollider1.node().addSolid(CollisionSphere(0,0,0,0.005))
	self.targCollider1.node().setFromCollideMask(LOVE_MASK)
	self.cTrav.addCollider(self.targCollider1, self.collisionHandler)
	self.accept('colliderc-in-cyclenode', self.collideEventIn3)
	self.accept('colliderc-out-cyclenode', self.collideEventOut3)
	self.accept('colliderh-in-cyclenode', self.collideEventIn4)
	self.accept('colliderh-out-cyclenode', self.collideEventOut4)
	self.cycle.setPos(-229.627,13.4441,0)
	self.cycle.setH(-30)
	
	
	self.visited = []
	for i in range(len(self.heartModel1)):
		self.visited.append(1)
 def destroy1(self ):
	global score
	self.speedobj = Effect()
	self.healthobj = Health()
	self.obj.killobj()
	taskMgr.remove("make env")
	taskMgr.remove("setlight")
	taskMgr.remove("cycle move")
	#taskMgr.remove("make light")
	taskMgr.remove("timerTask")
	taskMgr.remove("hawame") 
	#taskMgr.remove("setlight")
	score=0
	#self.obj.score["text"] = "Score: 00"
	#self.obj.var = 0
	self.cycle.cleanup()
	self.pandaActor1.cleanup()
	for i in range(len(self.aeroModel1)):
		#self.lm[i].cleanup()
		self.aeroModel1[i].removeNode()
	for i in range(len(self.lm)):
		#self.lm[i].cleanup()
		self.lm[i].removeNode()
	for i in range(len(self.treeModel1)):
		#self.lm[i].cleanup()
		self.treeModel1[i].removeNode()	
	for i in range(len(self.heartModel1)):
		#self.heartModel1[i].cleanup()
		self.heartModel1[i].removeNode()
	for i in range(len(self.bikeModel1)):
		#self.bikeModel1[i].cleanup()
		self.bikeModel1[i].removeNode()
	#for i in range(len(self.heartCollider1)):
		#self.heartCollider1[i].removeNode()
	#for i in range(len(self.bikeCollider1)):
		#self.bikeCollider1[i].removeNode()
	self.env16.removeNode()
	self.env17.removeNode()
	self.cycle.detachNode()
	self.lm = []
	self.pandaActor1.removeNode()
	self.aeroModel1 = []
	self.heartModel1 = []
	self.bikeModel1 = []
	self.treeModel1 = []
	self.heartCollider1=[]
	self.bikeCollider1=[]
 def addsound(self):
	self.snd1 = base.loader.loadSfx("videos/base.ogg")
	self.snd1.setLoop(True)
	self.snd1.play()
	self.snd1.setVolume(0.5)
 def pointsound(self):
	self.snd2 = base.loader.loadSfx("videos/point.wav")
	self.snd2.play()
 def diesound(self):
	self.snd3 = base.loader.loadSfx("videos/die1.wav")
	self.snd3.play()
 def pausebasesound(self):
	self.snd1.stop()
	
 def setAI(self, entry):
        #Creating AI World
		self.AIworld = AIWorld(render)
 
		self.AIchar = AICharacter( "entry", entry, 340, 1, 600)
		self.AIworld.addAiChar(self.AIchar)
		self.AIbehaviors = self.AIchar.getAiBehaviors()
        
		self.AIbehaviors.pursue(self.cycle)
		#self.AIbehaviors.pathFollow(1.0)
		#self.AIbehaviors.addToPath(self.cycle.getPos())
		#self.AIbehaviors.startFollow()
		# Obstacle avoidance
		#self.AIbehaviors.obstacleAvoidance(1.0)
		#self.AIworld.addObstacle(self.heartModel1[1])
		#self.AIworld.addObstacle(self.lm[2])
		#self.AIworld1 = AIWorld(render)
 
		#self.AIchar1 = AICharacter( "pursuer1", self.pursuer1, 100, 0.05, 30)
		#self.AIworld1.addAiChar(self.AIchar1)
		#self.AIbehaviors1 = self.AIchar1.getAiBehaviors()
        
		#self.AIbehaviors.pursue(self.pandaActor)
        
        # Obstacle avoidance
		#self.AIbehaviors1.obstacleAvoidance(1.0)
		#self.AIworld1.addObstacle(self.box1)
		#self.AIworld1.addObstacle(self.box)
        #AI World update        
		taskMgr.add(self.AIUpdate,"AIUpdate")
		
 def AIUpdate(self, task):
		self.AIworld.update()
		
		#self.AIbehaviors1.pursue(self.pandaActor)
		return task.cont
 def setAI1(self, entry):
        #Creating AI World
		self.AIworld = AIWorld(render)
 
		self.AIchar = AICharacter( "entry", entry, 10000, 25.55, 3000000)
		self.AIworld.addAiChar(self.AIchar)
		self.AIbehaviors = self.AIchar.getAiBehaviors()
        
		self.AIbehaviors.pursue(self.pandaActor)
        
        # Obstacle avoidance
		self.AIbehaviors.obstacleAvoidance(1.0)
		self.AIworld.addObstacle(self.box1)
		self.AIworld.addObstacle(self.box)
		#self.AIworld1 = AIWorld(render)
 
		#self.AIchar1 = AICharacter( "pursuer1", self.pursuer1, 100, 0.05, 30)
		#self.AIworld1.addAiChar(self.AIchar1)
		#self.AIbehaviors1 = self.AIchar1.getAiBehaviors()
        
		#self.AIbehaviors.pursue(self.pandaActor)
        
        # Obstacle avoidance
		#self.AIbehaviors1.obstacleAvoidance(1.0)
		#self.AIworld1.addObstacle(self.box1)
		#self.AIworld1.addObstacle(self.box)
        #AI World update        
		taskMgr.add(self.AIUpdate1,"AIUpdate1")
		
 def AIUpdate1(self, task):
		self.AIworld.update()
		
		#self.AIbehaviors1.pursue(self.pandaActor)
		return task.cont
	
 def collideEventIn1(self, entry):
		#print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
		#global score
		#score = score + 1
		#self.pointsound()
		#self.bt["text"] = str(score)
		#self.obj.score["text"] = "Score: "+str(score)
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#colliderINTO.removeNode()
		#colliderFROM.removeNode()
		#print "idhar"
		#taskMgr.remove("AIUpdate")
	
 def collideEventOut1(self, entry):
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		colliderINTO.setColor(.4, .4, .4, 1)
		#colliderFROM.setPos
		#colliderFROM.setScale(0.05) 
		colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#self.setAI(self.pursuer1)
		#colliderFROM.removeNode()
		#print(colliderFROM.getZ())
  #colliderFROM = None
		#self.cycle.setLightOff()	
 def collideEventIn3(self, entry):
		#print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
		#global score
		#score = score + 1
		#self.pointsound()
		#self.bt["text"] = str(score)
		#self.obj.score["text"] = "Score: "+str(score)
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		
		self.gate1.removeNode()
		self.para1a.removeNode()
		#taskMgr.remove("AIUpdate")
		#self.pandaActor2.setPos(-173.041, -312.835,0)
		#self.cycle.setPos(-155.278,-308.95,0)
		#self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
		#colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#colliderINTO.removeNode()
		#colliderFROM.removeNode()
		print "idhar"
		#taskMgr.remove("AIUpdate")
	
 def collideEventOut3(self, entry):
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		colliderINTO.setColor(.4, .4, .4, 1)
		self.gate1.removeNode()
		self.para1a.removeNode()
		#colliderFROM.setPos
		#colliderFROM.setScale(0.05)
		#taskMgr.remove("AIUpdate")
		#self.pandaActor2.setPos(-173.041, -312.835,0)
		#self.cycle.setPos(-155.278,-308.95,0)
		#self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
		#colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#self.setAI(self.pursuer1)
		#colliderFROM.removeNode()
		print("udhar")
 def collideEventIn4(self, entry):
		global present_health
		present_health += 10
		self.healthobj.set_value(present_health)
		#print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
		#global score
		#score = score + 1
		#self.pointsound()
		#self.bt["text"] = str(score)
		#self.obj.score["text"] = "Score: "+str(score)
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		colliderINTO.setScale(0.5)
		colliderFROM.removeNode()
		#self.gate1.removeNode()
		#self.para1a.removeNode()
		#taskMgr.remove("AIUpdate")
		#self.pandaActor2.setPos(-173.041, -312.835,0)
		#self.cycle.setPos(-155.278,-308.95,0)
		#self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
		#colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#colliderINTO.removeNode()
		#colliderFROM.removeNode()
		print "idhar"
		#taskMgr.remove("AIUpdate")
	
 def collideEventOut4(self, entry):
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		colliderINTO.setColor(.4, .4, .4, 1)
		colliderINTO.setScale(0.5)
		colliderFROM.removeNode()
		#self.gate1.removeNode()
		#self.para1a.removeNode()
		#colliderFROM.setPos
		#colliderFROM.setScale(0.05)
		#taskMgr.remove("AIUpdate")
		#self.pandaActor2.setPos(-173.041, -312.835,0)
		#self.cycle.setPos(-155.278,-308.95,0)
		#self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
		#colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#self.setAI(self.pursuer1)
		#colliderFROM.removeNode()
		print("udhar")
 
 def collideEventIn2(self, entry):
		#print("idhar bhoi aaya")
  # we retrieve the two object nodepaths - note that we need to go back the nodes hierarchy because the getXXXNodePath methods returns just the collision geometry, that we know is parented to the very object nodepath we need to manage here
		#global score
		#score = score + 1
		#self.pointsound()
		#self.bt["text"] = str(score)
		#self.obj.score["text"] = "Score: "+str(score)
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		taskMgr.remove("AIUpdate")
		self.pandaActor2.setPos(-173.041, -312.835,0)
		self.cycle.setPos(-155.278,-308.95,0)
		#self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
		#colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#colliderINTO.removeNode()
		#colliderFROM.removeNode()
		print "idhar"
		#taskMgr.remove("AIUpdate")
	
 def collideEventOut2(self, entry):
		colliderFROM = entry.getFromNodePath().getParent()
		colliderINTO = entry.getIntoNodePath().getParent()
		colliderINTO.setColor(.4, .4, .4, 1)
		#colliderFROM.setPos
		#colliderFROM.setScale(0.05)
		taskMgr.remove("AIUpdate")
		self.pandaActor2.setPos(-173.041, -312.835,0)
		self.cycle.setPos(-155.278,-308.95,0)
		#self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
		#colliderFROM.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-300,int(abs(self.cycle.getY()))-300,0))
		#self.setAI(self.pursuer1)
		#colliderFROM.removeNode()
		print("udhar")
  #colliderFROM = None
		#self.cycle.setLightOff()
 def controlCamera(self, task):
        # figure out how much the mouse has moved (in pixels)
		base.camera.lookAt(self.cycle)
		md = base.win.getPointer(0)
		x = md.getX()
		y = md.getY()
		if base.win.movePointer(0, 100, 100):
			self.heading = self.heading - (x - 100) * 0.2
			self.pitch = self.pitch - (y - 100) * 0.2
		if (self.pitch < -45): self.pitch = -45
		if (self.pitch >  45): self.pitch =  45
		base.camera.setHpr(self.heading,self.pitch,0)
		dir = base.camera.getMat().getRow3(1)
		elapsed = task.time - self.last
		if (self.last == 0): elapsed = 0
		#if (self.mousebtn[0]):
            #self.focus = self.focus + dir * elapsed*30
        #if (self.mousebtn[1]) or (self.mousebtn[2]):
            #self.focus = self.focus - dir * elapsed*30
		base.camera.setPos(self.cycle.getPos())
		if (base.camera.getX() < -59.0): base.camera.setX(-59)
		if (base.camera.getX() >  59.0): base.camera.setX( 59)
		if (base.camera.getY() < -59.0): base.camera.setY(-59)
		if (base.camera.getY() >  59.0): base.camera.setY( 59)
		if (base.camera.getZ() <   5.0): base.camera.setZ(  5)
		if (base.camera.getZ() >  45.0): base.camera.setZ( 45)
		#self.focus = base.camera.getPos() + (dir*5)
		self.last = task.time
		return Task.cont		
 def police1(self, task):
		global score,click2,time1 
		if(((abs(abs(self.cycle.getX())) -(abs(self.pandaActor2.getX()))) < 30) and ((abs((abs(self.cycle.getY()))-(abs(self.pandaActor2.getY()))))<30) ):
			self.speedobj.playpolice(1,0)
			#print "Police Around"
			if(((abs(abs(self.cycle.getX())) -(abs(self.pandaActor2.getX()))) <= 1.5) and ((abs((abs(self.cycle.getY()))-(abs(self.pandaActor2.getY()))))<=1.5) ):
				#print "Caught"
				click2 = 1
				self.pausekaro('options')
				#self.setnote = self.addInstructions(0.90,"Police Caught\n20$ penalty")
				
				#self.pb = DirectButton(text = "Pay Fine",pos = (0,0,-1.0),scale = 0.1,command = self.bhagao,frameSize = (-2,2,-1,1),extraArgs = [click2])
				self.setnote.show()
				self.pbutton.show()
				if(time1 == 0):
					time1 = 1
					score = score-10
				self.obj.score['text'] = "Score: "+str(score)+"$"
				#self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
				#taskMgr.remove("AIUpdate")
		else:
			#taskMgr.remove("AIUpdate")
			self.speedobj.playpolice(2,0)
			#print "Police Away"
		if(((abs(abs(self.cycle.getX())) -(abs(self.para1.getX()))) < 300) and ((abs((abs(self.cycle.getY()))-(abs(self.para1.getY()))))<300) ):
			self.speedobj.playplane(1,0)
			#print "Plane Near"
		else:
			self.speedobj.playplane(2,0)
			#print "Plane Away"
		return Task.cont
 def police(self, task):
		global score,click2,time1 
		if(((abs(abs(self.cycle.getX())) -(abs(self.pandaActor1.getX()))) < 40) and ((abs((abs(self.cycle.getY()))-(abs(self.pandaActor1.getY()))))<40) ):
			self.speedobj.playpolice(1,0)
			print "Police Around"
			if(((abs(abs(self.cycle.getX())) -(abs(self.pandaActor1.getX()))) < 1) and ((abs((abs(self.cycle.getY()))-(abs(self.pandaActor1.getY()))))<1) ):
				print "Caught"
				click2 = 1
				self.pausekaro('options')
				#self.setnote = self.addInstructions(0.90,"Police Caught\n20$ penalty")
				
				#self.pb = DirectButton(text = "Pay Fine",pos = (0,0,-1.0),scale = 0.1,command = self.bhagao,frameSize = (-2,2,-1,1),extraArgs = [click2])
				self.setnote.show()
				self.pbutton.show()
				if(time1 == 0):
					time1 = 1
					score = score-10
				self.obj.score['text'] = "Score: "+str(score)+"$"
				
		else:
			self.speedobj.playpolice(2,0)
			#print "Police Away"
		if(((abs(abs(self.cycle.getX())) -(abs(self.para1.getX()))) < 300) and ((abs((abs(self.cycle.getY()))-(abs(self.para1.getY()))))<300) ):
			#self.speedobj.playplane(1,0)
			print(self.cycle.getPos()) 
		else:
			self.speedobj.playplane(2,0)
			print(self.cycle.getPos())
		return Task.cont
 
 def bhagao(self):
	global click2,time1
	#self.pb['text'] = ""
	#self.setnote = self.addInstructions(0.90,"")
	if(click2 == 1):
		click2 = 0
		time1 = 0
		self.pbutton.hide()
		self.setnote.hide()
		self.resume()
		self.speed = 200
		#self.pandaActor1.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-350,int(abs(self.cycle.getY()))-350,0))
		self.pandaActor2.setPos(self.cycle.getPos()+Point3(int(abs(self.cycle.getX()))-20,int(abs(self.cycle.getY()))-20,0))
		taskMgr.remove("AIUpdate")
 def scorer(self,task):
	self.obj.score['text'] = "Score: "+str(score)+"$"
	return Task.cont
#w = World()
#run()