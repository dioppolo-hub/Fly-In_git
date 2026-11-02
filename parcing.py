from Drones import Drone
from Zones import Start_zone, End_zone, Zone
from Connections import Connection
from Map import GridMap


class Errors(Exception):
    pass


class MapParser():
    def __init__(self, name: str):
        self.name = name
        self.start_info: list[str] = []
        self.conn_info: list[str] = []
        self.end_info: list[str] = []
        self.zone_info: list[str] = []
        self.zones: list[Zone] = []
        self.connections: list[Connection] = []
        self.n_drones = 0

    def parce_map(self) -> GridMap:
        start = 0
        end = 0
        phase = 0
        col: list[str] = [
            "black", "blue", "brown",
            "cyan", "crimson", "darkred",
            "gold", "green", "lime",
            "magenta", "maroon", "orange",
            "purple", "rainbow", "red",
            "violet", "yellow"
            ]
        with open(self.name, "r") as f:
            for i, line in enumerate(f, start=1):
                if line.startswith("nb_drones:"):
                    if phase != 0:
                        raise Errors(
                            "[ERROR], nb_drones must be declared first"
                            )
                    phase = 1
                    self.n_drones = int(line.split(":")[1])
                    if self.n_drones <= 0:
                        raise Errors(
                            f"[ERROR], line {i}, nb_drones cannot be 0 or less"
                            )
                elif line.startswith("start_hub:"):
                    if phase == 0:
                        raise Errors(
                            f"[ERROR], line {i}, nb_drones must be"
                            "declared before hubs"
                            )
                    if phase == 2:
                        raise Errors(
                            f"[ERROR], line {i}, hubs must"
                            "be declared before connections"
                            )
                    start += 1
                    if start > 1:
                        raise Errors(
                            f"[ERROR], line {i}, Too many Start Zones"
                            )
                    self.start_info.append(line.split(":")[1])
                    self.zones.append(self.parce_start_info(i, col))
                elif line.startswith("end_hub:"):
                    if phase == 0:
                        raise Errors(
                            f"[ERROR], line {i}, nb_drones must"
                            "be declared before hubs"
                            )
                    if phase == 2:
                        raise Errors(
                            f"[ERROR], line {i}, hubs must be"
                            "declared before connections"
                            )
                    end += 1
                    if end > 1:
                        raise Errors(f"[ERROR], line {i}, Too many End Zones")
                    self.end_info.append(line.split(":")[1])
                    self.zones.append(self.parce_end_info(i, col))
                elif line.startswith("hub:"):
                    if phase == 0:
                        raise Errors(
                            f"[ERROR], line {i}, nb_drones must be"
                            "declared before hubs"
                            )
                    if phase == 2:
                        raise Errors(
                            f"[ERROR], line {i}, hubs must be"
                            "declared before connections"
                            )
                    item = line.split(":")[1]
                    self.zone_info.append(item)
                    self.zones.append(self.parce_hub_info(item, i, col))
                elif line.startswith("connection:"):
                    if phase == 0:
                        raise Errors(
                            f"[ERROR], line {i}, nb_drones must be"
                            "declared first"
                            )
                    phase = 2
                    item = line.split(":")[1].strip()
                    self.conn_info.append(item)
                    self.connections.append(self.parce_conn_info(item, i))
            self.check_same_cords_zone()
            map = self.create_map()
        return map

    def parce_conn_info(self, item: str, line: int) -> Connection:
        zones_by_names = {}
        connection_data = item.split("[", 1)
        names = connection_data[0].strip().split("-")
        self.check_dup_conn(names, line)
        if len(names) != 2:
            raise Errors(f"[ERROR], line {line}, Invalid connection")
        for zone in self.zones:
            zones_by_names[zone.name] = zone
        zone_a = zones_by_names.get(names[0])
        zone_b = zones_by_names.get(names[1])
        if zone_a is None or zone_b is None:
            raise Errors(
                f"[ERROR], line {line}, Connection reference"
                "to unknown hub"
                )
        conn = Connection(zone_a, zone_b)
        conn.conn_name = str(names[0]) + "-" + str(names[1])
        if len(connection_data) > 1:
            extra = connection_data[1].split("]", 1)[0]
            for option in extra.split():
                if option.startswith("max_link_capacity="):
                    try:
                        cap = int(option.split("=", 1)[1])
                    except ValueError:
                        raise Errors(
                            f"[ERROR], line {line},"
                            "Invalid connection capacity"
                            )
                    if cap <= 0:
                        raise Errors(
                            f"[ERROR], line {line}, max_link_capacity"
                            " must be a positive integer"
                        )
                    conn.capacity = cap
                else:
                    raise Errors(
                        f"[ERROR], line {line}, metadata block unknown or "
                        "syntactically invalid"
                    )
        return conn

    def parce_hub_info(
            self,
            oggetto: str,
            line: int,
            colors:
            list[str]
            ) -> Zone:
        items = oggetto.split()
        if len(items) < 3:
            raise Errors(f"[ERROR], line {line}, Invalid hub")
        name = items[0]
        self.repetition_zone_name(name, line)
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
                    if color not in colors:
                        raise Errors(
                            f"[ERROR], line {line}, metadata color"
                            " must be syntactically valid"
                            )
                    hub.color = color
                elif option.startswith("max_drones="):
                    cap = option.split("=", 1)[1]
                    if int(cap) <= 0:
                        raise Errors(
                            f"[ERROR], line {line}, Zone capacity"
                            " must be a positive integer"
                        )
                    hub.capacity = float(cap)
                elif option.startswith("zone="):
                    zone_type = option.split("=", 1)[1]
                    if zone_type == "restricted":
                        hub.cost = 2.0
                    elif zone_type == "priority":
                        hub.cost = 0.9
                    else:
                        raise Errors(
                            f"[ERROR], line {line}, metadata zone type"
                            " must be syntactically correct"
                        )
                else:
                    raise Errors(
                        f"[ERROR], line {line}, metadata block"
                        " must be syntactically correct"
                    )
        return hub

    def parce_start_info(self, line: int, colors: list[str]) -> Start_zone:
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
                    if color not in colors:
                        raise Errors(
                            f"[ERROR], line {line}, metadata color"
                            " must be syntactically valid"
                            )
                    start.color = color
                else:
                    continue
        return start

    def parce_end_info(self, line: int, colors: list[str]) -> End_zone:
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
                    if color not in colors:
                        raise Errors(
                            f"[ERROR], line {line}, metadata color"
                            " must be syntactically valid"
                            )
                    end.color = color
        return end

    def repetition_zone_name(self, name: str, line: int) -> None:
        for z in self.zones:
            count = 1
            if z.name == name:
                count += 1
            if count > 1:
                raise Errors(
                    f"[ERROR], line {line}, "
                    "Multiple Zones with same name"
                    )

    def check_dup_conn(self, names: list[str], line: int) -> None:
        rev_conn_name = str(names[1]) + "-" + str(names[0])
        conn_name = str(names[0]) + "-" + str(names[1])
        for conn in self.connections:
            count = 1
            if conn.conn_name == conn_name or conn.conn_name == rev_conn_name:
                count += 1
            if count > 1:
                raise Errors(
                    f"[ERROR], line {line}, "
                    "Same connection appear more than once"
                    )

    def zone_name(self, name: str, line: int) -> bool:
        if name.find("/") != -1 or name.find(" ") != -1:
            raise Errors(f"[ERROR], line {line}, Invalid zone name")
        return True

    def check_same_cords_zone(self) -> None:
        for z in self.zones:
            count = 0
            for i in self.zones:
                if z.x == i.x and z.y == i.y:
                    count += 1
                    if count > 1:
                        raise Errors(
                            "[ERROR], Multiple zones"
                            "with same coordinates"
                            )

    def create_map(self) -> GridMap:
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        for z in self.zones:
            if z.x < min_x:
                min_x = z.x
            if z.x > max_x:
                max_x = z.x
            if z.y < min_y:
                min_y = z.y
            if z.y > max_y:
                max_y = z.y
        map = GridMap(min_x, max_x, min_y, max_y)
        for z in self.zones:
            map.add_zone(z)
            if isinstance(z, Start_zone):
                start = z
        for i in self.connections:
            i.zone_a.connect_zones(i.zone_b)
        n_d = self.n_drones
        id = 1
        while n_d > 0:
            d = Drone(f"D{id}", id)
            start.enter_zone(d)
            id += 1
            n_d -= 1
        return map
