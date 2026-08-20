import pygame
from .menu import Text
from constants import get_font, MENU_BG, MENU_BTN_DARK, MENU_BTN_LIGHT, BLACK, RED


class InputField:
    def __init__(self, coords, label, max_chars=12, width=300, height=50):
        self.max_chars = max_chars
        self.input_rect = pygame.Rect(0, 0, width, height)
        self.input_rect.center = coords
        self.input_active = False
        self.input_label = Text(label,
                                coords=(self.input_rect.centerx, 
                                self.input_rect.centery - 50))
        self.user_input_string = ''
        self.user_input = Text(self.user_input_string, 
                               coords=self.input_rect.center,
                               colour=BLACK)
        self.error_message = Text('', 
                                  coords=(self.input_rect.centerx, 
                                          self.input_rect.centery + 50), 
                                  font=get_font(size=20),
                                  colour=RED)

    def show(self, screen):
        input_colour = MENU_BTN_LIGHT if self.input_active else MENU_BTN_DARK
        pygame.draw.rect(screen, input_colour, self.input_rect)
        self.input_label.show(screen)
        self.user_input.show(screen)
        self.error_message.show(screen)

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
                    self.user_input.set_content(self.user_input_string)
                elif event.unicode and len(self.user_input_string) < self.max_chars:
                    self.user_input_string += event.unicode
                    self.user_input.set_content(self.user_input_string)
        return None

    def process_user_input(self):
        raise NotImplementedError

    def reset(self):
        self.user_input_string = ''
        self.user_input.set_content('')
        self.error_message.set_content('')
        self.input_active = False


class ChoosePlayerInput(InputField):
    def __init__(self, coords, conn):
        super().__init__(coords, label='Input player name:')
        self.conn = conn

    def process_user_input(self):
        if len(self.user_input_string) == 0:
            self.error_message.set_content('Player name cannot be empty')
        elif not self.user_input_string.isalpha():
            self.error_message.set_content('Player name can only contain letters')
        else:
            result = self.conn.execute('SELECT NAME, BEST_SCORE FROM players WHERE NAME = ?', 
                                       (self.user_input_string,)).fetchone()
            if result is None:
                self.error_message.set_content('Player name not found')
            else:
                self.reset()
                return result

        return None


class ChoosePlayer:
    def __init__(self, screen, conn):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.input_field = ChoosePlayerInput(coords=(self.screen_rect.center),
                                             conn=conn)

        self.title_font = get_font(size=45)
        self.titles = [
            Text('CHOOSE AN EXISTING', 
                 coords=(self.screen_rect.centerx, 80),
                 font=self.title_font),
            Text('PLAYER PROFILE', 
                 coords=(self.screen_rect.centerx, 140),
                 font=self.title_font)
        ]

    def display(self):
        self.screen.fill(MENU_BG)
        for title in self.titles:
            title.show(self.screen)
        self.input_field.show(self.screen)

    def handle_events(self, events):
        result = self.input_field.handle_events(events)
        if result is not None:
            self.selected_player = result[0]
            self.best_score = result[1]
            return 'gameplay'
        return 'choose_player'
