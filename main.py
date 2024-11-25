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

# Adicionar algumas cartas à mesa
remaining_cards = players.initialize_players()  # Já distribui as cartas para os jogadores
board.board = remaining_cards  # Adiciona as cartas restantes no tabuleiro

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