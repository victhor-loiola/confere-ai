# Loop principal do jogo "Confere Aí!": eventos, atualização e desenho na tela.
import random

import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    BRANCO,
    PRETO,
    CINZA,
    CINZA_ESCURO,
    FUNDO,
    AZUL,
    VERDE,
    VERMELHO,
    AMARELO,
    VIDAS_INICIAIS,
    VERIFICACOES_INICIAIS,
    MAX_VERIFICACOES,
    META_PONTOS,
    PONTOS_PARA_BONUS,
    CONFIANCA_MINIMA,
    CONFIANCA_MAXIMA,
    VELOCIDADE_JOGADOR,
    LARGURA_JOGADOR,
    ALTURA_JOGADOR,
    LARGURA_POST,
    ALTURA_POST,
    VELOCIDADE_POST,
    INTERVALO_NOVO_POST,
    COLUNAS_POSTS,
    ALTURA_HUD,
    DURACAO_MENSAGEM,
    CAMINHO_RECORDE,
    CAMINHO_POSTS,
)
from src.funcoes import (
    calcular_pontos,
    tomar_dano,
    jogador_perdeu,
    jogador_venceu,
    limitar_valor,
    verificar_colisao,
    classificar_post,
    ia_acertou,
    confianca_baixa,
    texto_rotulo_ia,
    resultado_post_pego,
    resultado_post_perdido,
    usar_verificacao,
    aplicar_bonus_verificacao,
    calcular_taxa_acerto,
    colunas_disponiveis,
    quebrar_texto,
)
from src.dados import salvar_recorde, carregar_recorde, carregar_posts

MAX_LINHAS_POST = 3
ALTURA_LINHA_POST = 19
ALTURA_FAIXA_ROTULO = 26


# ======================================================================
# Criação do estado do jogo
# ======================================================================
def criar_jogador():
    """Cria o 'feed' do jogador: a barra azul no rodapé que recebe os posts."""
    x = (LARGURA_TELA - LARGURA_JOGADOR) // 2
    y = ALTURA_TELA - ALTURA_JOGADOR - 36
    return {"rect": pygame.Rect(x, y, LARGURA_JOGADOR, ALTURA_JOGADOR)}


def criar_estado(banco_posts, recorde, agora):
    """Monta o dicionário com tudo o que muda durante uma partida."""
    return {
        "jogador": criar_jogador(),
        "posts": [],
        "banco_posts": banco_posts,
        "pontos": 0,
        "vidas": VIDAS_INICIAIS,
        "verificacoes": VERIFICACOES_INICIAIS,
        "proximo_bonus": PONTOS_PARA_BONUS,
        "recorde": recorde,
        # Começa "atrasado" para o primeiro post aparecer logo no início.
        "ultimo_post_ms": agora - INTERVALO_NOVO_POST,
        "ultima_coluna": None,
        "mensagem": "Pegue os posts REAIS e deixe os FALSOS caírem!",
        "cor_mensagem": BRANCO,
        "mensagem_ate_ms": agora + 3000,
        "situacao": "jogando",  # "jogando", "vitoria" ou "derrota"
        "estatisticas": {
            "ia_acertos": 0,
            "ia_total": 0,
            "verificacoes_usadas": 0,
            "falsos_barrados": 0,
            "falsos_compartilhados": 0,
        },
    }


def criar_post(banco_posts, coluna, textos_na_tela):
    """Sorteia um post do banco e pede ao 'assistente de IA' um rótulo para ele."""
    # Evita mostrar dois posts iguais ao mesmo tempo.
    candidatos = []
    for modelo in banco_posts:
        if modelo["texto"] not in textos_na_tela:
            candidatos.append(modelo)
    if len(candidatos) == 0:
        candidatos = banco_posts

    modelo = random.choice(candidatos)
    confianca = random.uniform(CONFIANCA_MINIMA, CONFIANCA_MAXIMA)
    rotulo_ia = classificar_post(modelo["real"], confianca, random.random())

    return {
        "texto": modelo["texto"],
        "real": modelo["real"],          # verdade (o jogador não vê)
        "rotulo_ia": rotulo_ia,          # o que a IA diz (pode estar errado)
        "confianca": confianca,
        "verificado": False,
        # Nasce escondido atrás do placar e vai descendo.
        "y": float(ALTURA_HUD - ALTURA_POST),  # guarda casas decimais da queda
        "rect": pygame.Rect(coluna, ALTURA_HUD - ALTURA_POST, LARGURA_POST, ALTURA_POST),
    }


def mostrar_mensagem(estado, texto, cor, agora):
    """Mostra uma mensagem temporária abaixo do placar."""
    estado["mensagem"] = texto
    estado["cor_mensagem"] = cor
    estado["mensagem_ate_ms"] = agora + DURACAO_MENSAGEM


