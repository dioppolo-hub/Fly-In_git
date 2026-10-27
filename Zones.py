from typing import Any


class Zone():
	def __init__(self, name: str, x: int, y: int):
		self.name = name
		self.capacity: float = 1.0
		self.x, self.y = x, y
		self.cost: float = 1.0
		self.color = "blue"
		self.is_blocked = False
		self.neighbours: set = set()
		self.drones: list = []
		self.connections: dict = {}

	def get_zone_name(self) -> str:
		return self.name

	def add_connection(self, connection: Any) -> bool:
		if connection.zone_a is self:
			other_zone = connection.zone_b
		elif connection.zone_b is self:
			other_zone = connection.zone_a
		else:
			return False
		self.connections[other_zone] = connection
		return True

	def is_zone_full(self) -> bool:
		capacity = float(self.capacity)
		if capacity == float('inf'):
			capacity = 100000000
		if len(self.drones) >= int(capacity):
			return True
		else:
			return False

	def can_enter_zone(self) -> bool:
		if not self.is_blocked and not self.is_zone_full():
			return True
		else:
			return False

	def enter_zone(self, drone: Any) -> bool:
		if not self.can_enter_zone():
			return False
		self.drones.append(drone)
		drone.x = self.x
		drone.y = self.y
		return True

	def leave_zone(self, drone: Any) -> bool:
		if not drone in self.drones:
			return False
		self.drones.remove(drone)
		return True

	def connect_zones(self, other_zone: Any, bidirectional: bool=True) -> bool:
		if other_zone == self:
			return False
		self.neighbours.add(other_zone)
		if bidirectional:
			other_zone.neighbours.add(self)
		return True

	def is_connected_to(self, other_zone: Any) -> bool:
		if other_zone in self.neighbours:
			return True
		else:
			return False

	def get_neighbours(self) -> set:
		return self.neighbours.copy()

	def get_zone_pos(self) -> tuple:
		return (self.x, self.y)

	def get_drones(self) -> list[Any]:
		return self.drones


class Start_zone(Zone):
	def __init__(self, name: str, x: int, y: int):
		super().__init__(name, x, y)
		self.capacity = float('inf')


class End_zone(Zone):
	def __init__(self, name: str, x: int, y: int):
		super().__init__(name, x, y)
		self.capacity = float('inf')

