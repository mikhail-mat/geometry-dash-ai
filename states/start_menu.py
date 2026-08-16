import pygame
from constants import WHITE, MENU_BG, MENU_BTN_DARK, MENU_BTN_LIGHT


class Text():
    def __init__(self, font=None, content='Blank', coords=(100,100), colour=WHITE):
        if font is None:
            font = pygame.font.SysFont('Arial', 30, bold=True)
        self.text_content = font.render(content, True, colour)
        self.text_rect = self.text_content.get_rect(center=coords)

    def show(self, screen):
        screen.blit(self.text_content, self.text_rect)


class Button():
    def __init__(self, x=100, y=100, width=140, height=50):
        self.button_rect = pygame.Rect(0, 0, width, height)
        self.button_rect.centerx = x
        self.button_rect.centery = y

    def show(self, screen, colour_light=MENU_BTN_LIGHT, 
             colour_dark=MENU_BTN_DARK, border_radius=20):
        self.mouse = pygame.mouse.get_pos()
        pygame.draw.rect(
            screen, 
            colour_light if self.button_rect.collidepoint(self.mouse) else colour_dark, 
            self.button_rect, border_radius=border_radius)


class StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        title_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.title_text = Text(content='GeometryDash', font=title_font,
                               coords=(self.screen_rect.centerx, 80), colour=WHITE)

        self.play_button = Button(x=self.screen_rect.centerx, y=self.screen_rect.centery-35)
        self.quit_button = Button(x=self.screen_rect.centerx, y=self.screen_rect.centery+35)

        self.play_text = Text(
            content='Play', 
            coords=(self.play_button.button_rect.centerx, self.play_button.button_rect.centery), 
            colour=WHITE)
        self.quit_text = Text(
            content='Quit', 
            coords=(self.quit_button.button_rect.centerx, self.quit_button.button_rect.centery), 
            colour=WHITE)

    def display(self):
        self.screen.fill(MENU_BG)
    
        self.title_text.show(self.screen)

        self.play_button.show(self.screen)
        self.quit_button.show(self.screen)
    
        self.play_text.show(self.screen)
        self.quit_text.show(self.screen)
    
    def handle_events(self, events):
        self.mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.button_rect.collidepoint(self.mouse):
                    return 'gameplay'
                elif self.quit_button.button_rect.collidepoint(self.mouse):
                    return 'quit'
        return 'start_menu'
