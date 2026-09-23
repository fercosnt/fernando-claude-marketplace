# Plugin MKT Fotona — v2.2.0

O Claude na rotina do **time** de Marketing da Fotona (as 11 pessoas), sobre o sistema no Notion. É
o irmão do `pmo-fotona` com a regra invertida: o PMO lê tudo e escreve pouco; este **escreve o que
a pessoa disse, sobre o trabalho da própria pessoa**, e não lê o que é dos outros.

| Skill | Quem usa | O que faz | O que grava no Notion |
|---|---|---|---|
| **`mkt-ajuda`** | todos | Balcão de dúvidas do sistema — "isso é projeto ou campanha?", "em que área entra essa aula?", "esse campo é o quê?". Explica, diz onde clicar e entrega para a skill que faz | **Nada.** Só explica |
| **`mkt-nova-demanda`** | todos | Abre uma demanda conversando — pergunta quem pede, cobre as 9 perguntas do formulário em ≤ 3 trocas, insiste no "para quê", checa duplicata | 1 página em `Triagem`, só com o que a pessoa disse; inferência vai para `🤖` |
| **`mkt-brief-conteudo`** | social, criação, copy | Briefing da peça na voz da empresa (objetivo · público · mensagem · CTA · o que não dizer · aprovação clínica) | O corpo da página da peça, depois de mostrar |
| **`mkt-pauta-conteudo`** | social media, coord. de criação | Propõe a pauta do mês (e declara a regra), confirma, propõe donos por fase, cria as peças | Mãe + 5 fases (6 em vídeo), prazos escalonados, só o confirmado |
| **`mkt-meu-mes`** | cada pessoa, sobre si | Relatório individual do mês, em absoluto, contra a própria série | Nada; registro no Log do PMO |
| **`mkt-resultados-conteudo`** | social media, quinzenal | Busca alcance e engajamento por publicação no **Reportei** (casando pelo permalink com o `Link do post`), ou aceita os números colados do painel nativo, e lê o que performou por pilar e canal | Só os 3 campos de métrica, só em peça com `Link do post` |

Chame pelo nome (`/mkt-nova-demanda`) ou simplesmente peça: "isso é projeto ou campanha?", "preciso de um carrossel
do GLP1TIGHT pra semana que vem", "monta a pauta de outubro", "escreve o brief desse reels", "como foi meu mês",
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

`evals/` traz **17 casos** com e sem skill sobre **fixtures fictícias** (nomes inventados; nunca o
Notion real), rodados com o `skill-creator`. Nos 11 casos das skills que escrevem: **100% com skill
× 48–56% sem**. Nos 6 casos da `mkt-ajuda`: **93% com skill × 73% sem** — sem ela o Claude responde
razoavelmente, mas monta o card campo a campo (trabalho da `mkt-nova-demanda`), inventa nome de
campo e recusa gestão por falta de acesso em vez de por escopo. O que eles cobrem:
paridade com o formulário (mesma demanda → mesmos campos), o nome sempre perguntado, duplicata antes
de criar, teto de 3 trocas, estrutura da peça (arte = 6 páginas, vídeo = 7, prazos batendo com a
tabela, fim de semana e feriado recuando), recusa de escrita fora da classe, recusa do mês de outra
pessoa, e — no eval do Reportei — casamento por permalink, zero falso tratado como ausência de dado,
e métrica sempre com fonte.

## Histórico

- **2.3.0 (21/09/2026)** — o sistema ganhou o status **`Refação`** (entre `Em produção` e `Em aprovação`) e o
  contador **`Refações`** (automação nativa, sem motivo). **`mkt-ajuda`** responde "não aprovaram, e agora?",
  diz que `Refações` não se zera e não é nota de ninguém, e declara quando o Manual está atrás do
  `sistema-mkt.md`. Evals 20 e 21 novos (fixture `ajuda-manual-refacao.json`): 90% × 79% na bateria de refação.

- **2.2.0 (09/09/2026)** — alinhado ao schema depois da revisão do guia de propriedades (08/09):
  **`mkt-resultados-conteudo`** passa a ler pelos **três ciclos** (D+7 · D+15 · D+30 a partir de
  `Publicado em`; nunca regrava peça em D+30) e grava os 8 campos de métrica (`Alcance`, `Engajamento`,
  `Curtidas`, `Comentários`, `Salvamentos`, `Compartilhamentos`, `Visualizações`, `Seguidores ganhos`)
  sempre com `Ciclo de métricas` e `Métricas atualizadas em`; **`Aprovação clínica`** virou select
  (Não requer · Aguardando · Aprovada · Reprovada) e o checkbox `Requer aprovação clínica?` saiu —
  `mkt-pauta-conteudo` e `mkt-brief-conteudo` leem/escrevem o select; **`mkt-nova-demanda`** escreve
  `Entregas pedidas` (multi) e deixa `Tipo de entrega` para a triagem, e `Origem` só quando o pedido
  vem de fora do MKT (vazio = demanda interna); `mkt-ajuda` conhece `Link da entrega`, o fluxo de
  revisão (Aprovador + Em aprovação) e a automação Tarefa → Base de Conhecimento. Evals 10, 11 e 5
  reescritos; evals 18 (ajuda: entrega/aprovação) e 19 (nova demanda interna com 3 entregas) novos.

- **2.1.0 (06/09/2026)** — entra a **`mkt-ajuda`**, o balcão de dúvidas do sistema. O time é guest e
  não tem Notion AI: dúvida de dois minutos hoje vira interrupção ou chute em campo de
  classificação. Ela só explica — a fronteira que a iteração 2 dos evals cravou é que *explicar o
  que um campo é* é a resposta, e *listar os campos a preencher* já é a `mkt-nova-demanda`.
- **2.0.1 (06/09/2026)** — o escopo do sistema passou a **cinco empresas**: entra a marca pessoal
  `Fernando Costa Jr`, ao lado de Fotona · GTS · Beauty Smile · IC360. A `mkt-brief-conteudo`
  ganhou a regra de voz dela (primeira pessoa, sem inventar opinião do dono da marca).
- **2.0.0 (06/09/2026)** — plugin do time, 5 skills. As três skills da v1 (`mkt-triagem`,
  `mkt-status-semana`, `mkt-relatorio-mensal`) migraram para o `pmo-fotona` v2.0.0: quem as usava
  era a coordenação, não o time. O `shared/` saiu do marketplace.
- **1.0.0 (05/09/2026)** — onda 1: triagem, leitura da semana, relatório mensal.
