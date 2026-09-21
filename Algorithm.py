# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Algorithm.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dioppolo <dioppolo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/21 15:16:35 by dioppolo          #+#    #+#              #
#    Updated: 2026/09/21 15:59:20 by dioppolo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Drones import Drone
from Zones import Zone
from Connections import Connection

def get_neighbours(self, zone: Zone, allow_diagonals=False):
	directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
	if allow_diagonals:
		directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
	neighbors = []
	for dx, dy in directions:
		target_pos = (zone.x + dx, zone.y + dy)
		if target_pos in self.zones:
			neighbor = self.zones[target_pos]
			if not neighbor.is_blocked:
				neighbor.append(neighbor)
	return neighbors