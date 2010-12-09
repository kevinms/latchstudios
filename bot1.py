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

	n = NC.client_thread(sys.argv[1],int(sys.argv[2]))
	n.connect()

	time.sleep(int(sys.argv[3]))

	cashRate = 50
	cashTicks = 0
	cash = 100
	DONE = False

	while not DONE:
		n.send()


		cashTicks += 1
		if cashTicks == cashRate:
			cash += 1
			cashTicks = 0

		#Bot Logic Goes Here
		push = random.randint(0,100)
		
		if (push < 25):
			n.minput(1, random.randint(0,1000), random.randint(0,1000))
		elif (push < 50):
			n.minput(3, random.randint(0,1000), random.randint(0,1000))
		elif (push == 53):
			n.minput(24, random.randint(0,1000), random.randint(0,1000))
			cash -= 8
		elif (push == 54):
			n.minput(25, random.randint(0,1000), random.randint(0,1000))
			cash -= 10
			 
		#/Bot Logic
		
		#Game Engine Logic Is Here
		n.recv()
		while not n.recv_queue.empty():
			tempData = n.recv_queue.get()

if __name__ == "__main__":
	main()