# ======================================================================
# Entrada do jogador
# ======================================================================
def processar_eventos(estado, agora):
    """Trata os eventos da janela. Retorna 'sair', 'reiniciar' ou None."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "sair"

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "sair"
            if evento.key == pygame.K_r and estado["situacao"] != "jogando":
                return "reiniciar"
            if evento.key == pygame.K_SPACE and estado["situacao"] == "jogando":
                post = post_mais_proximo_do_feed(estado["posts"])
                if post is not None:
                    verificar_post(estado, post, agora)

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Cliques no placar são ignorados (ali os posts ainda estão escondidos).
            if estado["situacao"] == "jogando" and evento.pos[1] > ALTURA_HUD:
                post = post_na_posicao(estado["posts"], evento.pos)
                if post is not None:
                    verificar_post(estado, post, agora)

    return None


def mover_jogador(jogador, teclas):
    """Move o feed para os lados com as setas ou A/D, sem sair da tela."""
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador["rect"].x -= VELOCIDADE_JOGADOR
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador["rect"].x += VELOCIDADE_JOGADOR

    jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)


def post_na_posicao(posts, posicao):
    """Retorna o post que está embaixo do clique do mouse (ou None)."""
    # Percorre de trás para frente para pegar o post desenhado por cima.
    for post in reversed(posts):
        if post["rect"].collidepoint(posicao):
            return post
    return None


def post_mais_proximo_do_feed(posts):
    """Retorna o post ainda não verificado que está mais perto do feed (ou None)."""
    escolhido = None
    for post in posts:
        if not post["verificado"]:
            if escolhido is None or post["rect"].bottom > escolhido["rect"].bottom:
                escolhido = post
    return escolhido


def verificar_post(estado, post, agora):
    """Gasta uma verificação para revelar se o post é real ou falso."""
    if post["verificado"]:
        return

    verificacoes, conseguiu = usar_verificacao(estado["verificacoes"])
    estado["verificacoes"] = verificacoes

    if not conseguiu:
        mostrar_mensagem(estado, f"Sem verificações! Ganhe +1 a cada {PONTOS_PARA_BONUS} pontos.", AMARELO, agora)
        return

    post["verificado"] = True
    estado["estatisticas"]["verificacoes_usadas"] += 1

    if post["real"]:
        texto, cor = "Fonte conferida: o post é REAL.", VERDE
    else:
        texto, cor = "Fonte conferida: o post é FALSO.", VERMELHO

    if not ia_acertou(post["real"], post["rotulo_ia"]):
        texto = texto + " A IA tinha errado!"

    mostrar_mensagem(estado, texto, cor, agora)


# ======================================================================
# Atualização das regras
# ======================================================================
def atualizar_posts(estado, agora):
    """Cria novos posts, faz os posts caírem e resolve os que chegaram ao fim."""
    if agora - estado["ultimo_post_ms"] >= INTERVALO_NOVO_POST:
        colunas = colunas_disponiveis(COLUNAS_POSTS, estado["ultima_coluna"])
        coluna = random.choice(colunas)

        textos_na_tela = []
        for post in estado["posts"]:
            textos_na_tela.append(post["texto"])

        estado["posts"].append(criar_post(estado["banco_posts"], coluna, textos_na_tela))
        estado["ultima_coluna"] = coluna
        estado["ultimo_post_ms"] = agora

    posts_restantes = []
    for post in estado["posts"]:
        post["y"] += VELOCIDADE_POST
        post["rect"].y = int(post["y"])

        if verificar_colisao(estado["jogador"]["rect"], post["rect"]):
            resolver_post(estado, post, True, agora)
        elif post["rect"].top > ALTURA_TELA:
            resolver_post(estado, post, False, agora)
        else:
            posts_restantes.append(post)

    estado["posts"] = posts_restantes


def resolver_post(estado, post, foi_pego, agora):
    """Aplica pontos, vidas e estatísticas quando um post sai do jogo."""
    if foi_pego:
        pontos, dano = resultado_post_pego(post["real"])
    else:
        pontos, dano = resultado_post_perdido(post["real"])

    estado["pontos"] = calcular_pontos(estado["pontos"], pontos)
    estado["vidas"] = tomar_dano(estado["vidas"], dano)

    estatisticas = estado["estatisticas"]
    estatisticas["ia_total"] += 1
    acertou = ia_acertou(post["real"], post["rotulo_ia"])
    if acertou:
        estatisticas["ia_acertos"] += 1

    if foi_pego and post["real"]:
        texto, cor = f"+{pontos} Post real no seu feed!", VERDE
    elif foi_pego:
        texto, cor = "-1 vida: você espalhou um post falso!", VERMELHO
        estatisticas["falsos_compartilhados"] += 1
    elif post["real"]:
        texto, cor = f"{pontos} Um post real ficou de fora.", AMARELO
    else:
        texto, cor = f"+{pontos} Post falso barrado!", VERDE
        estatisticas["falsos_barrados"] += 1

    if not acertou and not post["verificado"]:
        texto = texto + " (a IA tinha errado)"

    verificacoes_antes = estado["verificacoes"]
    estado["verificacoes"], estado["proximo_bonus"] = aplicar_bonus_verificacao(
        estado["pontos"], estado["proximo_bonus"], estado["verificacoes"]
    )
    if estado["verificacoes"] > verificacoes_antes:
        texto = texto + " +1 verificação!"

    mostrar_mensagem(estado, texto, cor, agora)


def verificar_fim(estado):
    """Confere vitória/derrota e salva o recorde quando a partida acaba."""
    if jogador_perdeu(estado["vidas"]):
        estado["situacao"] = "derrota"
    elif jogador_venceu(estado["pontos"], META_PONTOS):
        estado["situacao"] = "vitoria"

    if estado["situacao"] != "jogando" and estado["pontos"] > estado["recorde"]:
        estado["recorde"] = estado["pontos"]
        salvar_recorde(CAMINHO_RECORDE, estado["recorde"])


# ======================================================================
# Desenho na tela
# ======================================================================
def carregar_fontes():
    """Cria as fontes usadas no jogo (fonte padrão do Pygame)."""
    return {
        "hud": pygame.font.Font(None, 28),
        "post": pygame.font.Font(None, 21),
        "rotulo": pygame.font.Font(None, 22),
        "mensagem": pygame.font.Font(None, 26),
        "ajuda": pygame.font.Font(None, 20),
        "titulo": pygame.font.Font(None, 64),
        "texto": pygame.font.Font(None, 28),
    }


def desenhar_texto(tela, texto, fonte, cor, x, y, centralizado=False):
    """Escreve um texto na tela. Se centralizado, x é o centro horizontal."""
    imagem = fonte.render(texto, True, cor)
    if centralizado:
        x = x - imagem.get_width() // 2
    tela.blit(imagem, (x, y))


def desenhar_post(tela, post, fontes):
    """Desenha o cartão do post com o texto e o rótulo da IA (ou o resultado da verificação)."""
    rect = post["rect"]
    pygame.draw.rect(tela, BRANCO, rect, border_radius=8)

    def largura_do_trecho(trecho):
        return fontes["post"].size(trecho)[0]

    linhas = quebrar_texto(post["texto"], rect.width - 20, largura_do_trecho)
    for indice, linha in enumerate(linhas[:MAX_LINHAS_POST]):
        desenhar_texto(tela, linha, fontes["post"], PRETO, rect.x + 10, rect.y + 8 + indice * ALTURA_LINHA_POST)

    faixa = pygame.Rect(rect.x, rect.bottom - ALTURA_FAIXA_ROTULO, rect.width, ALTURA_FAIXA_ROTULO)

    if post["verificado"]:
        if post["real"]:
            cor, texto = VERDE, "CONFERIDO: REAL"
        else:
            cor, texto = VERMELHO, "CONFERIDO: FALSO"
        pygame.draw.rect(tela, cor, faixa, border_bottom_left_radius=8, border_bottom_right_radius=8)
        pygame.draw.rect(tela, cor, rect, 4, border_radius=8)
        desenhar_texto(tela, texto, fontes["rotulo"], BRANCO, faixa.centerx, faixa.y + 6, True)
    else:
        if confianca_baixa(post["confianca"]):
            cor_texto = AMARELO
        elif post["rotulo_ia"]:
            cor_texto = VERDE
        else:
            cor_texto = VERMELHO
        pygame.draw.rect(tela, CINZA_ESCURO, faixa, border_bottom_left_radius=8, border_bottom_right_radius=8)
        pygame.draw.rect(tela, CINZA, rect, 2, border_radius=8)
        texto = texto_rotulo_ia(post["rotulo_ia"], post["confianca"])
        desenhar_texto(tela, texto, fontes["rotulo"], cor_texto, faixa.centerx, faixa.y + 6, True)


def desenhar_jogador(tela, jogador, fontes):
    """Desenha o feed do jogador."""
    rect = jogador["rect"]
    pygame.draw.rect(tela, AZUL, rect, border_radius=6)
    desenhar_texto(tela, "SEU FEED", fontes["rotulo"], BRANCO, rect.centerx, rect.y + 5, True)


def desenhar_hud(tela, estado, fontes):
    """Desenha o placar no topo da tela."""
    pygame.draw.rect(tela, CINZA_ESCURO, (0, 0, LARGURA_TELA, ALTURA_HUD))
    pygame.draw.line(tela, FUNDO, (0, 38), (LARGURA_TELA, 38), 2)
    recorde = max(estado["recorde"], estado["pontos"])
    desenhar_texto(tela, f"Pontos: {estado['pontos']}/{META_PONTOS}", fontes["hud"], BRANCO, 12, 10)
    desenhar_texto(tela, f"Vidas: {estado['vidas']}", fontes["hud"], BRANCO, 220, 10)
    desenhar_texto(tela, f"Verificações: {estado['verificacoes']}/{MAX_VERIFICACOES}", fontes["hud"], BRANCO, 350, 10)
    desenhar_texto(tela, f"Recorde: {recorde}", fontes["hud"], BRANCO, 640, 10)


def desenhar_mensagem(tela, estado, fontes, agora):
    """Desenha, na 2ª linha do placar, o resultado da última ação (ou uma dica)."""
    if agora < estado["mensagem_ate_ms"] and estado["mensagem"] != "":
        texto, cor = estado["mensagem"], estado["cor_mensagem"]
    else:
        texto, cor = "Dica: rótulo com '?' = IA com pouca confiança. Vale verificar!", CINZA
    desenhar_texto(tela, texto, fontes["mensagem"], cor, LARGURA_TELA // 2, 48, True)


def desenhar_ajuda(tela, fontes):
    """Mostra os controles no rodapé."""
    texto = "Setas/A-D: mover   |   Clique ou ESPAÇO: verificar post   |   ESC: sair"
    desenhar_texto(tela, texto, fontes["ajuda"], CINZA, LARGURA_TELA // 2, ALTURA_TELA - 22, True)


def desenhar_tela_final(tela, estado, fontes):
    """Desenha o resumo da partida (vitória ou derrota) por cima do jogo."""
    camada = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    camada.fill((0, 0, 0, 200))
    tela.blit(camada, (0, 0))

    if estado["situacao"] == "vitoria":
        titulo, cor = "VOCÊ VENCEU!", VERDE
    else:
        titulo, cor = "FIM DE JOGO", VERMELHO

    estatisticas = estado["estatisticas"]
    taxa = calcular_taxa_acerto(estatisticas["ia_acertos"], estatisticas["ia_total"])
    centro = LARGURA_TELA // 2

    desenhar_texto(tela, titulo, fontes["titulo"], cor, centro, 120, True)
    linhas = [
        f"Pontos: {estado['pontos']}     Recorde: {estado['recorde']}",
        f"O assistente de IA acertou {estatisticas['ia_acertos']} de {estatisticas['ia_total']} rótulos ({taxa}%).",
        f"Verificações usadas: {estatisticas['verificacoes_usadas']}",
        f"Falsos barrados: {estatisticas['falsos_barrados']}     "
        f"Falsos compartilhados: {estatisticas['falsos_compartilhados']}",
        "A IA ajuda, mas quem confere a fonte é você.",
    ]
    if estado["situacao"] == "vitoria":
        linhas.insert(0, "Seu feed ficou confiável.")
    for indice, linha in enumerate(linhas):
        desenhar_texto(tela, linha, fontes["texto"], BRANCO, centro, 220 + indice * 40, True)

    desenhar_texto(tela, "R: jogar de novo    |    ESC: sair", fontes["texto"], AMARELO, centro, 480, True)


def desenhar(tela, estado, fontes, agora):
    """Desenha um quadro completo do jogo."""
    tela.fill(FUNDO)
    desenhar_ajuda(tela, fontes)  # desenhada antes, para ficar atrás dos posts

    for post in estado["posts"]:
        desenhar_post(tela, post, fontes)

    desenhar_jogador(tela, estado["jogador"], fontes)
    desenhar_hud(tela, estado, fontes)
    desenhar_mensagem(tela, estado, fontes, agora)

    if estado["situacao"] != "jogando":
        desenhar_tela_final(tela, estado, fontes)

    pygame.display.flip()


def atualizar_titulo(estado):
    """Mostra as informações principais também no título da janela."""
    pygame.display.set_caption(
        f"{TITULO_JOGO} | Pontos: {estado['pontos']} | Vidas: {estado['vidas']} | "
        f"Verificações: {estado['verificacoes']}"
    )


# ======================================================================
# Função principal
# ======================================================================
def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()
    fontes = carregar_fontes()

    banco_posts = carregar_posts(CAMINHO_POSTS)
    estado = criar_estado(banco_posts, carregar_recorde(CAMINHO_RECORDE), pygame.time.get_ticks())

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    rodando = True
    while rodando:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()

        acao = processar_eventos(estado, agora)
        if acao == "sair":
            rodando = False
        elif acao == "reiniciar":
            estado = criar_estado(banco_posts, estado["recorde"], agora)

        if estado["situacao"] == "jogando":
            mover_jogador(estado["jogador"], pygame.key.get_pressed())
            atualizar_posts(estado, agora)
            verificar_fim(estado)

        atualizar_titulo(estado)
        desenhar(tela, estado, fontes, agora)

    pygame.quit()
