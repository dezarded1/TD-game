#lib
import pygame
import numpy
import pytmx

SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
FPS=60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Меню
MENU_BG_COLOR = (15, 15, 30)
MENU_TITLE_COLOR = YELLOW
BUTTON_NORMAL_COLOR = (50, 50, 80)
BUTTON_HOVER_COLOR = (80, 80, 130)
BUTTON_TEXT_COLOR = WHITE
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
BUTTON_BORDER_RADIUS = 10

# Шрифты
pygame.font.init()
FONT_SMALL = pygame.font.Font(None, 36)
FONT_MEDIUM = pygame.font.Font(None, 48)
FONT_LARGE = pygame.font.Font(None, 72)
FONT_TITLE = pygame.font.Font(None, 100)
