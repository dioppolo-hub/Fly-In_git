from Zones import Zone, Start_zone, End_zone
from Drones import Drone
from Map import GridMap
from parcing import MapParser, Errors
from Scheduler import assign_path_drone
from Visual_Rep import Graphic
from Menu import menu


def main():
	chosen_map = menu()
	parced = MapParser(f"maps/{chosen_map}")
	try:
		map = parced.parce_map()
		drones = assign_path_drone(map)
		end = map.get_end_zone()
		turn = 0
		test = Graphic()
		while drones:
			test.visual_rep(map, turn, drones)
			drones = [drone for drone in drones if drone not in end.drones]
	except Errors as error:
		print(error)

main()
