# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Scheduler.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dioppolo <dioppolo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/23 13:52:39 by dioppolo          #+#    #+#              #
#    Updated: 2026/09/29 11:09:00 by dioppolo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Drones import Drone
from Map import GridMap
from Zones import Zone
from Connections import Connection
from typing import Any
from Algorithm import A_Star

def assign_path_drone(map: GridMap) -> list:
	zones = map.get_all_zones()
	Start = map.get_start_zone()
	End = map.get_end_zone()
	drones = []
	for zone in zones:
		drones += zone.get_drones()
	for d in drones:
		path = A_Star(map, Start, End, None)
		"""MODIFICA LO 0: CON 1: PER NON VEDERE START A TURNO 1"""
		d.path = path[1:] if path else []
	return drones

def move_one_turn(map: GridMap, drones: list[Drone]) -> list[str]:
	zones = map.get_all_zones()
	zone_by_drone = {}
	for zone in zones:
		for drone in zone.drones:
			zone_by_drone[drone] = zone
	candidates = []
	for drone in drones:
		if not drone.path:
			continue
		curr_zone = zone_by_drone.get(drone)
		if curr_zone is None:
			continue
		next_zone = drone.path[0]
		if next_zone.is_blocked:
			print("\nGestire zone bloccate\n")
			continue
		candidates.append((drone, curr_zone, next_zone))
	accepted = [True] * len(candidates)
	"""Calcolo delle mosse possibili affiancate da una lista che
	determina se le mosse si possono fare"""
	while True:
		changed = False
		for zone in zones:
			"""Conta le mosse in cui i droni vogliono entrare in una zona"""
			incoming = [
				index for index, (_, _, destination) in enumerate(candidates)
				if accepted[index] and destination is zone
			]
			"""Conta le mosse in cui i droni voglio uscire"""
			outgoing = sum(
				1 for index, (_, source, _) in enumerate(candidates)
				if accepted[index] and source is zone
			)
			"""Conta quanti droni resterebbero oltre la capacita'
			Se overflow e' minore di 0 significa che la capacita'
			e' rispettata, se e' positivo ci sono troppi arrivi"""
			overflow = len(zone.drones) + len(incoming) - outgoing - zone.capacity
			if overflow > 0:
				for index in reversed(incoming[-overflow:]):
					accepted[index] = False
					changed = True
		if not changed:
			break
	"""Ricalcolo del path in caso di strada chiusa"""
	end_zone = map.get_end_zone()
	avoided_zones = {
		dest for index, (_, _, dest) in enumerate(candidates)
		if not accepted[index]
	}
	for index, (drone, curr_zone, _) in enumerate(candidates):
		if accepted[index]:
			continue
		new_path = A_Star(map, curr_zone, end_zone, avoided_zones)
		if new_path:
			drone.path = new_path[1:]
	"""Spostamento dei droni"""
	selected_moves = [
		candidate for index, candidate in enumerate(candidates)
		if accepted[index]
	]
	for drone, curr_zone, _ in selected_moves:
		curr_zone.leave_zone(drone)
	for drone, _, next_zone in selected_moves:
		next_zone.enter_zone(drone)
		drone.path.pop(0)
		drone.status = "moving" if drone.path else "idle"
	return [f"D{drone.drone_id}-{next_zone.name}"
			for drone, _, next_zone in selected_moves
		]
