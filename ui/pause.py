import pygame
from settings import *
from core.states import GameState

class RetryButton:
    def __init__(self, x, y, width, height, text, font=None,
                 normal_color=BUTTON_NORMAL_COLOR,
                 hover_color=BUTTON_HOVER_COLOR,
                 text_color=BUTTON_TEXT_COLOR,
                 border_radius=BUTTON_BORDER_RADIUS):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font if font else FONT_MEDIUM
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius

        self.is_hovered = False
        self.is_clicked = False

        self._render_text()

    def _render_text(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_clicked and self.rect.collidepoint(event.pos):
                    self.is_clicked = False
                    return True
                self.is_clicked = False
        return False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=self.border_radius)
        surface.blit(self.text_surface, self.text_rect)
class MenuButton:
    def __init__(self, x, y, width, height, text, font=None,
                 normal_color=BUTTON_NORMAL_COLOR,
                 hover_color=BUTTON_HOVER_COLOR,
                 text_color=BUTTON_TEXT_COLOR,
                 border_radius=BUTTON_BORDER_RADIUS):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font if font else FONT_MEDIUM
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius

        self.is_hovered = False
        self.is_clicked = False

        self._render_text()

    def _render_text(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_clicked and self.rect.collidepoint(event.pos):
                    self.is_clicked = False
                    return True
                self.is_clicked = False
        return False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=self.border_radius)
        surface.blit(self.text_surface, self.text_rect)

class Pause:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Кнопка retry
        button_xretry = screen_width // 2 - BUTTON_WIDTH // 2
        button_yretry = screen_height // 2+100

        self.retry_button = RetryButton(button_xretry, button_yretry,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            "ПРОДОЛЖИТЬ"
        )
        # Кнопка menu
        button_xmenu = screen_width // 2 - BUTTON_WIDTH // 2
        button_ymenu = screen_height // 2-100

        self.menu_button = MenuButton(
            button_xmenu, button_ymenu,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            "ГЛАВНОЕ МЕНЮ"
        )

        # Простая анимация
        self.pulse_alpha = 255
        self.pulse_direction = -5

    def handle_events(self, events):
        for event in events:
            if self.retry_button.handle_event(event):
                return GameState.PLAYING
        for event in events:
            if self.menu_button.handle_event(event):
                return GameState.MENU
        return None
    def draw(self, screen):
        screen.fill(MENU_BG_COLOR)
        screen.blit(self.title_surface, self.title_rect)
        self.retry_button.draw(screen)
        self.menu_button.draw(screen)