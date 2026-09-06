# Plugin MKT Fotona — v2.0.0

O Claude na rotina do **time** de Marketing da Fotona (as 11 pessoas), sobre o sistema no Notion. É
o irmão do `pmo-fotona` com a regra invertida: o PMO lê tudo e escreve pouco; este **escreve o que
a pessoa disse, sobre o trabalho da própria pessoa**, e não lê o que é dos outros.

| Skill | Quem usa | O que faz | O que grava no Notion |
|---|---|---|---|
| **`mkt-nova-demanda`** | todos | Abre uma demanda conversando — pergunta quem pede, cobre as 9 perguntas do formulário em ≤ 3 trocas, insiste no "para quê", checa duplicata | 1 página em `Triagem`, só com o que a pessoa disse; inferência vai para `🤖` |
| **`mkt-brief-conteudo`** | social, criação, copy | Briefing da peça na voz da empresa (objetivo · público · mensagem · CTA · o que não dizer · aprovação clínica) | O corpo da página da peça, depois de mostrar |
| **`mkt-pauta-conteudo`** | social media, coord. de criação | Propõe a pauta do mês (e declara a regra), confirma, propõe donos por fase, cria as peças | Mãe + 5 fases (6 em vídeo), prazos escalonados, só o confirmado |
| **`mkt-meu-mes`** | cada pessoa, sobre si | Relatório individual do mês, em absoluto, contra a própria série | Nada; registro no Log do PMO |
| **`mkt-resultados-conteudo`** | social media, quinzenal | Pede alcance, engajamento e cliques das peças publicadas (do painel nativo — o GHL não devolve métrica por post, testado em 06/09) e lê o que performou por pilar e canal | Só os 3 campos de métrica, só em peça com `Link do post` |

Chame pelo nome (`/mkt-nova-demanda`) ou simplesmente peça: "preciso de um carrossel do GLP1TIGHT
pra semana que vem", "monta a pauta de outubro", "escreve o brief desse reels", "como foi meu mês",
"atualiza as métricas dos posts".

## O que nenhuma skill deste plugin faz

Mudar `Status`, `Prazo`, `Responsável`, `Prioridade`, `Tipo de trabalho` ou `Estimativa` de
qualquer tarefa existente (mover card é na UI; dono e prazo são triagem). Ler carga, aging ou
atraso de outra pessoa (isso é o `pmo-fotona`, da coordenação). Mostrar o mês de outra pessoa.
Publicar. Criar projeto ou campanha. O formulário 📥 Solicitações continua existindo e é o padrão
se as duas portas divergirem.

## Antes de usar: o contexto

Este plugin **não** carrega IDs de banco nem nomes de pessoas — isso é contexto privado, num
repositório separado, o mesmo do `pmo-fotona`. Clone-o uma vez e mantenha atualizado:

```
git clone git@github.com:fercosnt/fotona-mkt-contexto.git ~/fotona-mkt-contexto
cd ~/fotona-mkt-contexto && git pull      # antes de usar, sempre
```

`CONTEXTO.md` explica a ordem de busca. Sem o contexto, as skills param e dizem o que falta — nunca
inventam ID. O conector do Notion precisa estar autenticado **na sua conta** (guest do workspace).

## Instalar

```
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install mkt-fotona@fernando-claude-marketplace
```

## Como foi testado

`evals/` traz os casos com e sem skill sobre **fixtures fictícias** (nomes inventados; nunca o Notion
real), rodados com o `skill-creator`. O que os evals cobrem: paridade com o formulário (mesma demanda
→ mesmos campos), o nome sempre perguntado, duplicata antes de criar, teto de 3 trocas, estrutura da
peça (arte = 6 páginas, vídeo = 7, prazos batendo com a tabela, fim de semana recuando), recusa de
escrita fora da classe, recusa do mês de outra pessoa, métrica só com fonte.

## Histórico

- **2.0.0 (06/09/2026)** — plugin do time, 5 skills. As três skills da v1 (`mkt-triagem`,
  `mkt-status-semana`, `mkt-relatorio-mensal`) migraram para o `pmo-fotona` v2.0.0: quem as usava
  era a coordenação, não o time. O `shared/` saiu do marketplace.
- **1.0.0 (05/09/2026)** — onda 1: triagem, leitura da semana, relatório mensal.
