import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Самонаводящиеся снаряды")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
RED = (255, 70, 70)
YELLOW = (255, 230, 50)
GREEN = (50, 255, 100)
ORANGE = (255, 160, 30)
PURPLE = (180, 60, 255)

# ============================================================
# КЛАСС: ШАР-ЦЕЛЬ (просто движется и отскакивает)
# ============================================================
class TargetBall:
    def __init__(self, x, y, radius=18):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = 3
        self.speed_y = 2
        self.color = RED

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x < self.radius or self.x > WIDTH - self.radius:
            self.speed_x *= -1
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Блик
        pygame.draw.circle(surface, WHITE, (int(self.x - 5), int(self.y - 5)), 4)

    def get_pos(self):
        return self.x, self.y


# ============================================================
# КЛАСС: ТРЕУГОЛЬНИК-ЦЕЛЬ (тоже движется)
# ============================================================
class TargetTriangle:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = -2
        self.speed_y = 4
        self.color = GREEN
        self.angle = 0

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.angle += 1  # медленно вращается
        if self.x < self.size or self.x > WIDTH - self.size:
            self.speed_x *= -1
        if self.y < self.size or self.y > HEIGHT - self.size:
            self.speed_y *= -1

    def get_vertices(self):
        """Возвращает 3 вершины треугольника с учётом поворота"""
        rad = math.radians(self.angle)
        h = self.size * 0.866  # высота равностороннего
        points = [
            (self.x + self.size * math.cos(rad),
             self.y - self.size * math.sin(rad)),
            (self.x + self.size * math.cos(rad + 2.094),
             self.y - self.size * math.sin(rad + 2.094)),
            (self.x + self.size * math.cos(rad + 4.188),
             self.y - self.size * math.sin(rad + 4.188)),
        ]
        return points

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.get_vertices())

    def get_pos(self):
        return self.x, self.y


# ============================================================
# КЛАСС: САМОНАВОДЯЩИЙСЯ СНАРЯД
# ============================================================
class HomingBullet:
    def __init__(self, x, y, target, speed=6, turn_rate=3.5):
        self.x = float(x)
        self.y = float(y)
        self.radius = 4
        self.speed = speed
        self.turn_rate = turn_rate  # градусов в кадр — насколько резко поворачивает
        self.target = target        # цель (объект с методом get_pos())
        self.angle = 0              # текущее направление (градусы)
        self.color = YELLOW

    def update(self):
        # 1. Получаем позицию цели
        tx, ty = self.target.get_pos()

        # 2. Вычисляем желаемый угол к цели
        dx = tx - self.x
        dy = ty - self.y
        desired_angle = math.degrees(math.atan2(-dy, dx))  # минус dy — ось Y вниз

        # 3. Плавно доворачиваем к желаемому углу
        diff = (desired_angle - self.angle + 180) % 360 - 180  # кратчайший поворот
        if abs(diff) <= self.turn_rate:
            self.angle = desired_angle
        else:
            self.angle += self.turn_rate if diff > 0 else -self.turn_rate
        self.angle %= 360

        # 4. Двигаемся в текущем направлении
        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)  # минус — ось Y вниз

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Хвостик (линия позади, показывает траекторию)
        rad = math.radians(self.angle)
        tail_x = self.x - 6 * math.cos(rad)
        tail_y = self.y + 6 * math.sin(rad)
        pygame.draw.line(surface, ORANGE, (self.x, self.y), (tail_x, tail_y), 2)

    def is_off_screen(self):
        return (self.x < -20 or self.x > WIDTH + 20 or
                self.y < -20 or self.y > HEIGHT + 20)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)


