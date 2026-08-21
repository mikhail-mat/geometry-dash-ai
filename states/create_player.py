import pygame
from .choose_player import InputField, SelectPlayer
from .menu import Text


class CreatePlayerInput(InputField):
    def __init__(self, coords, conn):
        super().__init__(coords, label='Enter player name to create:')
        self.conn = conn

    def process_user_input(self):
        if len(self.user_input_string) == 0:
            self.error_message.set_content('Player name cannot be empty')
        elif not self.user_input_string.isalpha():
            self.error_message.set_content('Player name can only contain letters')
        else:
            result = self.conn.execute('SELECT * FROM players WHERE NAME = ?', 
                                        (self.user_input_string,)).fetchone()
            if result is None:
                self.conn.execute('INSERT INTO players (NAME, BEST_SCORE) VALUES (?, ?)', 
                                  (self.user_input_string, 0))
                self.conn.commit()
                self.reset()
                return (self.user_input_string, 0)
            else:
                self.error_message.set_content('Player name already exists')
        return None


class CreatePlayer(SelectPlayer):
    def __init__(self, screen, conn):
        super().__init__(screen)
        self.input_field = CreatePlayerInput(coords=(self.screen_rect.center),
                                             conn=conn)
        self.titles = [
            Text('CREATE A NEW', 
                    coords=(self.screen_rect.centerx, 80),
                    font=self.title_font),
            Text('PLAYER PROFILE', 
                    coords=(self.screen_rect.centerx, 140),
                    font=self.title_font)
        ]

    def handle_events(self, events):
        result = self.input_field.handle_events(events)
        if result is not None:
            self.selected_player = result[0]
            self.best_score = result[1]
            return 'gameplay'
        return 'create_player'
