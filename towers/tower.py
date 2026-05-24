import pygame
import math
from settings import *


class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.type = tower_type

        self.damage = tower_type["damage"]
        self.range = tower_type["range"]
        self.fire_rate = tower_type["fire_rate"]
        self.color = tower_type["color"]
        self.name = tower_type["name"]
        self.cost = tower_type["cost"]


        self.size = 30
        self.attack_cooldown = 0
        self.target = None
        self.angle = 0

        self.shooting = False
        self.shoot_animation = 0

    def find_target(self, enemies):
        closest_enemy = None
        min_distance = self.range

        for enemy in enemies:
            if not enemy.alive:
                continue

            distance = math.sqrt(
                (enemy.x - self.x) ** 2 +
                (enemy.y - self.y) ** 2
            )

            if distance <= min_distance:
                min_distance = distance
                closest_enemy = enemy

        self.target = closest_enemy
        return closest_enemy is not None

    def update(self, enemies, projectiles):

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Ищем цель если её нет
        if self.target is None or not self.target.alive:
            self.find_target(enemies)

        if self.target and self.target.alive and self.attack_cooldown <= 0:
            distance = math.sqrt(
                (self.target.x - self.x) ** 2 +
                (self.target.y - self.y) ** 2
            )

            if distance <= self.range:
                self.attack(projectiles)
                self.attack_cooldown = self.fire_rate
            else:
                self.target = None

    def attack(self, projectiles):
        if self.target:
            # Вычисляем угол к цели
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
            if self.name == "Заморозка":
                self.target.slow_effect = True
                self.target.slow_duration = FPS*2
            projectile = {
                "x": self.x,
                "y": self.y,
                "target": self.target,
                "damage": self.damage,
                "speed": BULLET_SPEED,
                "color": RED if self.name != "Лазер" else BLUE
            }
            projectiles.append(projectile)

    def sell_price(self):
        return self.cost // 2

    def draw(self, screen):
        #oтрисовка башни
        pygame.draw.circle(screen, DARK_GRAY, (int(self.x), int(self.y)), self.size)


        tower_color = self.color
        if self.shooting:
            tower_color = tuple(min(255, c + 100) for c in tower_color)

        pygame.draw.circle(screen, tower_color, (int(self.x), int(self.y)), self.size - 5)
        if self.target and self.target.alive:
            end_x = self.x + math.cos(self.angle) * (self.size - 5)
            end_y = self.y + math.sin(self.angle) * (self.size - 5)
            pygame.draw.line(screen, WHITE, (self.x, self.y), (end_x, end_y), 4)
        range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            range_surface,
            (*self.color, 30),  # очень прозрачный
            (self.range, self.range),
            self.range
        )
        screen.blit(range_surface,
                    (self.x - self.range, self.y - self.range))