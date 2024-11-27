import pygame
from settings import screen, init_pygame
from assets import load_assets
from player import PlayerManager

pygame.init()

# Inicializações
init_pygame()
assets = load_assets()
player = PlayerManager(assets)
background = pygame.image.load(assets["bg_image"])

# Embaralha e distribui cartas
player.initialize_players()

# Loop principal
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player.handle_event(event, mouse_pos)

    # Atualizar a tela
    screen.blit(background, (0, 0))
    
    player.draw_player_hand(mouse_pos)
    player.draw_board(mouse_pos)
    player.draw_decks()
    player.draw_game_info()

    pygame.display.flip()

pygame.quit()
