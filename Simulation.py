from Zones import Zone, Blocked_zone, Restricted_zone, Priority_zone, Start_zone, End_zone
from Drones import Drone
from Map import GridMap
from Algorithm import A_Star
from Scheduler import assign_path_drone


def test():
	easy_linear_map = GridMap(3, 0)

	start_base = Start_zone(0, 0, "Start")
	d1 = Drone("D1", 1)
	d2 = Drone("D2", 2)
	zone1 = Zone(1, 0, "Waypoint1")
	zone2 = Zone(2, 0, "Waypoint2")
	end_base = End_zone(3, 0, "Goal")
	easy_linear_map.add_zone(start_base)
	easy_linear_map.add_zone(zone1)
	easy_linear_map.add_zone(zone2)
	easy_linear_map.add_zone(end_base)
	start_base.connect_zones(zone1)
	zone1.connect_zones(zone2)
	zone2.connect_zones(end_base)
	start_base.enter_zone(d1)
	start_base.enter_zone(d2)
	assign_path_drone(easy_linear_map)
	


test()
