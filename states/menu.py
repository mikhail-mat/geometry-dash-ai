import pygame
from ui import Text, Button
from constants import get_font, WHITE, MENU_BG, MENU_BTN_DARK, MENU_BTN_LIGHT


class Menu:
    def __init__(self, screen, state_name):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.state_name = state_name
        self.title_font = get_font(size=45)
        self.titles = []
        self.buttons = []

    def display(self):
        self.screen.fill(MENU_BG)
        for title in self.titles:
            title.show(self.screen)
        for button in self.buttons:
            button.show(self.screen)

    def handle_events(self, events):
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(mouse):
                        return button.action
        return self.state_name


class StartMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen, 'start_menu')

        self.titles = [
            Text('GeometryDash', 
                 coords=(self.screen_rect.centerx, 80), 
                 font=self.title_font)
        ]
        self.buttons = [
            Button(x=self.screen_rect.centerx, y=self.screen_rect.centery-35,
                   label='Play', action='player_menu'),
            Button(x=self.screen_rect.centerx, y=self.screen_rect.centery+35,
                   label='Quit', action='quit')
        ]


class PlayerMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen, 'player_menu')

        self.titles = [
            Text('CHOOSE AN EXISTING PLAYER', 
                 coords=(self.screen_rect.centerx, 80), 
                 font=self.title_font),
            Text('OR CREATE A NEW ONE',
                 coords=(self.screen_rect.centerx, 140), 
                 font=self.title_font)
        ]

        self.buttons = [
            Button(x=self.screen_rect.centerx, y=self.screen_rect.centery-35,
                   label='Choose', action='choose_player'),
            Button(x=self.screen_rect.centerx, y=self.screen_rect.centery+35,
                   label='Create', action='create_player')
        ]
