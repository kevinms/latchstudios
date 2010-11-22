

class WorldMap:
	def __init__(self, dX, dY, screenLocX, screenLocY):
		self.sizeX = dX
		self.sizeY = dY
		self.view = ViewPort(10, 10)
		
		




class ViewPort:
	locX = 10
	locY = 10
	def __init__(self,X, Y):
		self.locX = X
		self.locY = Y
		self.sizeX = 640
		self.sizeY = 480
