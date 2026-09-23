# Onde está o contexto (leia isto antes de qualquer skill)

As skills deste plugin não carregam IDs de banco, nomes de pessoas nem a hierarquia do time — isso
é **contexto privado** e vive num repositório separado. A lógica (este plugin) é pública; o contexto
não. Antes de consultar qualquer coisa, localize a pasta `shared/` nesta ordem:

1. `$FOTONA_CONTEXTO/shared/` (variável de ambiente, se definida)
2. `~/fotona-mkt-contexto/shared/` (clone local do repositório privado — o padrão)
3. `<raiz deste plugin>/shared/` (só existe no pacote de transição entregue em mãos; nunca no marketplace)

Se não encontrar nenhuma, **pare** e diga: "não achei o contexto do sistema; clone o repositório
`fotona-mkt-contexto` em `~/fotona-mkt-contexto` (ou aponte `$FOTONA_CONTEXTO`) e rode `git pull`".
Nunca invente ID nem nome de campo.

Arquivos e quando ler cada um:

| Arquivo | Leia quando |
|---|---|
| `sistema-mkt.md` | sempre — IDs, campos, as 10 regras, quem é quem |
| `contrato-de-escrita.md` | antes de gravar qualquer coisa |
| `formato-de-saida.md` | antes de responder — dado bruto → leitura → uma pergunta |
| `log-do-pmo.md` | antes de responder (ler a memória) e ao fim (gravar) |
| `queries.md` | ao consultar — cada consulta nas duas sintaxes |
| `formulas-espelho.md` | ao precisar de qualquer derivado (pontos, aging, sinal de prazo…) — a API não devolve fórmula |
| `conteudo.md` | quando o assunto é peça de conteúdo, fases, calendário |

**Modo fixture.** Se o pedido trouxer um arquivo de dados dizendo "use como resultado da consulta,
não consulte o Notion", trate o arquivo como o retorno das consultas e **não** toque no Notion nem
grave no Log — descreva o que gravaria. É assim que os evals rodam.

**Nomes vêm dos dados, papéis vêm do contexto.** O "quem é quem" do `sistema-mkt.md` serve para
mapear papel → pessoa (quem é o coordenador de MKT, quem é da coordenação) e para checar acesso.
Quando os dados consultados (ou a fixture) trazem os nomes das pessoas, **use esses nomes** — nunca
substitua por nomes do contexto. Se divergirem, diga em uma linha e siga com os dados.

**Some antes de escrever.** Contagens e pontos que você cita precisam fechar entre si (por pessoa
× total, por status × abertas). Se os números lidos não fecham, escreva a discrepância como dado
("carga por pessoa soma 26; lista de atrasadas soma 18") em vez de escolher um em silêncio.

**O que não foi lido é hipótese.** Prazo de gráfica, data de evento, regra de terceiro que não
estava na consulta entra como "não consegui ler" ou "hipótese", nunca como afirmação.

**A regra que sustenta tudo:** a IA sugere, o humano decide. Nada deste plugin muda status,
reprioriza sozinho ou fala com o time. Fala com a coordenação.
