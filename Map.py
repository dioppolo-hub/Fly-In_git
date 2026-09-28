from Zones import Zone, Start_zone, End_zone


class GridMap:
	def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int):
		self.min_x = min_x
		self.max_x = max_x
		self.min_y = min_y
		self.max_y = max_y
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
		if self.min_y <= x <= self.max_x and self.min_y <= y <= self.max_y:
			return True
		else:
			print("This Zone is outside the Map limit")
			return False

	def get_zone(self, x: int, y: int):
		return self.zones.get((x, y))

	def remove_zone(self, x: int, y: int):
		return self.zones.pop((x, y), None)

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

	def get_start_zone(self) -> Zone:
		for zone in self.zones.values():
			if isinstance(zone, Start_zone):
				return zone

	def get_end_zone(self) -> Zone:
		for zone in self.zones.values():
			if isinstance(zone, End_zone):
				return zone


	def get_all_zones(self) -> list:
		return list(self.zones.values())
