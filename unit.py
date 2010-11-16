#0 building
#1 troop
#2 support


class Unit:
	def __init__(self, spawnLocX, spawnLocY):
		#Initialization of basic stats
		self.maxHealth = 100
		self.currHealth = self.maxHealth
		self.killCount = 0
		self.rank = 0
		self.unitType = -1
		self.selected = False
		#Movement
		self.speed = 1

		self.moveToTargetX = self.locationX
		self.moveToTargetY = self.locationY

	def position(self):
		return self.locationX , self.locationY, self.rotation

	def setPosition(locX, locY):
		self.rotation = 0 #TODO: Math to calculate what rotation it will have after move		
		self.locationX = locX
		self.locationY = locY

	def isSelected(self):
		return self.selected

	def selectMe(self):
		self.selected = True

	def deselectMe(self):
		self.selected = False

