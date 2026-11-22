# Configurações centrais do jogo (tela, cores, regras e caminhos de arquivos).
import os

# ---------------------------------------------------------------- Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Confere Aí!"

# ---------------------------------------------------------------- Cores (R, G, B)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
CINZA_ESCURO = (60, 60, 70)
FUNDO = (30, 34, 48)
AZUL = (52, 120, 246)
VERDE = (46, 160, 90)
VERMELHO = (210, 60, 60)
AMARELO = (240, 190, 40)

# ---------------------------------------------------------------- Regras do jogo
VIDAS_INICIAIS = 3
VERIFICACOES_INICIAIS = 3
MAX_VERIFICACOES = 5
META_PONTOS = 150

PONTOS_REAL_COMPARTILHADO = 10   # pegou um post real
PONTOS_FALSO_BARRADO = 5         # deixou um post falso cair
PONTOS_REAL_PERDIDO = -5         # deixou um post real cair
DANO_FALSO_COMPARTILHADO = 1     # pegou um post falso (perde vida)

PONTOS_PARA_BONUS = 50           # a cada 50 pontos ganha +1 verificação

# Confiança que o "assistente de IA" mostra em cada rótulo (0.0 a 1.0).
# Quanto menor a confiança, maior a chance de o rótulo estar errado.
CONFIANCA_MINIMA = 0.55
CONFIANCA_MAXIMA = 0.98
LIMITE_CONFIANCA_BAIXA = 0.70

# ---------------------------------------------------------------- Elementos
VELOCIDADE_JOGADOR = 7
LARGURA_JOGADOR = 140
ALTURA_JOGADOR = 24

LARGURA_POST = 250
ALTURA_POST = 100
VELOCIDADE_POST = 1.4            # pixels por quadro
INTERVALO_NOVO_POST = 2200       # milissegundos entre um post e outro
COLUNAS_POSTS = (20, 275, 530)   # posições x onde os posts podem aparecer

ALTURA_HUD = 74                  # placar (linha 1) + mensagens (linha 2)
DURACAO_MENSAGEM = 1800          # milissegundos que a mensagem fica na tela

# ---------------------------------------------------------------- Arquivos
# Caminhos montados a partir da pasta do projeto, para funcionar
# mesmo se o jogo for aberto de outra pasta (ex.: pelo PyCharm).
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAMINHO_RECORDE = os.path.join(PASTA_PROJETO, "data", "recorde.txt")
CAMINHO_POSTS = os.path.join(PASTA_PROJETO, "data", "posts.txt")
CAMINHO_SPRITES = os.path.join(PASTA_PROJETO, "assets", "imagens", "spritesheet.bmp")