#!/usr/bin/env python

import sys
import os
import pygame
from pygame.locals import *
from pygame.color import THECOLORS


def main():
	windowSize = 640,480
	pygame.init()
	screen = pygame.display.set_mode(windowSize,0,8)
	pygame.display.set_caption('Made by: Latch Studios')
	screen.fill((159, 180,200))
	mainMenu(screen)
	pygame.display.update()
	
	done = False
	while not done:
		#event handling
		events = pygame.event.get()
		for e in events:
			if(e.type == QUIT):
				done = True
				break
			else:
				pass

	print "Exiting"



def mainMenu(screen):
	
	font = pygame.font.Font(None, 30)
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
	newGameR.centery = screen.get_rect().centery - 30

	joinGameR.centerx = screen.get_rect().centerx
	joinGameR.centery = screen.get_rect().centery

	settingsR.centerx = screen.get_rect().centerx
	settingsR.centery = screen.get_rect().centery + 30

	quitR.centerx = screen.get_rect().centerx
	quitR.centery = screen.get_rect().centery + 60

	screen.blit(newGame,newGameR)
	screen.blit(joinGame,joinGameR)
	screen.blit(settings,settingsR)
	screen.blit(quit,quitR)


	pygame.display.update()

	done = False
	while not done:
		#event handling
		events = pygame.event.get()
		for e in events:
			if(e.type == QUIT):
				print "Exiting"
				exit()
			else:
				pass
if __name__ == "__main__":
	main()
