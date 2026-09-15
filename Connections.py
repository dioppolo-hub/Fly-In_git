from typing import Any
from Zones import Zone

class Connection():
	def __init__(
		self,
		x: int,
		y: int,
		zone_a: Zone,
		zone_b: Zone,
	):
		self.zone_a = zone_a
		self.zone_b = zone_b
		self.x, self.y = x, y
		self.capacity = 1
		self.bidirectional = True
		self.waiting_drones = []

	def get_conn_pos(self):
		return (self.x, self.y)
