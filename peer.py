#!/usr/bin/env python

import sys
import os
import pygame
import string
import net
import gui

import troop

from vec import *
import netserver as NS
from pygame.locals import *
from pygame.color import THECOLORS


def main():
	windowSize = 640,480
	pygame.init()
	screen = pygame.display.set_mode(windowSize,0,8)
	settingData = parseSettings()
	pygame.display.set_caption('Made by: Latch Studios')
	troopList = []
	screen.fill((159, 180,200))
	action = mainMenu(screen, settingData)

	if action == 0 :
		node = nGame(screen, settingData)
	elif action == 1:
		connectGame()
	elif action == 2:
		settin()
	else:
		print "Exiting"
		exit()

	

	screen.fill((200, 180,200))

        dx = screen.get_rect().centerx
	dy = screen.get_rect().centery
	velocity = .5
	tx = dx
	ty = dy
	directionX = 0
	directionY = 0

	troopList.append(troop.Troop(0,0))


	pygame.display.update()
	done = False
	while not done:
		player = pygame.image.load("sprite3.gif").convert()
		screen.fill((200, 180,200))
		#event loop
		events = pygame.event.get()
		for e in events:
			#quit
			if(e.type == QUIT):
				done = True
				break
			#key recognition branch
			elif(e.type == pygame.KEYDOWN):
				if (e.key == K_UP):
					print "Key up"
					for tro in troopList:
						if tro.isSelected():
							tro.locationY = tro.locationY - tro.speed
					
					
				elif (e.key == K_DOWN):
					print "Key down"
					for tro in troopList:
						if tro.isSelected():
							tro.locationY = tro.locationY + tro.speed

				elif (e.key == K_RIGHT):
					print "Key right"
					for tro in troopList:
						if tro.isSelected():
							tro.locationX = tro.locationX + tro.speed
				elif (e.key == K_LEFT):
					print "Key Left"
					for tro in troopList:
						if tro.isSelected():
							tro.locationX = tro.locationX - tro.speed

				else:
					pass
			elif(e.type == pygame.MOUSEBUTTONDOWN):
				for tro in troopList:
					if tro.isSelected():
						mouse_position = list(e.pos)
						tro.moveToTargetX = e.pos[0]
						tro.moveToTargetY = e.pos[1]
				
			else:
				pass

		#Update Units loop goes here ((once we have a unit class
		for tro in troopList:
			unitDirect = unitdir(tx, ty, dx, dy, velocity)
			tro.locationX = tro.locationX + (tro.speed * unitDirect[0])
			tro.locationY = tro.locationY + (tro.speed * unitDirect[1])
			screen.blit(player, (tro.locationX,tro.locationY))
		
		#print unitDirect[0]
		#print unitDirect[1]


		gui.drawPanels(-1)
		gui.refresh(screen)

	print "Exiting"

def nGame(screen, settingData):
	print "Starting New Game"
	print settingData[1]
	#n = NS.server_thread(int(settingData[1]),3)
	#n.start()
	n = 1
	pygame.display.set_caption('New Game')

	print "Done"
	return n;


	

def connectGame():
	print "Connecting To Game"

def settin():
	print "Opening Settings"

def parseSettings():
	try:
		f = open("settings.conf", 'r')
		confData = f.readlines();
		for i in range(len(confData)):
			confData[i] = confData[i].strip("\n")
	except:
		print "Error: Settings file cannot be found"
		confData = [0,0,"Default"]
	return confData

def writeConf(Data):
	f = open("settings.conf", 'w')
	for i in range(len(Data)):
		f.write(str(Data[i])+"\n")


