import pygame
import unit
import math
import weakref

class Missile(unit.Unit):
	def __init__(self, positionX, positionY, colorVal):
		unit.Unit.__init__(self, positionX, positionY)
		
		self.normalSprite = pygame.image.load("images/missile.png").convert()
		self.selectedSprite = pygame.image.load("images/missile.png").convert()

		self.mySprite = self.normalSprite
		self.baseSprite = self.mySprite
		self.rotation = 0
		self.speed = 5

		self.isActive = False

		self.whenFired = 0
		self.lifeTime = 40
		
		#Offensive
		self.attackDamage = 5

		self.attackAtX = -1
		self.attackAtY = -1

		self.setupColors(colorVal)


	def activate(self, t):
		self.attackingTarget = weakref.ref(t)

	def disable(self):
		self.isActive = False
		self.locationX = -10
		self.locationY= -10
		self.attackAtX = -10
		self.attackAtY = -10

