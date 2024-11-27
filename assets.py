import os
import pygame

def load_assets():
    card_deck = {}
    for i in range(1, 14):
        card_path = os.path.join("assets", "cartas", f"Card_{i}.jpg")
        card_deck[i] = pygame.image.load(card_path)

    card_closed = pygame.image.load(os.path.join("assets\cartas", "Card_0.jpg"))

    bg_image = os.path.join("assets", "imagens", "Board.png")
    font_path = os.path.join("assets", "fontes", "Marhey-Regular.ttf")

    assets = {
        "card_deck": card_deck,
        "card_closed": card_closed,
        "button_font": pygame.font.Font(font_path, 70),
        "bg_image": bg_image
        
    }

    return assets
