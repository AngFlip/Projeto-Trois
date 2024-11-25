import pygame

def load_assets():
    card_deck = {}
    for i in range(1, 14):
        card_path = f"cartas\\Card_{i}.jpg"
        card_deck[i] = pygame.image.load(card_path)

    card_closed = pygame.image.load(f"cartas\\Card_0.jpg")

    assets = {
        "card_deck": card_deck,
        "card_closed": card_closed,
        "button_font": pygame.font.Font(None, 36)
    }

    return assets