# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Scheduler.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dioppolo <dioppolo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/23 13:52:39 by dioppolo          #+#    #+#              #
#    Updated: 2026/09/23 16:15:58 by dioppolo         ###   ########.fr        #
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
	drones = []
	for zone in zones:
		drones += zone.get_drones()
	for d in drones:
		d.path = A_Star(map)
	return drones

def move_one_turn(map: GridMap, drones: list[Drone]) -> None:
	planned_moves = []
	reserved_zones = set()
	for drone in drones:
		if not drone.path:
			continue
		current_zone = None
		for zone in map.get_all_zones():
			if drone in zone.drones:
				current_zone = zone
				break
		if current_zone is None:
			continue
		next_zone = drone.path[0]
		if next_zone in reserved_zones:
			continue
		if next_zone.is_blocked:
			continue
		if next_zone.is_zone_full():
			continue
		reserved_zones.add(next_zone)
		planned_moves.append((drone, current_zone, next_zone))
	for drone, current_zone, next_zone in planned_moves:
		current_zone.leave_zone(drone)
		next_zone.enter_zone(drone)
		drone.path.pop(0)
		if not drone.path:
			drone.status = "idle"
		else:
			drone.status = "moving"
