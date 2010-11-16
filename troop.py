import unit

class Troop(unit.Unit):
	def __init__(self, positionX, positionY):

		self.unitType = 1
		
		self.locationX = positionX
		self.locationY = positionY
		self.rotation = 0
		self.speed = 10
		
		#Offensive
		self.attackRate = 0.8
		self.attackRange = 45
		self.attackDamage = 5
		self.attackExplosionSize = 15
		self.attackChanceOfCriticalHit = 0.05

		#Defensive
		self.damageResistance = 10
