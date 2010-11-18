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

def drawTopPanel(selectedUnit):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    topPanel = pygame.Surface((680, 36))
    topPanel.fill((0,0,0))
    gameWindow.blit(topPanel,(0,0))
    gameWindow.blit(font.render('Unit', 0, (255,255,255)), (80,0))
    gameWindow.blit(font.render('Power', 0, (255,255,255)), (240, 0))
    gameWindow.blit(font.render('Cash', 0, (255,255,255)), (400, 0))
    gameWindow.blit(font.render('Latch Studios',0, (255,255,255)), (545, 0))
    gameWindow.blit(font.render('0/10', 0, (0,255,0)), (80,18))
    gameWindow.blit(font.render('0/200', 0, (0,255,0)), (240, 18))
    gameWindow.blit(font.render('$0', 0, (0,255,0)), (406, 18))

def drawPanels(selectedUnit):
    drawTopPanel(selectedUnit)
    drawRightPanel(selectedUnit)    

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
        gameWindow.blit(font.render('Building',0, (255,255,255)), (558, 60))
        gameWindow.blit(font.render('Construction',0, (255,255,255)), (540, 80))
        base = pygame.image.load('base.jpg')
        barracks = pygame.image.load('barracks.jpg')
        base.set_clip((0,0), (90,90))
        barracks.set_clip((0,0), (90,90))
        gameWindow.blit(font.render('Base',0, (255,255,255)), (565, 120))
        gameWindow.blit(base, (530, 140))
        gameWindow.blit(font.render('Barracks',0, (255,255,255)), (550, 280))
        gameWindow.blit(barracks, (530, 300))
        pygame.display.update()

    # -- TROOP -- #
    elif (selectedUnitType == 0):

        # UNIT NAME AND INFO SECTION #
        if (selectedUnit.unitType == 1):
            gameWindow.blit(font.render('Troop',0, (255,255,255)), (560, 60))
            gameWindow.blit(ifont.render('The backbone of', 0, (255,255,255)), (525, 260))
            gameWindow.blit(ifont.render('any good military', 0, (255,255,255)), (525, 280))
            gameWindow.blit(ifont.render('force. These units', 0, (255,255,255)), (525, 300))
            gameWindow.blit(ifont.render('are the perfect', 0, (255,255,255)), (525, 320))
            gameWindow.blit(ifont.render('balance of attack,', 0, (255,255,255)), (525, 340))
            gameWindow.blit(ifont.render('defense, and speed.', 0, (255,255,255)), (525, 360))
        elif (selectedUnit.unitType == 4):
            gameWindow.blit(font.render('Speedster',0, (255,255,255)), (550, 60))
            gameWindow.blit(ifont.render('Built for speed,', 0, (255,255,255)), (525, 260))
            gameWindow.blit(ifont.render('these weaker units', 0, (255,255,255)), (525, 280))
            gameWindow.blit(ifont.render('are ideal for', 0, (255,255,255)), (525, 300))
            gameWindow.blit(ifont.render('scouting or for', 0, (255,255,255)), (525, 320))
            gameWindow.blit(ifont.render('launching quick hit', 0, (255,255,255)), (525, 340))
            gameWindow.blit(ifont.render('and runs against', 0, (255,255,255)), (525, 360))
            gameWindow.blit(ifont.render('your enemy.', 0, (255,255,255)), (525, 380))

        # UNIT PICTURE #
        gameWindow.blit(selectedUnit.baseSprite, (570, 90))

        # HEALTH #
        curHealth = 100
        maxHealth = 100
        gameWindow.blit(font.render('Health',0, (255,255,255)), (560, 120))
        healthBar = gameWindow.subsurface(530,140,100,15)
        healthBar.fill((0,255,0), rect=pygame.Rect(0,0,curHealth,15))
        healthBar.fill((255,0,0), rect=pygame.Rect(maxHealth-curHealth,0,maxHealth-curHealth,15))
        gameWindow.blit(font.render(str(curHealth) + " / " + str(maxHealth), 0, (0,0,0)), (555,140))

        # UNIT INFO #
        gameWindow.blit(font.render('Speed',0, (255,255,255)), (530, 160))
        gameWindow.blit(font.render('Damage',0, (255,255,255)), (530, 180))
        gameWindow.blit(font.render('Range',0, (255,255,255)), (530, 200))
        gameWindow.blit(font.render(str(selectedUnit.speed),0, (255,255,255)), (595, 160))
        gameWindow.blit(font.render(str(selectedUnit.attackDamage),0, (255,255,255)), (595, 180))
        gameWindow.blit(font.render(str(selectedUnit.attackRange),0, (255,255,255)), (595, 200))

    # -- BUILDING -- #
    elif (selectedUnitType == 1):
        gameWindow.fill((0,0,0), rect=rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), rect=topPanel, special_flags=0)

'''
    # -- SUPPORT -- #
    elif (selectedUnit == 2):
        gameWindow.fill((0,0,0), rect=rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), rect=topPanel, special_flags=0)
'''

def drawTopPanel_Player(currentPlayer):
    font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
    gameWindow = pygame.display.get_surface()

    topPanel = pygame.Surface((680, 36))
    topPanel.fill((0,0,0))
    gameWindow.blit(topPanel,(0,0))

    # TOP PANEL INFO BAR #
    gameWindow.blit(font.render('<Game Name Here>', 0, (255,255,255)), (15, 10))
    gameWindow.blit(font.render(currentPlayer.name, 0, (255,255,255)), (200, 10))
    gameWindow.blit(font.render('Units', 0, (255,255,255)), (300,0))
    gameWindow.blit(font.render('Power', 0, (255,255,255)), (370, 0))
    gameWindow.blit(font.render('Cash', 0, (255,255,255)), (440, 0))
    gameWindow.blit(font.render('Latch Studios',0, (255,255,255)), (535, 10))
    if (len(currentPlayer.troops) <= 10):
        gameWindow.blit(font.render(str(len(currentPlayer.troops))+'/10', 0, (0,255,0)), (300,18))
    else:
        gameWindow.blit(font.render(str(len(currentPlayer.troops))+'/10', 0, (255,0,0)), (300,18))
    gameWindow.blit(font.render('0/200', 0, (0,255,0)), (370, 18))
    gameWindow.blit(font.render('$0', 0, (0,255,0)), (446, 18))

def drawPanels_Player(currentPlayer):
    drawTopPanel_Player(currentPlayer)
    drawRightPanel_Player(currentPlayer)    
