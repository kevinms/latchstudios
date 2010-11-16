import unit

class Support(unit.Unit):
	def __init__(self, positionX, positionY):

		self.unitType = 2
		
		self.locationX = positionX
		self.locationY = positionY
		self.rotation = 0
		self.speed = 10
		
		self.supportActionAtX = -1
		self.supportActionAtY = -1

		self.hugDiameter = 10  #(units inside the 'hug' diameter will have the benefits the support gives)
		self.healRate = 3
		self.addedSpeed = 3
		self.addedAttackRate = 3
		self.addedAttackRange = 25
		self.addedAttackDamage = 5
		self.addedAttackExplosionSize = 5
		self.addedAttackChanceOfCriticalHit = .02
		self.addedDamageResistance = 5
