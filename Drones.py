from typing import Any


class Drone():
	def __init__(self,  name: str, x: int, y: int):
		self.name = name
		self.drone_id = 1
		self.x = x
		self.y = y
		self.status = "idle"
		self.path = []

	def get_drone_pos(self) -> tuple:
		return (self.x, self.y)

	def set_position(self, x: int, y: int) -> None:
		self.x = x
		self.y = y

	def is_at(self, x: int, y: int) -> bool:
		if self.get_drone_pos() == (x, y):
			return True
		else:
			return False

	def move_to(self, x: int, y: int) -> bool:
		self.status = "moving"
		self.x = x
		self.y = y

	def set_destination(self, path: list) -> None:
		self.path = path.copy()
		if path:
			self.status = "moving"
		else:
			self.status = "idle"

	def has_destination(self) -> bool:
		if len(self.path) > 0:
			return True
		else:
			return False

	def next_position(self) -> None | tuple:
		if not self.path:
			self.status = "idle"
			return None
		next_pos = self.path.pop(0)
		self.x, self.y = next_pos
		if not self.path:
			self.status = "idle"
		return next_pos

	def stop(self) -> None:
		self.path.clear()
		self.status = "idle"
