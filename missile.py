import pygame
import unit
import math

class Missile(unit.Unit):
	def __init__(self, positionX, positionY, colorVal):
		unit.Unit.__init__(self, positionX, positionY)
		
		self.normalSprite = pygame.image.load("images/arrow.png").convert()
		self.selectedSprite = pygame.image.load("images/arrows.png").convert()

		self.mySprite = self.normalSprite
		self.baseSprite = self.mySprite
		self.rotation = 0
		self.speed = .5

		self.isActive = False
		
		#Offensive
		self.attackDamage = 5

		self.attackAtX = -1
		self.attackAtY = -1

		self.setupColors(colorVal)
