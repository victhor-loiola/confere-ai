# Proposta Inicial do Jogo

Introdução a Algoritmos (PUC Minas, 2026/2) · Projeto Final "Jogos para o Futuro" · Eixo temático: IA no Cotidiano e Uso Responsável.

## 1. Nome provisório do jogo

**Nome:**

> Confere Aí!

## 2. Integrantes do grupo

- Nome 1: Victhor Guilherme Santos Loiola
- Nome 2: Pietro Lage Gomes Fernandes
- Nome 3: —
- Nome 4: —

## 3. Tema escolhido

**Tema:**

> Confiabilidade de sistemas inteligentes aplicada a conteúdos reais e artificiais: um assistente de IA que classifica posts de uma rede social como "real" ou "falso", mas que pode errar.
>
> **Aspecto de uso responsável:** confiabilidade e análise crítica dos resultados. A IA ajuda, mas não deve ser seguida às cegas; antes de compartilhar algo, é preciso conferir a fonte. O jogo também trabalha transparência, porque o assistente mostra o quanto está confiante em cada rótulo.

**Como esse tema se relaciona com o jogo?**

> Cada post que cai na tela recebe um rótulo do assistente de IA ("IA: REAL 92%" ou "IA: FALSO? 58%"). O rótulo é gerado por uma IA simulada que erra com mais frequência quando a confiança é baixa. O jogador decide se coloca o post no seu feed ou se o deixa cair, e pode gastar uma das poucas **verificações** para conferir a verdade. Compartilhar um post falso tira vida; confiar cegamente na IA faz o jogador perder.

## 4. Tipo de jogo

**Tipo escolhido:**

> Coleta e desvio de itens que caem (estilo "pegar/desviar"), com decisão do jogador e recurso limitado de verificação.

## 5. Descrição geral do jogo

**Descrição:**

> A tela mostra posts (cartões com uma manchete curta) caindo do topo. Embaixo de cada post aparece o rótulo dado pelo assistente de IA, com a porcentagem de confiança. O jogador controla o "SEU FEED", uma barra no rodapé que se move para os lados. Encostar o feed em um post significa compartilhá-lo; deixar o post cair significa barrá-lo. O desafio é descobrir quais posts são confiáveis lendo o texto (urgência, promessas fáceis, pedidos de senha, sinais de imagem ou áudio gerados por IA) e usando as verificações nos casos duvidosos, já que o rótulo da IA nem sempre está certo.

## 6. Objetivo do jogador

**Objetivo:**

> Montar um feed confiável: chegar a 150 pontos compartilhando posts reais e barrando posts falsos, sem esgotar as vidas.

## 7. Regras principais

- Regra 1: O jogador começa com 3 vidas e 3 verificações (máximo de 5).
- Regra 2: Colocar um post **real** no feed dá +10 pontos; deixar um post **falso** cair dá +5 pontos.
- Regra 3: Colocar um post **falso** no feed tira 1 vida; deixar um post **real** cair tira 5 pontos.
- Regra 4: Clicar em um post (ou apertar ESPAÇO) gasta 1 verificação e revela se ele é real ou falso. A cada 50 pontos o jogador ganha +1 verificação.
- Regra 5: O rótulo da IA acerta com probabilidade igual à confiança mostrada; rótulos abaixo de 70% aparecem em amarelo com "?" para indicar pouca confiança.

## 8. Condição de vitória

**Condição de vitória:**

> Alcançar 150 pontos.

## 9. Condição de derrota ou encerramento

**Condição de derrota ou encerramento:**

> A partida termina em derrota quando as vidas chegam a zero (o jogador compartilhou 3 posts falsos). O jogador também pode encerrar a qualquer momento com ESC. Ao final, a tela mostra o resumo: pontos, recorde, quantas vezes a IA acertou, verificações usadas e falsos barrados/compartilhados.

## 10. Elementos previstos no jogo

- **Personagem ou elemento principal:** o "SEU FEED", barra controlada pelo jogador no rodapé.
- **Obstáculos ou desafios:** posts falsos (sensacionalismo, golpes, imagens e áudios gerados por IA) e rótulos errados do assistente de IA.
- **Itens ou objetos de interação (se houver):** posts reais para coletar; verificações para conferir a fonte de um post.
- **Pontuação, vidas, tempo ou progresso:** pontos (meta de 150), vidas, verificações e recorde salvo em arquivo; estatísticas de acerto da IA no fim da partida.

## 11. Controles previstos

**Controles:**

> Setas ← → (ou A/D) movem o feed; clique com o botão esquerdo do mouse em um post para verificá-lo; ESPAÇO verifica o post mais próximo do feed (alternativa sem mouse); R reinicia depois do fim da partida; ESC sai do jogo.

## 12. Principais dificuldades esperadas

