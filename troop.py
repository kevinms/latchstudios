
import pygame
import unit
import math

class Troop(unit.Unit):
	def __init__(self, positionX, positionY):
		
		self.mySprite = pygame.image.load("arrow.gif").convert() 
		
		mySprite = self.mySprite
		self.baseImage = self.mySprite
		
		self.unitType = 1		
		self.locationX = positionX
		self.locationY = positionY
		self.rotation = 0
		self.speed = .5
		
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
			temp = math.tan(rise/run)
			temp = math.degrees(temp)
			self.rotation = math.fabs(temp);
			print self.rotation
			self.mySprite = pygame.transform.rotate(self.baseImage, self.rotation)
		
