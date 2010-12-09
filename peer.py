#!/usr/bin/env python

import sys
import os
import pygame
import string
import net
import gui
import player
import weakref
from math import *

import troop
import speedster
import building
import missile
import unit

import world

import vec
import netserver as NS
import netclient as NC
from pygame.locals import *
from pygame.color import THECOLORS

building_mode = 0
selected_building = 0
framesPast = 0

def main():
	windowSize = 640,480
	
	worldMap = world.WorldMap(1000, 1000, 10, 10)

	lobby = True
	unitAttacked = False
	pygame.init()
	screen = pygame.display.set_mode(windowSize,0,8)
	settingData = parseSettings()
	pygame.display.set_caption('Made by: Latch Studios')
	playerList = []
	screen.fill((159, 180,200))
	backRect = pygame.Rect(0,36,640-125,480-36)
	action = mainMenu(screen, settingData)

	if action == 0 :
		n = nGame(screen, settingData)
	elif action == 1:
		n = connectGame(screen, settingData)
	elif action == 2:
		settin()
	else:
		nExit()

	screen.fill((200, 180,200))

	for peer in n.peer_list:
		playerList.append(player.Player(peer[0], peer[1]))
	done = False
	mySelf = None
	n.send()
	#n.minput(1, -5000, -5000)

	cashRate = 50
	cashTicks = 0

	mygui = gui.Gui()
	while not done:
		if not lobby:
			n.send()
			screen.fill((80, 110, 80),backRect)
	
			# update economy
			cashTicks += 1
			if mySelf != None and cashTicks == cashRate:
				mySelf.cash += 1
				cashTicks = 0
	
			#event loop
			eventLoop(worldMap, n, backRect, screen, playerList,mygui)
	
			n.recv()
			while not n.recv_queue.empty():
				tempData = n.recv_queue.get()
				#start debug line
				#if tempData[2] == 2:
					#print "Info: %d %d %d" % (tempData[0], tempData[1], tempData[2])
				if tempData[2] == 7:
					#print "Adding player CID: %d Name: %s" % (tempData[3], tempData[4])
					playerList.append(player.Player(tempData[3], tempData[4]))
					for person in playerList:
						if n.info.cid == person.playerID:
							mySelf = person
	
					#print len(playerList)
					#for peer in playerList:
					#	print peer.troops
	
				for person in playerList:
					#if tempData[2] == 2:
						#print "playerID: %d" % person.playerID
						#print "tempData[0]: %d" % tempData[0]					
					if tempData[0] == person.playerID:
					#if True:
						if tempData[2] == 2:
							#print "Recieved %d %d %d" % (tempData[3][0], tempData[3][1], tempData[3][2])
							if tempData[3][0] == 1:
								for b in person.buildings:
									b.setSelectVal(False)
								for b in person.buildings:
									if b.rect.collidepoint(tempData[3][1],tempData[3][2]):
										b.setSelectVal(True)
										break
								for tro in person.troops:
									tro.setSelectVal(False)
								for tro in person.troops:
									touchRect = pygame.Rect(tro.getLocationX()- worldMap.view.locX, tro.getLocationY() - worldMap.view.locY, tro.mySprite.get_rect()[2], tro.mySprite.get_rect()[3])
									if touchRect.collidepoint(tempData[3][1] - worldMap.view.locX,tempData[3][2] - worldMap.view.locY):
										#print "selected player %d's unit" % person.playerID
										tro.setSelectVal(True)
										break
									else:
										tro.setSelectVal(False)
	
							elif tempData[3][0] == 3:
								for tro in person.troops:
									if tro.isSelected():
			
										for p in playerList:
											for t in p.troops:
												tRect = pygame.Rect(t.getLocationX()- worldMap.view.locX, t.getLocationY() - worldMap.view.locY, t.mySprite.get_rect()[2], t.mySprite.get_rect()[3])
												if tRect.collidepoint(tempData[3][1] - worldMap.view.locX,tempData[3][2] - worldMap.view.locY):
													if (person.playerID != p.playerID):
														tro.attack(t)
														unitAttacked = True
														break
												else:
													pass
														#tro.attacking = False
											for b in p.buildings:
												tRect = pygame.Rect(b.getLocationX()- worldMap.view.locX, b.getLocationY() - worldMap.view.locY, b.mySprite.get_rect()[2], b.mySprite.get_rect()[3])
												if tRect.collidepoint(tempData[3][1] - worldMap.view.locX,tempData[3][2] - worldMap.view.locY):
													if (person.playerID != p.playerID):
														tro.attack(b)
														unitAttacked = True
														break
												else:
													pass
														#tro.attacking = False
	
	
	
										if (unitAttacked == False):
											tro.attacking = False
											tro.attackingUnit = None
											tro.moveToTargetX = tempData[3][1]
											tro.moveToTargetY = tempData[3][2]
							elif tempData[3][0] == 11 or tempData[3][0] == 12:
								person.buildings.append(building.Building(tempData[3][1]-45,tempData[3][2]-45,person.color,tempData[3][0]-10))
								if mySelf.playerID == person.playerID:
									mySelf.cash -= 100
	
							elif tempData[3][0] == 24:
								person.troops.append(troop.Troop(tempData[3][1],tempData[3][2], person.color))
							elif tempData[3][0] == 25:
								person.troops.append(speedster.Speedster(tempData[3][1],tempData[3][2], person.color))
	
			#Update Units loop goes here ((once we have a unit class
			updateUnits(screen, playerList, worldMap,mygui)
			mygui.drawRightPanel_Player(mySelf)
			mygui.drawTopPanel_Player(mySelf)
			mygui.refresh(screen)
			unitAttacked = False
		elif lobby:
			n.send()
			screen.blit(pygame.image.load('images/splash.png').convert(),(0,0))
			mygui.refresh(screen)
			first = False
			if len(playerList) == 0:
				first = True
			if first:

				while True:
					events = pygame.event.get()
					for e in events:
						#n.send()
						if e.type == pygame.KEYDOWN:
							if e.key == K_RETURN:
								n.minput(42,1,1)
								#n.send()
								#n.minput(1, -5000, -5000)
								lobby = False
								break
						elif e.type == pygame.MOUSEBUTTONDOWN:
							n.minput(42,1,1)
							#n.send()
							#n.minput(1, -5000, -5000)
							lobby = False
							break

					n.recv()
					while not n.recv_queue.empty():
						tup = n.recv_queue.get()
						if tup[2] == 7:
							#print "Adding player CID: %d Name: %s" % (tempData[3], tempData[4])
							playerList.append(player.Player(tup[3], tup[4]))
							for person in playerList:
								if n.info.cid == person.playerID:
									mySelf = person
						if tup[2] == 2:
							if (tup[3][0] == 42):
								lobby = False
								n.minput(1, -5000, -5000)
								break
					if lobby == False:
						break
					n.send()

			else:
				#n.send()
				while True:
					n.recv()
					while not n.recv_queue.empty():
						tup = n.recv_queue.get()
						if tup[2] == 7:
							#print "Adding player CID: %d Name: %s" % (tempData[3], tempData[4])
							playerList.append(player.Player(tup[3], tup[4]))
							for person in playerList:
								if n.info.cid == person.playerID:
									mySelf = person
						if tup[2] == 2:
							if (tup[3][0] == 42):
								lobby = False
								n.minput(1, -5000, -5000)
								break
					if lobby == False:
						break
					n.send()
	
	print "Exiting"


