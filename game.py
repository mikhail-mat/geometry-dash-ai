import pygame
import sqlite3
from states.menu import StartMenu, PlayerMenu
from states.gameplay import Gameplay
from states.choose_player import ChoosePlayer
from states.create_player import CreatePlayer
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DB_PATH


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('GeometryDash')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()

        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS players(
                NAME TEXT PRIMARY KEY,
                BEST_SCORE INTEGER
            )
        ''')
        self.conn.commit()

        self.start_menu = StartMenu(self.screen)
        self.player_menu = PlayerMenu(self.screen)
        self.choose_player = ChoosePlayer(self.screen, self.conn)
        self.create_player = CreatePlayer(self.screen, self.conn)
        self.gameplay = Gameplay(self.screen)

        self.states = {'start_menu': self.start_menu, 
                       'player_menu': self.player_menu,
                       'choose_player': self.choose_player, 
                       'create_player': self.create_player,
                       'gameplay': self.gameplay, 
                       'game_over': None, 
                       'quit': None}
        
        self.current_state = 'start_menu'

    def run(self):
        self.game_open = True

        while self.game_open:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.shutdown()

            new_state = self.current_state
            for state_name, state in self.states.items():
                if self.current_state == state_name:
                    if self.current_state == 'gameplay':
                        state.update()
                    state.display()
                    new_state = state.handle_events(events)
                    break

            if new_state != self.current_state:
                if new_state in self.states.keys():
                    self.current_state = new_state
                else:
                    print(f'Invalid state: {new_state}')

            if self.current_state == 'quit':
                self.shutdown()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def shutdown(self):
        self.game_open = False
        self.conn.close()
