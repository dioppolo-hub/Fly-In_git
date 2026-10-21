import pygame, sys, time
from Map import GridMap
from Zones import Zone, Start_zone, End_zone


class Graphic:
	def __init__(self):
		self.dronespng = []

	def visual_rep(self, map: GridMap, movement: list[str], turn: int):
		pygame.init()
		drones = []
		size = width, height = 1920, 1000
		speed = [2, 2]
		zones = map.get_all_zones()
		start = map.get_start_zone()
		if turn == 1:
			drones = start.get_drones()
		black = 0, 0, 0
		screen = pygame.display.set_mode(size)
		dpng = pygame.image.load("Start.png")
		drect = dpng.get_rect()
		while movement:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			screen.fill(black)
			screen.blit(dpng, drect)
			time.sleep(0.01)
			pygame.display.flip()