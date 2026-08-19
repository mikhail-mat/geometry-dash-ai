import pygame
from constants import GAME_BG

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.og_player_img = pygame.image.load('player.png').convert_alpha()
        self.player_img = pygame.transform.scale(self.og_player_img, (80, 80))
        self.player_coords = (375,400)

    def display(self):
        self.screen.fill(GAME_BG)
        self.screen.blit(self.player_img, self.player_coords)

    def handle_events(self, events):
        return 'gameplay' # replace later
