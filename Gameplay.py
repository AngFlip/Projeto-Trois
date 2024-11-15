import pygame
import random
from pygame.locals import *
from sys import exit

pygame.init()

# Tela inicial
screen_height = 800
screen_width = 1200
titulo_jogo = "Trois"

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(titulo_jogo)

# Configuração das cartas
card_deck = {}
for i in range(1,14):
    card_path = f"cartas\\Card_{i}.jpg"
    card_deck[i] = pygame.image.load(card_path)

# Carta fechada
card_closed = pygame.image.load(f"cartas\\Card_0.jpg")

# Definindo as cartas e embaralhando
card_value = list(range(1,14)) * 3
random.shuffle(card_value)

# Definindo jogadores
card_quantity = 7
player = [{"cartas": [], "pontos":0} for _ in range(4)]
board = card_value[4 * card_quantity:]
for i in range(4):
    player[i]["cartas"] = card_value[i * card_quantity:(i + 1) * card_quantity]
player_turn = 0

# Função de dispor as cartas na tela
def screen_update():
    screen.fill((0,100,0))

# Cartas do jogador ativo
    x_init = 100
    for idx, card_value in enumerate(player[player_turn]["cartas"]):
        card_img = card_deck[card_value]
        screen.blit(card_img, (x_init + idx * 110, screen_height - 180))

# Cartas dos demais jogadores
    #Jogador 2
    for idx in range(3):
        screen.blit(card_closed, (x_init - 25 + idx * 110, 50))

    #Jogador 3
    for idx in range(3):
        screen.blit(card_closed, (x_init - 25 + 360 + idx * 110, 50))

    #Jogador 4
    for idx in range(3):
        screen.blit(card_closed, (x_init - 25 + 720 + idx * 110, 50))

# Área da mesa
    pygame.draw.rect(screen, (0, 128, 0), (0, 230, screen_width, 340))

# Cartas na mesa
    cards_in_table = len(board)
    first_line = (cards_in_table + 1) // 2
    odd_or_even = len(board) % 2

    #Primeira linha
    for idx, card_value in enumerate(board[:first_line]):
        card_img = card_deck[card_value]
        screen.blit(card_img, (x_init + idx * 110, 255))

    #Segunda linha
    for idx, card_value in enumerate(board[first_line:]):
        card_img = card_deck[card_value]
        if odd_or_even == 0:
            screen.blit(card_img, (x_init + idx * 110, 405))
        else:
            screen.blit(card_img, (x_init + 50 + idx * 110, 405))

    pygame.display.flip()

# Função para verificar ponto
def check_trio(cards):
    if len(cards) == 3 and cards[0] == cards[1] == cards[2]:
        return True
    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            pass
    
    screen_update()

pygame.quit()