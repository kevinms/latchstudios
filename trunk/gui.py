import pygame

def drawPanels(selectedUnit):
    size = 108,480
    font = pygame.font.Font(None, 14)
    gameWindow = pygame.display.get_surface()
    rightPanel = pygame.Rect(532, 25, 108, 455)
    topPanel = pygame.Rect(0, 0, 640, 25)

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
        gameWindow.fill((0,0,0), rect=rightPanel, special_flags=0)
        gameWindow.fill((0,0,0), rect=topPanel, special_flags=0)

def refresh(screen):
	pygame.display.update()


