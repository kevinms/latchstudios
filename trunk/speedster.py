#This is a test subclass for troop, a test for having different types of troops

import pygame
import troop

class Speedster(troop.Troop):
	size = 20
	def __init__(self, positionX, positionY, colorVal):


		self.normalSprite = pygame.image.load("sprite4.png").convert()
		self.selectedSprite = pygame.image.load("sprite4s.png").convert()

		self.mySprite = self.normalSprite
		self.baseSprite = self.mySprite


		self.unitType = 4
		self.locationX = positionX
		self.locationY = positionY
		self.rotation = 0
		self.speed = 1.4

		self.moveToTargetX = self.locationX
		self.moveToTargetY = self.locationY		

		#Offensive
		self.attackRate = 0.2
		self.attackRange = 8
		self.attackDamage = 3
		self.attackExplosionSize = 3
		self.attackChanceOfCriticalHit = 0.3

		self.attackAtX = -1
		self.attackAtY = -1

		#Defensive
		self.damageResistance = 1
		self.setupColors(colorVal)

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
