import inicio
import jogo

# Inicializa o jogo
def main():
    tela_atual = "inicio"
    while True:
        if tela_atual == "inicio":
            tela_atual = inicio.executar()
        elif tela_atual == "jogo":
            tela_atual = jogo.executar()

if __name__ == "__main__":
    main()
