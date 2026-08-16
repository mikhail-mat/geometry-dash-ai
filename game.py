import pygame
from states.start_menu import StartMenu
from states.gameplay import Gameplay
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('GeometryDash')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.states = ('start_menu', 'choose_player', 'gameplay', 'game_over', 'quit')
        self.current_state = 'start_menu'

        self.start_menu = StartMenu(self.screen)
        self.gameplay = Gameplay(self.screen)

    def run(self):
        game_open = True

        while game_open:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    game_open = False
            
            if self.current_state == 'start_menu':
                self.start_menu.display()
                new_state = self.start_menu.handle_events(events)
            elif self.current_state == 'gameplay':
                self.gameplay.display()
                new_state = self.gameplay.handle_events(events)
            else:
                new_state = self.current_state

            if new_state != self.current_state:
                if new_state in self.states:
                    self.current_state = new_state
                else:
                    print(f'Invalid state: {new_state}')

            if self.current_state == 'quit':
                game_open = False

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
