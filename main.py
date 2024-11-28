import pygame
import sys
import settings
from assets import load_assets
from player import PlayerManager

STATE_START = "start"
STATE_PLAYING = "playing"
STATE_END = "end"

settings.init_pygame()
assets = load_assets()

def show_start_screen(screen, assets):
    screen.blit(assets['start'], (0, 0))
    pygame.display.flip()

def show_game_screen(screen, assets):
    screen.fill((0, 0, 0))
    screen.blit(assets['background'], (0, 0))

def show_end_screen(screen, assets, victory):
    if victory:
        end_image = assets['victory']
    else:
        end_image = assets['defeat']
    screen.blit(end_image, (0, 0))
    pygame.display.flip()

def main():
    screen = settings.screen
    clock = pygame.time.Clock()

    game_state = STATE_START
    running = True
    victory = False
    player_manager = None

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == STATE_START:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    start_button_rect = pygame.Rect(settings.START_POS_X, settings.START_POS_Y, settings.START_WIDTH, settings.START_HEIGHT)
                    if start_button_rect.collidepoint(mouse_pos):
                        game_state = STATE_PLAYING
                        player_manager = PlayerManager(assets)
                        player_manager.initialize_players()

            elif game_state == STATE_PLAYING:
                if player_manager:
                    player_manager.handle_event(event, mouse_pos)
                    if player_manager.win_condition:
                        victory = True
                        game_state = STATE_END
                    elif player_manager.turn_count > 15:
                        victory = False
                        game_state = STATE_END

            elif game_state == STATE_END:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    restart_button_rect = pygame.Rect(settings.TRY_AGAIN_POS_X, settings.TRY_AGAIN_POS_Y,settings.TRY_AGAIN_WIDTH, settings.TRY_AGAIN_HEIGHT)
                    if restart_button_rect.collidepoint(mouse_pos):
                        game_state = STATE_START

        # Renderizar a tela com base no estado atual
        if game_state == STATE_START:
            show_start_screen(screen, assets)
        elif game_state == STATE_PLAYING:
            show_game_screen(screen, assets)
            if player_manager:
                mouse_pos = pygame.mouse.get_pos()
                player_manager.draw_board(mouse_pos)
                player_manager.draw_player_hand(mouse_pos)
                player_manager.draw_decks()
                player_manager.draw_game_info()
            pygame.display.flip()
        elif game_state == STATE_END:
            show_end_screen(screen, assets, victory)

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()