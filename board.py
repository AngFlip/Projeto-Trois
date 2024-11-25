import pygame
from settings import screen

class Board:
    def __init__(self, assets):
        self.board = []
        self.revealed_cards = []
        self.assets = assets

    def draw(self, mouse_pos):
        for idx, card_value in enumerate(self.board):
            card_img = self.assets["card_closed"]
            if idx in self.revealed_cards:
                card_img = self.assets["card_deck"][card_value]

            if idx < 6:  # Primeira linha (6 cartas)
                pos_x = 100 + idx * 110
                pos_y = 280
            else:  # Segunda linha (5 cartas)
                pos_x = 100 + (idx - 6) * 110
                pos_y = 430

            # Elevar carta se o mouse estiver sobre ela
            card_rect = pygame.Rect(pos_x, pos_y, card_img.get_width(), card_img.get_height())
            if card_rect.collidepoint(mouse_pos):
                pos_y -= 20

            screen.blit(card_img, (pos_x, pos_y))

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, card_value in enumerate(self.board):
                if idx < 6:
                    pos_x = 100 + idx * 110
                    pos_y = 280
                else:
                    pos_x = 100 + (idx - 6) * 110
                    pos_y = 430

                card_rect = pygame.Rect(pos_x, pos_y, self.assets["card_closed"].get_width(), self.assets["card_closed"].get_height())

                if card_rect.collidepoint(mouse_pos) and idx not in self.revealed_cards:
                    self.revealed_cards.append(idx)  # Revela a carta
                    break
