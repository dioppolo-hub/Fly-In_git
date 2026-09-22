# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Algorithm.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dioppolo <dioppolo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/21 15:16:35 by dioppolo          #+#    #+#              #
#    Updated: 2026/09/22 11:58:40 by dioppolo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Drones import Drone
from Map import GridMap
from Zones import Zone
from Connections import Connection
from typing import Any

def Algoritm(linear_map: GridMap):
	zones = linear_map.get_all_zones()
	Start = linear_map.get_start_zone()
	End = linear_map.get_end_zone()
	open = set()
	close = set()
	path: dict = {}
	open.add(Start)
	curr: Zone = Start
	g_score = {
			linear_map.cell_pos(row, nodo): float('inf')
			for row in range(linear_map.width)
			for nodo in range(linear_map.height)
		}
	g_score[Start] = 0
	f_score = {
				linear_map.cell_pos(row, nodo): float('inf')
				for row in range(linear_map.width)
				for nodo in range(linear_map.height)
			}
	f_score[Start] = Calculate_cost(Start, End, g_score[Start])
	while open:
		print("coming soon")
		break

def find_lowest(open: set, fcost: dict):
	best_zone: Any = None
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

def get_neighbours(zone: Zone, map: GridMap):
	neighbours = []
	directions = [(0, -1, 'N'), (1, 0, 'E'), (0, 1, 'S'), (-1, 0, 'W')]
	for dx, dy, dir in directions:
		x = zone.x + dx
		y = zone.y + dy
		if 0 <= x <= map.width and 0 <= y <= map.height:
			neighbour = map.get_zone(x, y)
			neighbours.append((neighbour, dir))
	return neighbours
