import pygame

# Configurações da tela
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Cores
GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Inicializar a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trois")

def init_pygame():
    pygame.init()