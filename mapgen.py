import random as R

class Block:
	def __init__(self, t, n, s, e, w, rez):
		self.BlockID = t
		self.north = n
		self.south = s
		self.east = e
		self.west = w
		self.probabilityMap = []
		self.pixMap = []
		self.res = rez

		for x in range(self.res):
			self.probabilityMap.append([])
			self.pixMap.append([])

			for y in range(self.res):
				self.probabilityMap[x].append(0)
				self.pixMap[x].append(0)
                    

	def gen(self, n, w, water):
		self.north = n.south
		self.west = w.east

		randTmp = R.random()
		if randTmp < water :
			self.east = 1
		else:
			self.east = 0

		randTmp = R.random()
		if randTmp < water :
			self.west = 1
		else:
			self.west = 0

                self.genProbabilityMap()
                self.genPixMap()
	def genProbabilityMap(self):
		for i in range(self.res):
			self.probabilityMap[0][i] = self.north
		for i in range(self.res):
			self.probabilityMap[self.res - 1][i] = self.south
		for i in range(self.res):
			self.probabilityMap[i][0] = self.west
		for i in range(self.res):
			self.probabilityMap[i][self.res -1 ] = self.east
                if (self.north == 1 and self.west == 0) or (self.north == 0 and self.west == 1) :
			self.probabilityMap[0][0] = .5
                if (self.north == 1 and self.east == 0) or (self.north == 0 and self.east == 1) :
			self.probabilityMap[0][self.res - 1] = .5
                if (self.south == 1 and self.west == 0) or (self.south == 0 and self.west == 1) :
			self.probabilityMap[self.res - 1][0] = .5
                if (self.south == 1 and self.east == 0) or (self.south == 0 and self.east == 1) :
			self.probabilityMap[self.res - 1][self.res - 1] = .5

		for x in range(self.res - 2):
			for y in range(self.res - 2):
				self.probabilityMap[y+1][x+1] = ((self.probabilityMap[x+1][y] + self.probabilityMap[x][y+1] + self.probabilityMap[x+2][y+1] + self.probabilityMap[x+1][y+2]) / 2)

	def genPixMap(self):
		for x in range(self.res):
			for y in range(self.res):
				randTmp = R.random()
				if randTmp < self.probabilityMap[y][x]:
					self.pixMap[y][x] = 1
				else:
					self.pixMap[y][x] = 0
		

class WorldMap:
	worldPixMap = []
        res = 0
	world = []

	def __init__(self, x = 10, y = 10, rez = 4, water = .5):
		self.dx = x
		self.dy = y
		self.res = rez
		self.wat = water
		for x in range(self.dx):
			self.world.append([])
			for y in range(self.dy):
				self.world[x].append(Block(0,0,0,0,0,self.res))
		for x in range(self.dx * self.res):
			self.worldPixMap.append([])
			for y in range(self.dy * self.res):
				self.worldPixMap[x].append(0)
		self.generate()

	def generate(self):
		print "generating"
		for x in range(self.dx - 2):
			for y in range(self.dy - 2):
				self.world[x+1][y+1].gen(self.world[x+1][y],self.world[x][y+1], self.wat)
		self.assemble()
							
	def assemble(self):
		print "assembleing"
		for x in range(self.dx):
			for y in range(self.dy):
				for subX in range(self.res):
					for subY in range(self.res):
						self.worldPixMap[y*self.res+subY][x*self.res+subX] = self.world[y][x].pixMap[subY][subX]

	def display(self):
		for y in range(self.dx * self.res):
			print self.worldPixMap[y]
				

						
		

	
