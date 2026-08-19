from pygame.font import SysFont
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'players.db'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TITLE_FONT = SysFont('Arial', 45, bold=True)
FONT = SysFont('Arial', 30, bold=True)

# colours
MENU_BG = (24, 24, 24)
GAME_BG = (24, 24, 24)
MENU_BTN_LIGHT = (44, 220, 255)
MENU_BTN_DARK = (0, 170, 204)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
