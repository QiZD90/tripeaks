def minabs(a, b):
	if abs(a) < abs(b):
		return a
	return b

class Animation: # TODO: Rework this into 4 separate classes?
	STOCK_TO_WASTE = 1
	ARR_TO_WASTE = 2
	WASTE_TO_STOCK = 3
	WASTE_TO_ARR = 4

	def isFinished(self):
		if not self.active:
			return False

		return self.x == self.end_pos[0] and self.y == self.end_pos[1]

	def tick(self, dt):
		if not self.active:
			return

		self.x += minabs(self.dx * dt, self.end_pos[0] - self.x)
		self.y += minabs(self.dy * dt, self.end_pos[1] - self.y)

		if self.isFinished():
			self.active = False

	def isActive(self):
		return self.active

	def getState(self):
		if not self.active:
			return None, None

		return self.card, (self.x, self.y)

	def getType(self):
		if not self.active:
			return None

		return self.type

	def start(self, type, card, start_pos, end_pos, speed = 3):
		self.active = True
		self.type = type
		self.card = card
		self.start_pos = start_pos
		self.end_pos = end_pos
		self.x = start_pos[0]
		self.y = start_pos[1]
		self.speed = speed
		self.dx = (end_pos[0] - start_pos[0]) / 1000 * speed
		self.dy = (end_pos[1] - start_pos[1]) / 1000 * speed

	def stop(self):
		self.active = False

	def __init__(self):
		self.active = False
		

animation = Animation()