def eventLoop(worldMap, n, backRect, screen, playerList, mygui):
	global building_mode, selected_building
	
	# figure out who I am
	for p in playerList:
		if n.info.cid == p.playerID:
			mySelf = p
			break
	
	events = pygame.event.get()
	for e in events:
		#quit
		if(e.type == QUIT):
			nExit()
		#key recognition branch
		elif(e.type == pygame.KEYDOWN):
			if (e.key == K_UP):
				#print "Key up"
				if (worldMap.view.locY - 100 < 0):
					worldMap.view.locY = 0
				else:
					worldMap.view.locY -= 100
				updateUnits(screen, playerList, worldMap,mygui)
			elif (e.key == K_DOWN):
				#print "Key down"
				if (worldMap.view.locY + worldMap.view.sizeY + 100 > worldMap.sizeY):
					worldMap.view.locY = worldMap.sizeY - worldMap.view.sizeY
				else:
					worldMap.view.locY += 100
				updateUnits(screen, playerList, worldMap,mygui)
			elif (e.key == K_RIGHT):
				#print "Key right"
				if (worldMap.view.locX + worldMap.view.sizeX + 100 > worldMap.sizeX):
					worldMap.view.locX = worldMap.sizeX - worldMap.view.sizeX
				else:
					worldMap.view.locX += 100
				updateUnits(screen, playerList, worldMap,mygui)
			elif (e.key == K_LEFT):
				#print "Key Left"
				if (worldMap.view.locX - 100 < 0):
					worldMap.view.locX = 0
				else:
					worldMap.view.locX -= 100
				updateUnits(screen, playerList, worldMap,mygui)

			elif (e.key == K_INSERT):
				worldMap.view.locX = 0
				worldMap.view.locY = 0
			elif (e.key == K_PAGEUP):
				worldMap.view.locX = worldMap.sizeX - worldMap.view.sizeX
				worldMap.view.locY = 0
			elif (e.key == K_DELETE):
				worldMap.view.locX = 0
				worldMap.view.locY = worldMap.sizeY - worldMap.view.sizeY
			elif (e.key == K_PAGEDOWN):
				worldMap.view.locX = worldMap.sizeX - worldMap.view.sizeX
				worldMap.view.locY = worldMap.sizeY - worldMap.view.sizeY
			else:
				pass
		elif(e.type == pygame.MOUSEBUTTONDOWN):
			#print e.button
			if (backRect.collidepoint(e.pos[0], e.pos[1])):
				if (e.button == 1):
					if not building_mode:
						print "not building mode"
						globalX = worldMap.view.locX + e.pos[0]
						globalY = worldMap.view.locY + e.pos[1]
						n.minput(1, globalX, globalY)
					elif building_mode:
						# check if the mouse was clicked in the world
						ground_clear = 1
						for p in playerList:
							for b in p.buildings:
								if b.rect.colliderect(pygame.Rect((e.pos[0]+worldMap.view.locX)-45,(e.pos[1]+worldMap.view.locY)-45,90,90)):
									ground_clear = 0
							for t in p.troops:
								tmpRect = pygame.Rect(t.locationX,t.locationY,t.mySprite.get_rect()[2], t.mySprite.get_rect()[3])
								if tmpRect.colliderect(pygame.Rect((e.pos[0]+worldMap.view.locX)-45,(e.pos[1]+worldMap.view.locY)-45,90,90)):
									ground_clear = 0
						if ground_clear:
							n.minput(10+selected_building,(e.pos[0]+worldMap.view.locX),(e.pos[1]+worldMap.view.locY))
							building_mode = 0

				elif (e.button == 3):
					building_mode = 0
					globalX = worldMap.view.locX + e.pos[0]
					globalY = worldMap.view.locY + e.pos[1]
					n.minput(3, globalX, globalY)
			else: # not in backRect
				if (e.button == 1 and mygui.selectedUnitType < 0):
					# if a building was clicked set 'place building mode'
					if mygui.baseRect.collidepoint(e.pos[0],e.pos[1]) and mySelf.cash >= building.Building.costBase:
						print "hit base"
						building_mode = 1
						selected_building = 1
					elif mygui.barracksRect.collidepoint(e.pos[0],e.pos[1]) and mySelf.cash >= building.Building.costBarracks:
						print "hit barracks"
						building_mode = 1
						selected_building = 2

				elif (e.button == 1 and mygui.selectedUnitType == 1):
					for person in playerList:
						if n.info.cid == person.playerID:
							m = person

					for b in m.buildings:
						if b.selected and selected_building == 2:
							if mygui.troopRect.collidepoint(e.pos[0],e.pos[1]) and mySelf.cash >= unit.Unit.troopCost:
								n.minput(25,(b.locationX+95),(b.locationY + 50))
								mySelf.cash -= unit.Unit.troopCost
								
							elif mygui.speedsterRect.collidepoint(e.pos[0],e.pos[1]) and mySelf.cash >= unit.Unit.speedsterCost:
								print "hit speedster"
								n.minput(24,(b.locationX +95),(b.locationY + 50))
								mySelf.cash -= unit.Unit.speedsterCost

				elif (e.button == 3):
					building_mode = 0
		else:
			pass

