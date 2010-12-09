import pygame   
   
class Gui:
    def __init__(self):
        self.base = pygame.image.load('images/IntranetExploder.png').convert()
        self.barracks = pygame.image.load('images/Fireblox.png').convert()
        self.defaultRight = pygame.image.load('images/defaultrightpanel.png').convert()
        self.speedsterRight = pygame.image.load('images/speedsterPanel.png').convert()
        self.troopRight = pygame.image.load('images/troop.png').convert()
        self.topPanel = pygame.image.load('images/toppanel.png').convert()
        #self.base.set_clip((0,0), (90,90))
        #self.barracks.set_clip((0,0), (90,90))
        self.basePanel = pygame.image.load('images/baseRight.png').convert()
        self.barracksPanel = pygame.image.load('images/barracksRight.png').convert()
        self.baseRect = pygame.Rect(530,165,90,90)
        self.barracksRect = pygame.Rect(530,310,90,90)
        self.font = pygame.font.Font(pygame.font.match_font('Arial'), 14)
        self.selectedUnitType = -1
        self.speedster = pygame.image.load('images/speedster_s.png').convert()
        self.troop = pygame.image.load('images/troop_s.png').convert()
        self.troopRect = pygame.Rect(530,300,30,25)
        self.speedsterRect = pygame.Rect(580,300,30,25)

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
                selectedUnit = unit
                self.selectedUnitType = 1
    
        # -- NOTHING SELECTED -- #
        if self.selectedUnitType < 0:
    
            # BUILDING SELECTION #
            gameWindow.blit(self.defaultRight, (515, 36))
            gameWindow.blit(self.base, (530, 165))
            gameWindow.blit(self.barracks, (530, 310))
    
        # -- UNIT -- #
        elif (self.selectedUnitType == 0):
            #gameWindow.blit()
            # TROOP #
            if (selectedUnit.unitType == 1):
                gameWindow.blit(self.troopRight, (515, 36))
                gameWindow.blit(self.troop, (570, 95))
    
    		# SPEEDSTER #
            elif (selectedUnit.unitType == 4):
                gameWindow.blit(self.troopRight, (515, 36))
                gameWindow.blit(self.speedster, (570, 95))
    
            # HEALTH #
            curHealth = selectedUnit.currHealth
            maxHealth = selectedUnit.maxHealth
            ratio = 100 / maxHealth
            healthBar = gameWindow.subsurface(530,165,100,15)
            healthBar.fill((0,255,0), pygame.Rect(0,0,curHealth*ratio,15))
            healthBar.fill((255,0,0), pygame.Rect(curHealth*ratio,0,(maxHealth-curHealth)*ratio,15))
            gameWindow.blit(self.font.render(str(curHealth) + " / " + str(maxHealth), 0, (0,0,0)), (555,165))
    
            # UNIT INFO #
            gameWindow.blit(self.font.render(str(selectedUnit.speed),0, (255,255,255)), (605, 212))
            gameWindow.blit(self.font.render(str(selectedUnit.attackDamage),0, (255,255,255)), (605, 235))
            gameWindow.blit(self.font.render(str(selectedUnit.attackRange),0, (255,255,255)), (605, 258))
    
        # -- BUILDING -- #
        elif (self.selectedUnitType == 1):

            # BASE #
            if (selectedUnit.buildingType == 1):
                gameWindow.blit(self.basePanel, (515, 36))
                gameWindow.blit(self.base, (530, 90))

            # BARRACKS #
            elif (selectedUnit.buildingType == 2):
                gameWindow.blit(self.barracksPanel, (515, 36))
                gameWindow.blit(self.barracks, (530, 90))
                gameWindow.blit(self.speedster, (530, 300))
                gameWindow.blit(self.troop, (580, 300))

            # HEALTH #
            curHealth = selectedUnit.currHealth
            maxHealth = selectedUnit.maxHealth
            ratio = float(100 / maxHealth)
            healthBar = gameWindow.subsurface(530,215,100,15)
            healthBar.fill((255,0,0), pygame.Rect(0,0,int(curHealth*ratio),15))
            healthBar.fill((0,255,0), pygame.Rect(int(curHealth*ratio),0,int((maxHealth-curHealth)*ratio),15))            
            gameWindow.blit(self.font.render(str(curHealth) + " / " + str(maxHealth), 0, (0,0,0)), (545,215))
    
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
        if (len(currentPlayer.troops) <= 10):
            gameWindow.blit(self.font.render(str(len(currentPlayer.troops))+'/10', 0, (0,255,0)), (313,18))
        else:
            gameWindow.blit(self.font.render(str(len(currentPlayer.troops))+'/10', 0, (255,0,0)), (313,18))
        gameWindow.blit(self.font.render('0/200', 0, (0,255,0)), (385, 18))
        gameWindow.blit(self.font.render('$'+str(currentPlayer.cash), 0, (0,255,0)), (469, 18))
    
    def drawPanels_Player(self, currentPlayer):
        self.drawTopPanel_Player(currentPlayer)
        self.drawRightPanel_Player(currentPlayer)                    
