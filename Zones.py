from typing import Any


class Zone():
	def __init__(self, x: int, y: int):
		self.x, self.y = x, y
		self.priority = 0
		self.cost = 1
		self.is_blocked = False
		self.neighbours = set()
	
	def connect(self, other_zone, bidirectional=True):
		self.neighbours.add(other_zone)
		if bidirectional:
			other_zone.neighbours.add(self)
	
	def disconnect(self, other_zone, bidirectional=True):
		self.neighbours.discard(other_zone)
		if bidirectional:
			other_zone.neighbours.discard(self)


class Restricted_zone(Zone):
	def __init__(self, x: int, y: int):
		super().__init__(x, y)
		self.cost = 2


class Priority_zone(Zone):
	def __init__(self, x: int, y: int):
		super().__init__(x, y)
		self.priority = 1


class Blocked_zone(Zone):
	def __init__(self, x: int, y: int):
		super().__init__(x, y)
		self.is_blocked = True