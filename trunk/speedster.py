#This is a test subclass for troop, a test for having different types of troops

import troop
import pygame

class Speedster(troop.Troop):
	def __init__(self, positionX, positionY):

		self.mySprite = pygame.image.load("sprite2.gif").convert() 

		self.unitType = 4
		self.locationX = positionX
		self.locationY = positionY
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
