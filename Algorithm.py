# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Algorithm.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dioppolo <dioppolo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/21 15:16:35 by dioppolo          #+#    #+#              #
#    Updated: 2026/09/23 14:37:30 by dioppolo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Drones import Drone
from Map import GridMap
from Zones import Zone
from Connections import Connection
from typing import Any

def A_Star(map: GridMap):
	Start = map.get_start_zone()
	End = map.get_end_zone()
	if Start is None or End is None:
		return []
	open = {Start}
	path: dict = {}
	g_score = {
			zone: float("inf")
			for zone in map.get_all_zones()
		}
	f_score = {
				zone: float("inf")
				for zone in map.get_all_zones()
			}
	g_score[Start] = 0
	f_score[Start] = Calculate_cost(Start, End, g_score[Start])
	while open:
		curr = find_lowest(open, f_score)
		if curr == End:
			return build_path(path, Start, End)
		open.remove(curr)
		for neighbour in curr.get_neighbours():
			if neighbour.is_blocked:
				continue
			temp_g = g_score[curr] + neighbour.cost
			if temp_g < g_score[neighbour]:
				path[neighbour] = curr
				g_score[neighbour] = temp_g
				f_score[neighbour] = Calculate_cost(neighbour, End, temp_g)
				open.add(neighbour)
	return []

def build_path(path: dict, start: Zone, end: Zone) -> list:
	curr: Zone = end
	final_path: list = []
	while curr != start:
		final_path.append(curr)
		curr = path[curr]
	final_path.append(start)
	final_path.reverse()
	return final_path

def find_lowest(open: set, fcost: dict) -> Zone:
	best_zone: Zone = None
	best_f = float('inf')
	for zone in open:
		f = fcost[zone]
		if f < best_f:
			best_f = f
			best_zone = zone
	return best_zone

def Calculate_cost(zone: Zone, end: Zone, gcost: float) -> float:
	x, y = zone.x, zone.y
	ex, ey = end.x, end.y
	hcost = abs(ex - x) + abs(ey - y)
	fcost = gcost + hcost
	return fcost
