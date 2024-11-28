import os
import pygame

def load_assets():
    card_deck = {}
    for i in range(1, 14):
        card_path = os.path.join("assets", "cartas", f"Card_{i}.jpg")
        card_deck[i] = pygame.image.load(card_path)

    # imagens
    start_image = pygame.image.load(os.path.join("assets", "imagens", "Start.png"))
    bg_image = pygame.image.load(os.path.join("assets", "imagens", "Board.png"))
    card_closed = pygame.image.load(os.path.join("assets","cartas", "Card_0.jpg"))
    victory_image = pygame.image.load(os.path.join("assets", "imagens", "Victory.png"))
    defeat_image = pygame.image.load(os.path.join("assets", "imagens", "Defeat.png"))

    # fontes
    font_path = os.path.join("assets", "fontes", "Marhey-Regular.ttf")

    # sons
    win = os.path.join("assets", "sons", "Win.mp3")
    initial = os.path.join("assets", "sons", "Initial.mp3")
    lose = os.path.join("assets", "sons", "Lose.mp3")
    click = pygame.mixer.Sound(os.path.join("assets", "sons", "Card_Click.mp3"))
    score = pygame.mixer.Sound(os.path.join("assets", "sons", "Get_Point.mp3"))
    wrong = pygame.mixer.Sound(os.path.join("assets", "sons", "Wrong.mp3"))

    assets = {
        "card_deck": card_deck,
        "card_closed": card_closed,
        "button_font": pygame.font.Font(font_path, 70),
        "background": bg_image,
        "victory": victory_image,
        "defeat": defeat_image,
        "start": start_image,
        "win": win,
        "lose": lose,
        "click": click,
        "score": score,
        "wrong": wrong,
        "initial": initial
    }

    return assets
