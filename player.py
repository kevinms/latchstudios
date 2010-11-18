#!/usr/bin/env python

import troop
import speedster
import building

class Player:
	mouseX = 50
	mouseY = 50
	playerID = -1

	def __init__(self, cid, playerName):
		self.troops = []
		self.buildings = []
		self.troops.append(speedster.Speedster(50,50))
		self.troops.append(troop.Troop(100,100, cid*5))

		self.playerID = cid
		self.name = playerName

