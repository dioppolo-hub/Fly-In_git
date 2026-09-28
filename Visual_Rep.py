from Drones import Drone
from Map import GridMap
from Zones import (
	Blocked_zone,
	End_zone,
	Priority_zone,
	Restricted_zone,
	Start_zone,
)

def print_movement(map: GridMap, drones: list[Drone]):
	output = {}
	zones = map.get_all_zones()
	for z in zones:
		if isinstance(z, Start_zone):
			output[z.get_zone_pos()] = "S"
		elif isinstance(z, End_zone):
			output[z.get_zone_pos()] = "E"
		elif isinstance(z, Blocked_zone):
			output[z.get_zone_pos()] = "B"
		elif isinstance(z, Restricted_zone):
			output[z.get_zone_pos()] = "R"
		elif isinstance(z, Priority_zone):
			output[z.get_zone_pos()] = "P"
		else:
			output[z.get_zone_pos()] = z.name
	drones_by_position = {}
	for drone in drones:
		position = drone.get_drone_pos()
		drones_by_position.setdefault(position, []).append(drone.name)
	for position, names in drones_by_position.items():
		if position in output:
			output[position] = "/".join(names)
	width = abs(map.min_x) + abs(map.max_x)
	height = abs(map.min_y) + abs(map.max_y)
	cell_width = max(
		4,
		max((len(label) for label in output.values()), default=1),
		len(str(width)),
	)
	for y in range(height, -1, -1):
		row = []
		for x in range(width + 1):
			label = output.get((x, y), ".")
			row.append(f"{label:^{cell_width}}")
	print(" | ".join(row))
