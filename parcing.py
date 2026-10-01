from typing import Any
from Zones import Start_zone, End_zone, Zone
from Map import GridMap


class Errors(Exception):
	pass


class MapParser():
	def __init__(self, name):
		self.name = name
		self.error = []
		self.start_info = []
		self.conn_info = []
		self.end_info = []
		self.zone_info = []
		self.n_drones = 0

	def parce_map(self):
		start = 0
		end = 0
		nb_drone_index = None
		with open(self.name, "r") as f:
			for i, line in enumerate(f):
				print(f"{i}", line)
				if line.startswith("nb_drones:"):
					nb_drone_index = i
					self.n_drones = int(line.split(":")[1])
					if self.n_drones == 0:
						raise Errors(f"[ERROR], line {i}, nb_drones cannot be 0")
				elif line.startswith("start_hub:"):
					if not nb_drone_index or i < nb_drone_index:
						raise Errors(
							f"[ERROR], line {i}, "
							"Hub is before nb_drones declaration"
							)
					start += 1
					self.start_info.append(line.split(":")[1])
				elif line.startswith("end_hub:"):
					end += 1
					self.end_info.append(line.split(":")[1])
				elif line.startswith("hub:"):
					self.zone_info.append(line.split(":")[1])
				elif line.startswith("connection:"):
					self.conn_info.append(line.split(":")[1])
	


	def repetition_zone_name(self, zone_list: list) -> int:
		try:
			i = 0
			for z1 in zone_list:
				for z2 in zone_list:
					if z1 == z2:
						i += 1
					if i > 1:
						raise Errors
			return 1
		except Errors:
			self.error.append(f"{i} zones with same name")
			return 0

	def zone_name(self, zone_list: list) -> int:
		try:
			for zone in zone_list:
				if zone.find("/") or zone.find(" "):
					raise Errors
			return 1
		except Errors:
			self.error.append(f"{zone} contains invalid char")
			return 0

	def start_zone_num(self, zone_list: list):
		try:
			i = 0
			for zone in zone_list:
				if isinstance(zone, Start_zone):
					i += 1
			if i > 1:
				raise Errors
			else:
				return 1
		except Errors:
			self.error.append("Too many Start Zones")

	def end_zone_num(self, zone_list: list):
		try:
			i = 0
			for zone in zone_list:
				if isinstance(zone, End_zone):
					i += 1
			if i > 1:
				raise Errors
			else:
				return 1
		except Errors:
			self.error.append("Too many End Zones")
