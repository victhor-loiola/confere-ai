from src.config import MAX_VERIFICACOES, PONTOS_PARA_BONUS
from src.funcoes import (
    calcular_pontos,
    tomar_dano,
    jogador_perdeu,
    jogador_venceu,
    limitar_valor,
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


# ---------------------------------------------------------------- Testes do template
def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


# ---------------------------------------------------------------- Pontos, vidas e fim de jogo
def test_calcular_pontos_nao_fica_negativo():
    """Perder mais pontos do que se tem deve deixar a pontuacao em zero."""
    assert calcular_pontos(3, -5) == 0


def test_tomar_dano_nao_fica_negativo():
    """As vidas nao devem ficar abaixo de zero."""
    assert tomar_dano(1, 3) == 0


def test_jogador_venceu_ao_atingir_a_meta():
    """Deve indicar vitoria quando os pontos alcancam a meta."""
    assert jogador_venceu(150, 150) is True


def test_jogador_ainda_nao_venceu():
    """Nao deve indicar vitoria abaixo da meta."""
    assert jogador_venceu(140, 150) is False


# ---------------------------------------------------------------- IA simulada
def test_classificar_post_acerta_quando_sorteio_menor_que_confianca():
    """Com sorteio abaixo da confianca, o rotulo deve ser igual a verdade."""
    assert classificar_post(True, 0.9, 0.5) is True
    assert classificar_post(False, 0.9, 0.5) is False


def test_classificar_post_erra_quando_sorteio_maior_que_confianca():
    """Com sorteio acima da confianca, o rotulo deve ser o contrario da verdade."""
    assert classificar_post(True, 0.6, 0.8) is False
    assert classificar_post(False, 0.6, 0.8) is True


def test_ia_acertou():
    """Deve comparar o rotulo da IA com a verdade do post."""
    assert ia_acertou(True, True) is True
    assert ia_acertou(False, True) is False


def test_confianca_baixa():
    """Confianca abaixo de 70% deve ser considerada baixa."""
    assert confianca_baixa(0.65) is True
    assert confianca_baixa(0.85) is False


def test_texto_rotulo_ia_confianca_alta():
    """Rotulo com confianca alta nao deve ter interrogacao."""
    assert texto_rotulo_ia(True, 0.92) == "IA: REAL 92%"


def test_texto_rotulo_ia_confianca_baixa():
    """Rotulo com confianca baixa deve ter interrogacao."""
    assert texto_rotulo_ia(False, 0.58) == "IA: FALSO? 58%"


# ---------------------------------------------------------------- Resultado dos posts
def test_pegar_post_real_da_pontos():
    """Colocar um post real no feed deve dar pontos e nenhum dano."""
    assert resultado_post_pego(True) == (10, 0)


def test_pegar_post_falso_tira_vida():
    """Colocar um post falso no feed deve tirar uma vida."""
    assert resultado_post_pego(False) == (0, 1)


def test_deixar_post_falso_cair_da_pontos():
    """Barrar um post falso deve dar pontos."""
    assert resultado_post_perdido(False) == (5, 0)


def test_deixar_post_real_cair_tira_pontos():
    """Perder um post real deve tirar pontos."""
    assert resultado_post_perdido(True) == (-5, 0)


# ---------------------------------------------------------------- Verificacoes
def test_usar_verificacao_com_saldo():
    """Deve gastar uma verificacao quando houver saldo."""
    assert usar_verificacao(2) == (1, True)


def test_usar_verificacao_sem_saldo():
    """Não deve verificar quando o saldo for zero."""
    assert usar_verificacao(0) == (0, False)


def test_bonus_ao_alcancar_marco():
    """Ao chegar no marco de pontos, ganha +1 verificacao e o marco avanca."""
    assert aplicar_bonus_verificacao(50, 50, 1) == (2, 50 + PONTOS_PARA_BONUS)


def test_sem_bonus_antes_do_marco():
    """Antes do marco nada muda."""
    assert aplicar_bonus_verificacao(40, 50, 1) == (1, 50)


def test_bonus_respeita_maximo():
    """O total de verificacoes nunca passa do maximo."""
    verificacoes, _ = aplicar_bonus_verificacao(50, 50, MAX_VERIFICACOES)
    assert verificacoes == MAX_VERIFICACOES


# ---------------------------------------------------------------- Auxiliares
def test_taxa_de_acerto():
    """Deve calcular a porcentagem inteira de acertos."""
    assert calcular_taxa_acerto(3, 4) == 75


def test_taxa_de_acerto_sem_tentativas():
    """Sem tentativas, a taxa deve ser zero (sem divisao por zero)."""
    assert calcular_taxa_acerto(0, 0) == 0


def test_colunas_disponiveis_evita_a_ultima():
    """A ultima coluna usada nao deve ser oferecida de novo."""
    assert colunas_disponiveis((20, 275, 530), 275) == [20, 530]


def test_quebrar_texto_respeita_largura():
    """Nenhuma linha deve passar da largura maxima (medida em caracteres)."""
    linhas = quebrar_texto("Banco nunca pede sua senha por mensagem", 15, len)
    assert linhas == ["Banco nunca", "pede sua senha", "por mensagem"]
    for linha in linhas:
        assert len(linha) <= 15


def test_quebrar_texto_palavra_maior_que_a_largura():
    """Uma palavra maior que a largura fica sozinha na linha, sem travar."""
    assert quebrar_texto("supercalifragilistico ok", 5, len) == ["supercalifragilistico", "ok"]