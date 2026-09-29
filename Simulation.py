from Zones import Zone, Blocked_zone, Restricted_zone, Priority_zone, Start_zone, End_zone
from Drones import Drone
from Map import GridMap
from Algorithm import A_Star
from Scheduler import assign_path_drone, move_one_turn


def easy_linear_map():
	easy_linear_map = GridMap(min_x=0, max_x=3, min_y=0, max_y=0)
	start_base = Start_zone(0, 0, "Start", 2)
	d1 = Drone("D1", 1)
	d2 = Drone("D2", 2)
	zone1 = Zone(1, 0, "Waypoint1", 1)
	zone2 = Zone(2, 0, "Waypoint2", 1)
	end_base = End_zone(3, 0, "Goal", 2)
	easy_linear_map.add_zone(start_base)
	easy_linear_map.add_zone(zone1)
	easy_linear_map.add_zone(zone2)
	easy_linear_map.add_zone(end_base)
	start_base.connect_zones(zone1)
	zone1.connect_zones(zone2)
	zone2.connect_zones(end_base)
	start_base.enter_zone(d1)
	start_base.enter_zone(d2)
	drones = assign_path_drone(easy_linear_map)
	turn = 0
	while drones:
		turn += 1
		print(f"\n=====(turn: {turn})=====")
		movement = move_one_turn(easy_linear_map, drones)
		print(" ".join(movement))
		drones = [drone for drone in drones if drone not in end_base.drones]
		if drones and not movement:
			print("[ERRORE] - Simulazione Bloccata")
			exit(0)


def simple_fork():
	simple_fork = GridMap(min_x=0, max_x=3, min_y=-1, max_y=1)
	start_base = Start_zone(0, 0, "Start", 4)
	junction = Zone(1, 0, "Junction", 2)
	path_a = Zone(2, 1, "Path_A", 1)
	path_b = Zone(2, -1, "Path_B", 1)
	Goal = End_zone(3, 0, "Goal", 4)
	d1 = Drone("D1", 1)
	d2 = Drone("D2", 2)
	d3 = Drone("D3", 3)
	d4 = Drone("D4", 4)
	simple_fork.add_zone(start_base)
	simple_fork.add_zone(junction)
	simple_fork.add_zone(path_a)
	simple_fork.add_zone(path_b)
	simple_fork.add_zone(Goal)
	start_base.connect_zones(junction)
	junction.connect_zones(path_a)
	junction.connect_zones(path_b)
	path_a.connect_zones(Goal)
	path_b.connect_zones(Goal)
	start_base.enter_zone(d1)
	start_base.enter_zone(d2)
	start_base.enter_zone(d3)
	start_base.enter_zone(d4)
	drones = assign_path_drone(simple_fork)
	turn = 0
	while drones:
		turn += 1
		print(f"\n=====(turn: {turn})=====")
		movement = move_one_turn(simple_fork, drones)
		print(" ".join(movement))
		drones = [drone for drone in drones if drone not in Goal.drones]
		if drones and not movement:
			print("[ERRORE] - Simulazione Bloccata")
			exit(0)

print("==== MAP2 - Easy ====")
simple_fork()

