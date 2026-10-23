from Zones import Zone, Start_zone, End_zone
from Drones import Drone
from Map import GridMap
from parcing import MapParser, Errors
from Scheduler import assign_path_drone
from Visual_Rep import Graphic


def test():
	parced = MapParser("maps/hard/01_maze_nightmare.txt")
	try:
		map = parced.parce_map()
		drones = assign_path_drone(map)
		end = map.get_end_zone()
		turn = 0
		test = Graphic()
		while drones:
			turn += 1
			test.visual_rep(map, turn, drones)
			print(f"\n=====(turn: {turn})=====")
			drones = [drone for drone in drones if drone not in end.drones]
	except Errors as error:
		print(error)

test()
