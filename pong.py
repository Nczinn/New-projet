import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Pong")

# Cores
branco = (255, 255, 255)
vermelho = (255, 0, 0)
azul_escuro = (0, 0, 139)  # Cor azul escuro
preto = (0, 0, 0)

# Configurações das raquetes
largura_raquete = 15
altura_raquete = 100
velocidade_raquete = 10

# Posições iniciais das raquetes
raquete1_x = 50
raquete1_y = altura_tela // 2 - altura_raquete // 2

raquete2_x = largura_tela - 50 - largura_raquete
raquete2_y = altura_tela // 2 - altura_raquete // 2

# Configurações da bola
largura_bola = 15
altura_bola = 15
bola_x = largura_tela // 2 - largura_bola // 2
bola_y = altura_tela // 2 - altura_bola // 2
velocidade_bola_x = 7 * random.choice((1, -1))
velocidade_bola_y = 7 * random.choice((1, -1))
incremento_velocidade = 1.1  # Fator de incremento da velocidade da bola

# Placar
placar_jogador1 = 0
placar_jogador2 = 0

# Fonte do placar
fonte_placar = pygame.font.Font(None, 50)

# Configuração fixa do bot
velocidade_bot = velocidade_raquete
precision = 1  # Dificuldade média

# Carregar a imagem de fundo
imagem_fundo = pygame.image.load('fundo pong.png')
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura_tela, altura_tela))  # Redimensionar para caber na tela

# Função para desenhar os elementos na tela
def desenhar():
    tela.blit(imagem_fundo, (0, 0))  # Desenhar a imagem de fundo
    pygame.draw.rect(tela, vermelho, (raquete1_x, raquete1_y, largura_raquete, altura_raquete))  # Raquete 1 vermelha
    pygame.draw.rect(tela, azul_escuro, (raquete2_x, raquete2_y, largura_raquete, altura_raquete))  # Raquete 2 azul escuro
    pygame.draw.ellipse(tela, branco, (bola_x, bola_y, largura_bola, altura_bola))

    # Desenhar o placar
    texto_placar = fonte_placar.render(f"{placar_jogador1}  -  {placar_jogador2}", True, branco)
    tela.blit(texto_placar, (largura_tela // 2 - texto_placar.get_width() // 2, 20))

    pygame.display.flip()

# Função para mostrar o menu inicial com seleção por mouse
def mostrar_menu():
    tela.fill(preto)
    fonte_titulo = pygame.font.Font(None, 100)
    fonte_opcao = pygame.font.Font(None, 50)

    texto_titulo = fonte_titulo.render("PONG", True, branco)
    texto_vs_bot = fonte_opcao.render("Jogar contra Bot", True, branco)
    texto_vs_amigo = fonte_opcao.render("Jogar contra Amigo", True, branco)

    # Obter os retângulos para posicionamento e detecção de clique
    titulo_rect = texto_titulo.get_rect(center=(largura_tela // 2, 150))
    vs_bot_rect = texto_vs_bot.get_rect(center=(largura_tela // 2, 300))
    vs_amigo_rect = texto_vs_amigo.get_rect(center=(largura_tela // 2, 400))

    # Desenhar os textos na tela
    tela.blit(texto_titulo, titulo_rect)
    tela.blit(texto_vs_bot, vs_bot_rect)
    tela.blit(texto_vs_amigo, vs_amigo_rect)
    pygame.display.flip()

    # Loop para esperar a escolha do jogador
    escolha = None
    while escolha is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Botão esquerdo do mouse
                mouse_pos = evento.pos
                if vs_bot_rect.collidepoint(mouse_pos):
                    escolha = "bot"
                elif vs_amigo_rect.collidepoint(mouse_pos):
                    escolha = "amigo"
    return escolha

# Função para iniciar o jogo
def iniciar_jogo(modo):
    global raquete1_y, raquete2_y, bola_x, bola_y, velocidade_bola_x, velocidade_bola_y, placar_jogador1, placar_jogador2
    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Movimentação da raquete 1 (controlada pelo jogador)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and raquete1_y > 0:
            raquete1_y -= velocidade_raquete
        if teclas[pygame.K_s] and raquete1_y < altura_tela - altura_raquete:
            raquete1_y += velocidade_raquete

        if modo == "amigo":
            # Movimentação da raquete 2 (controlada pelo segundo jogador)
            if teclas[pygame.K_UP] and raquete2_y > 0:
                raquete2_y -= velocidade_raquete
            if teclas[pygame.K_DOWN] and raquete2_y < altura_tela - altura_raquete:
                raquete2_y += velocidade_raquete
        else:
            # Movimentação da raquete 2 (controlada pelo bot)
            if raquete2_y + altura_raquete / 2 < bola_y - (altura_bola * precision):
                raquete2_y += velocidade_bot
            elif raquete2_y + altura_raquete / 2 > bola_y + (altura_bola * precision):
                raquete2_y -= velocidade_bot

            # Mantém a raquete do bot dentro da tela
            if raquete2_y < 0:
                raquete2_y = 0
            if raquete2_y > altura_tela - altura_raquete:
                raquete2_y = altura_tela - altura_raquete

        # Movimentação da bola
        bola_x += velocidade_bola_x
        bola_y += velocidade_bola_y

        # Colisões com a parede superior e inferior
        if bola_y <= 0 or bola_y >= altura_tela - altura_bola:
            velocidade_bola_y *= -1

        # Colisões com as raquetes
        if (bola_x <= raquete1_x + largura_raquete and raquete1_y < bola_y + altura_bola / 2 < raquete1_y + altura_raquete) or \
           (bola_x + largura_bola >= raquete2_x and raquete2_y < bola_y + altura_bola / 2 < raquete2_y + altura_raquete):
            velocidade_bola_x *= -1

        # Pontuação
        if bola_x <= 0:  # Ponto para o jogador 2
            placar_jogador2 += 1
            bola_x = largura_tela // 2 - largura_bola // 2
            bola_y = altura_tela // 2 - altura_bola // 2
            velocidade_bola_x = 7 * random.choice((1, -1))
            velocidade_bola_y = 7 * random.choice((1, -1))
            velocidade_bola_x *= incremento_velocidade
            velocidade_bola_y *= incremento_velocidade
        if bola_x >= largura_tela - largura_bola:  # Ponto para o jogador 1
            placar_jogador1 += 1
            bola_x = largura_tela // 2 - largura_bola // 2
            bola_y = altura_tela // 2 - altura_bola // 2
            velocidade_bola_x = 7 * random.choice((1, -1))
            velocidade_bola_y = 7 * random.choice((1, -1))
            velocidade_bola_x *= incremento_velocidade
            velocidade_bola_y *= incremento_velocidade

        desenhar()

        # Controla a taxa de atualização
        clock.tick(60)

    pygame.quit()

# Executa o menu inicial
modo_de_jogo = mostrar_menu()

# Inicia o jogo com a configuração do bot ou para dois jogadores
iniciar_jogo(modo_de_jogo)
