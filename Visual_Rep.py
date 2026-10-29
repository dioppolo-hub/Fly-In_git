from typing import Any
import pygame
import sys
import time
import math
from Map import GridMap
from Drones import Drone
from Zones import Zone
from Scheduler import move_one_turn


class DroneSprite(pygame.sprite.Sprite):
    def __init__(self, image: Any, x: float, y: float):
        super().__init__()
        self.image = image
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.x, self.y = float(x), float(y)
        self.target_x, self.target_y = float(x), float(y)
        self.rect.center = (int(x), int(y))

    def set_target(self, tx: int, ty: int) -> None:
        self.target_x = float(tx)
        self.target_y = float(ty)

    def update_pos(self, speed: float) -> None:
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.hypot(dx, dy)
        if distance > speed:
            self.x += (dx / distance) * speed
            self.y += (dy / distance) * speed
        else:
            self.x = self.target_x
            self.y = self.target_y
        self.rect.center = (int(self.x), int(self.y))


class Graphic:
    def __init__(self) -> None:
        self.dronespng: list[DroneSprite] = []

    def visual_rep(self, map: GridMap, turn: int, drones: list[Drone]) -> None:
        pygame.init()
        movement: list = []
        all_drones = pygame.sprite.Group()
        drone_sprites: dict = {}
        size = width, height = 1920, 1000
        zones: list[Zone] = map.get_all_zones()
        speed: float = 20.0
        black: tuple = (0, 0, 0)
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

        def scale_pos(x: float, y: float) -> tuple[float, float]:
            screen_x = 200 + int((x - min_x) * scale_x)
            screen_y = 200 + int((y - min_y) * scale_y)
            return (screen_x, screen_y)

        save_zone_pos = {}
        for z in zones:
            zx, zy = scale_pos(z.x, z.y)
            save_zone_pos[z] = (zx, zy)
        zones_data = []
        lines_data = []
        for d in drones:
            dx, dy = scale_pos(d.x, d.y)
            drone = DroneSprite(pygame.image.load("Drone.png"), dx, dy)
            all_drones.add(drone)
            drone_sprites[d] = drone
        for z in zones:
            zx, zy = save_zone_pos[z]
            zones_data.append((zx, zy, z.color, z.name, z.cost, z.capacity))
            for n in z.get_neighbours():
                if n in save_zone_pos:
                    nx, ny = save_zone_pos[n]
                    lines_data.append(((zx, zy), (nx, ny)))
        font = pygame.font.SysFont("Arial", 20)
        is_animating = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not is_animating:
                        movement = move_one_turn(map, drones)
                        turn += 1
                        for m in movement:
                            z_or_conn = m.count("-")
                            if z_or_conn == 1:
                                d_id, zname = m.split("-")
                                zone = map.get_zone_by_name(zname)
                                d_label = int(d_id[1:])
                                drn = map.get_drone_by_id(d_label)
                                if zone and drn:
                                    drn.x, drn.y = zone.x, zone.y
                                    dest_x, dest_y = scale_pos(drn.x, drn.y)
                                    if drn in drone_sprites:
                                        drone_sprites[drn].set_target(dest_x, dest_y)
                            elif z_or_conn == 2:
                                d_id, zstart, zend = m.split("-")
                                zs = map.get_zone_by_name(zstart)
                                ze = map.get_zone_by_name(zend)
                                d_label = int(d_id[1:])
                                drn = map.get_drone_by_id(d_label)
                                if zs and ze and drn:
                                    drn.x = float((zs.x + ze.x) / 2)
                                    drn.y = float((zs.y + ze.y) / 2)
                                    dst_x, dst_y = scale_pos(drn.x, drn.y)
                                    if drn in drone_sprites:
                                        drone_sprites[drn].set_target(dst_x, dst_y)
                        if movement:
                            print(f"\n=====(turn: {turn})=====")
                            print(" ".join(movement))
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    else:
                        continue
                if turn > 1 and drones and not movement and not map.end_simulation():
                    print("[ERRORE] - Simulazione Bloccata")
                    sys.exit(0)
            for drone_sprite in drone_sprites.values():
                drone_sprite.update_pos(speed)
            is_animating = any(
                math.hypot(
                    sprite.target_x - sprite.x,
                    sprite.target_y - sprite.y,
                ) > 0.5
                for sprite in drone_sprites.values()
            )
            screen.fill(black)
            for start_point, end_point in lines_data:
                pygame.draw.line(screen, (70, 70, 70), start_point, end_point)
            for zx, zy, color, name, cost, capacity in zones_data:
                cap_label = (
                    f" MAX:{int(capacity)}"
                    if math.isfinite(float(capacity)) and float(capacity) > 1
                    else ""
                    )
                if color == "rainbow":
                    rainbow_colors: list[tuple[int, int, int]] = [
                        (255, 0, 0),
                        (255, 165, 0),
                        (255, 255, 0),
                        (0, 255, 0),
                        (0, 255, 255),
                        (0, 0, 255),
                        (255, 0, 255)
                    ]
                    for radius, ring_color in zip(range(50, 0, -8), rainbow_colors):
                        pygame.draw.circle(screen, ring_color, (zx, zy), radius)
                else:
                    pygame.draw.circle(screen, color, (zx, zy), 50)
                if int(cost) == 1:
                    testo = font.render(
                        f"{str(name)}{cap_label}", True, (255, 255, 255)
                        )
                elif float(cost) == 0.9:
                    testo = font.render(
                        f"P: {str(name)}{cap_label}", True, (255, 255, 255)
                        )
                elif float(cost) == 2:
                    testo = font.render(
                        f"R: {str(name)}{cap_label}", True, (255, 255, 255))
                testo_rect = testo.get_rect(center=(zx, zy-75))
                screen.blit(testo, testo_rect)
            all_drones.draw(screen)
            time.sleep(0.01)
            pygame.display.flip()
