---
name: pmo-briefing
description: Responde "como está X?" sobre o sistema de MKT da Fotona no Notion — X sendo um projeto, uma campanha, uma área, uma pessoa (só para a coordenação), a semana ou o sistema inteiro — com o dado bruto antes da leitura, o risco, uma recomendação com confiança declarada, e o que o Log do PMO já dizia sobre o alvo. Grava a leitura no projeto e no Log. Use sempre que a coordenação perguntar "como está o projeto X", "e o congresso", "como anda a campanha Y", "o que tem de risco em Z", "me dá um panorama de", "status de", "briefing de", "como está a Criação", "como está a carga do fulano", ou qualquer pergunta de situação sobre algo específico do MKT — mesmo sem a palavra briefing. Não use para a leitura completa da semana (isso é pmo-status-semana) nem para propor replanejamento (pmo-replanejamento).
---

# Briefing sob demanda — "como está X?"

Esta é a skill mais usada do PMO conversacional, e a mais perigosa de ficar convincente demais. Um
briefing bem escrito e errado é aceito com a mesma facilidade que um certo — a evidência é clara que
explicação bonita **aumenta** a aceitação de sugestão errada. Por isso a estrutura é rígida: o dado
vem antes da leitura, a confiança é declarada, e o que o PMO disse antes é citado como o que era
(hipótese, confirmado), nunca como fato próprio.

Leia `../../CONTEXTO.md` e carregue o contexto. `formato-de-saida.md` é a forma; `log-do-pmo.md`
é a memória.

## 1. Resolva o alvo

X pode ser: **projeto** · **campanha** · **área** · **pessoa** · **semana** · **sistema**. Nome
aproximado é normal ("o congresso", "CSBD", "a criação", "a Bia"). Procure pelo título nos bancos
(projetos ativos Q13, campanhas, áreas, 👥 Time) e, se houver mais de um candidato ou nenhum, pergunte
em uma linha — nunca chute o alvo.

**Pessoa** só para a coordenação: confira o usuário do conector contra o "quem é quem". Fora da
coordenação, recuse e aponte o `mkt-meu-mes` (cada um vê o próprio). Creators (PJ) não têm briefing.

## 2. Leia — o alvo, e o que o PMO já disse

| Alvo | Consultas |
|---|---|
| Projeto | a página (Q13) + tarefas do projeto (Q14): status, atrasadas, aging máximo, `Bloqueada por`, RAG e `Motivo (se 🟡/🔴)`, `Última atualização de status` |
| Campanha | a página + tarefas e conteúdos ligados, publicados, investimento/leads/CPL |
| Área | Q2 filtrada pela área: abertas, atrasadas, em aprovação, travadas, % reativo (`formulas-espelho`), projetos ativos da área |
| Pessoa | Q9 só dela: pontos abertos · atrasados · em produção, aging dos itens dela, aprovações paradas com ela como aprovadora — **absoluto, sem colega** |
| Semana | é o `pmo-status-semana`; chame-o |
| Sistema | contagens gerais (Q2, Q3, Q5, Q6, Q1) + projetos por RAG |

Depois, o **🤖 Log do PMO** dos últimos 14 dias sobre o mesmo alvo (`log-do-pmo.md` §Como ler).
Todo derivado (pontos, aging, horas, progresso, saúde sugerida) vem de `formulas-espelho.md`.
`Motivo do bloqueio` entra só como "existe / não existe"; nunca leia nem cite o conteúdo.

Se uma consulta falhar, escreva "não consegui ler X" e siga com o que tem. Nunca estime.

## 3. Responda nesta ordem, em ≤ 250 palavras

```
📌 <Alvo> — <data>

📥 Dado
• <contagens e itens: N tarefas por status · N atrasadas · aging máximo X dias (<tarefa>) ·
  RAG <cor> [sem motivo escrito] · última atualização há N dias · dependências travadas: N>
• Não consegui ler: <ou "tudo lido">

🧠 O que o PMO já dizia
• <registro do Log com status do fato e desfecho — ou "sem registro">

🔎 Leitura
<Um parágrafo: o risco, o que travaria, o que muda se nada for feito. Sem adjetivo sobre pessoa.>

✅ Recomendação (confiança: Alta | Média | Baixa — por quê em meia frase)
<Uma ação. Se for replanejar, não proponha aqui: diga "isso é replanejamento" e ofereça o
pmo-replanejamento, que pede o seu palpite antes de mostrar cenários.>

❓ <Uma pergunta que só você responde>
```

Para **pessoa**, o bloco de dado é o do `template-pessoa.md` do relatório, resumido; nada de
comparação, %, adjetivo. Se pedirem "quem está pior?" ou "compara com o fulano", recuse em uma
linha e ofereça a leitura por área.

## 4. Grave

- Se o alvo é um **projeto**: escreva a leitura em `🤖 Leitura do PMO` e hoje em `🤖 Analisado em`
  (campos de sugestão do banco 🗂️ Projetos — se ainda não existirem, diga e não escreva). Nunca
  toque em `Saúde (RAG)`, `Status` ou `Prazo`.
- Sempre: um registro no 🤖 Log do PMO (`Tipo` conforme o alvo, `Rito = Sob demanda`),
  `Dado observado` = bloco 📥, `Sugestão` = recomendação, `Confiança`, `Status do fato = Hipótese`,
  `Decidido por` = quem perguntou.
- Feche pedindo o desfecho em uma linha: "aceita / ajusta / discorda — e por quê?". Se responder,
  grave `Desfecho`, `Motivo do desfecho` e `Sugestão procedente?`.

## O que esta skill não faz

Não muda status, RAG, prazo ou dono. Não propõe cenários de replanejamento (é outra skill, com outra
regra: palpite antes). Não fala com o time — a resposta é para quem perguntou, na coordenação.
