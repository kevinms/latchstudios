import unit

class Building(unit.Unit):
	def __init__(self, positionX, positionY, colorVal):
		unit.Unit.__init__(self, positionX, positionY)

		self.unitType = 0		
		self.rotation = 0
		self.speed = 0
		self.maxHealth = 1000
		self.currHealth = self.maxHealth

		self.attackAtX = -1
		self.attackAtY = -1
