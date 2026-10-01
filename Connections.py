from typing import Any
from Zones import Zone
from Drones import Drone

class Connection():
	def __init__(
		self,
		zone_a: Zone,
		zone_b: Zone
	):
		self.zone_a = zone_a
		self.zone_b = zone_b
		self.capacity = 1
		self.bidirectional = True
		self.waiting_drones = []
		self.active_drones = []
		zone_a.add_connection(self)
		zone_b.add_connection(self)

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
		return not self.is_conn_full() and drone not in self.active_drones

	def enter_conn(self, drone) -> bool:
		if not self.can_enter_conn(drone):
			return False
		self.active_drones.append(drone)
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
