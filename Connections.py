from typing import Any
from Zones import Zone
from Drones import Drone

class Connection():
	def __init__(
		self,
		x: int,
		y: int,
		zone_a: Zone,
		zone_b: Zone,
		name: str
	):
		self.zone_a = zone_a
		self.zone_b = zone_b
		self.name = name
		self.x, self.y = x, y
		self.capacity = 1
		self.bidirectional = True
		self.waiting_drones = []
		self.active_drones = []

	def get_conn_pos(self) -> tuple:
		return (self.x, self.y)

	def get_other_zone(self, zone) -> Zone:
		if zone == self.zone_a:
			return self.zone_b
		elif zone == self.zone_b:
			return self.zone_a
		raise ValueError("This zone does not belong to this connections")

	def is_conn_full(self) -> bool:
		if len(self.active_drones) >= self.capacity:
			return True
		else:
			return False

	def can_enter_conn(self, drone) -> bool:
		if self.is_conn_full() or drone not in self.active_drones:
			return True
		else:
			return False

	def enter_conn(self, drone) -> bool:
		if not self.can_enter_conn(drone):
			return False
		self.active_drones.append(drone)
		drone.x = self.x
		drone.y = self.y
		return True

	def leave_conn(self, drone) -> bool:
		if not drone in self.active_drones:
			return False
		self.active_drones.remove(drone)
		return True

	def add_to_queue(self, drone) -> None:
		if drone not in self.waiting_drones:
			self.waiting_drones.append(drone)
		return None

	def get_first_waiting_drone(self) -> None | Drone:
		if self.is_conn_full() or not self.waiting_drones:
			return None
		drone = self.waiting_drones.pop(0)
		self.active_drones.append(drone)
		return drone

	def is_blocked(self, zone) -> bool:
		next_zone = self.get_other_zone(zone)
		if next_zone.is_blocked:
			return True
		else:
			return False

	def get_active_drones_conn(self) -> int:
		return len(self.active_drones)
