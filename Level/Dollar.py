import pygame
import math
from settings import *
from enemies.Dollar_green import Dollar_green
from towers.tower import Tower
from ui.hud import HUD


class Level:
    def __init__(self):
        self.towers = []
        self.projectiles = []
        self.hud=HUD()

        self.grid_size = {
            "x": 20,
            "y": 15
        }
        self.cell_size = 64
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        ]
        self.waypoints = []
        self.start_position = {
            "x": 18,
            "y": 14
        }
        self.end_position = {
            "x": 0,
            "y": 3
        }
        self.position = self.start_position.copy()
        self.visited = {
            "x": None,
            "y": None
        }

        self.waypoints = self.calculate_path()

        self.waypoints[0] = (self.start_position['y'] * self.cell_size + self.cell_size // 2,
                             self.start_position['x'] * self.cell_size + self.cell_size // 2)

        self.enemies = []
        self.spawn_rate_timer = 0

        self.path_color = YELLOW
        self.ground_colour = GREEN

        self.base_heath=MAIN_HEALTH
        self.base_money=30

        self.game_timer=WIN_TIME*FPS
        
        
        
        

    def is_visited(self, y, x):
        return (x != self.visited['x'] or y != self.visited['y'])

    def is_within_bounds(self, y, x):
        return 0 <= y < self.grid_size['y'] and 0 <= x < self.grid_size['x']

    def calculate_path(self):
        waypoints = [(self.start_position['y'], self.start_position['x'])]

        while self.position != self.end_position:
            if self.is_visited(self.position['y'] + 1, self.position['x']) and self.is_within_bounds(
                    self.position['y'] + 1, self.position['x']) and self.grid[self.position['y'] + 1][
                self.position['x']] == 1:
                self.visited = self.position.copy()
                self.position['y'] += 1

            elif self.is_visited(self.position['y'], self.position['x'] - 1) and self.is_within_bounds(
                    self.position['y'], self.position['x'] - 1) and self.grid[self.position['y']][
                self.position['x'] - 1] == 1:
                self.visited = self.position.copy()
                self.position['x'] -= 1

            elif self.is_visited(self.position['y'] - 1, self.position['x']) and self.is_within_bounds(
                    self.position['y'] - 1, self.position['x']) and self.grid[self.position['y'] - 1][
                self.position['x']] == 1:
                self.visited = self.position.copy()
                self.position['y'] -= 1

            waypoints.append((self.position['y'] * self.cell_size + self.cell_size // 2,
                              self.position['x'] * self.cell_size + self.cell_size // 2))

        return waypoints

    def place_tower(self, grid_x, grid_y, tower_data):
        """Размещение башни на сетке"""
        # Проверяем, что клетка свободна
        if self.grid[grid_y][grid_x] != 0:
            return False

        # Конвертируем координаты сетки в пиксели
        pixel_x = grid_x * self.cell_size + self.cell_size // 2
        pixel_y = grid_y * self.cell_size + self.cell_size // 2

        # Создаём башню

        new_tower = Tower(pixel_x, pixel_y, tower_data)
        self.grid[grid_y][grid_x] = 2  # 2 - занято башней

        self.towers.append(new_tower)
        return True

    def _update_projectiles(self):
        """Обновление снарядов и проверка попаданий"""
        for projectile in self.projectiles[:]:
            if not projectile["target"].alive:
                self.projectiles.remove(projectile)
                continue

            # Движение к цели
            dx = projectile["target"].x - projectile["x"]
            dy = projectile["target"].y - projectile["y"]
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < projectile["speed"]:
                # Попадание
                projectile["target"].health -= projectile["damage"]
                if projectile["target"].health <= 0:
                    projectile["target"].alive = False
                    # Начисление денег за убийство
                    self.hud.money += KILL_INKREAS
                self.projectiles.remove(projectile)
            else:
                projectile["x"] += (dx / distance) * projectile["speed"]
                projectile["y"] += (dy / distance) * projectile["speed"]

    def update(self):
        #время
        self.game_timer -= 1

        if self.game_timer<=0:
            return "win"


        #Добавление врагов
        self.new_enemy = Dollar_green(self.waypoints)
        self.spawn_rate_timer += 1
        if self.spawn_rate_timer >= (ENEMY_SPAWN_RATE-(DIFFICULTY_LEVEL_SPAWN_RATE*(1-((self.game_timer//FPS)/WIN_TIME)))):
            self.spawn_rate_timer = 0
            self.enemies.append(self.new_enemy)

        #Обновление врагов
        for enemy in self.enemies[:]:
            enemy.update()

            if enemy.reached_base or not enemy.alive:
                if enemy.reached_base:
                    self.base_heath-=ENEMY_DAMAGE

                if self.base_heath<=0:
                    self.base_heath=0
                    return "defeat"

                elif not enemy.alive and not enemy.reached_base :
                    self.base_money+=KILL_INKREAS
                   
                self.enemies.remove(enemy)

        

        for tower in self.towers:
            tower.update(self.enemies, self.projectiles)

        # Обновление снарядов
        self._update_projectiles()

    def draw(self, screen):

        # Отрисовка фона
        for row in range(self.grid_size['y']):
            for col in range(self.grid_size['x']):
                x = col * self.cell_size
                y = row * self.cell_size

                if self.grid[row][col] == 1:
                    color = self.path_color
                else:
                    color = self.ground_colour

                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, cell_rect)

                pygame.draw.rect(screen, DARK_GRAY, cell_rect, width=1)

                pygame.draw.rect(screen, DARK_GRAY, cell_rect, width=1)

        for enemy in self.enemies:
            enemy.draw(screen)
        for projectile in self.projectiles:
            pygame.draw.circle(screen, projectile["color"], (int(projectile["x"]), int(projectile["y"])), 5)

        # Отрисовка башен
        for tower in self.towers:
            tower.draw(screen)




