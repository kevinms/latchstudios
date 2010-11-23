#This is a test subclass for troop, a test for having different types of troops

import pygame
import troop
import unit

class Speedster(unit.Unit):
	def __init__(self, positionX, positionY, colorVal):
		unit.Unit.__init__(self, positionX, positionY)

		self.normalSprite = pygame.image.load("images/sprite4.png").convert()
		self.selectedSprite = pygame.image.load("images/sprite4s.png").convert()

		self.mySprite = self.normalSprite
		self.baseSprite = self.mySprite


		self.unitType = 4
		self.rotation = 0
		self.speed = 1.4

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