# ============================================================
# КЛАСС: ТУРЕЛЬ (прямоугольник)
# ============================================================
class Turret:
    def __init__(self, x, y, width=50, height=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = 0

        # Оригинальное изображение
        self.original = pygame.Surface((width, height), pygame.SRCALPHA)
        self.original.fill((0, 0, 0, 0))
        pygame.draw.rect(self.original, CYAN, (0, 0, width, height), border_radius=4)
        # Ствол (маленький прямоугольник сверху)
        pygame.draw.rect(self.original, WHITE, (width // 2 - 4, -12, 8, 14))

        self.image = self.original
        self.rect = self.image.get_rect(center=(x, y))

        # Стрельба
        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 25  # кадров между выстрелами

    def find_closest_target(self, targets):
        """Возвращает ближайшую цель из списка"""
        if not targets:
            return None
        closest = min(targets,
                      key=lambda t: math.hypot(t.get_pos()[0] - self.x,
                                               t.get_pos()[1] - self.y))
        return closest

    def shoot(self, target):
        """Создаёт самонаводящийся снаряд к цели"""
        if target and self.shoot_cooldown <= 0:
            # Начальная позиция — конец ствола
            rad = math.radians(self.angle)
            barrel_len = self.height // 2 + 14
            bx = self.x + barrel_len * math.cos(rad)
            by = self.y - barrel_len * math.sin(rad)
            self.bullets.append(HomingBullet(bx, by, target))
            self.shoot_cooldown = self.shoot_delay

    def update(self, target):
        # Кулдаун
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Поворот к цели
        if target:
            tx, ty = target.get_pos()
            dx = tx - self.x
            dy = ty - self.y
            self.angle = -math.degrees(math.atan2(dy, dx))  # минус — ось Y вниз
            self.image = pygame.transform.rotate(self.original, self.angle)
            self.rect = self.image.get_rect(center=(self.x, self.y))
            # Авто-стрельба
            self.shoot(target)

        # Обновление всех снарядов
        for b in self.bullets[:]:
            b.update()
            if b.is_off_screen():
                self.bullets.remove(b)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for b in self.bullets:
            b.draw(surface)


# ============================================================
# ИНИЦИАЛИЗАЦИЯ ОБЪЕКТОВ
# ============================================================
turret = Turret(WIDTH // 2, HEIGHT // 2 + 100)

# Несколько целей
targets = [
    TargetBall(200, 150),
    TargetBall(600, 300),
    TargetTriangle(400, 100, 25),
    TargetTriangle(150, 400, 20),
    TargetBall(700, 500, 14),
]

# ============================================================
# ГЛАВНЫЙ ЦИКЛ
# ============================================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление целей
    for t in targets:
        t.update()

    # Поиск ближайшей цели и обновление турели
    closest = turret.find_closest_target(targets)
    turret.update(closest)

    # Проверка попаданий (пуля касается цели)
    for b in turret.bullets[:]:
        bullet_rect = b.get_rect()
        hit = False
        for t in targets[:]:
            tx, ty = t.get_pos()
            target_rect = pygame.Rect(tx - t.size if hasattr(t, 'size') else tx - t.radius,
                                      ty - t.size if hasattr(t, 'size') else ty - t.radius,
                                      (t.size if hasattr(t, 'size') else t.radius) * 2,
                                      (t.size if hasattr(t, 'size') else t.radius) * 2)
            if bullet_rect.colliderect(target_rect):
                targets.remove(t)
                if b in turret.bullets:
                    turret.bullets.remove(b)
                # Спавним новую цель где-то в стороне
                import random
                if random.random() < 0.5:
                    targets.append(TargetBall(random.randint(50, WIDTH - 50),
                                              random.randint(50, HEIGHT - 50)))
                else:
                    targets.append(TargetTriangle(random.randint(50, WIDTH - 50),
                                                  random.randint(50, HEIGHT - 50)))
                hit = True
                break
        if hit:
            continue

    # Отрисовка
    screen.fill(BLACK)
    for t in targets:
        t.draw(screen)
    turret.draw(screen)

    # Информация
    font = pygame.font.Font(None, 28)
    text = font.render(f'Целей: {len(targets)} | Снарядов: {len(turret.bullets)}',
                       True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()