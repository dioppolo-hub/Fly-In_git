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
		self.capacity: float = 1.0
		self.bidirectional = True
		self.waiting_drones: list = []
		self.active_drones: list = []
		zone_a.add_connection(self)
		zone_b.add_connection(self)

	def get_other_zone(self, zone: Zone) -> Zone:
		if zone == self.zone_a:
			return self.zone_b
		elif zone == self.zone_b:
			return self.zone_a
		raise ValueError("This zone does not belong to this connections")

	def is_conn_full(self) -> bool:
		if len(self.active_drones) >= int(self.capacity):
			return True
		else:
			return False

	def can_enter_conn(self, drone: Drone) -> bool:
		return not self.is_conn_full() and drone not in self.active_drones

	def enter_conn(self, drone: Drone) -> bool:
		if not self.can_enter_conn(drone):
			return False
		self.active_drones.append(drone)
		return True

	def leave_conn(self, drone: Drone) -> bool:
		if not drone in self.active_drones:
			return False
		self.active_drones.remove(drone)
		return True
