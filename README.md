# Confere Aí!

Projeto final da disciplina de Introdução a Algoritmos (PUC Minas, 2026/2), desenvolvido com Python e Pygame a partir do template oficial da disciplina.

**Tema:** IA no Cotidiano e Uso Responsável, com foco em **confiabilidade de sistemas inteligentes** e **conteúdos reais e artificiais**.

## Integrantes do grupo

- Victhor Guilherme Santos Loiola
- Pietro Lage

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/config.py`: constantes de tela, cores, regras e caminhos de arquivos.
- `src/funcoes.py`: regras do jogo sem Pygame (pontos, vidas, IA simulada, verificações).
- `src/dados.py`: leitura e gravação de arquivos (recorde e banco de posts).
- `src/jogo.py`: loop principal, eventos, atualização e desenho na tela.
- `src/sprites.py`: recorte de spritesheet (mantido do template; não usado nesta versão).
- `assets/`: imagens, fontes e sons (vazia nesta versão, exceto o spritesheet do template).
- `data/posts.txt`: banco de posts lido pelo jogo (`tipo;texto`).
- `data/recorde.txt`: melhor pontuação.
- `tests/`: testes unitários com `pytest`.
- `docs/proposta.MD`: proposta do jogo.

## Descrição do jogo

Posts de uma rede social caem do topo da tela. Um **assistente de IA** coloca em cada post um rótulo ("IA: REAL 92%" ou "IA: FALSO? 58%"), mas ele **pode errar**, principalmente quando a confiança é baixa. O jogador controla o **SEU FEED**, uma barra no rodapé: encostar em um post significa compartilhá-lo, e deixá-lo cair significa barrá-lo. Para os casos duvidosos, o jogador pode gastar uma **verificação** e conferir a fonte.

A ideia é mostrar, na própria jogabilidade, que a IA ajuda, mas o resultado precisa ser analisado com senso crítico antes de compartilhar.

## Objetivo do jogador

Chegar a **150 pontos** montando um feed confiável, sem perder as 3 vidas.

## Regras do jogo

- O jogador começa com 3 vidas e 3 verificações (máximo de 5).
- Post **real** no feed: +10 pontos. Post **falso** barrado (caiu): +5 pontos.
- Post **falso** no feed: −1 vida. Post **real** que caiu: −5 pontos.
- Clicar em um post (ou ESPAÇO) gasta 1 verificação e revela a verdade. A cada 50 pontos ganha +1 verificação.
- O rótulo da IA acerta com a probabilidade da confiança mostrada. Rótulos abaixo de 70% aparecem em amarelo, com "?".
- Vitória: 150 pontos. Derrota: 0 vidas. No fim aparece um resumo com o desempenho do jogador e da IA.

## Controles

- Seta para esquerda / A: mover o feed para a esquerda
- Seta para direita / D: mover o feed para a direita
- Clique do mouse em um post: verificar aquele post
- Espaço: verificar o post mais próximo do feed
- R: jogar de novo (após o fim da partida)
- ESC: sair do jogo

## Como executar o projeto

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Estado atual (Entrega 2 – versão parcial, 22/11/2026)

Pronto: janela e loop principal, movimento do feed, posts com rótulo da IA, verificação, pontos, vidas, vitória/derrota, tela de resumo, reinício, leitura de `data/posts.txt`, recorde em arquivo e testes das funções de lógica e de arquivos.

Previsto para a entrega final: tela inicial com instruções, ranking com nome, dificuldade progressiva e ajustes a partir do acompanhamento em aula.

## Recursos externos

- [Pygame](https://www.pygame.org/) (licença LGPL) e [pytest](https://pytest.org/) (licença MIT).
- Template oficial da disciplina: [IntroAlgs_pygame_template](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template).
- Fonte padrão do Pygame (FreeSansBold, distribuída com o Pygame).
- Os posts do jogo são fictícios.
