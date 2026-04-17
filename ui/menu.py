import pygame
from settings import *
from ui.button import Button
from core.states import GameState


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Заголовок
        self.title_surface = FONT_TITLE.render("TOWER DEFENSE", True, MENU_TITLE_COLOR)
        self.title_rect = self.title_surface.get_rect(
            center=(screen_width // 2, screen_height // 3)
        )

        # Кнопка Старт
        button_x = screen_width // 2 - BUTTON_WIDTH // 2
        button_y = screen_height // 2

        self.start_button = Button(
            button_x, button_y,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            "ИГРАТЬ"
        )

        # Простая анимация
        self.pulse_alpha = 255
        self.pulse_direction = -5

    def handle_events(self, events):
        for event in events:
            if self.start_button.handle_event(event):
                return GameState.PLAYING
        return None

    def update(self):
        # Пульсация заголовка
        self.pulse_alpha += self.pulse_direction
        if self.pulse_alpha <= 180 or self.pulse_alpha >= 255:
            self.pulse_direction *= -1

        # Обновляем цвет заголовка
        color_value = self.pulse_alpha
        pulsed_color = (255, 255, color_value // 2)
        self.title_surface = FONT_TITLE.render("TOWER DEFENSE", True, pulsed_color)

    def draw(self, screen):
        screen.fill(MENU_BG_COLOR)
        screen.blit(self.title_surface, self.title_rect)
        self.start_button.draw(screen)