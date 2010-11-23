import pygame   

def refresh(screen):
	pygame.display.update()

def drawRightPanel_Player(currentPlayer):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    ifont = pygame.font.Font(pygame.font.match_font('Courier_New'), 10)
    gameWindow = pygame.display.get_surface()
    rightPanel = gameWindow.subsurface(520 ,25, 120, 455)
    rightPanel.fill((0,0,0))

    selectedUnitType = -1

    for unit in currentPlayer.troops:
        if unit.selected == 1:
            selectedUnitType = 0
            selectedUnit = unit

    for unit in currentPlayer.buildings:
        if unit.selected == 1:
            selectedUnit = 1

    # -- NOTHING SELECTED -- #
    if selectedUnitType < 0:

        # BUILDING SELECTION #
        base = pygame.image.load('images/base.jpg').convert()
        barracks = pygame.image.load('images/barracks.jpg').convert()
        panel = pygame.image.load('images/defaultrightpanel.png').convert()
        base.set_clip((0,0), (90,90))
        barracks.set_clip((0,0), (90,90))
        gameWindow.blit(panel, (515, 36))
        gameWindow.blit(base, (530, 165))
        gameWindow.blit(barracks, (530, 310))

    # -- UNIT -- #
    elif (selectedUnitType == 0):

        # TROOP #
        if (selectedUnit.unitType == 1):
            panel = pygame.image.load('images/troop.png').convert()

		# SPEEDSTER #
        elif (selectedUnit.unitType == 4):
            panel = pygame.image.load('images/speedster.png').convert()

        gameWindow.blit(panel, (515, 36))

        # UNIT PICTURE #
        gameWindow.blit(selectedUnit.baseSprite, (570, 90))

        # HEALTH #
        curHealth = 100
        maxHealth = 100
        healthBar = gameWindow.subsurface(530,165,100,15)
        healthBar.fill((0,255,0), pygame.Rect(0,0,curHealth,15))
        healthBar.fill((255,0,0), pygame.Rect(maxHealth-curHealth,0,maxHealth-curHealth,15))
        gameWindow.blit(font.render(str(curHealth) + " / " + str(maxHealth), 0, (0,0,0)), (555,165))

        # UNIT INFO #
        gameWindow.blit(font.render(str(selectedUnit.speed),0, (255,255,255)), (605, 212))
        gameWindow.blit(font.render(str(selectedUnit.attackDamage),0, (255,255,255)), (605, 235))
        gameWindow.blit(font.render(str(selectedUnit.attackRange),0, (255,255,255)), (605, 258))

    # -- BUILDING -- #
    elif (selectedUnitType == 1):
        gameWindow.fill((0,0,0), rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), topPanel, special_flags=0)

'''
    # -- SUPPORT -- #
    elif (selectedUnit == 2):
        gameWindow.fill((0,0,0), rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), topPanel, special_flags=0)
'''

def drawTopPanel_Player(currentPlayer):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    topPanel = pygame.image.load('images/toppanel.png').convert()
    gameWindow.blit(topPanel,(0,0))

    # TOP PANEL INFO BAR #
    gameWindow.blit(font.render('<Game Name Here>', 0, (255,255,255)), (15, 10))
    gameWindow.blit(font.render(currentPlayer.name, 0, (255,255,255)), (200, 10))
    if (len(currentPlayer.troops) <= 10):
        gameWindow.blit(font.render(str(len(currentPlayer.troops))+'/10', 0, (0,255,0)), (313,18))
    else:
        gameWindow.blit(font.render(str(len(currentPlayer.troops))+'/10', 0, (255,0,0)), (313,18))
    gameWindow.blit(font.render('0/200', 0, (0,255,0)), (385, 18))
    gameWindow.blit(font.render('$0', 0, (0,255,0)), (469, 18))

def drawPanels_Player(currentPlayer):
    drawTopPanel_Player(currentPlayer)
    drawRightPanel_Player(currentPlayer)    
