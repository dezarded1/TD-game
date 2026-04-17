import pygame
import sys
from settings import *
from core.states import GameState
from ui.menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.running = True

        self.current_state = GameState.MENU
        self.menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

    def run(self):
        while self.running:
            events = pygame.event.get()
            self._handle_global_events(events)
            self._handle_state_events(events)
            self._update_state()
            self._draw_state()
            self.clock.tick(FPS)

    def _handle_global_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == GameState.MENU:
                        self.running = False
                    else:
                        self.current_state = GameState.MENU

    def _handle_state_events(self, events):
        if self.current_state == GameState.MENU:
            new_state = self.menu.handle_events(events)
            if new_state:
                self.current_state = new_state

    def _update_state(self):
        if self.current_state == GameState.MENU:
            self.menu.update()

    def _draw_state(self):
        if self.current_state == GameState.MENU:
            self.menu.draw(self.screen)
        elif self.current_state == GameState.PLAYING:
            # Заглушка игрового экрана
            self.screen.fill(DARK_GRAY)

            # Текст "ИГРА НАЧАЛАСЬ"
            game_text = FONT_LARGE.render("ИГРА НАЧАЛАСЬ", True, WHITE)
            text_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_text, text_rect)

            # Подсказка
            hint_text = FONT_SMALL.render("Нажми ESC для возврата в меню", True, LIGHT_GRAY)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(hint_text, hint_rect)

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()