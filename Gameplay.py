import pygame
import random
from pygame.locals import *
import sys

pygame.init()

# Tela inicial
screen_height = 800
screen_width = 1200
titulo_jogo = "Trois"

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(titulo_jogo)

# Configuração das cartas
card_deck = {}
for i in range(1, 14):
    card_path = f"cartas\\Card_{i}.jpg"
    card_deck[i] = pygame.image.load(card_path)

# Carta fechada
card_closed = pygame.image.load(f"cartas\\Card_0.jpg")

# Definindo as cartas e embaralhando
card_value = list(range(1, 14)) * 3
random.shuffle(card_value)

# Definindo jogadores
card_quantity = 7
player = [{"cartas": [], "pontos": 0, "reveladas": []} for _ in range(4)]
board = card_value[4 * card_quantity:]
for i in range(4):
    player[i]["cartas"] = card_value[i * card_quantity:(i + 1) * card_quantity]
player_turn = 0

# Fontes
font = pygame.font.Font(None, 36)

# Botões e áreas clicáveis
buttons = []
clickable_areas = []
popup_active = False  # Flag para saber se o pop-up está ativo
popup_choice = None  # Armazenar a escolha do pop-up
popup_rect = pygame.Rect(400, 300, 400, 200)  # Retângulo do pop-up
popup_buttons = {
    "maior": pygame.Rect(470, 350, 80, 40),
    "menor": pygame.Rect(560, 350, 80, 40),
    "cancelar": pygame.Rect(650, 350, 80, 40)
}

# Lista de cartas reveladas na mesa
revealed_cards_on_table = []

# Função para desenhar a tela
def screen_update(mouse_pos):
    global buttons, clickable_areas, popup_active
    screen.fill((0, 100, 0))
    buttons = []  # Limpa a lista de botões
    clickable_areas = []  # Limpa a lista de áreas clicáveis

    # Cartas do jogador ativo
    x_init = 100
    for idx, card_value in enumerate(player[player_turn]["cartas"]):
        card_img = card_deck[card_value]
        pos_x = x_init + idx * 110
        pos_y = screen_height - 180

        # Elevar carta se o mouse estiver sobre ela
        card_rect = pygame.Rect(pos_x, pos_y, card_img.get_width(), card_img.get_height())
        if card_rect.collidepoint(mouse_pos):
            pos_y -= 20  # Eleva a carta 20 pixels

        screen.blit(card_img, (pos_x, pos_y))
        clickable_areas.append((card_rect, "player_card", idx, card_value))

    # Outros jogadores
    for i in range(4):
        if i != player_turn:
            x_offset = 100 + (i - 1) * 360
            y_offset = 50

            # Exibir as cartas (fechadas ou reveladas)
            for idx in range(3):
                if idx < len(player[i]["reveladas"]):
                    card_value = player[i]["reveladas"][idx]
                    card_img = card_deck[card_value]
                else:
                    card_img = card_closed
                screen.blit(card_img, (x_offset + idx * 110, y_offset))

            # Adicionar botão do jogador
            button_rect = pygame.Rect(x_offset, y_offset + 150, 200, 40)

            # Muda a cor do botão se o mouse estiver sobre ele
            button_color = (200, 200, 200) if button_rect.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)

            # Nome do jogador
            player_text = font.render(f"Jogador {i + 1}", True, (0, 0, 0))
            screen.blit(player_text, (x_offset + 10, y_offset + 155))
            buttons.append((button_rect, i))  # Associa o botão ao jogador

    # Cartas na mesa
    cards_in_table = len(board)
    first_line = (cards_in_table + 1) // 2
    odd_or_even = len(board) % 2

    # Primeira linha
    for idx, card_value in enumerate(board[:first_line]):
        card_img = card_deck[card_value]
        pos_x = x_init + idx * 110
        pos_y = 255

        # Elevar carta se o mouse estiver sobre ela
        card_rect = pygame.Rect(pos_x, pos_y, card_img.get_width(), card_img.get_height())
        if card_rect.collidepoint(mouse_pos):
            pos_y -= 20  # Eleva a carta 20 pixels

        # Mostrar carta revelada ou fechada
        if card_value in revealed_cards_on_table:
            screen.blit(card_img, (pos_x, pos_y))
        else:
            screen.blit(card_closed, (pos_x, pos_y))

        clickable_areas.append((card_rect, "table_card", idx + 1, card_value))

    # Segunda linha
    for idx, card_value in enumerate(board[first_line:]):
        card_img = card_deck[card_value]
        pos_x = x_init + idx * 110
        pos_y = 405 if odd_or_even == 0 else 405

        # Elevar carta se o mouse estiver sobre ela
        card_rect = pygame.Rect(pos_x, pos_y, card_img.get_width(), card_img.get_height())
        if card_rect.collidepoint(mouse_pos):
            pos_y -= 20  # Eleva a carta 20 pixels

        # Mostrar carta revelada ou fechada
        if card_value in revealed_cards_on_table:
            screen.blit(card_img, (pos_x, pos_y))
        else:
            screen.blit(card_closed, (pos_x, pos_y))

        clickable_areas.append((card_rect, "table_card", idx + first_line + 1, card_value))

    # Desenhando o pop-up se estiver ativo
    if popup_active:
        pygame.draw.rect(screen, (255, 255, 255), popup_rect)  # Fundo branco do pop-up
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)  # Borda preta

        # Texto do pop-up
        popup_text = font.render("Revelar carta maior ou menor?", True, (0, 0, 0))
        screen.blit(popup_text, (popup_rect.x + 50, popup_rect.y + 30))

        # Botões do pop-up
        pygame.draw.rect(screen, (255, 0, 0), popup_buttons["maior"])  # Botão "maior"
        pygame.draw.rect(screen, (255, 0, 0), popup_buttons["menor"])  # Botão "menor"
        pygame.draw.rect(screen, (255, 0, 0), popup_buttons["cancelar"])  # Botão "cancelar"
        
        # Texto dos botões
        maior_text = font.render("Maior", True, (255, 255, 255))
        menor_text = font.render("Menor", True, (255, 255, 255))
        cancelar_text = font.render("Cancelar", True, (255, 255, 255))

        screen.blit(maior_text, (popup_buttons["maior"].x + 10, popup_buttons["maior"].y + 10))
        screen.blit(menor_text, (popup_buttons["menor"].x + 10, popup_buttons["menor"].y + 10))
        screen.blit(cancelar_text, (popup_buttons["cancelar"].x + 10, popup_buttons["cancelar"].y + 10))

    pygame.display.flip()