def updateUnits(screen, playerList, worldMap, mygui):

	global framesPast
	global building_mode, selected_building

	framesPast += 1
	
	for person in playerList:
		for tro in person.troops:

			if tro.isAlive:


				if tro.attacking:
					distanceToTarget = vec.distance((tro.getLocationX() , tro.getLocationY() ) , (tro.attackingTarget().getLocationX() ,tro.attackingTarget().getLocationY() ))
					unitDirect = vec.unitdir(tro.getMoveToTargetX(), tro.getMoveToTargetY(), tro.getLocationX(), tro.getLocationY(), tro.getSpeed())
					tro.setRotation(unitDirect)
					if distanceToTarget < tro.attackRange:
						tro.moveToTargetX = tro.getLocationX()
						tro.moveToTargetY = tro.getLocationY()
						tro.fire(framesPast)
					else:
						tro.moveToTargetX = tro.attackingTarget().getLocationX()
						tro.moveToTargetY = tro.attackingTarget().getLocationY()
	
	
				unitDirect = vec.unitdir(tro.getMoveToTargetX(), tro.getMoveToTargetY(), tro.getLocationX(), tro.getLocationY(), tro.getSpeed())
				tro.setRotation(unitDirect)
	
				newMoveRect = pygame.Rect(tro.locationX + (tro.speed * unitDirect[0]),tro.locationY + (tro.speed * unitDirect[1]),tro.mySprite.get_rect()[2], tro.mySprite.get_rect()[3])
				for p in playerList:
					for b in p.buildings:
						newRect = pygame.Rect(b.locationX ,b.locationY,b.mySprite.get_rect()[2], b.mySprite.get_rect()[3])
						if newMoveRect.colliderect(newRect):
							tro.moveToTargetX = tro.getLocationX()
							tro.moveToTargetY = tro.getLocationY()
	
				unitDirect = vec.unitdir(tro.getMoveToTargetX(), tro.getMoveToTargetY(), tro.getLocationX(), tro.getLocationY(), tro.getSpeed())
				tro.setRotation(unitDirect)
		
				tro.locationX = tro.locationX + (tro.speed * unitDirect[0])
				tro.locationY = tro.locationY + (tro.speed * unitDirect[1])
				tro.centerX = tro.locationX + (tro.mySprite.get_rect()[2] / 2)
				tro.centerY = tro.locationY + (tro.mySprite.get_rect()[3] / 2)
				translatedX = tro.locationX - worldMap.view.locX
				translatedY = tro.locationY - worldMap.view.locY
				#print translatedX
				#print translatedY
				#print worldMap.view.sizeX
				#print worldMap.view.sizeY
				if translatedX > 0 and translatedY > 0 and translatedX < worldMap.view.sizeX and translatedY < worldMap.view.sizeY:
					screen.blit(tro.mySprite, (translatedX,translatedY))
	
				for b in tro.bulletList:
					if b.isActive:
						if (framesPast - b.whenFired) > b.lifeTime:
							b.disable()
						
						unitDirect = vec.unitdir(b.attackingTarget().locationX, b.attackingTarget().locationY, b.getLocationX(), b.getLocationY(), b.getSpeed())
						b.setRotation(unitDirect)
						b.locationX = b.locationX + (b.speed * unitDirect[0])
						b.locationY = b.locationY + (b.speed * unitDirect[1])
						b.centerX = b.locationX + (b.mySprite.get_rect()[2] / 2)
						b.centerY = b.locationY + (b.mySprite.get_rect()[3] / 2)
						translatedX = b.locationX - worldMap.view.locX
						translatedY = b.locationY - worldMap.view.locY
						newMoveRect = pygame.Rect(b.locationX,b.locationY,b.mySprite.get_rect()[2], b.mySprite.get_rect()[3])
						for p in playerList:
							for t in p.troops:
								if id(tro) != id(t):
									if t.isAlive:
										newRect = pygame.Rect(t.locationX ,t.locationY,t.mySprite.get_rect()[2], t.mySprite.get_rect()[3])
										if newMoveRect.colliderect(newRect):
											b.disable()
											t.takeDamage(tro.attackDamage, tro, p.troops, playerList)
											if t.isAlive == False:
												tro.attacking = False
												tro.attackingTarget = None

							for bild in p.buildings:
								if bild.isAlive:
									newRect = pygame.Rect(bild.locationX, bild.locationY, bild.mySprite.get_rect()[2], bild.mySprite.get_rect()[3])
									if newMoveRect.colliderect(newRect):
										b.disable()
										bild.takeDamage(tro.attackDamage, tro, p.buildings, playerList)
										if bild.isAlive == False:
											tro.attackingTarget = None
									
	
						if translatedX > 0 and translatedY > 0 and translatedX < worldMap.view.sizeX and translatedY < worldMap.view.sizeY:
							screen.blit(b.mySprite, (translatedX,translatedY))
	
	
	
		for b in person.buildings:
			if b.isAlive:
				translatedX = b.locationX - worldMap.view.locX
				translatedY = b.locationY - worldMap.view.locY
				if translatedX > 0 and translatedY > 0 and translatedX < worldMap.view.sizeX and translatedY < worldMap.view.sizeY:
					screen.blit(b.mySprite, (translatedX,translatedY))

	if building_mode:
		loc = pygame.mouse.get_pos()
		if selected_building == 1:
			#print "blit base"
			screen.blit(mygui.base, (loc[0]-45,loc[1]-45))
		elif selected_building == 2:
			#print "blit barracks"
			screen.blit(mygui.barracks, (loc[0]-45,loc[1]-45))
		

def nGame(screen, settingData):
	print "Starting New Game"
	print settingData[1]
	#n = NS.server_thread(int(settingData[1]),3)
	#n.start()
	n = 1
	pygame.display.set_caption('New Game')

	print "Done"
	return n;

def nExit():
	print "Starting Shutdown Process"
	print "done"
	sys.exit()
	

def connectGame(screen, settingData):
	print "Starting New Game"
	print settingData[1]
	n = NC.client_thread(settingData[0],int(settingData[1]))
	n.connect()

	pygame.display.set_caption('New Game')

	print "Done"
	return n;

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
