from typing import Any
from Zones import Start_zone, End_zone, Zone
from Connections import Connection
from Map import GridMap


class Errors(Exception):
	pass


class MapParser():
	def __init__(self, name):
		self.name = name
		self.start_info = []
		self.conn_info = []
		self.end_info = []
		self.zone_info = []
		self.zones = []
		self.connections = []
		self.n_drones = 0

	def parce_map(self):
		start = 0
		end = 0
		phase = 0
		with open(self.name, "r") as f:
			for i, line in enumerate(f):
				if line.startswith("nb_drones:"):
					if phase != 0:
						raise Errors(f"[ERROR], nb_drones must be declared first")
					phase = 1
					self.n_drones = int(line.split(":")[1])
					if self.n_drones == 0:
						raise Errors(f"[ERROR], line {i}, nb_drones cannot be 0")
				elif line.startswith("start_hub:"):
					if phase == 0:
						raise Errors(f"[ERROR], line {i}, nb_drones must be declared before hubs")
					if phase == 2:
						raise Errors(f"[ERROR], line {i}, hubs must be declared before connections")
					start += 1
					if start > 1:
						raise Errors(f"[ERROR], line {i}, Too many Start Zones")
					self.start_info.append(line.split(":")[1])
					self.zones.append(self.parce_start_info(i))
				elif line.startswith("end_hub:"):
					if phase == 0:
						raise Errors(f"[ERROR], line {i}, nb_drones must be declared before hubs")
					if phase == 2:
						raise Errors(f"[ERROR], line {i}, hubs must be declared before connections")
					end += 1
					if end > 1:
						raise Errors(f"[ERROR], line {i}, Too many End Zones")
					self.end_info.append(line.split(":")[1])
					self.zones.append(self.parce_end_info(i))
				elif line.startswith("hub:"):
					if phase == 0:
						raise Errors(f"[ERROR], line {i}, nb_drones must be declared before hubs")
					if phase == 2:
						raise Errors(f"[ERROR], line {i}, hubs must be declared before connections")
					item = line.split(":")[1]
					self.zone_info.append(item)
					self.zones.append(self.parce_hub_info(item, i))
				elif line.startswith("connection:"):
					if phase == 0:
						raise Errors(f"[ERROR], line {i}, nb_drones must be declared first")
					phase = 2
					item = line.split(":")[1].strip()
					self.conn_info.append(item)
					self.connections.append(self.parce_conn_info(item, i))
			self.repetition_zone_name()

	def parce_conn_info(self, item: str, line: int) -> Connection:
		zones_by_names = {}
		connection_data = item.split("[", 1)
		names = connection_data[0].strip().split("-")
		if len(names) != 2:
			raise Errors(f"[ERROR], line {line}, Invalid connection")
		for zone in self.zones:
			zones_by_names[zone.name] = zone
		zone_a = zones_by_names.get(names[0])
		zone_b = zones_by_names.get(names[1])
		if zone_a is None or zone_b is None:
			raise Errors(f"[ERROR], line {line}, Connection reference to unknown hub")
		conn = Connection(zone_a, zone_b)
		if len(connection_data) > 1:
			extra = connection_data[1].split("]", 1)[0]
			for option in extra.split():
				if option.startswith("max_link_capacity="):
					try:
						conn.capacity = int(option.split("=", 1)[1])
					except ValueError:
						raise Errors(f"[ERROR], line {line}, Invalid connection capacity")
		return conn



	def parce_hub_info(self, oggetto: str, line: int) -> Zone:
		items = oggetto.split()
		if len(items) < 3:
			raise Errors(f"[ERROR], line {line}, Invalid hub")
		name = items[0]
		self.zone_name(name, line)
		try:
			x, y = int(items[1]), int(items[2])
		except ValueError:
			raise Errors(f"[ERROR], line {line}, Invalid coordinates value")
		hub = Zone(name, x, y)
		start_bracket = oggetto.find("[")
		end_bracket = oggetto.find("]", start_bracket + 1)
		if start_bracket != -1 and end_bracket != -1:
			extra = oggetto[start_bracket + 1:end_bracket]
			for option in extra.split():
				if option.startswith("color="):
					color = option.split("=", 1)[1]
					hub.color = color
				elif option.startswith("max_drones="):
					cap = option.split("=", 1)[1]
					hub.capacity = cap
				elif option.startswith("zone="):
					zone_type = option.split("=", 1)[1]
					if zone_type == "restricted":
						hub.cost = 2
					elif zone_type == "priority":
						hub.priority = 1
		return hub


	def parce_start_info(self, line) -> Start_zone:
		if not self.start_info:
			raise Errors(f"[ERRORS], line {line}, Missing start hub")
		item = self.start_info[-1].strip()
		items = item.split()
		if len(items) < 3:
			raise Errors(f"[ERRORS], line {line}, Invalid start hub")
		name = items[0]
		self.zone_name(name, line)
		try:
			x, y = int(items[1]), int(items[2])
		except ValueError:
			raise Errors(f"[ERROR], line {line}, Invalid coordinates value")
		start = Start_zone(name, x, y)
		start_bracket = item.find("[")
		end_bracket = item.find("]", start_bracket + 1)
		if start_bracket != -1 and end_bracket != -1:
			extra = item[start_bracket + 1:end_bracket]
			for i in extra.split():
				if i.startswith("color="):
					color = i.split("=", 1)[1]
					start.color = color
		return start

	def parce_end_info(self, line) -> End_zone:
		if not self.end_info:
			raise Errors(f"[ERRORS], line {line}, Missing end hub")
		item = self.end_info[-1].strip()
		items = item.split()
		if len(items) < 3:
			raise Errors(f"[ERRORS], line {line}, Invalid end hub")
		name = items[0]
		self.zone_name(name, line)
		try:
			x, y = int(items[1]), int(items[2])
		except ValueError:
			raise Errors(f"[ERROR], line {line}, Invalid coordinates value")
		end = End_zone(name, x, y)
		start_bracket = item.find("[")
		end_bracket = item.find("]", start_bracket + 1)
		if start_bracket != -1 and end_bracket != -1:
			extra = item[start_bracket + 1:end_bracket]
			for i in extra.split():
				if i.startswith("color="):
					color = i.split("=", 1)[1]
					end.color = color
		return end


	def repetition_zone_name(self) -> int:
		for z1 in self.zones:
			for z2 in self.zones[1:]:
				print(z1.name, z2.name)
				if z1.name == z2.name:
					raise Errors(f"[ERROR], Zones cannot have the same name")
		return 1

	def zone_name(self, name: str, line: int) -> bool:
		if name.find("/") != -1 or name.find(" ") != -1:
			raise Errors(f"[ERROR], line {line}, Invalid zone name")
		return True
