from typing import Any


class Zone():
	def __init__(self, x: int, y: int, name: str):
		self.name = name
		self.capacity = 1
		self.x, self.y = x, y
		self.priority = 0
		self.cost = 1
		self.is_blocked = False
		self.neighbours = set()
		self.drones = []

	def get_zone_name(self) -> str:
		return self.name

	def is_zone_full(self) -> bool:
		if len(self.drones) >= self.capacity:
			return True
		else:
			return False

	def can_enter_zone(self) -> bool:
		if not self.is_blocked and not self.is_zone_full():
			return True
		else:
			return False

	def enter_zone(self, drone) -> bool:
		if not self.can_enter_zone():
			return False
		self.drones.append(drone)
		drone.x = self.x
		drone.y = self.y
		return True

	def leave_zone(self, drone) -> bool:
		if not drone in self.drones:
			return False
		self.drones.remove(drone)
		return True

	def connect_zones(self, other_zone, bidirectional=True) -> bool:
		if other_zone == self:
			return False
		self.neighbours.add(other_zone)
		if bidirectional:
			other_zone.neighbours.add(self)
		return True
	
	def disconnect_zones(self, other_zone, bidirectional=True) -> bool:
		if other_zone == self:
			return False
		self.neighbours.discard(other_zone)
		if bidirectional:
			other_zone.neighbours.discard(self)
		return True

	def is_connected_to(self, other_zone) -> bool:
		if other_zone in self.neighbours:
			return True
		else:
			return False

	def get_active_drones_zone(self):
		return len(self.drones)

	def get_neighbours(self) -> set:
		return self.neighbours.copy()

	def get_zone_pos(self) -> tuple:
		return (self.x, self.y)

	def get_drones(self):
		return self.drones


class Start_zone(Zone):
	def __init__(self, x: int, y: int, name: str):
		super().__init__(x, y, name)
		self.capacity = 25


class End_zone(Zone):
	def __init__(self, x: int, y: int, name: str):
		super().__init__(x, y, name)
		self.capacity = 25


class Restricted_zone(Zone):
	def __init__(self, x: int, y: int, name: str):
		super().__init__(x, y, name)
		self.cost = 2


class Priority_zone(Zone):
	def __init__(self, x: int, y: int, name: str):
		super().__init__(x, y, name)
		self.priority = 1


class Blocked_zone(Zone):
	def __init__(self, x: int, y: int, name: str):
		super().__init__(x, y, name)
		self.is_blocked = True
