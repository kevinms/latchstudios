import pygame

def drawPanels(selectedUnit):
    size = 108,480
    font = pygame.font.Font(None, 14)
    gameWindow = pygame.display.get_surface()
    rightPanel = pygame.Surface((108, 455))
    topPanel = pygame.Surface((680, 25))
    rightPanel.fill((0,0,0))
    topPanel.fill((0,0,0))
    #rightPanel = pygame.Rect(532, 25, 108, 455)
    #topPanel = pygame.Rect(0, 0, 640, 25)
    unit = font.render("Unit", 0, (255,255,255))
    power = font.render("Power", 0, (255,255,255))
    cash = font.render("Cash", 0, (255,255,255))
    logo = font.render("Latch Studios", 0, (255,255,255))
    textpos = unit.get_rect()
    textpos.centerx = topPanel.get_rect().centerx
    topPanel.blit(unit, (80, 0))
    topPanel.blit(power, (240, 0))
    topPanel.blit(cash, (400, 0))
    topPanel.blit(logo, (560, 0))
    rightPanel.blit(unit, (54, 60))
    rightPanel.blit(power, (54, 180))
    rightPanel.blit(cash, (54, 300))
    rightPanel.blit(logo, (54, 420))
    gameWindow.blit(rightPanel,(532, 25))
    gameWindow.blit(topPanel,(0,0))
    pygame.display.flip()
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



