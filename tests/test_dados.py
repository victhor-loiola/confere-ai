from src.config import CAMINHO_POSTS
from src.dados import (
    POSTS_PADRAO,
    salvar_recorde,
    carregar_recorde,
    interpretar_linha_post,
    carregar_posts,
)


def test_interpretar_linha_post_real():
    """Uma linha 'real;texto' deve virar um dicionario com real=True."""
    assert interpretar_linha_post("real;Site oficial divulga horario\n") == {
        "texto": "Site oficial divulga horario",
        "real": True,
    }


def test_interpretar_linha_post_falso_com_maiusculas():
    """O tipo deve ser aceito mesmo escrito em maiusculas."""
    assert interpretar_linha_post("FALSO; Compartilhe urgente!") == {
        "texto": "Compartilhe urgente!",
        "real": False,
    }


def test_interpretar_linha_ignora_comentario_e_vazia():
    """Comentarios e linhas vazias devem ser ignorados."""
    assert interpretar_linha_post("# comentario") is None
    assert interpretar_linha_post("   ") is None


def test_interpretar_linha_invalida():
    """Linhas sem ';', sem texto ou com tipo desconhecido sao invalidas."""
    assert interpretar_linha_post("real sem separador") is None
    assert interpretar_linha_post("real;") is None
    assert interpretar_linha_post("talvez;Texto") is None


def test_carregar_posts_do_arquivo(tmp_path):
    """Deve ler somente as linhas validas do arquivo."""
    arquivo = tmp_path / "posts.txt"
    arquivo.write_text("# teste\nreal;A\nlinha errada\nfalso;B\n", encoding="utf-8")
    assert carregar_posts(str(arquivo)) == [
        {"texto": "A", "real": True},
        {"texto": "B", "real": False},
    ]


def test_carregar_posts_arquivo_inexistente(tmp_path):
    """Sem arquivo, deve usar a lista padrao para o jogo nao travar."""
    assert carregar_posts(str(tmp_path / "nao_existe.txt")) == POSTS_PADRAO


def test_salvar_e_carregar_recorde(tmp_path):
    """O recorde salvo deve ser lido de volta igual."""
    arquivo = tmp_path / "recorde.txt"
    salvar_recorde(str(arquivo), 120)
    assert carregar_recorde(str(arquivo)) == 120


def test_carregar_recorde_invalido(tmp_path):
    """Conteudo que nao e numero deve virar recorde 0."""
    arquivo = tmp_path / "recorde.txt"
    arquivo.write_text("abc", encoding="utf-8")
    assert carregar_recorde(str(arquivo)) == 0


def test_carregar_recorde_arquivo_inexistente(tmp_path):
    """Sem arquivo, o recorde deve ser 0."""
    assert carregar_recorde(str(tmp_path / "nao_existe.txt")) == 0


def test_arquivo_de_posts_do_jogo_e_valido():
    """O banco de posts do jogo deve ter posts reais e falsos."""
    posts = carregar_posts(CAMINHO_POSTS)
    reais = [post for post in posts if post["real"]]
    falsos = [post for post in posts if not post["real"]]
    assert len(reais) >= 5
    assert len(falsos) >= 5