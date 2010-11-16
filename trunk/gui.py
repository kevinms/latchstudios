import pygame

def drawPanels(selectedUnit):
    size = 108,480
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    if selectedUnit < 0:
        rightPanel = pygame.Surface((120, 455))
        topPanel = pygame.Surface((680, 36))
        rightPanel.fill((0,0,0))
        topPanel.fill((0,0,0))
        gameWindow.blit(rightPanel,(520, 36))
        gameWindow.blit(topPanel,(0,0))
    
        # TOP PANEL INFO BAR #
        gameWindow.blit(font.render('Unit', 0, (255,255,255)), (80,0))
        gameWindow.blit(font.render('Power', 0, (255,255,255)), (240, 0))
        gameWindow.blit(font.render('Cash', 0, (255,255,255)), (400, 0))
        gameWindow.blit(font.render('Latch Studios',0, (255,255,255)), (545, 0))
        gameWindow.blit(font.render('0/10', 0, (0,255,0)), (80,18))
        gameWindow.blit(font.render('0/200', 0, (0,255,0)), (240, 18))
        gameWindow.blit(font.render('$0', 0, (0,255,0)), (406, 18))
    
        # SIDE PANEL INFO BAR #
        base = pygame.image.load('base.jpg')
        barracks = pygame.image.load('barracks.jpg')
        base.set_clip((0,0), (90,90))
        barracks.set_clip((0,0), (90,90))
        gameWindow.blit(font.render('Build a Base',0, (255,255,255)), (525, 60))
        gameWindow.blit(base, (525, 100))
        gameWindow.blit(font.render('Build a Barracks',0, (255,255,255)), (525, 240))
        gameWindow.blit(barracks, (525, 280))
        pygame.display.update()
'''
    # -- BUILDING -- #
    if (selectedUnit == 0):
        gameWindow.fill((0,0,0), rect=rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), rect=topPanel, special_flags=0)

    # -- TROOP -- #
    elif (selectedUnit == 1):
        gameWindow.fill((0,0,0), rect=rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), rect=topPanel, special_flags=0)

    # -- SUPPORT -- #
    elif (selectedUnit == 2):
        gameWindow.fill((0,0,0), rect=rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), rect=topPanel, special_flags=0)

    else:
        #gameWindow.fill((0,0,0), rect=rightPanel, special_flags=0)
        #gameWindow.fill((0,0,0), rect=topPanel, special_flags=0)
'''
    

def refresh(screen):
	pygame.display.update()



