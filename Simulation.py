from Zones import Zone, Blocked_zone, Restricted_zone, Priority_zone
from Drones import Drone
from Map import GridMap


def test():
	start_base = Zone(0, 0, "Start")
	rest_zone = Restricted_zone(0, 1, "Area Restricted")
	prio_zone = Priority_zone(1, 0, "Area Pryority")
	block_zone = Blocked_zone(1, 1, "Wall")
	end_zone = Zone(2, 0, "End")
	start_base.connect_zones(rest_zone)
	start_base.connect_zones(prio_zone)
	start_base.connect_zones(block_zone)
	rest_zone.connect_zones(end_zone)
	prio_zone.connect_zones(end_zone)
	block_zone.connect_zones(end_zone)
	print(f"Zona: {start_base.name}, Posizione: {start_base.get_zone_pos()}, Costo: {start_base.cost}")
	print(f"Zona: {rest_zone.name}, Costo: {rest_zone.cost}")
	print(f"Zona: {prio_zone.name}, Priorità: {prio_zone.priority}")
	print(f"Zona: {block_zone.name}, Bloccata: {block_zone.is_blocked}")


test()
