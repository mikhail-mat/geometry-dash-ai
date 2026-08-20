import pygame
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'players.db'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

_font_cache = {}

def get_font(size=30, name='Arial', bold=True):
    key = (name, size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont(name, size, bold=bold)
    return _font_cache[key]

# colours
MENU_BG = (24, 24, 24)
GAME_BG = (24, 24, 24)
MENU_BTN_LIGHT = (44, 220, 255)
MENU_BTN_DARK = (0, 170, 204)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
