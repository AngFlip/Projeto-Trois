import pygame
import random
import settings
import time

class PlayerManager:

    def __init__(self, assets): 
        self.player = {
            "cartas": [],
             "pontos": 0,
             "reveladas": []}
        self.decks = [[], [], []]
        self.board = []
        self.turn_count = 1
        self.assets = assets
        self.button_rects = {}  # Inicializa os botões como um dicionário vazio
        self.last_action_time = 0
        self.action_delay = 5000

    def initialize_players(self): 
        # Embaralha as cartas
        card_value = list(enumerate(list(range(1, 14)) * 3))
        print("Iniciado: ", card_value)
        random.shuffle(card_value)
        print("Embaralhado: ", card_value)
        
        card_quantity = 7

        self.player["cartas"] = card_value[:card_quantity]
        self.decks = [card_value[card_quantity * (i + 1):card_quantity * (i + 2)] for i in range(3)]
        self.board = card_value[card_quantity * 4:]
        print("Monte: ", self.decks)

    def draw_board(self, mouse_pos):
        # Desenha as cartas da mesa
        for i, card_tuple in enumerate(self.board):
            idx, card_value = card_tuple
            card_img = self.assets["card_closed"]

            if any(revealed[0] == idx for revealed in self.player["reveladas"]):
                card_img = self.assets["card_deck"][card_value]

            pos_x = 50 + (i % 6) * 120
            pos_y = 290 if i < 6 else 440
            card_rect = pygame.Rect(pos_x, pos_y, settings.CARD_WIDTH, settings.CARD_HEIGHT)

            if card_rect.collidepoint(mouse_pos):
                pos_y -= 20 # Eleva a carta 20 pixels quando mouse passa por cima

            settings.screen.blit(card_img, (pos_x, pos_y))


    def draw_player_hand(self, mouse_pos):
        # Desenha as cartas do jogador
        x_init = 50
        for i, card_tuple in enumerate(self.player["cartas"]): 
            card_img = self.assets["card_deck"][card_tuple[1]]
            pos_x = x_init + i * 120
            pos_y = 630
            card_rect = pygame.Rect(pos_x, pos_y, settings.CARD_WIDTH, settings.CARD_HEIGHT)

            if card_rect.collidepoint(mouse_pos):
                pos_y -= 20  # Eleva a carta 20 pixels quando mouse passa por cima

            settings.screen.blit(card_img, (pos_x, pos_y))


    def draw_decks(self):
        # Desenha os montes e seus botões
        for i in range(3):
            x = 50 + i * 385
            y = 50
            for j in range(3):
                if j < len(self.decks[i]):
                    settings.screen.blit(self.assets["card_closed"], (x + j * 115, y))

            # Desenha as cartas reveladas
            revealed_cards = [card for card in self.player["reveladas"] if card in self.decks[i]]
            for k, card in enumerate(revealed_cards):
                card_img = self.assets["card_deck"][card[1]]
                pos_x = x + k * 115
                pos_y = y
                settings.screen.blit(card_img, (pos_x, pos_y))
            
            # Áreas clicáveis substituindo os botões
            left_button_area = pygame.Rect(45 + i * 385, 210, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT)
            right_button_area = pygame.Rect(45 + i * 385 + settings.BUTTON_WIDTH + settings.BUTTON_SPACE, 210, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT)

            self.button_rects[f"left_{i}"] = left_button_area
            self.button_rects[f"right_{i}"] = right_button_area


    def draw_game_info(self):
        x, y = 970, 340
        font = self.assets["button_font"]

        # Exibir número de turnos e pontos do jogador
        turn_text = font.render(f"{self.turn_count}", True, settings.WHITE)
        settings.screen.blit(turn_text, (x, y))
        points_text = font.render(f"{self.player['pontos']}", True, settings.WHITE)
        settings.screen.blit(points_text, (x, y + 135))


    def handle_event(self, event, mouse_pos):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            card = None

            # Verifica se houve cliques nas cartas da mesa
            for i, card_tuple in enumerate(self.board):
                
                idx, card_value = card_tuple
                pos_x = 50 + (i % 6) * 120
                pos_y = 290 if i < 6 else 440
                card_rect = pygame.Rect(pos_x, pos_y, settings.CARD_WIDTH, settings.CARD_HEIGHT)

                if card_rect.collidepoint(mouse_pos) and not any(revealed[0] == idx for revealed in self.player["reveladas"]):
                    self.player["reveladas"].append(card_tuple)
                    print(f"Carta escolhida da mesa: {idx} - {card_value}")
                    break

            # Verifica se houve cliques nas cartas da mão do jogador
            for i, card_tuple in enumerate(self.player["cartas"]):
                
                idx, card_value = card_tuple[0], card_tuple[1]
                pos_x = 50 + i * 120
                pos_y = 630
                card_rect = pygame.Rect(pos_x, pos_y, settings.CARD_WIDTH, settings.CARD_HEIGHT)

                if card_rect.collidepoint(mouse_pos) and idx not in self.player["reveladas"]:
                    self.player["reveladas"].append(card_tuple)
                    print(f"Carta escolhida da mão do jogador: {idx} - {card_value}")
                    break

            # Verifica se houve cliques nos botões  
            for key, button_rect in self.button_rects.items():
                if button_rect.collidepoint(mouse_pos):
                    side, deck_idx = key.split("_")
                    deck_idx = int(deck_idx)

                    # Revela a carta
                    card = self.reveal_card(deck_idx, "smaller" if side == "left" else "larger")

                    if card is not None:
                        if card not in self.player["reveladas"]:
                            self.player["reveladas"].append(card)
                            print(f"Carta escolhida do monte {deck_idx}: {card}")
   

            print("Escolhas: ", self.player['reveladas'])

            # Verifica se fez as 3 jogadas e se as cartas são iguais
            if len(self.player["reveladas"]) == 3:
                

                if len(set(self.player["reveladas"])) == 1:
                    self.player["pontos"] += 1
                    print("Ponto marcado! Todas as cartas são iguais.")

                # Avança para o próximo turno
                self.turn_count += 1

                # Reseta a seleção de cartas
                self.player["reveladas"].clear()

                print(f"Turno {self.turn_count} iniciado.")
        

    def reveal_card(self, deck_idx, choice):
        deck = self.decks[deck_idx]
        revealed_cards = self.player["reveladas"]

        remaining_cards = [c for c in deck if c not in revealed_cards]  # Filtra as cartas restantes no deck
        if not remaining_cards:
            return  # Se não houver mais cartas para revelar, retorna

        # Escolhe a carta com base na opção "larger" ou "smaller" (usa segundo valor da tupla)
        card = max(remaining_cards, key=lambda c: c[1]) if choice == "larger" else min(remaining_cards, key=lambda c: c[1])
        revealed_cards.append(card)

        return card
