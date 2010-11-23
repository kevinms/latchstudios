
import pygame
import unit
import math

class Troop(unit.Unit):
	def __init__(self, positionX, positionY, colorVal):
		unit.Unit.__init__(self, positionX, positionY)
		
		self.normalSprite = pygame.image.load("images/arrow.png").convert()
		self.selectedSprite = pygame.image.load("images/arrows.png").convert()

		self.mySprite = self.normalSprite
		self.baseSprite = self.mySprite
		self.unitType = 1
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
		self.setupColors(colorVal)
		self.rotation = 0
