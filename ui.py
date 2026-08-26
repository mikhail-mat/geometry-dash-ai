import pygame
from constants import get_font, WHITE, BLACK, RED, MENU_BTN_LIGHT, MENU_BTN_DARK


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
