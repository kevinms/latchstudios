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
		self.isSelected = False
		#Movement
		self.speed = 1
		
	def position(self):
		return self.locationX , self.locationY, self.rotation

	def setPosition(locX, locY)
		self.rotation = 0 #TODO: Math to calculate what rotation it will have after move		
		self.locationX = locX
		self.locationY = locY
		

'''


		if unitType == 'troop':
			'troop
		if unitType == 'support':
			'support
			self.hugDiameter = 10 '(all units inside the hug diameter will have the benefits the support gives)
			self.healRate = 3
			self.addedSpeed = 3
			self.addedAttackRate = 
			self.addedAttackRange = 25
			self.addedAttackDamage
			self.addedAttackExplosionSize
			self.addedAttackChanceOfCriticalHit
			self.addedDamageResistance
'''
