import pygame
from .menu import Text
from constants import get_font, MENU_BG, MENU_BTN_DARK, MENU_BTN_LIGHT, BLACK, RED


class ChoosePlayer:
    def __init__(self, screen, conn):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.conn = conn
        
        self.input_rect = pygame.Rect(0, 0, 300, 50)
        self.input_rect.center = (self.screen_rect.centerx, 
                                  self.screen_rect.centery + 35)
        
        self.input_active = False

        self.user_input_string = ''
        self.user_input_text = Text(self.user_input_string, 
                                    coords=self.input_rect.center,
                                    colour=BLACK)

        self.err_message_font = pygame.font.SysFont('Arial', 20)
        self.input_err_message = Text('', 
                                      coords=(self.screen_rect.centerx, 
                                              self.screen_rect.centery + 100), 
                                      font=self.err_message_font,
                                      colour=RED)

        self.title_font = get_font(size=45)
        self.texts = [
            Text('CHOOSE AN EXISTING', 
                 coords=(self.screen_rect.centerx, 80),
                 font=self.title_font),
            Text('PLAYER PROFILE', 
                 coords=(self.screen_rect.centerx, 160),
                 font=self.title_font),
            Text('Input the player name:',
                 coords=(self.screen_rect.centerx, 
                         self.screen_rect.centery - 35)),
            self.user_input_text,
            self.input_err_message
        ]

    def display(self):
        self.screen.fill(MENU_BG)

        input_colour = MENU_BTN_LIGHT if self.input_active else MENU_BTN_DARK
        pygame.draw.rect(self.screen, input_colour, self.input_rect)

        for text in self.texts:
            text.show(self.screen)

    def handle_events(self, events):
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(mouse):
                    self.input_active = True
                else:
                    self.input_active = False

            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    return self.process_user_input()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input_string = self.user_input_string[:-1]
                    self.user_input_text.set_content(self.user_input_string)
                else:
                    if len(self.user_input_string) < 12:
                        self.user_input_string += event.unicode
                        self.user_input_text.set_content(self.user_input_string)

        return 'choose_player'

    def process_user_input(self):
        if len(self.user_input_string) == 0:
            self.input_err_message.set_content('Player name cannot be empty')
        elif not self.user_input_string.isalpha():
            self.input_err_message.set_content('Player name can only contain letters')
        else:
            result = self.conn.execute('SELECT NAME FROM players WHERE NAME = ?', 
                                        (self.user_input_string,)).fetchone()
            if result is None:
                self.input_err_message.set_content('Player name not found')
            else:
                print(f'Found player name: {result[0]}')
                self.input_err_message.set_content('')
                self.selected_player = result[0]
                return 'gameplay'

        return 'choose_player'
