#0 building
#1 troop
#2 support

import pygame
import math

class Unit:
	moveToTargetX = -1
	moveToTargetY = -1
	selected = False
	maxHealth = 100
	#mySprite = pygame.imasige.load("error.gif").convert()

	def __init__(self, spawnLocX, spawnLocY):
		#Initialization of basic stats
		self.maxHealth = 100
		self.currHealth = self.maxHealth
		self.killCount = 0
		self.rank = 0
		self.unitType = -1
		self.selected = False

		#Offensive
		self.attackRate = 0
		self.attackRange = 0
		self.attackDamage = 0
		self.attackExplosionSize = 0
		self.attackChanceOfCriticalHit = 0.05

		#Movement
		self.speed = 1

		self.locationX = spawnLocX
		self.locationY = spawnLocY

		self.moveToTargetX = spawnLocX
		self.moveToTargetY = spawnLocY

		#Defense
		self.damageResistance = 0

	def position(self):
		return self.locationX , self.locationY, self.rotation

	def setPosition(locX, locY):
		self.rotation = 0 #TODO: Math to calculate what rotation it will have after move		
		self.locationX = locX
		self.locationY = locY

	def isSelected(self):
		return self.selected

	def selectMe(self):
		self.selected = True

	def deselectMe(self):
		self.selected = False
		
	def setSelected(self):
		#TODO
		i=0

	def getMoveToTargetX(self):
		return self.moveToTargetX

	def getMoveToTargetY(self):
		return self.moveToTargetY

	def getLocationX(self):
		return self.locationX

	def getLocationY(self):
		return self.locationY

	def getSpeed(self):
		return self.speed

	def setRotation(self, unitDirect):
		if(unitDirect[1] != 0 and unitDirect[0] != 0):
			run = unitDirect[0]
			rise = unitDirect[1]
			temp = math.atan(rise/run)
			temp = math.degrees(temp)
			self.rotation = 0-temp
			if(run < 0):
				self.rotation = 180-temp
			self.mySprite = pygame.transform.rotate(self.baseSprite, self.rotation)

	def setSelectVal(self, val):
		self.selected = val
		if val:
			self.mySprite = self.selectedSprite
			self.baseSprite = self.mySprite
			self.mySprite = pygame.transform.rotate(self.baseSprite, self.rotation)
		else:
			self.mySprite = self.normalSprite	
			self.baseSprite = self.mySprite	
			self.mySprite = pygame.transform.rotate(self.baseSprite, self.rotation)

	def setupColors(self, colorVal):
		for x in range(self.normalSprite.get_width()):
			for y in range(self.normalSprite.get_height()):
				locationOf = (x,y)

				newR = self.normalSprite.get_at(locationOf)[0] 
				newG = self.normalSprite.get_at(locationOf)[1]
				newB = self.normalSprite.get_at(locationOf)[2] 
				newA = self.normalSprite.get_at(locationOf)[3]

				newColor = pygame.Color(newR,newG,newB,newA)

				colorKey = self.normalSprite.get_colorkey()	
				if newColor == colorKey:
					newColor = pygame.Color(0, 0, 0, 0)
				elif (newR == 255 and newG == 0 and newB == 0):
					newColor = pygame.Color((newR + colorVal[0])%255,(newG + colorVal[1])%255,(newB + colorVal[2])%255,255)
				self.normalSprite.set_at(locationOf, newColor)
		self.normalSprite.set_colorkey((0,0,0,0))

		for x in range(self.selectedSprite.get_width()):
			for y in range(self.selectedSprite.get_height()):
				locationOf = (x,y)

				newR = self.selectedSprite.get_at(locationOf)[0] 
				newG = self.selectedSprite.get_at(locationOf)[1]  
				newB = self.selectedSprite.get_at(locationOf)[2] 
				newA = self.selectedSprite.get_at(locationOf)[3]

				newColor = pygame.Color(newR,newG,newB,newA)

				colorKey = self.selectedSprite.get_colorkey()	
				if newColor == colorKey:
					newColor = pygame.Color(0, 0, 0, 0)
				elif (newR == 255 and newG == 0 and newB == 0):
					newColor = pygame.Color((newR + colorVal[0])%255,(newG + colorVal[1])%255,(newB + colorVal[2])%255,255)
				self.selectedSprite.set_at(locationOf, newColor)
		self.selectedSprite.set_colorkey((0,0,0,0))
