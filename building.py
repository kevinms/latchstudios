import pygame
import unit

class Building(unit.Unit):
	
	costBase = 100
	costBarracks = 100
	
	def __init__(self, positionX, positionY, colorVal, buildingType):
		unit.Unit.__init__(self, positionX, positionY)
		
		self.buildingType = buildingType
		self.base = pygame.image.load('images/base.png').convert()
		self.barracks = pygame.image.load('images/barracks.png').convert()

		if buildingType == 1:
			self.mySprite = self.base
		if buildingType == 2:
			self.mySprite = self.barracks

		self.normalSprite = self.mySprite
		self.selectedSprite = self.mySprite

		self.centerX = self.locationX + (self.mySprite.get_rect()[2] / 2)
		self.centerY = self.locationY + (self.mySprite.get_rect()[3] / 2)
		self.rect = pygame.Rect(positionX,positionY,90,90)
		self.unitType = 0
		self.rotation = 0
		self.speed = 0
		self.maxHealth = 1000
		self.currHealth = self.maxHealth

		self.attackAtX = -1
		self.attackAtY = -1
