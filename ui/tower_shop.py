import pygame
from settings import *


class TowerShop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected_tower = None
        self.is_open = False
        self.shop_width = 300
        self.shop_height = 250
        self.button_size = 50
        self.padding = 10

        # Панель магазина (изначально скрыта)
        self.panel_rect = pygame.Rect(
            self.x, self.y,
            self.shop_width, self.shop_height
        )


        self.tower_buttons = []
        self._create_tower_buttons()
        self.close_button = pygame.Rect(
            self.x + self.shop_width - 30,
            self.y + 10,
            20, 20
        )

    def _create_tower_buttons(self):
        towers_data = [
            {
                "name": "Пулемёт",
                "color": GRAY,
                "cost": 10,
                "damage": 5,
                "range": 150,
                "fire_rate": 10
            },
            {
                "name": "Пушка",
                "color": RED,
                "cost": 25,
                "damage": 20,
                "range": 200,
                "fire_rate": 30
            },
            {
                "name": "Лазер",
                "color": BLUE,
                "cost": 50,
                "damage": 40,
                "range": 250,
                "fire_rate": 15
            },
            {
                "name": "Заморозка",
                "color": (100, 200, 255),
                "cost": 35,
                "damage": 8,
                "range": 180,
                "fire_rate": 20
            }
        ]

        start_x = self.x + self.padding
        start_y = self.y + 50

        for i, tower_data in enumerate(towers_data):
            col = i % 2
            row = i // 2

            button_x = start_x + col * (self.button_size + self.padding)
            button_y = start_y + row * (self.button_size + self.padding + 30)

            button_rect = pygame.Rect(button_x, button_y, self.button_size, self.button_size)

            self.tower_buttons.append({
                "rect": button_rect,
                "data": tower_data,
                "hover": False
            })

    def toggle(self):
        self.is_open = not self.is_open
        self.selected_tower = None

    def close(self):
        self.is_open = False
        self.selected_tower = None

    def handle_events(self, events):
        if not self.is_open:
            return None

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos


                    if self.close_button.collidepoint(mouse_pos):
                        self.close()
                        return None


                    for button in self.tower_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            self.selected_tower = button["data"].copy()
                            return "select_tower"
                    if not self.panel_rect.collidepoint(mouse_pos):
                        self.close()
                        return None

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in self.tower_buttons:
                    button["hover"] = button["rect"].collidepoint(mouse_pos)

        return None

    def get_selected_tower(self):
        tower = self.selected_tower
        self.selected_tower = None
        self.close()
        return tower

    def can_afford(self, tower_data, money):
        return money >= tower_data["cost"]

    def draw(self, screen):
        if not self.is_open:
            return

        panel = pygame.Surface((self.shop_width, self.shop_height))
        panel.set_alpha(220)
        panel.fill((20, 20, 40))
        screen.blit(panel, self.panel_rect)
        pygame.draw.rect(screen, YELLOW, self.panel_rect, 2)
        title = FONT_SMALL.render("МАГАЗИН БАШЕН", True, YELLOW)
        title_rect = title.get_rect(
            centerx=self.x + self.shop_width // 2,
            top=self.y + 10
        )
        screen.blit(title, title_rect)
        pygame.draw.rect(screen, RED, self.close_button)
        close_text = FONT_VERY_SMALL.render("X", True, WHITE)
        screen.blit(close_text, (self.close_button.x + 4, self.close_button.y + 2))

        for button in self.tower_buttons:
            color = button["data"]["color"]
            if button["hover"]:
                color = tuple(min(255, c + 50) for c in color)

            pygame.draw.rect(screen, color, button["rect"])
            pygame.draw.rect(screen, WHITE, button["rect"], 1)

            data = button["data"]

            cost_text = FONT_VERY_SMALL.render(f"${data['cost']}", True, YELLOW)
            cost_rect = cost_text.get_rect(
                centerx=button["rect"].centerx,
                top=button["rect"].bottom + 2
            )
            screen.blit(cost_text, cost_rect)

            name_text = FONT_VERY_SMALL.render(data["name"], True, WHITE)
            name_rect = name_text.get_rect(
                centerx=button["rect"].centerx,
                top=cost_rect.bottom + 1
            )
            screen.blit(name_text, name_rect)
        if self.selected_tower:
            info_y = self.y + self.shop_height - 80
            info_bg = pygame.Rect(self.x + 10, info_y, self.shop_width - 20, 70)
            pygame.draw.rect(screen, (40, 40, 60), info_bg)
            pygame.draw.rect(screen, GREEN, info_bg, 1)

            info_texts = [
                f"Урон: {self.selected_tower['damage']}",
                f"Радиус: {self.selected_tower['range']}",
                f"Скорость: {self.selected_tower['fire_rate']}",
                f"Цена: {self.selected_tower['cost']}$"
            ]

            for i, text in enumerate(info_texts):
                info_surface = FONT_VERY_SMALL.render(text, True, WHITE)
                screen.blit(info_surface, (info_bg.x + 10, info_bg.y + 5 + i * 15))