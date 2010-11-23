import pygame   
   
class Gui():
    def __init__(self):
        self.base = pygame.image.load('images/base.png').convert()
        self.barracks = pygame.image.load('images/barracks.png').convert()
        self.defaultRight = pygame.image.load('images/defaultrightpanel.png').convert()
        self.speedsterRight = pygame.image.load('images/speedster.png').convert()
        self.troopRight = pygame.image.load('images/troop.png').convert()
        self.topPanel = pygame.image.load('images/toppanel.png').convert()
        #self.base.set_clip((0,0), (90,90))
        #self.barracks.set_clip((0,0), (90,90))
        self.baseRect = pygame.Rect(530,165,90,90)
        self.barracksRect = pygame.Rect(530,310,90,90)
        self.font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
        self.selectedUnitType = -1

    def refresh(self, screen):
    	pygame.display.update()

    def drawRightPanel_Player(self, currentPlayer):
        gameWindow = pygame.display.get_surface()
    
        self.selectedUnitType = -1
    
        for unit in currentPlayer.troops:
            if unit.selected == 1:
                self.selectedUnitType = 0
                selectedUnit = unit
    
        for unit in currentPlayer.buildings:
            if unit.selected == 1:
                selectedUnit = 1
                print "building is selected with type: ", unit.buildingType
    
        # -- NOTHING SELECTED -- #
        if self.selectedUnitType < 0:
    
            # BUILDING SELECTION #
            gameWindow.blit(self.defaultRight, (515, 36))
            gameWindow.blit(self.base, (530, 165))
            gameWindow.blit(self.barracks, (530, 310))
    
        # -- UNIT -- #
        elif (self.selectedUnitType == 0):
    
            # TROOP #
            if (selectedUnit.unitType == 1):
                gameWindow.blit(self.troopRight, (515, 36))
    
    		# SPEEDSTER #
            elif (selectedUnit.unitType == 4):
                gameWindow.blit(self.speedsterRight, (515, 36))
    
            # UNIT PICTURE #
            gameWindow.blit(selectedUnit.baseSprite, (570, 90))
    
            # HEALTH #
            curHealth = 100
            maxHealth = 100
            healthBar = gameWindow.subsurface(530,165,100,15)
            healthBar.fill((0,255,0), pygame.Rect(0,0,curHealth,15))
            healthBar.fill((255,0,0), pygame.Rect(maxHealth-curHealth,0,maxHealth-curHealth,15))
            gameWindow.blit(self.font.render(str(curHealth) + " / " + str(maxHealth), 0, (0,0,0)), (555,165))
    
            # UNIT INFO #
            gameWindow.blit(self.font.render(str(selectedUnit.speed),0, (255,255,255)), (605, 212))
            gameWindow.blit(self.font.render(str(selectedUnit.attackDamage),0, (255,255,255)), (605, 235))
            gameWindow.blit(self.font.render(str(selectedUnit.attackRange),0, (255,255,255)), (605, 258))
    
        # -- BUILDING -- #
        elif (self.selectedUnitType == 1):
            gameWindow.fill((0,0,0), rightPanel, special_flags=0)
            gameWindow.fill((0,0,0), topPanel, special_flags=0)
    
    '''
        # -- SUPPORT -- #
        elif (selectedUnit == 2):
            gameWindow.fill((0,0,0), rightPanel, special_flags=0)
            gameWindow.fill((0,0,0), topPanel, special_flags=0)
    '''

    def drawTopPanel_Player(self, currentPlayer):
        gameWindow = pygame.display.get_surface()
    
        gameWindow.blit(self.topPanel,(0,0))
    
        # TOP PANEL INFO BAR #
        gameWindow.blit(self.font.render('<Game Name Here>', 0, (255,255,255)), (15, 10))
        gameWindow.blit(self.font.render(currentPlayer.name, 0, (255,255,255)), (200, 10))
        if (len(currentPlayer.troops) <= 10):
            gameWindow.blit(self.font.render(str(len(currentPlayer.troops))+'/10', 0, (0,255,0)), (313,18))
        else:
            gameWindow.blit(self.font.render(str(len(currentPlayer.troops))+'/10', 0, (255,0,0)), (313,18))
        gameWindow.blit(self.font.render('0/200', 0, (0,255,0)), (385, 18))
        gameWindow.blit(self.font.render('$0', 0, (0,255,0)), (469, 18))
    
    def drawPanels_Player(self, currentPlayer):
        self.drawTopPanel_Player(currentPlayer)
        self.drawRightPanel_Player(currentPlayer)                    
