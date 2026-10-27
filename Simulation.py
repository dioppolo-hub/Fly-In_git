from Zones import End_zone
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
		map: GridMap = parced.parce_map()
		drones: list[Drone] = assign_path_drone(map)
		end: End_zone = map.get_end_zone()
		turn: int = 0
		test = Graphic()
		while drones:
			test.visual_rep(map, turn, drones)
			drones = [drone for drone in drones if drone not in end.drones]
	except Errors as error:
		print(error)

main()
