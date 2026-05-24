import pygame
import sys
from settings import *
from core.states import GameState
from ui.menu import MainMenu
from Level.Dollar import Level
from ui.hud import HUD
from ui.pause import Pause
from ui.tower_shop import TowerShop
from endgame.defit import Defit
from endgame.win import Win
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.running = True

        self.tower_shop = TowerShop(SCREEN_WIDTH - 320, 20)
        self.level=Level()
        self.hud = HUD()
        self.current_state = GameState.MENU
        self.menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pause = Pause(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.defeat=Defit(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.victory = Win(SCREEN_WIDTH, SCREEN_HEIGHT)

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
                    elif self.current_state == GameState.PLAYING:
                        self.current_state = GameState.PAUSE
                    elif self.current_state == GameState.PAUSE:
                        self.current_state = GameState.PLAYING
                    else :
                        self.current_state= GameState.MENU

    def _handle_state_events(self, events):
        if self.current_state == GameState.MENU:
            new_state = self.menu.handle_events(events)
            if new_state:
                if new_state == GameState.PLAYING:
                    self.reset_game()
                self.current_state = new_state
        if self.current_state == GameState.PAUSE:
            new_state = self.pause.handle_events(events)
            if new_state:
                self.current_state = new_state
        if self.current_state == GameState.PLAYING:
            self._handle_playing_events(events)
        if self.current_state == GameState.DEFEAT:
            new_state = self.defeat.handle_events(events)
            if new_state:
                self.current_state = new_state

    def _handle_playing_events(self, events):
        """Обработка событий в игре"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # B открывает магазин
                    self.tower_shop.toggle()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверяем магазин
                    shop_result = self.tower_shop.handle_events([event])

                    if shop_result == "select_tower":
                        tower_data = self.tower_shop.get_selected_tower()
                        if tower_data and self.hud.money >= tower_data["cost"]:
                            # Режим размещения (можно добавить визуальное отображение)
                            self.placing_tower = tower_data

                    elif self.tower_shop.is_open:
                        # Магазин сам обработает клик
                        pass

                    elif hasattr(self, 'placing_tower') and self.placing_tower:
                        # Размещение башни
                        grid_x = mouse_pos[0] // self.level.cell_size
                        grid_y = mouse_pos[1] // self.level.cell_size

                        if (0 <= grid_x < self.level.grid_size["x"] and
                                0 <= grid_y < self.level.grid_size["y"]):

                            if self.level.place_tower(grid_x, grid_y, self.placing_tower):
                                self.level.base_money-=self.placing_tower["cost"]
                                

                                

                        self.placing_tower = None

    def _update_state(self):
        if self.current_state == GameState.MENU:
            self.menu.update()
        elif self.current_state == GameState.PLAYING:
            result = self.level.update()
            if result == "defeat":
                self.current_state = GameState.DEFEAT
            self.hud.money = self.level.money if hasattr(self.level, 'money') else self.hud.money

    def reset_game(self):
        self.tower_shop = TowerShop(SCREEN_WIDTH - 320, 20)
        self.level = Level()
        self.hud = HUD()


        if hasattr(self, 'placing_tower'):
            self.placing_tower = None

    def _draw_state(self):
        if self.current_state == GameState.MENU:
            self.menu.draw(self.screen)
        elif self.current_state == GameState.PLAYING:
            self.level.update()
            self.hud.update_health(self.level.base_heath)
            self.hud.update_money(self.level.base_money)
            self.level.draw(self.screen)
            self.hud.draw(self.screen)
        elif self.current_state == GameState.PAUSE:
            self.pause.draw(self.screen)
        if self.current_state == GameState.PLAYING:
            self.level.draw(self.screen)
            self.hud.draw(self.screen)
            self.tower_shop.draw(self.screen)
        elif self.current_state == GameState.DEFEAT:
            self.defeat.draw(self.screen)



        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()
