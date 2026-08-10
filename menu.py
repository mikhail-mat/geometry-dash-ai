import pygame
from constants import MENU_BG, WHITE, MENU_BTN_LIGHT, MENU_BTN_DARK

def start_menu(screen, mouse, font):
    screen.fill(MENU_BG)
    screen_rect = screen.get_rect()

    title_text = font.render("GeometryDash", True, WHITE)
    title_rect = title_text.get_rect(midtop=(screen_rect.centerx, 50))
    screen.blit(title_text, title_rect)

    play_button = pygame.Rect(0, 0, 140, 50)
    play_button.centerx = screen_rect.centerx
    play_button.centery = screen_rect.centery - 35

    quit_button = pygame.Rect(0, 0, 140, 50)
    quit_button.centerx = screen_rect.centerx
    quit_button.centery = screen_rect.centery + 35

    pygame.draw.rect(screen, 
                        MENU_BTN_LIGHT if play_button.collidepoint(mouse) else MENU_BTN_DARK, 
                        play_button, border_radius=20)
    pygame.draw.rect(screen,
                        MENU_BTN_LIGHT if quit_button.collidepoint(mouse) else MENU_BTN_DARK, 
                        quit_button, border_radius=20)
    
    play_text = font.render("Play", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)

    play_text_rect = play_text.get_rect(center=play_button.center)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)

    screen.blit(play_text, play_text_rect)
    screen.blit(quit_text, quit_text_rect)

    return (play_button, quit_button)
