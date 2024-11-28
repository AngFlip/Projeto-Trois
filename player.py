import pygame
import random
import settings

class PlayerManager:
    def __init__(self, assets):
        self.restart_requested = False 
        self.player = {
            "cartas": [],
             "pontos": 0,
             "reveladas": []}
        self.decks = [[], [], []]
        self.board = []
        self.turn_count = 1
        self.assets = assets
        self.button_rects = {}  # Inicializa os botões como um dicionário vazio
        self.action_delay = 1000  # 1 segundo
        self.validation_time = 0
        self.waiting_for_validation = False
        self.plus_point = False
        self.win_condition = False

        self.click_sound = assets["click"]
        self.score_sound = assets["score"]
        self.wrong_sound = assets["wrong"]
        
    def initialize_players(self): 
        # Embaralha as cartas
        card_value = list(enumerate(list(range(1, 14)) * 3))
        random.shuffle(card_value)
        
        card_quantity = 7
        self.player["cartas"] = card_value[:card_quantity]
        self.decks = [card_value[card_quantity * (i + 1):card_quantity * (i + 2)] for i in range(3)]
        self.board = card_value[card_quantity * 4:]

    def draw_board(self, mouse_pos):
        # Distribui as cartas da mesa
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
        # Distribui as cartas do jogador
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
        # Define os montes e seus botões
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
            
            # Áreas dps botões
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
        
        if self.waiting_for_validation:
            if pygame.time.get_ticks() - self.validation_time >= self.action_delay:
                self.waiting_for_validation = False
                # Remove cartas e limpa a seleção
                if self.plus_point: self.remove_cards()
                self.player["reveladas"].clear()
                # Avança um turno
                self.turn_count += 1 
                print(f"Turno {self.turn_count} iniciado.")
            return

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
                    self.click_sound.play()
                    break

            # Verifica se houve cliques nas cartas da mão do jogador
            for i, card_tuple in enumerate(self.player["cartas"]):
                
                idx, card_value = card_tuple[0], card_tuple[1]
                pos_x = 50 + i * 120
                pos_y = 630
                card_rect = pygame.Rect(pos_x, pos_y, settings.CARD_WIDTH, settings.CARD_HEIGHT)

                if card_rect.collidepoint(mouse_pos) and idx not in self.player["reveladas"]:
                    self.player["reveladas"].append(card_tuple)
                    self.click_sound.play()
                    break

            # Verifica se houve cliques nos botões  
            for key, button_rect in self.button_rects.items():
                if button_rect.collidepoint(mouse_pos):
                    self.click_sound.play()
                    side, deck_idx = key.split("_")
                    deck_idx = int(deck_idx)

                    # Revela a carta
                    card = self.reveal_card(deck_idx, "smaller" if side == "left" else "larger")

                    if card is not None:
                        if card not in self.player["reveladas"]:
                            self.player["reveladas"].append(card)

            # Verifica se fez as 3 jogadas e se as cartas são iguais
            if len(self.player["reveladas"]) == 3:
                print("Escolhas: ", self.player['reveladas'])
                self.waiting_for_validation = True
                self.validation_time = pygame.time.get_ticks()

                self.check_and_score()
                

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

    def check_and_score(self):

        if len(self.player["reveladas"]) == 3:
            
            self.plus_point = False
            self.win_condition = False

            card_values = [card[1] for card in self.player["reveladas"]]
            if len(set(card_values)) == 1 and card_values[0] == 7:
                self.win_condition = True
                self.score_sound.play()
            elif len(set(card_values)) == 1:
                self.player["pontos"] += 1
                self.plus_point = True
                self.score_sound.play()
                if self.player["pontos"] >= 7:
                    self.win_condition = True
            else:
                self.wrong_sound.play()

            self.waiting_for_removal = True
            self.validation_time = pygame.time.get_ticks()

    def remove_cards(self):

        for card in self.player["reveladas"]:
            self.player["cartas"] = [c for c in self.player["cartas"] if c[0] != card[0]]

        for card in self.player["reveladas"]:
            self.board = [c for c in self.board if c[0] != card[0]]

        for card in self.player["reveladas"]:
            for deck in self.decks:
                deck[:] = [c for c in deck if c[0] != card[0]]