def mainMenu(screen, settingData):
	
	selec = 0
	font = pygame.font.Font(None, 60)
	selected = (255,255, 0)
	unselected = (255,255, 255)
	newGame = font.render('Create Game', True, selected, (159, 182, 205))
	joinGame = font.render('Join Game', True, unselected, (159, 182, 205))
	settings = font.render('Settings', True, unselected, (159, 182, 205))
	quit = font.render('Quit', True, unselected, (159, 182, 205))

	newGameR = newGame.get_rect()
	joinGameR = joinGame.get_rect()
	settingsR = settings.get_rect()
	quitR = quit.get_rect()

	newGameR.centerx = screen.get_rect().centerx 
	newGameR.centery = screen.get_rect().centery - 60

	joinGameR.centerx = screen.get_rect().centerx
	joinGameR.centery = screen.get_rect().centery

	settingsR.centerx = screen.get_rect().centerx
	settingsR.centery = screen.get_rect().centery + 60

	quitR.centerx = screen.get_rect().centerx
	quitR.centery = screen.get_rect().centery + 120

	screen.blit(newGame,newGameR)
	screen.blit(joinGame,joinGameR)
	screen.blit(settings,settingsR)
	screen.blit(quit,quitR)


	pygame.display.update()

	done = False
	while not done:
		#event handling
		events = pygame.event.get()
		tmp = selec
		for e in events:
			if(e.type == QUIT):
				print "Exiting"
				exit()
			elif(e.type == pygame.KEYDOWN):
				if (e.key == K_UP):
					if selec == 0:
						selec = 3
					else:
						selec = selec - 1
				elif (e.key == K_DOWN):
					if selec == 3:
						selec = 0
					else:
						selec = selec + 1
				elif (e.key == K_RETURN):
					if selec == 2:
						print "settings"
						settin(screen, settingData)
						writeConf(settingData)
						screen.fill((159, 180,200))	
						screen.blit(newGame,newGameR)	
						screen.blit(joinGame,joinGameR)		
						screen.blit(settings,settingsR)	
						screen.blit(quit,quitR)
					else:
						return selec
				if tmp == 0:
					newGame = font.render('Create Game', True, unselected, (159, 182, 205))
					screen.blit(newGame,newGameR)
				elif tmp == 1:
					joinGame = font.render('Join Game', True, unselected, (159, 182, 205))
					screen.blit(joinGame,joinGameR)
				elif tmp == 2:
					settings = font.render('Settings', True, unselected, (159, 182, 205))
					screen.blit(settings,settingsR)
				elif tmp == 3:
					quit = font.render('Quit', True, unselected, (159, 182, 205))
					screen.blit(quit,quitR)
	
				if selec == 0:
					newGame = font.render('Create Game', True, selected, (159, 182, 205))
					screen.blit(newGame,newGameR)
				elif selec == 1:
					joinGame = font.render('Join Game', True, selected, (159, 182, 205))
					screen.blit(joinGame,joinGameR)
				elif selec == 2:
					settings = font.render('Settings', True, selected, (159, 182, 205))
					screen.blit(settings,settingsR)
				elif selec == 3:
					quit = font.render('Quit', True, selected, (159, 182, 205))
					screen.blit(quit,quitR)
				pygame.display.update()	

