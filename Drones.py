from typing import Any


class Drone():
    def __init__(self, name: str, drone_id: int):
        self.name = name
        self.drone_id = drone_id
        self.x = 0.0
        self.y = 0.0
        self.status = "idle"
        self.path: list[Any] = []
        self.current_connection: Any | None = None
        self.transit_target: Any | None = None
