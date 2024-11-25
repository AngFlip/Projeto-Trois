import pygame
import sys
import os

# Inicializa o Pygame
pygame.init()

# Configurações básicas
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Capa do Jogo")

# Caminho do arquivo da imagem de fundo
caminho_imagem = r"C:\projeto1\trois.png"

# Verificar se o arquivo existe
if not os.path.exists(caminho_imagem):
    print(f"Erro: Arquivo não encontrado em {caminho_imagem}")
    sys.exit()

# Carregar imagem de fundo
try:
    imagem_fundo = pygame.image.load(caminho_imagem)
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    sys.exit()

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 200, 0)
VERDE_CLARO = (0, 255, 0)

# Fonte
fonte = pygame.font.Font(None, 50)

# Função para desenhar botão
def desenhar_botao(texto, x, y, largura, altura, cor_normal, cor_hover):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()

    # Detecta se o mouse está sobre o botão
    if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
        pygame.draw.rect(TELA, cor_hover, (x, y, largura, altura))  # Cor ao passar o mouse
        if clique[0]:  # Clique esquerdo
            return True
    else:
        pygame.draw.rect(TELA, cor_normal, (x, y, largura, altura))  # Cor padrão

    # Renderizar o texto no botão
    texto_surface = fonte.render(texto, True, BRANCO)
    texto_rect = texto_surface.get_rect(center=(x + largura // 2, y + altura // 2))
    TELA.blit(texto_surface, texto_rect)
    return False

# Função principal
def tela_inicial():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Desenhar a imagem de fundo
        TELA.blit(imagem_fundo, (0, 0))

        # Desenhar botão de iniciar
        if desenhar_botao("Iniciar", 300, 400, 200, 70, VERDE, VERDE_CLARO):
            return  # Sai do loop e inicia o jogo

        # Atualizar a tela
        pygame.display.flip()

# Loop principal do jogo
def jogo():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fundo do jogo (apenas branco, por enquanto)
        TELA.fill(BRANCO)

        # Atualizar a tela
        pygame.display.flip()

# Fluxo do programa
tela_inicial()
jogo()
