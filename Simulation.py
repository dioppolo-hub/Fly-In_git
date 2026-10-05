from Zones import Zone, Start_zone, End_zone
from Drones import Drone
from Map import GridMap
from parcing import MapParser, Errors
from Scheduler import assign_path_drone, move_one_turn


def test():
	parced = MapParser("maps/easy/03_basic_capacity.txt")
	try:
		map = parced.parce_map()
		drones = assign_path_drone(map)
		end = map.get_end_zone()
		turn = 0
		while drones:
			turn += 1
			print(f"\n=====(turn: {turn})=====")
			movement = move_one_turn(map, drones)
			print(" ".join(movement))
			drones = [drone for drone in drones if drone not in end.drones]
			if drones and not movement:
				print("[ERRORE] - Simulazione Bloccata")
				exit(0)
	except Errors as error:
		print(error)

test()
