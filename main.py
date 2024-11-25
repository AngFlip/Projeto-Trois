import pygame
import random
from settings import screen, init_pygame
from assets import load_assets
from board import Board
from player import PlayerManager

pygame.init()

# Inicializações
init_pygame()
assets = load_assets()
board = Board(assets)
players = PlayerManager(assets)

# Embaralha e distribui cartas
remaining_cards = players.initialize_players()
board.board = remaining_cards

# Loop principal
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
                board.handle_event(event, mouse_pos)
                players.handle_event(event, mouse_pos)

    # Verificação de fim de jogo
    players.check_game_end()

    # Atualizar a tela
    screen.fill((0, 100, 0))  # Cor de fundo
    board.draw(mouse_pos)
    players.draw_opponents()
    players.draw(mouse_pos)  
    players.draw_player_info()

    pygame.display.flip()

pygame.quit()