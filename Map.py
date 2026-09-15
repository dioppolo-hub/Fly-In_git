from typing import Any
from Zones import Zone


class GridMap:
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height
		self.zones = {}


	def add_zone(self, zone: Zone):
		self.zones[(zone.x, zone.y)] = zone


	def get_neighbours(self, zone: Zone, allow_diagonals=False):
		directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
		if allow_diagonals:
			directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
		neighbors = []
		for dx, dy in directions:
			target_pos = (zone.x + dx, zone.y + dy)
			if target_pos in self.zones:
				neighbor = self.zones[target_pos]
				if not neighbor.is_blocked:
					neighbor.append(neighbor)
		return neighbors