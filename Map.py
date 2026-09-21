from typing import Any
from Zones import Zone


class GridMap:
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height
		self.zones = {}

	def add_zone(self, zone: Zone):
		position = zone.get_zone_pos()
		if not self.is_inside(position):
			return False
		if position in self.zones:
			return False
		self.zones[position] = zone
		return True

	def is_inside(self, position: tuple):
		x, y = position
		if 0 <= x < self.width and 0 <= y < self.height:
			return True
		else:
			return False

	def get_zone(self, x: int, y: int):
		return self.zone.get((x, y))

	def remove_zone(self, x: int, y: int):
		return self.zone.pop((x, y), None)

	def get_neighbours(self, zone: Zone, allow_diagonals=False):
		directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
		if allow_diagonals:
			directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
		neighbours = []
		for dx, dy in directions:
			neighbour = self.get_zone(zone.x + dx, zone.y + dy)
			if neighbour is not None and not neighbour.is_blocked:
				neighbours.append(neighbour)
		return neighbours

	def get_all_zones(self) -> list:
		return list(self.zones.values())
