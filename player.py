#!/usr/bin/env python

import troop
import speedster
import building
import random

class Player:
	mouseX = 50
	mouseY = 50
	playerID = -1

	def __init__(self, cid, playerName):
		self.troops = []
		self.buildings = []
		random.seed(cid)
		self.color = (cid+random.randint(0,1000), cid+random.randint(0,1000), cid+random.randint(0,1000))
		self.troops.append(speedster.Speedster(cid*50 + 50,50, self.color))
		self.troops.append(troop.Troop(cid*50 + 100,100, self.color))

		self.playerID = cid
		self.name = playerName

