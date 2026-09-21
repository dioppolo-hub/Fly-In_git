from typing import Any


class Drone():
	def __init__(self,  drone_id: str, x: int, y: int):
		self.drone_id = drone_id
		self.x = x
		self.y = y
		self.status = "idle"
		self.path = []

	def get_drone_pos(self) -> tuple:
		return (self.x, self.y)

	def set_position(self, x: int, y: int):
		self.x = x
		self.y = y

	def is_at(self, x: int, y: int):
		if self.get_drone_pos() == (x, y):
			return True
		else:
			return False

	def move_to(self, x: int, y: int):
		self.status = "moving"
		self.x = x
		self.y = y

	def set_destination(self, path: list):
		self.path = path.copy()
		if path:
			self.status = "moving"
		else:
			self.status = "idle"

	def has_destination(self):
		if len(self.path) > 0:
			return True
		else:
			return False

	def next_position(self):
		if not self.path:
			self.status = "idle"
			return None
		next_pos = self.path.pop(0)
		self.x, self.y = next_pos
		if not self.path:
			self.status = "idle"
		return next_pos

	def stop(self):
		self.path.clear()
		self.status = "idle"
