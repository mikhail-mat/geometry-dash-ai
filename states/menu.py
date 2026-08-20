import pygame
from constants import get_font, WHITE, MENU_BG, MENU_BTN_DARK, MENU_BTN_LIGHT


class Text:
    def __init__(self, content, coords, font=None, colour=WHITE):
        if font is None:
            font = get_font()
        self.font = font
        self.colour = colour
        self.coords = coords
        self.set_content(content)

    def set_content(self, content):
        self.text_content = self.font.render(content, True, self.colour)
        self.text_rect = self.text_content.get_rect(center=self.coords)

    def show(self, screen):
        screen.blit(self.text_content, self.text_rect)


class Button:
    def __init__(self, x, y, label, action, width=140, height=50, font=None):
        self.button_rect = pygame.Rect(0, 0, width, height)
        self.button_rect.center = (x, y)
        self.text = Text(content=label,
                         coords=self.button_rect.center,
                         font=font)
        self.action = action
         
    def show(self, screen):
        mouse = pygame.mouse.get_pos()
        colour = MENU_BTN_LIGHT if self.button_rect.collidepoint(mouse) else MENU_BTN_DARK
        pygame.draw.rect(screen, colour, self.button_rect, border_radius=20)
        self.text.show(screen)

    def is_clicked(self, mouse):
        return self.button_rect.collidepoint(mouse)


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
