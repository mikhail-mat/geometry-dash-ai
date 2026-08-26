from ui import Text, InputField
from constants import get_font, MENU_BG


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
            result = self.conn.execute('SELECT * FROM players WHERE NAME = ?', 
                                       (self.user_input_string,)).fetchone()
            if result is None:
                self.error_message.set_content('Player name not found')
            else:
                self.reset()
                return result
        return None


class SelectPlayer:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.title_font = get_font(size=45)
        self.titles = []
        self.input_field = InputField(coords=(0,0), label='Input:')

    def display(self):
        self.screen.fill(MENU_BG)
        for title in self.titles:
            title.show(self.screen)
        self.input_field.show(self.screen)

    def handle_events(self, events):
        raise NotImplementedError


class ChoosePlayer(SelectPlayer):
    def __init__(self, screen, conn):
        super().__init__(screen)
        self.input_field = ChoosePlayerInput(coords=(self.screen_rect.center),
                                             conn=conn)
        self.titles = [
            Text('CHOOSE AN EXISTING', 
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
        return 'choose_player'
