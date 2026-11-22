# Leitura e gravação de arquivos do jogo (recorde e banco de posts).

# Usados apenas se o arquivo data/posts.txt não existir ou estiver vazio.
POSTS_PADRAO = [
    {"texto": "Prefeitura divulga horários de vacinação no site oficial", "real": True},
    {"texto": "URGENTE: compartilhe antes que apaguem este vídeo!", "real": False},
]


def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se o arquivo não existir ou não tiver um número válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except (FileNotFoundError, ValueError):
        return 0


def interpretar_linha_post(linha):
    """Converte uma linha do arquivo de posts em dicionário.

    Formato esperado: tipo;texto  (tipo é 'real' ou 'falso').
    Exemplo: real;Prefeitura divulga horários no site oficial

    Retorna {"texto": ..., "real": True/False} ou None se a linha
    estiver vazia, for comentário (#) ou tiver formato inválido.
    """
    linha = linha.strip()

    if linha == "" or linha.startswith("#"):
        return None

    partes = linha.split(";", 1)
    if len(partes) != 2:
        return None

    tipo = partes[0].strip().lower()
    texto = partes[1].strip()

    if texto == "" or tipo not in ("real", "falso"):
        return None

    return {"texto": texto, "real": tipo == "real"}


def carregar_posts(caminho_arquivo):
    """Lê o banco de posts do arquivo e retorna uma lista de dicionários.

    Linhas inválidas são ignoradas. Se o arquivo não existir ou não tiver
    nenhum post válido, retorna a lista POSTS_PADRAO.
    """
    posts = []

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                post = interpretar_linha_post(linha)
                if post is not None:
                    posts.append(post)
    except FileNotFoundError:
        return list(POSTS_PADRAO)

    if len(posts) == 0:
        return list(POSTS_PADRAO)

    return posts