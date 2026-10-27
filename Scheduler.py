# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Scheduler.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dioppolo <dioppolo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/23 13:52:39 by dioppolo          #+#    #+#              #
#    Updated: 2026/10/27 12:01:31 by dioppolo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Drones import Drone
from Map import GridMap
from Zones import Zone
from Connections import Connection
from Algorithm import A_Star

def assign_path_drone(map: GridMap) -> list:
	zones = map.get_all_zones()
	Start = map.get_start_zone()
	End = map.get_end_zone()
	drones: list = []
	if Start and End:
		for zone in zones:
			drones += zone.get_drones()
		for d in drones:
			path = A_Star(map, Start, End, None)
			"""MODIFICA LO 0: CON 1: PER NON VEDERE START A TURNO 1"""
			d.path = path[1:] if path else []
	return drones

def get_connection(curr_zone: Zone, next_zone: Zone) -> Connection | None:
	return curr_zone.connections.get(next_zone)

def move_one_turn(map: GridMap, drones: list[Drone]) -> list[str]:
	zones = map.get_all_zones()
	zone_by_drone = {}
	movement = []
	"""Fotografa la posizione dei droni in transito prima dei movimenti"""
	transiting = [
		(drone, drone.current_connection, drone.transit_target)
		for drone in drones
		if drone.current_connection is not None
		and drone.transit_target is not None
	]
	"""Calcolo delle zone candidate per le nuove mosse"""
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
	"""tieni un set di zone che un drone deve evitare
	quando si cerca un percorso alternativo"""
	avoided_by_drone: dict = {drone: set() for drone, _, _ in candidates}
	blocked = set()
	"""Doppio ciclo while:
	WHILE ESTERNO: se una mossa viene rifiutata prova a ricalolare
	il percorso evitando la zona, poi ricalcola le capacita'
	WHILE INTERNO: stabilizza le mosse rispetto alle capacita',
	se una mossa viene rifiutata perche' la destinazione e' piena
	il drone non lascia la zona di partenza quindi vanno ricalcolati
	i conteggi di partenze e arrivi."""
	while True:
		accepted = [index not in blocked for index in range(len(candidates))]
		while True:
			changed = False
			connection_requests: dict = {}
			"""PER PRIORITY APPLICARE UN CRITERIO DI PRIORITA' SU CANDIDATES
				PRIMA DI SELEZIONARE QUALI DRONI RIFIUTARE E QUALI ACCETTARE"""
			for zone in zones:
				"""Conta le mosse in cui i droni vogliono entrare in una zona"""
				incoming = [
					index for index, (_, _, destination) in enumerate(candidates)
					if accepted[index] and destination is zone and destination.cost != 2
				]
				"""Conta le mosse in cui i droni voglio uscire"""
				outgoing = sum(
					1 for index, (_, source, _) in enumerate(candidates)
					if accepted[index] and source is zone
				)
				"""Conta quanti droni resterebbero oltre la capacita'
				Se overflow e' minore di 0 significa che la capacita'
				e' rispettata, se e' positivo ci sono troppi arrivi"""
				capacity = float(zone.capacity)
				transit_incoming = sum(1 for _, _, target in transiting if target is zone)
				if capacity == float('inf'):
					overflow = 0
				else:
					overflow = len(zone.drones) + len(incoming) + transit_incoming - outgoing - int(capacity)
				if overflow > 0:
					for index in reversed(incoming[-overflow:]):
						accepted[index] = False
						changed = True
			for index, (_, source, destination) in enumerate(candidates):
				if not accepted[index] or destination.cost != 2:
					continue
				conn = get_connection(source, destination)
				if conn is None:
					accepted[index] = False
					changed = True
					continue
				connection_requests.setdefault(conn, []).append(index)
			for conn, indexes in connection_requests.items():
				transit_leaving = sum(1 for _, transit_conn, _ in transiting if transit_conn is conn)
				available = max(0, int(conn.capacity) - len(conn.active_drones) + transit_leaving)
				for index in reversed(indexes[available:]):
					accepted[index] = False
					changed = True
			if not changed:
				break
		rejected = [
			index for index, is_accepted in enumerate(accepted)
			if not is_accepted and index not in blocked
		]
		if not rejected:
			break
		rerouted = False
		for index in rejected:
			drone, curr_zone, rejected_zone = candidates[index]
			avoided_by_drone[drone].add(rejected_zone)
			end_zone = map.get_end_zone()
			if end_zone:
				new_path = A_Star(map, curr_zone, end_zone, avoided_by_drone[drone])
			if len(new_path) > 1:
				drone.path = new_path[1:]
				candidates[index] = (drone, curr_zone, new_path[1])
				rerouted = True
		if rerouted:
			continue
		blocked.update(rejected)
	selected_moves = [
		candidates[index]
		for index, is_accepted in enumerate(accepted)
		if is_accepted
	]
	"""GESTIONE MOSSE"""
	normal_moves = []
	restricted_moves = []
	for drone, curr_zone, next_zone in selected_moves:
		if next_zone.cost == 2:
			restricted_moves.append((drone, curr_zone, next_zone))
		else:
			normal_moves.append((drone, curr_zone, next_zone))

	for drone, curr_zone, _ in normal_moves:
		curr_zone.leave_zone(drone)

	for drone, conn, target in transiting:
		if not target.enter_zone(drone):
			continue
		conn.leave_conn(drone)
		drone.current_connection = None
		drone.transit_target = None
		drone.path.pop(0)
		drone.status = "moving" if drone.path else "idle"
		movement.append(f"D{drone.drone_id}-{target.name}")

	for drone, curr_zone, next_zone in restricted_moves:
		conn = get_connection(curr_zone, next_zone)
		if conn is not None and conn.enter_conn(drone):
			curr_zone.leave_zone(drone)
			drone.current_connection = conn
			drone.transit_target = next_zone
			movement.append(f"D{drone.drone_id}-{conn.zone_a.name}-{conn.zone_b.name}")

	for drone, curr_zone, next_zone in normal_moves:
		if next_zone.enter_zone(drone):
			drone.path.pop(0)
			drone.status = "moving" if drone.path else "idle"
			movement.append(f"D{drone.drone_id}-{next_zone.name}")
	return sorted(movement)
