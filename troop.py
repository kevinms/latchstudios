
import pygame
import unit
import math

class Troop(unit.Unit):
	size = 10
	def __init__(self, positionX, positionY):
		
		self.mySprite = pygame.image.load("arrow.gif") 
		self.baseSprite = self.mySprite
		self.unitType = 1		
		self.locationX = positionX
		self.locationY = positionY
		self.rotation = 0
		self.speed = .5


		self.moveToTargetX = self.locationX
		self.moveToTargetY = self.locationY	
		
		#Offensive
		self.attackRate = 0.8
		self.attackRange = 45
		self.attackDamage = 5
		self.attackExplosionSize = 15
		self.attackChanceOfCriticalHit = 0.05

		self.attackAtX = -1
		self.attackAtY = -1

		#Defensive
		self.damageResistance = 10
	
	def setRotation(self, unitDirect):
		if(unitDirect[1] != 0 and unitDirect[0] != 0):
			run = unitDirect[0]
			rise = unitDirect[1]
			temp = math.atan(rise/run)
			temp = math.degrees(temp)
			rotation = 0-temp
			if(run < 0):
				rotation = 180-temp
			print "Setting rotation: ", rotation
			self.mySprite = pygame.transform.rotate(self.baseSprite, rotation)
	
	def setSelectVal(self, val):
		self.selected = val
		if val:
			self.mySprite = pygame.image.load("arrows.gif").convert()
			self.baseSprite = self.mySprite
		else:
			self.mySprite = pygame.image.load("arrow.gif").convert()	
			self.baseSprite = self.mySprite		 	 	 	   	 	  	   		  	 
