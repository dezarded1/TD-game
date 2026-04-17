import pygame
from settings import *


class Button:
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