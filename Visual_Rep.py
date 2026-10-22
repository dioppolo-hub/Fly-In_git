import pygame, sys, time
from Map import GridMap
from Zones import Zone, Start_zone, End_zone


class DroneSprite(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update_pos(self, x, y):
		self.rect.center = (x, y)


class Graphic:
	def __init__(self):
		self.dronespng = []

	def visual_rep(self, map: GridMap, movement: list[str], turn: int):
		pygame.init()
		drones = []
		all_drones = pygame.sprite.Group()
		size = width, height = 1920, 1000
		speed = [2, 2]
		zones = map.get_all_zones()
		start = map.get_start_zone()
		if turn == 1:
			drones = start.get_drones()
		black = 0, 0, 0
		screen = pygame.display.set_mode(size)
		if zones:
			min_x = min(z.x for z in zones)
			max_x = max(z.x for z in zones)
			min_y = min(z.y for z in zones)
			max_y = max(z.y for z in zones)
			range_x = max(max_x - min_x, 1)
			range_y = max(max_y - min_y, 1)
		else:
			min_x, range_x, min_y, range_y = 0, 1, 0, 1
		available_width = width - (2 * 200)
		available_height = height - (2 * 200)
		scale_x = available_width / range_x
		scale_y = available_height / range_y

		def scale_pos(x, y):
			screen_x = 200 + int((x - min_x) * scale_x)
			screen_y = 200 + int((y - min_y) * scale_y)
			return screen_x, screen_y

		save_zone_pos = {}
		for z in zones:
			zx, zy = scale_pos(z.x, z.y)
			save_zone_pos[z] = (zx, zy)
		zones_data = []
		lines_data = []
		for d in drones:
			d.x, d.y = scale_pos(d.x, d.y)
			drone = DroneSprite(pygame.image.load("Drone.png"), d.x, d.y)
			all_drones.add(drone)
		for z in zones:
			zx, zy = save_zone_pos[z]
			zones_data.append((zx, zy, z.color))
			for n in z.get_neighbours():
				if n in save_zone_pos:
					nx, ny = save_zone_pos[n]
					lines_data.append(((zx, zy), (nx, ny)))
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			screen.fill(black)
			for start_point, end_point in lines_data:
				pygame.draw.line(screen, (70, 70, 70), start_point, end_point)
			for zx, zy, color in zones_data:
				pygame.draw.circle(screen, color, (zx, zy), 50)
			all_drones.draw(screen)
			time.sleep(0.01)
			pygame.display.flip()