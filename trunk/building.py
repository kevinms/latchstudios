import pygame
import unit

class Building(unit.Unit):
	def __init__(self, positionX, positionY, colorVal, buildingType):
		unit.Unit.__init__(self, positionX, positionY)

		self.normalSprite = pygame.image.load("images/arrow.png").convert()
		
		self.base = pygame.image.load('images/base.jpg').convert()
		self.barracks = pygame.image.load('images/barracks.jpg').convert()

		if buildingType == 1:
			self.mySprite = self.base
		if buildingType == 2:
			self.mySprite = self.barracks

		self.unitType = 0		
		self.rotation = 0
		self.speed = 0
		self.maxHealth = 1000
		self.currHealth = self.maxHealth

		self.attackAtX = -1
		self.attackAtY = -1
