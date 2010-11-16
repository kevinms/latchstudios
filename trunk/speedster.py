#This is a test subclass for troop, a test for having different types of troops

import pygame
import troop

class Speedster(troop.Troop):
	size = 20
	def __init__(self, positionX, positionY):
		self.mySprite = pygame.image.load("sprite4.gif") 
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

	def setSelectVal(self, val):
		self.selected = val
		if val:
			self.mySprite = pygame.image.load("sprite4s.gif").convert()
			self.baseSprite = self.mySprite
		else:
			self.mySprite = pygame.image.load("sprite4.gif").convert()
			self.baseSprite = self.mySprite	
