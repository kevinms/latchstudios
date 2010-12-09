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

		self.playerID = cid
		self.name = playerName

		# economy
		self.cash = 300
