import unit

class Building(unit.Unit):
	def __init__(self, positionX, positionY):

		self.unitType = 0		
		self.locationX = positionX
		self.locationY = positionY
		self.rotation = 0
		self.speed = 0
		self.maxHealth = 1000
		self.currHealth = self.maxHealth
		
		#Offensive
		self.attackRate = 0
		self.attackRange = 0
		self.attackDamage = 0
		self.attackExplosionSize = 0
		self.attackChanceOfCriticalHit = 0.05

		self.attackAtX = -1
		self.attackAtY = -1

		#Defensive
		self.damageResistance = 0

		self.onDeathDamageNearby = 0