# Função para revelar a carta maior ou menor
def reveal_card(player_index, maior=None):
    cartas = sorted(player[player_index]["cartas"])
    if not cartas:
        print("Não há mais cartas para revelar!")
        return

    if maior is None:  # Se maior ou menor não foi escolhido, pergunta
        print("Escolha se deseja revelar a maior ou menor carta!")
        return

    carta_revelada = cartas[-1] if maior else cartas[0]

    if len(player[player_index]["reveladas"]) < 3:
        player[player_index]["reveladas"].append(carta_revelada)
        player[player_index]["cartas"].remove(carta_revelada)
    else:
        print("Este jogador já revelou o máximo de cartas!")

# Loop principal
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica cliques nos botões dos jogadores
            for button_rect, player_index in buttons:
                if button_rect.collidepoint(mouse_pos):
                    print(f"Botão do Jogador {player_index + 1} clicado.")
                    # Abre o pop-up
                    popup_active = True
                    popup_choice = player_index

            # Verifica cliques nas cartas
            for rect, area_type, idx, card_value in clickable_areas:
                if rect.collidepoint(mouse_pos):
                    if area_type == "table_card" and card_value not in revealed_cards_on_table:
                        revealed_cards_on_table.append(card_value)

            # Verifica cliques nos botões do pop-up
            if popup_active:
                if popup_buttons["maior"].collidepoint(mouse_pos):
                    reveal_card(popup_choice, maior=True)
                    popup_active = False  # Fecha o pop-up
                elif popup_buttons["menor"].collidepoint(mouse_pos):
                    reveal_card(popup_choice, maior=False)
                    popup_active = False  # Fecha o pop-up
                elif popup_buttons["cancelar"].collidepoint(mouse_pos):
                    popup_active = False  # Fecha o pop-up

    screen_update(mouse_pos)

pygame.quit()
