import pygame, sys


class button:
	def __init__(self, x, y, width, height, text, action=None):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.action = action
	
	def draw(self, surface, font):
		mouse_pos = pygame.mouse.get_pos()
		color = (0, 255, 0) if self.rect.collidepoint(mouse_pos) else (255, 0, 0)
		pygame.draw.rect(surface, color, self.rect, border_radius=8)
		pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)
		text_surf = font.render(self.text, True, (0, 0, 0))
		text_rect = text_surf.get_rect(center=self.rect.center)
		surface.blit(text_surf, text_rect)

	def is_clicked(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.rect.collidepoint(event.pos):
				return True
		return False


def load_map_button(diff, maps_data) -> list:
	map_button = []
	maps = maps_data[diff]
	for i, map_name in enumerate(maps):
		btn = button(780, 334 + (i * 88), 360, 68, map_name, action=map_name)
		map_button.append(btn)
	return map_button

def menu():
	pygame.init()
	font = None
	width, height = 1920, 1000
	screen = pygame.display.set_mode((width, height))
	font = pygame.font.Font(None, 40)
	pygame.display.set_caption("MENU INIZIALE")
	maps_data = {
		"easy": ["01_linear_path.txt", "02_simple_fork.txt", "03_basic_capacity.txt"],
		"medium": ["01_dead_end_trap.txt", "02_circular_loop.txt", "03_priority_puzzle.txt"],
		"hard": ["01_maze_nightmare.txt", "02_capacity_hell.txt", "03_ultimate_challenge.txt"],
		"challenger": ["01_the_impossible_dream.txt"]
	}
	home_buttons = []
	for i, diff in enumerate(maps_data.keys()):
		btn = button(780, 334 + (i * 88), 360, 68, diff, action=diff)
		home_buttons.append(btn)
	current_state = "HOME"
	sel_diff = None
	clock = pygame.time.Clock()
	while True:
		screen.fill((255, 255, 255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if current_state == "HOME":
				for btn in home_buttons:
					if btn.is_clicked(event):
						sel_diff = btn.action
						map_button = load_map_button(sel_diff, maps_data)
						current_state = "MAP_SELECT"
			elif current_state == "MAP_SELECT":
				for btn in map_button:
					if btn.is_clicked(event):
						chosen_map = btn.action
						current_state = "PLAYING"
				back_btn = button(50, 500, 120, 50, "Indietro")
				if back_btn.is_clicked(event):
					current_state = "HOME"
		if current_state == "HOME":
			title_surf = font.render("SELECT DIFFICULTY", True, (0, 0, 0))
			screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 80)))
			for btn in home_buttons:
				btn.draw(screen, font)
			pygame.display.flip()
		elif current_state == "MAP_SELECT":
			title_surf = font.render(f"{sel_diff.upper()}", True, (0, 0, 0))
			screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 80)))
			for btn in map_button:
				btn.draw(screen, font)
			back_btn = button(50, 500, 120, 50, "Indietro")
			back_btn.draw(screen, font)
			pygame.display.flip()
		elif current_state == "PLAYING":
			pygame.quit()
			return str(sel_diff) + "/" + str(chosen_map)