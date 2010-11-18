import pygame

def drawRightPanel(selectedUnit):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    if selectedUnit < 0:
        rightPanel = gameWindow.subsurface(520 ,25, 120, 455)
        rightPanel.fill((0,0,0))

        # HEALTH #
        curHealth = 50
        maxHealth = 100
        gameWindow.blit(font.render('Health',0, (255,255,255)), (550, 60))
        healthBar = gameWindow.subsurface(525,80,100,15)
        healthBar.fill((0,255,0), rect=pygame.Rect(0,0,curHealth,15))
        healthBar.fill((255,0,0), rect=pygame.Rect(maxHealth-curHealth,0,maxHealth-curHealth,15))
        gameWindow.blit(font.render(str(curHealth) + " / " + str(maxHealth), 0, (0,0,0)), (555,80))
        
    
        # SIDE PANEL INFO BAR #
        base = pygame.image.load('base.jpg')
        barracks = pygame.image.load('barracks.jpg')
        base.set_clip((0,0), (90,90))
        barracks.set_clip((0,0), (90,90))
        gameWindow.blit(font.render('Build a Base',0, (255,255,255)), (525, 100))
        gameWindow.blit(base, (525, 120))
        gameWindow.blit(font.render('Build a Barracks',0, (255,255,255)), (525, 260))
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
def drawTopPanel(selectedUnit):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    if selectedUnit < 0:
        topPanel = pygame.Surface((680, 36))
        topPanel.fill((0,0,0))
        gameWindow.blit(topPanel,(0,0))
    
        # TOP PANEL INFO BAR #
        gameWindow.blit(font.render('Unit', 0, (255,255,255)), (80,0))
        gameWindow.blit(font.render('Power', 0, (255,255,255)), (240, 0))
        gameWindow.blit(font.render('Cash', 0, (255,255,255)), (400, 0))
        gameWindow.blit(font.render('Latch Studios',0, (255,255,255)), (545, 0))
        gameWindow.blit(font.render('0/10', 0, (0,255,0)), (80,18))
        gameWindow.blit(font.render('0/200', 0, (0,255,0)), (240, 18))
        gameWindow.blit(font.render('$0', 0, (0,255,0)), (406, 18))
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

def drawPanels(selectedUnit):
    drawTopPanel(selectedUnit)
    drawRightPanel(selectedUnit)    

def refresh(screen):
	pygame.display.update()

def drawRightPanel_Player(currentPlayer):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    selectedUnit = -1

    if selectedUnit < 0:
        rightPanel = gameWindow.subsurface(520 ,25, 120, 455)
        rightPanel.fill((0,0,0))

        # HEALTH #
        curHealth = 50
        maxHealth = 100
        gameWindow.blit(font.render('Health',0, (255,255,255)), (550, 60))
        healthBar = gameWindow.subsurface(525,80,100,15)
        healthBar.fill((0,255,0), rect=pygame.Rect(0,0,curHealth,15))
        healthBar.fill((255,0,0), rect=pygame.Rect(maxHealth-curHealth,0,maxHealth-curHealth,15))
        gameWindow.blit(font.render(str(curHealth) + " / " + str(maxHealth), 0, (0,0,0)), (555,80))
        
    
        # SIDE PANEL INFO BAR #
        base = pygame.image.load('base.jpg')
        barracks = pygame.image.load('barracks.jpg')
        base.set_clip((0,0), (90,90))
        barracks.set_clip((0,0), (90,90))
        gameWindow.blit(font.render('Build a Base',0, (255,255,255)), (525, 100))
        gameWindow.blit(base, (525, 120))
        gameWindow.blit(font.render('Build a Barracks',0, (255,255,255)), (525, 260))
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
def drawTopPanel_Player(currentPlayer):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    topPanel = pygame.Surface((680, 36))
    topPanel.fill((0,0,0))
    gameWindow.blit(topPanel,(0,0))

    # TOP PANEL INFO BAR #
    gameWindow.blit(font.render('Unit', 0, (255,255,255)), (80,0))
    gameWindow.blit(font.render('Power', 0, (255,255,255)), (240, 0))
    gameWindow.blit(font.render('Cash', 0, (255,255,255)), (400, 0))
    gameWindow.blit(font.render('Latch Studios',0, (255,255,255)), (545, 0))
    gameWindow.blit(font.render('0/10', 0, (0,255,0)), (80,18))
    gameWindow.blit(font.render('0/200', 0, (0,255,0)), (240, 18))
    gameWindow.blit(font.render('$0', 0, (0,255,0)), (406, 18))

def drawPanels_Player(currentPlayer):
    drawTopPanel_Player(currentPlayer)
    drawRightPanel_Player(currentPlayer)    
