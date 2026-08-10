import pygame
from menu import start_menu
from constants import GAME_BG, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BG, WHITE, MENU_BTN_LIGHT, MENU_BTN_DARK

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('GeometryDash')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.states = ('start_menu', 'choose_player', 'gameplay', 'game_over', 'quit')
        self.current_state = 'start_menu'

        self.start_menu = StartMenu(self.screen)
        self.gameplay = Gameplay(self.screen)

    def run(self):
        game_open = True

        while game_open:
            events = pygame.event.get()

            for event in pygame.event.get():
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

        pygame.quit()


class Gameplay():
    def __init__(self, screen):
        self.screen = screen
        self.og_player_img = pygame.image.load('player.png').convert_alpha()
        self.player_img = pygame.transform.scale(self.og_player_img, (80, 80))
        self.player_coords = (375,400)

    def display(self):
        self.screen.fill(GAME_BG)
        self.screen.blit(self.player_img, self.player_coords)

    def handle_events(self, events):
        return 'gameplay' # replace later


class StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.font = pygame.font.SysFont('Arial', 30, bold=True)

        self.title_text = self.font.render("GeometryDash", True, WHITE)
        self.title_rect = self.title_text.get_rect(midtop=(self.screen_rect.centerx, 50))

        self.play_button = pygame.Rect(0, 0, 140, 50)
        self.quit_button = pygame.Rect(0, 0, 140, 50)

        self.play_button.centerx = self.screen_rect.centerx
        self.play_button.centery = self.screen_rect.centery - 35
    
        self.quit_button.centerx = self.screen_rect.centerx
        self.quit_button.centery = self.screen_rect.centery + 35

        self.play_text = self.font.render("Play", True, WHITE)
        self.quit_text = self.font.render("Quit", True, WHITE)
        self.play_text_rect = self.play_text.get_rect(center=self.play_button.center)
        self.quit_text_rect = self.quit_text.get_rect(center=self.quit_button.center)

    def display(self):
        self.screen.fill(MENU_BG)
    
        self.screen.blit(self.title_text, self.title_rect)

        self.mouse = pygame.mouse.get_pos()
        pygame.draw.rect(self.screen, 
                            MENU_BTN_LIGHT if self.play_button.collidepoint(self.mouse) else MENU_BTN_DARK, 
                            self.play_button, border_radius=20)
        pygame.draw.rect(self.screen,
                            MENU_BTN_LIGHT if self.quit_button.collidepoint(self.mouse) else MENU_BTN_DARK, 
                            self.quit_button, border_radius=20)
    
        self.screen.blit(self.play_text, self.play_text_rect)
        self.screen.blit(self.quit_text, self.quit_text_rect)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(self.mouse):
                    return 'gameplay'
                elif self.quit_button.collidepoint(self.mouse):
                    return 'quit'
        return 'start_menu'

if __name__ == '__main__':
    game = Game()
    game.run()

# pygame.init()

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# font = pygame.font.SysFont('Arial', 30, bold=True)

# pygame.display.set_caption('GeometryDash')

# og_player_img = pygame.image.load('player.png').convert_alpha()
# og_width, og_height = og_player_img.get_size()
# player_img = pygame.transform.scale(og_player_img, (80, 80))
# player_coords = (375,400)

# def game():
#     game_running = True
#     while game_running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 game_running = False
        
#         screen.fill(GAME_BG)
#         screen.blit(player_img, player_coords)

#         pygame.display.update()

# menu_running = True
# while menu_running:
#     mouse = pygame.mouse.get_pos()
#     play_btn, quit_btn = start_menu(screen, mouse, font)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             menu_running = False

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if play_btn.collidepoint(mouse):
#                 game()

#             if quit_btn.collidepoint(mouse):
#                 menu_running = False

#     pygame.display.update()