- Dificuldade 1: Equilibrar a dificuldade (velocidade de queda, intervalo entre posts e chance de erro da IA) para que o jogador tenha tempo de ler e decidir.
- Dificuldade 2: Testar funções que usam sorteio; a solução foi receber o número sorteado como parâmetro, para que os testes sejam previsíveis.
- Dificuldade 3: Fazer o texto dos posts caber nos cartões (quebra de linha automática) e organizar o código em funções pequenas.

## 13. Escopo mínimo para a entrega final

**Escopo mínimo:**

> Tela de jogo com o feed controlado pelo teclado; posts caindo com o rótulo e a confiança da IA; verificação por clique/ESPAÇO com limite; pontos, vidas e verificações no placar e no título da janela; vitória com 150 pontos e derrota sem vidas; tela de resumo com R para reiniciar; posts lidos de `data/posts.txt`; recorde salvo em `data/recorde.txt`; testes com `pytest` para as funções de lógica e de arquivos.

## 14. Possíveis melhorias, caso haja tempo

- Melhoria 1: Tela inicial com instruções e explicação do tema antes da partida.
- Melhoria 2: Ranking com o nome do jogador salvo em `data/ranking.txt`.
- Melhoria 3: Dificuldade progressiva (posts mais rápidos e IA menos confiável a cada 50 pontos) e efeitos sonoros.

## 15. Organização inicial do código

O projeto segue a estrutura do template oficial:

- `main.py`: ponto de entrada; chama `executar_jogo()`.
- `src/config.py`: constantes (tela, cores, regras, velocidades e caminhos de arquivos).
- `src/funcoes.py`: regras puras do jogo, sem Pygame (pontos, vidas, vitória/derrota, IA simulada, verificações, quebra de texto). São as funções testadas.
- `src/dados.py`: leitura e gravação de arquivos (recorde e banco de posts).
- `src/jogo.py`: loop principal dividido em funções de criação do estado, entrada (`processar_eventos`, `mover_jogador`), atualização (`atualizar_posts`, `resolver_post`, `verificar_fim`) e desenho (`desenhar_hud`, `desenhar_post`, `desenhar_tela_final` etc.).
- `src/sprites.py`: mantido do template (não usado nesta versão, pois os elementos são desenhados com formas e texto).
- `tests/`: testes com `pytest`.

## 16. Estruturas de dados utilizadas

- **Dicionários:** o estado da partida (`pontos`, `vidas`, `posts`, `estatisticas`...), cada post (`texto`, `real`, `rotulo_ia`, `confianca`, `verificado`, `rect`) e o jogador.
- **Listas:** posts na tela, banco de posts lido do arquivo, linhas de texto quebradas e linhas do resumo final.
- **Tuplas:** cores RGB, colunas onde os posts aparecem e retornos de funções como `(pontos, dano)`.

## 17. Uso de arquivos

- `data/posts.txt` (leitura): banco de posts no formato `tipo;texto`, com linhas de comentário iniciadas por `#`. Assim é possível acrescentar posts sem mexer no código.
- `data/recorde.txt` (leitura e escrita): melhor pontuação, salva ao fim da partida.
- `data/ranking.txt` (previsto para a entrega final): ranking com nomes.

## 18. Testes planejados

Testes com `pytest` em `tests/test_logica.py` e `tests/test_dados.py`, cobrindo:

- soma de pontos sem ficar negativa, dano, vitória e derrota;
- IA simulada (acerta quando o sorteio é menor que a confiança, erra caso contrário) e texto do rótulo;
- pontos e dano ao pegar ou deixar cair posts reais e falsos;
- uso de verificações e bônus a cada 50 pontos, respeitando o máximo;
- quebra de texto, taxa de acerto e escolha de coluna;
- leitura do arquivo de posts (linhas válidas, comentários, linhas inválidas, arquivo inexistente) e gravação/leitura do recorde.

## 19. Recursos utilizados

- Python 3 e Pygame (biblioteca do jogo) e pytest (testes).
- Template oficial da disciplina (IntroAlgs_pygame_template).
- Fonte padrão do Pygame; nenhuma imagem ou som externo nesta versão.
- Os posts do jogo são fictícios e foram escritos pelo grupo.

## 20. Declaração de originalidade

O grupo declara que o jogo "Confere Aí!" é uma proposta própria, desenvolvida a partir do template oficial da disciplina, e não reutiliza jogos de semestres anteriores nem tutoriais prontos. Os recursos externos e as ferramentas de apoio utilizadas estão identificados no `README.md`.

## 21. Histórico de atualizações

- **Entrega 1:** proposta inicial preenchida (planejamento).
- **Entrega 2 (22/11/2026):** primeira versão executável, sem mudanças no planejamento. Já funcionam: janela e loop principal, movimento do feed, posts caindo com rótulo da IA, verificação por clique/ESPAÇO, pontos, vidas, bônus de verificação, vitória/derrota, tela de resumo, reinício, leitura de `data/posts.txt`, recorde em arquivo e 40 testes. Falta para a entrega final: tela inicial, ranking com nome, dificuldade progressiva e ajustes de jogabilidade a partir do acompanhamento em aula.
