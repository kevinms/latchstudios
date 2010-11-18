#!/usr/bin/env python

import troop
import speedster
import building

class Player:
	troops = []
	buidings = []
	mouseX = 50
	mouseY = 50
	playerID = -1

	def __init__(self, cid, playerName):
		self.troops.append(speedster.Speedster(50,50))
		self.troops.append(troop.Troop(100,100))
		self.playerID = cid
		self.name = playerName

