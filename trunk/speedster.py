#This is a test subclass for troop, a test for having different types of troops

import pygame
import troop
import unit
import missile

class Speedster(unit.Unit):
	def __init__(self, positionX, positionY, colorVal):
		unit.Unit.__init__(self, positionX, positionY)

		self.normalSprite = pygame.image.load("images/speedster.png").convert()
		self.selectedSprite = pygame.image.load("images/speedster_s.png").convert()

		self.mySprite = self.normalSprite
		self.baseSprite = self.mySprite


		self.unitType = 4
		self.rotation = 0
		self.speed = 1.4

		self.bulletList = []
		for bullets in range(1):
			self.bulletList.append(missile.Missile(-10, -10, colorVal))

		#Offensive
		self.attackRate = 0.2
		self.attackRange = 50
		self.attackDamage = 3
		self.attackExplosionSize = 3
		self.attackChanceOfCriticalHit = 0.3

		self.attackAtX = -1
		self.attackAtY = -1

		#Defensive
		self.damageResistance = 1
		self.setupColors(colorVal)
