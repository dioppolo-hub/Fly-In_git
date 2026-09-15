from typing import Any


class Drone():
	def __init__(self,  drone_id: str, x: int, y: int):
		self.drone_id = drone_id
		self.x = x
		self.y = y

	def get_drone_pos(self) -> tuple:
		return (self.x, self.y)
