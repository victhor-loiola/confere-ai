# Funções de regra e lógica do jogo.
# Nenhuma delas depende do Pygame, por isso todas podem ser testadas com pytest.
from src.config import (
    PONTOS_REAL_COMPARTILHADO,
    PONTOS_FALSO_BARRADO,
    PONTOS_REAL_PERDIDO,
    DANO_FALSO_COMPARTILHADO,
    PONTOS_PARA_BONUS,
    MAX_VERIFICACOES,
    LIMITE_CONFIANCA_BAIXA,
)


# ---------------------------------------------------------------- Pontos e vidas
def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos (ou perdidos) à pontuação atual, sem deixar ficar negativa."""
    return max(0, pontos_atual + pontos_ganhos)


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido, sem passar de zero."""
    return max(0, vida_atual - dano)


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def jogador_venceu(pontos, meta):
    """Indica se o jogador alcançou a pontuação necessária para vencer."""
    return pontos >= meta


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)


# ---------------------------------------------------------------- "IA" simulada
def classificar_post(eh_real, confianca, sorteio):
    """Simula o assistente de IA rotulando um post.

    O assistente acerta quando o sorteio (número entre 0 e 1) é menor que a
    confiança. Assim, um rótulo com 95% de confiança quase sempre está certo,
    e um com 55% erra quase metade das vezes.

    Retorna True se o assistente diz que o post é REAL e False se diz FALSO.
    """
    if sorteio < confianca:
        return eh_real
    return not eh_real


def ia_acertou(eh_real, rotulo_ia):
    """Indica se o rótulo do assistente corresponde à verdade do post."""
    return eh_real == rotulo_ia


def confianca_baixa(confianca):
    """Indica se a confiança do assistente está abaixo do limite considerado seguro."""
    return confianca < LIMITE_CONFIANCA_BAIXA


def texto_rotulo_ia(rotulo_ia, confianca):
    """Monta o texto do rótulo mostrado no post. Ex.: 'IA: REAL 92%' ou 'IA: FALSO? 58%'."""
    if rotulo_ia:
        palavra = "REAL"
    else:
        palavra = "FALSO"

    if confianca_baixa(confianca):
        palavra = palavra + "?"

    porcentagem = round(confianca * 100)
    return f"IA: {palavra} {porcentagem}%"


# ---------------------------------------------------------------- Resultado dos posts
def resultado_post_pego(eh_real):
    """Retorna (pontos, dano) quando o jogador coloca o post no feed."""
    if eh_real:
        return PONTOS_REAL_COMPARTILHADO, 0
    return 0, DANO_FALSO_COMPARTILHADO


def resultado_post_perdido(eh_real):
    """Retorna (pontos, dano) quando o post cai sem entrar no feed."""
    if eh_real:
        return PONTOS_REAL_PERDIDO, 0
    return PONTOS_FALSO_BARRADO, 0


# ---------------------------------------------------------------- Verificações
def usar_verificacao(verificacoes):
    """Gasta uma verificação, se houver.

    Retorna (verificacoes_restantes, conseguiu_verificar).
    """
    if verificacoes <= 0:
        return 0, False
    return verificacoes - 1, True


def aplicar_bonus_verificacao(pontos, proximo_bonus, verificacoes):
    """Dá +1 verificação cada vez que o jogador alcança um novo marco de pontos.

    Retorna (verificacoes, proximo_bonus) atualizados. O total nunca passa
    de MAX_VERIFICACOES.
    """
    while pontos >= proximo_bonus:
        verificacoes = min(MAX_VERIFICACOES, verificacoes + 1)
        proximo_bonus = proximo_bonus + PONTOS_PARA_BONUS
    return verificacoes, proximo_bonus


# ---------------------------------------------------------------- Auxiliares
def calcular_taxa_acerto(acertos, total):
    """Retorna a porcentagem inteira de acertos (0 quando não houve tentativas)."""
    if total == 0:
        return 0
    return round(acertos * 100 / total)


def colunas_disponiveis(colunas, ultima_coluna):
    """Retorna as colunas onde um novo post pode nascer, evitando repetir a última."""
    disponiveis = []
    for coluna in colunas:
        if coluna != ultima_coluna:
            disponiveis.append(coluna)
    return disponiveis


def quebrar_texto(texto, largura_maxima, medir_largura):
    """Divide um texto em linhas que cabem em largura_maxima.

    medir_largura é uma função que recebe um trecho de texto e retorna a sua
    largura (no jogo, em pixels; nos testes, pode ser a própria função len).
    """
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if linha_atual == "":
            tentativa = palavra
        else:
            tentativa = linha_atual + " " + palavra

        if medir_largura(tentativa) <= largura_maxima or linha_atual == "":
            linha_atual = tentativa
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual != "":
        linhas.append(linha_atual)

    return linhas