def settin(screen, settingData):
	
	selec = 0
	font = pygame.font.Font(None, 60)
	selected = (255,255, 0)
	unselected = (255,255, 255)
	menu1 = 'SET IP'
	menu2 = 'SET Port'
	menu3 = 'SET Game Name'
	menu4 = 'Back'
	newGame = font.render(menu1, True, selected, (159, 182, 205))
	joinGame = font.render(menu2, True, unselected, (159, 182, 205))
	settings = font.render(menu3, True, unselected, (159, 182, 205))
	quit = font.render(menu4, True, unselected, (159, 182, 205))

	screen.fill((159, 180,200))

	newGameR = newGame.get_rect()
	joinGameR = joinGame.get_rect()
	settingsR = settings.get_rect()
	quitR = quit.get_rect()

	newGameR.centerx = screen.get_rect().centerx 
	newGameR.centery = screen.get_rect().centery - 60

	joinGameR.centerx = screen.get_rect().centerx
	joinGameR.centery = screen.get_rect().centery

	settingsR.centerx = screen.get_rect().centerx
	settingsR.centery = screen.get_rect().centery + 60

	quitR.centerx = screen.get_rect().centerx
	quitR.centery = screen.get_rect().centery + 120

	screen.blit(newGame,newGameR)
	screen.blit(joinGame,joinGameR)
	screen.blit(settings,settingsR)
	screen.blit(quit,quitR)


	pygame.display.update()

	done = False
	while not done:
		#event handling
		events = pygame.event.get()
		tmp = selec
		for e in events:
			if(e.type == QUIT):
				print "Exiting"
				exit()
			elif(e.type == pygame.KEYDOWN):
				if (e.key == K_UP):
					if selec == 0:
						selec = 3
					else:
						selec = selec - 1
				elif (e.key == K_DOWN):
					if selec == 3:
						selec = 0
					else:
						selec = selec + 1
				elif (e.key == K_RETURN):
					if selec == 0:
						IP = prompt(screen, "IP: ")
						settingData[0] = str(IP)
						print settingData
					elif selec == 1:
						PORT = prompt(screen, "Port: ")
						settingData[1] = int(PORT)
						print settingData
					elif selec == 2:
						GAMENAME = prompt(screen, "Game Name: ")
						settingData[2] = str(GAMENAME)
						print settingData
					elif selec == 3:
						return
					screen.fill((159, 180,200))	
					screen.blit(newGame,newGameR)	
					screen.blit(joinGame,joinGameR)		
					screen.blit(settings,settingsR)	
					screen.blit(quit,quitR)
				if tmp == 0:
					newGame = font.render(menu1, True, unselected, (159, 182, 205))
					screen.blit(newGame,newGameR)
				elif tmp == 1:
					joinGame = font.render(menu2, True, unselected, (159, 182, 205))
					screen.blit(joinGame,joinGameR)
				elif tmp == 2:
					settings = font.render(menu3, True, unselected, (159, 182, 205))
					screen.blit(settings,settingsR)
				elif tmp == 3:
					quit = font.render(menu4, True, unselected, (159, 182, 205))
					screen.blit(quit,quitR)
	
				if selec == 0:
					newGame = font.render(menu1, True, selected, (159, 182, 205))
					screen.blit(newGame,newGameR)
				elif selec == 1:
					joinGame = font.render(menu2, True, selected, (159, 182, 205))
					screen.blit(joinGame,joinGameR)
				elif selec == 2:
					settings = font.render(menu3, True, selected, (159, 182, 205))
					screen.blit(settings,settingsR)
				elif selec == 3:
					quit = font.render(menu4, True, selected, (159, 182, 205))
					screen.blit(quit,quitR)
				pygame.display.update()	


def prompt(screen, question):
	pygame.font.init()
	currData = []
	pygame.display.update()	
	drawPrompt(screen, question + " " + string.join(currData, ""))
	while True:
		keystroke = getKeystroke()
		if keystroke == K_RETURN:
			break
		elif keystroke == K_BACKSPACE:
			currData = currData[0:(len(currData)-1)]
			drawPrompt(screen, question + " " + string.join(currData, ""))
		elif keystroke < 128:
			currData.append(chr(keystroke))
			drawPrompt(screen, question + " " + string.join(currData, ""))
	return string.join(currData, "")

def getKeystroke():
	while True:
		event = pygame.event.poll()
		if (event.type == KEYDOWN):			
			return event.key


def drawPrompt(screen, message):
	screen.fill((159, 180,200))
	font = pygame.font.Font(None, 60)
	settings = font.render(message, True, (255,255, 255), (159, 182, 205))
	settingsR = settings.get_rect()
	settingsR.centerx = screen.get_rect().centerx
	settingsR.centery = screen.get_rect().centery - 60
	screen.blit(settings,settingsR)
	pygame.display.update()

if __name__ == "__main__":
	main()