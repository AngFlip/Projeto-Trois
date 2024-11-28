import pygame

# Configurações da tela
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Cartas

CARD_WIDTH = 104
CARD_HEIGHT = 134

# Cores
GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Botões
BUTTON_WIDTH = 55
BUTTON_HEIGHT = 55
BUTTON_SPACE = 15
BUTTON_COLOR = GRAY
TEXT_COLOR = BLACK

START_POS_X = 390
START_POS_Y = 325
START_WIDTH = 422
START_HEIGHT = 82

TRY_AGAIN_POS_X = 360
TRY_AGAIN_POS_Y = 470
TRY_AGAIN_WIDTH = 480
TRY_AGAIN_HEIGHT = 240

# Inicializar a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trois")

def init_pygame():
    pygame.init()
