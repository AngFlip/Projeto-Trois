import pygame
import random
from settings import screen

class PlayerManager:
    def __init__(self, assets):
        self.players = [{"cartas": [], "pontos": 0, "reveladas": [], "nome": f"Jogador {i+1}"} for i in range(4)]
        self.player_turn = 0
        self.assets = assets
        self.current_selection = []     # Cartas selecionadas para formar um trio
        self.selecting_cards = False    # Se o jogador está no processo de seleção
        self.button_rects = {}

    # Embaralhar e distribuir cartas
    def initialize_players(self):
        card_value = list(range(1, 14)) * 3
        random.shuffle(card_value)
        card_quantity = 7
        for i in range(4):
            self.players[i]["cartas"] = card_value[i * card_quantity:(i + 1) * card_quantity]
        return card_value[4 * card_quantity:]

    # Desenha as cartas do jogador atual
    def draw(self, mouse_pos):
        x_init = 100
        for idx, card_value in enumerate(self.players[self.player_turn]["cartas"]):
            card_img = self.assets["card_deck"][card_value]
            pos_x = x_init + idx * 110
            pos_y = screen.get_height() - 180
            card_rect = pygame.Rect(pos_x, pos_y, card_img.get_width(), card_img.get_height())

            if card_rect.collidepoint(mouse_pos):
                pos_y -= 20  # Eleva a carta 20 pixels

            screen.blit(card_img, (pos_x, pos_y))

    # Desenha os oponentes e suas cartas reveladas
    def draw_opponents(self):
        for i in range(4):
            if i == self.player_turn:
                continue  # Pula o jogador atual

            # Exibir o nome do jogador
            x = 50 + (i - 1) * 375
            y = 20
            font = pygame.font.Font(None, 30)
            text = font.render(f"Jogador {i+1}", True, (255, 255, 255))
            screen.blit(text, (x + 110, y))

            # Exibir cartas reveladas ou cartas fechadas
            y = 50
            for j in range(3):
                if j < len(self.players[i]["reveladas"]):
                    card_value = self.players[i]["reveladas"][j]
                    card_img = self.assets["card_deck"][card_value]
                else:
                    card_img = self.assets["card_closed"]
                screen.blit(card_img, (x + j * 110, y))

            # Configurar botões
            button_width = 100
            button_height = 40
            space_between_buttons = 15
            text_color = (0, 0, 0)
            font = self.assets["button_font"]

            # Botão esquerdo (Menor)
            button_left = pygame.Rect(x + 50, y + 145, button_width, button_height)
            pygame.draw.rect(screen, (200, 200, 200), button_left)
            text_left = font.render("Menor", True, text_color)
            text_left_rect = text_left.get_rect(center=button_left.center)
            screen.blit(text_left, text_left_rect)

            # Botão direito (Maior)
            button_right = pygame.Rect(button_left.right + space_between_buttons, y + 145, button_width, button_height)
            pygame.draw.rect(screen, (200, 200, 200), button_right)
            text_right = font.render("Maior", True, text_color)
            text_right_rect = text_right.get_rect(center=button_right.center)
            screen.blit(text_right, text_right_rect)

            # Atualizar os botões no dicionário de retângulos
            self.button_rects[f"button_left_{i}"] = button_left
            self.button_rects[f"button_right_{i}"] = button_right

    def draw_player_info(self):
        x_offset = screen.get_width() - 300
        y_offset = 325

        current_player_name = self.players[self.player_turn]["nome"]
        font = pygame.font.Font(None, 30)
        text = font.render(f"Jogador Atual: {current_player_name}", True, (255, 255, 255))
        screen.blit(text, (x_offset, y_offset))

        y_offset += 80

        for i, player in enumerate(self.players):
            text = font.render(f"{player['nome']}: {player['pontos']} pontos", True, (255, 255, 255))
            screen.blit(text, (x_offset, y_offset))
            y_offset += 30

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, button_rect in self.button_rects.items():
                if button_rect.collidepoint(mouse_pos):
                    _, action, player_idx = key.split("_")
                    player_idx = int(player_idx)

                    if action == "left":
                        self.choose_smaller(player_idx)
                    elif action == "right":
                        self.choose_larger(player_idx)

            if self.selecting_cards:
                for idx, card_value in enumerate(self.players[self.player_turn]["cartas"]):
                    pos_x = 100 + idx * 110
                    pos_y = screen.get_height() - 180
                    card_rect = pygame.Rect(
                        pos_x, pos_y, 
                        self.assets["card_deck"][card_value].get_width(),
                        self.assets["card_deck"][card_value].get_height()
                    )

                    if card_rect.collidepoint(mouse_pos) and card_value not in self.current_selection:
                        self.current_selection.append(card_value)
                        break

            if len(self.current_selection) == 3:
                self.selecting_cards = False
                self.check_for_set()

    def choose_smaller(self, player_idx):
        self.reveal_card(player_idx, "smaller")

    def choose_larger(self, player_idx):
        self.reveal_card(player_idx, "larger")

    def reveal_card(self, player_idx, choice):
        player_cards = self.players[player_idx]["cartas"]
        revealed_cards = self.players[player_idx]["reveladas"]

        remaining_cards = [c for c in player_cards if c not in revealed_cards]
        if not remaining_cards:
            return

        card = max(remaining_cards) if choice == "larger" else min(remaining_cards)
        revealed_cards.append(card)

    def check_for_set(self):
        if len(set(self.current_selection)) == 1:
            self.players[self.player_turn]["pontos"] += 1
            for card_value in self.current_selection:
                self.players[self.player_turn]["cartas"].remove(card_value)
            self.current_selection.clear()

    def check_game_end(self):
        for i, player in enumerate(self.players):
            if player["pontos"] >= 3:
                print(f"Jogador {i + 1} venceu!")
                pygame.quit()
                exit()

    def end_turn(self):
        self.players[self.player_turn]["reveladas"] = []
        self.player_turn = (self.player_turn + 1) % 4

