# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Scheduler.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dioppolo <dioppolo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/23 13:52:39 by dioppolo          #+#    #+#              #
#    Updated: 2026/09/23 14:41:47 by dioppolo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Drones import Drone
from Map import GridMap
from Zones import Zone
from Connections import Connection
from typing import Any
from Algorithm import A_Star

def assign_path_drone(map: GridMap):
	zones = map.get_all_zones()
	drones = []
	for zone in zones:
		drones += zone.get_drones()
	for d in drones:
		d.path = A_Star(map)