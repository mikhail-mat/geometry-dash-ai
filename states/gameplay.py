import pygame
from constants import GAME_BG, WHITE, SCREEN_WIDTH, BLACK
from game_logic.player import Player
from game_logic.logic import GameLogic
from game_logic.rl import Environment, TrainingLoop
from game_logic.constants import PLAYER_X, GROUND_Y

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.mode = 'human'

        self.game_logic = GameLogic()
        self.env = Environment()
        self.training_loop = TrainingLoop()
        self.training_loop.load()

        self.og_player_img = pygame.image.load('player.png').convert_alpha()
        self.player_img = pygame.transform.scale(self.og_player_img, (80, 80))

        self.action = 1 if self.mode == 'agent' else 0
        self.game_logic.step(action=self.action)

    def display(self):
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y))

        cam_offset_x = round(self.game_logic.player.x - PLAYER_X)

        for obs in self.game_logic.obstacles:
            if obs.type == 'block':
                pygame.draw.rect(self.screen, WHITE, 
                                 (round(obs.left) - cam_offset_x, 
                                  round(obs.top), 
                                  obs.width, obs.height), 2)
            elif obs.type == 'spike':
                pygame.draw.polygon(self.screen, WHITE, 
                    [
                        (round(obs.left) - cam_offset_x, round(obs.bottom)), 
                        (round(obs.right) - cam_offset_x, round(obs.bottom)), 
                        (round(obs.apex[0]) - cam_offset_x, round(obs.apex[1])),
                    ])

        screen_y = round(self.game_logic.player.y) - self.player_img.get_height()
        self.screen.blit(self.player_img, (PLAYER_X, screen_y))

    def handle_events(self, events):
        if self.mode == 'human':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.action = 1
        return 'gameplay'

    def update(self):
        if self.mode == 'agent':
            if self.game_logic.player.x > self.env.env_obstacles[-1][1] + 20:
                self.game_logic.reset()
                self.game_logic.step(action=1)
            
            self.env.player.x = self.game_logic.player.x
            self.env.player.y = self.game_logic.player.y

            if not self.game_logic.player.in_air:
                state = self.env.convert_to_state()
                self.action = max(range(2), 
                            key=lambda a: self.training_loop.Q.get(state, [0, 0])[a])
            else:
                self.action = 0

            self.game_logic.step(action=self.action)
        elif self.mode == 'human':
            self.game_logic.step(action=self.action)
            self.action = 0
