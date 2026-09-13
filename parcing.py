from typing import Any


class Errors(Exception):
	pass


def repetition_zone_name(zone_list: list, error: list) -> int:
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
		error.append(f"{i} zones with same name")
		return 0

def zone_name(zone_list: list, error: list) -> int:
	try:
		for zone in zone_list:
			if zone.find("/") or zone.find(" "):
				raise Errors
		return 1
	except:
		error.append(f"{zone} contains invalid char")
		return 0

