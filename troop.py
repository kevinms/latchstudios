
import pygame
import unit
import math
import missile

class Troop(unit.Unit):
	def __init__(self, positionX, positionY, colorVal):
		unit.Unit.__init__(self, positionX, positionY)
		
		self.normalSprite = pygame.image.load("images/troop.png").convert()
		self.selectedSprite = pygame.image.load("images/troop_s.png").convert()

		self.mySprite = self.normalSprite
		self.baseSprite = self.mySprite
		self.unitType = 1
		self.rotation = 0
		self.speed = .5


		self.bulletList = []
		for bullets in range(1):
			self.bulletList.append(missile.Missile(-10, -10, colorVal))
		
		#Offensive
		self.attackRate = 50
		self.attackRange = 150
		self.attackDamage = 25
		self.attackExplosionSize = 15
		self.attackChanceOfCriticalHit = 0.05

		self.attackAtX = -1
		self.attackAtY = -1

		#Defensive
		self.damageResistance = 10
		self.setupColors(colorVal)
		self.rotation = 0
