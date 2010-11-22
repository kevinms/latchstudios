#!/usr/bin/env python

import sys
import os
import pygame
import string
import net
import gui
import player
import time
import random
from math import *

import troop
import speedster
import building

import vec
import netserver as NS
import netclient as NC
from pygame.locals import *
from pygame.color import THECOLORS

def main():
	#connect to
	print sys.argv[1]
	#via this port
	print sys.argv[2]
	#wait before moveing around
	print sys.argv[3]

	playerList = []
	pygame.init()
	windowSize = 640,480
	screen = pygame.display.set_mode(windowSize,0,8)

	n = NC.client_thread(sys.argv[1],int(sys.argv[2]))
	n.connect()

	for peer in n.peer_list:
		playerList.append(player.Player(peer[0], peer[1]))

	time.sleep(int(sys.argv[3]))

	sel = False
	DONE = False
	mySelf = None

	n.minput(1,52,52)
	aDelta = time.time()
	elapsedTime = 0

	while not DONE:
		n.send()

		#Bot Logic Goes Here
		push = random.randint(0,4)

		# time deltas to keep track of when to click on the screen
		bDelta = time.time()
		elapsedTime += (bDelta - aDelta)
		aDelta = bDelta
		
		#Game Engine Logic Is Here
		n.recv()
		while not n.recv_queue.empty():
			tempData = n.recv_queue.get()
			if tempData[2] == 7:
				playerList.append(player.Player(tempData[3], tempData[4]))
				for person in playerList:
					if n.info.cid == person.playerID:
						mySelf = person
			for person in playerList:					
				if tempData[0] == person.playerID:
					if tempData[2] == 2:  
						if tempData[3][0] == 1:  # selecting
							for tro in person.troops:
								tro.setSelectVal(False)
							for tro in person.troops:
								dist = vec.subtract(tempData[3][1], tempData[3][2], tro.getLocationX(), tro.getLocationY())
								if fabs(dist[0])< tro.size and fabs(dist[1]) < tro.size:
									tro.setSelectVal(True)
									break
								else:
									tro.setSelectVal(False)
						elif tempData[3][0] == 3:  # orders
							for tro in person.troops:
								if tro.isSelected():
									tro.moveToTargetX = tempData[3][1]
									tro.moveToTargetY = tempData[3][2]

		for person in playerList:
			for tro in person.troops:
				unitDirect = vec.unitdir(tro.getMoveToTargetX(), tro.getMoveToTargetY(), tro.getLocationX(), tro.getLocationY(), tro.getSpeed())
				tro.setRotation(unitDirect)
				tro.locationX = tro.locationX + (tro.speed * unitDirect[0])
				tro.locationY = tro.locationY + (tro.speed * unitDirect[1])

		# Follow player 1's speedster troop
		if mySelf != None and elapsedTime > 0.5:
			elapsedTime = 0
			for person in playerList:
				if person.playerID == 1:
					unitDirect = vec.unitdir(person.troops[0].moveToTargetX, person.troops[0].moveToTargetY,
					                         person.troops[0].locationX, person.troops[0].locationY,
					                         person.troops[0].getSpeed())
					if unitDirect[0] != 0 and unitDirect[1] != 0:
						print "moving, must gettem"
						n.minput(3, person.troops[0].getLocationX(), person.troops[0].getLocationY())

if __name__ == "__main__":
	main()
