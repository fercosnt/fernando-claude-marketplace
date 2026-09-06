---
name: pmo-status-semana
description: Monta a leitura da semana do time de Marketing da Fotona a partir do Notion — atrasadas, foco dos próximos 7 dias, aprovações estouradas, travadas, carga por pessoa em pontos absolutos e o que o PMO apontou na semana anterior — e entrega um texto pronto para a reunião de segunda e para o grupo da coordenação, fechando com uma pergunta de decisão. Use sempre que pedirem "status da semana", "como estamos", "o que está atrasado", "resumo pra reunião de time", "o que temos essa semana", "prepara a segunda", "leitura da semana", "fechamento da semana", ou qualquer pedido de panorama do que o time de MKT está tocando. Também use para a leitura de sexta (o que fechou, o que escorregou e o padrão por trás). É a mesma leitura que o n8n gera agendado.
---

# A semana do MKT em um texto

Uma reunião de time que começa com "o que cada um tem?" gasta os primeiros 20 minutos
reconstruindo o que o Notion já sabe. Esta skill produz o texto que substitui essa reconstrução —
e, mais importante, aponta as **três coisas que precisam de decisão** em vez de listar tudo.

Ela também é o rito de segunda 8h e o de sexta 17h que o n8n dispara: os prompts do n8n derivam
desta skill, e um eval garante que as duas superfícies leem a mesma semana da mesma forma. Se você
mudar uma regra aqui, mude lá.

Leia `../../CONTEXTO.md` e carregue o contexto. `formato-de-saida.md` tem o esqueleto.

## Duas leituras, escolha pelo contexto

- **Segunda (padrão):** olha para frente. O que vence, o que já venceu, o que está travando.
- **Sexta:** olha para trás. O que fechou, o que escorregou para a semana que vem, o que entrou sem
  ter sido planejado — e **o padrão por trás**, não o evento.

Se o pedido não disser, use o dia de hoje para decidir e diga qual escolheu.

## O que consultar (queries.md)

Sempre sem contêiner e sem `Cancelada`:

1. **Atrasadas** — Q3.
2. **Foco da semana** — Q4.
3. **Em aprovação** — Q5, ordenadas pela mais antiga. Acima de 48h é fila, não aprovação. Carimbo
   `Entrou em aprovação em` vazio → "carimbo ausente", não zero horas.
4. **Travadas** — Q6. `Motivo do bloqueio` só como escrito/não escrito; sem motivo é um achado por
   si só. **Não leia nem cite o conteúdo do motivo** — pode ser dado sensível sobre a pessoa.
5. **Em triagem há mais de 2 dias úteis** — Q1.
6. **Carga** — Q9: pontos abertos · atrasados · itens em produção por responsável, em absoluto.
   Bloqueada conta. Creators fora.
7. **Conteúdo da semana** — Q10: o que vai ao ar e o que passou da `Data planejada` sem
   `Link do post` (furo de calendário).
8. **Memória** — o 🤖 Log do PMO dos últimos 14 dias: o que a leitura anterior apontou e o desfecho
   de cada registro (`log-do-pmo.md` §Como ler). Na sexta, também os registros `Sem resposta` da
   semana — são os que vão ser cobrados.
9. **Na sexta**, troque 1 e 2 por: concluídas nos últimos 7 dias (Q11 com o período da semana), e o
   que tinha prazo na semana e não fechou.

Todo derivado (pontos, aging, horas, sinal) vem de `formulas-espelho.md` — a API não devolve
fórmula. Se uma consulta falhar, escreva "não consegui ler X" no bloco de dados e siga.

## Como escrever

Este texto vai ser lido no celular, em pé, antes da reunião. Ele funciona se a pessoa entender a
situação nos primeiros 10 segundos. Use o esqueleto de `formato-de-saida.md` — a ordem é **dado
bruto → leitura → uma pergunta**, e essa ordem não é estilo: é o que faz o leitor discordar quando
deve, em vez de aceitar por inércia.

```
📊 Semana do MKT — <data>

<Uma frase com o estado geral: o número que mais importa esta semana e o que ele significa.>

📥 O que li
• N abertas · N atrasadas · N em aprovação (mais antiga: Xh) · N travadas · N em triagem há >2d
• Não consegui ler: <ou "tudo lido">

🔴 Precisa de decisão hoje
• <item> — <quem> — <o que está travando e o que resolveria>
(no máximo 3; se não houver nenhum, escreva "nada travado" e siga)

📅 Vence nesta semana (N)
• <agrupado por pessoa, no máximo 2 linhas por pessoa>

✋ Aprovação parada
• <item> — <Xh> com <aprovador>

⚖️ Carga (pontos abertos · atrasados · em produção)
<Uma linha por pessoa que está fora do padrão dela, para mais ou para menos. Não liste o time todo.
Nunca %, nunca ordenado por desempenho.>

📣 Conteúdo
<O que vai ao ar esta semana e o que já passou da data sem link.>

🧠 O que o PMO disse semana passada
• <registro + desfecho — ou "sem registro">
• <na sexta: o que ficou sem resposta>

❓ Uma decisão para hoje
<a pergunta que só a coordenação responde>
```

Regras de escrita que fazem diferença:

- **Nunca liste mais de 5 itens por bloco.** Acima disso, dê o número e o link da view. Lista de 30
  linhas não é informada, é ignorada.
- **Diga o que fazer, não só o que está errado.** "Aprovação do carrossel parada há 3 dias com a
  coordenadora de PR" é um fato; "…— vale cobrar hoje ou passar para o backup" é uma leitura.
- **Não compare pessoas.** Funções diferentes têm ritmos diferentes; comparar vira ranking e
  ranking mata o preenchimento honesto. Carga em absoluto, contra o padrão da própria pessoa, só
  no canal da coordenação. Sem adjetivo sobre ninguém.
- **Padrão só com contagem.** "Terceira semana seguida com aprovação estourando o SLA" vale mais que
  qualquer número isolado — e precisa do Log ou de contagem para ser dito. Sem base, escreva
  "impressão", ou não escreva.
- **Português do time.** Sem "throughput", sem "WIP" — a não ser que quem pediu use esses termos.
- **≤ 400 palavras.**

## Entrega e memória

Devolva o texto direto na conversa, pronto para copiar. Se pedirem para mandar no grupo, ofereça —
mas mostre o texto antes; mensagem para o grupo não se manda sem alguém ler. O agente não fala com o
time: este texto vai para a coordenação.

Se for para a reunião, acrescente no fim **três perguntas** que a leitura levantou e que só uma
pessoa pode responder — além da pergunta de decisão do esqueleto, que é uma só.

Grave no 🤖 Log do PMO um registro `Tipo = Leitura da semana` (ou `Fechamento`), `Rito = Sob
demanda`, com `Dado observado` = bloco "O que li", `Sugestão` = os blocos de decisão, `Confiança`,
`Status do fato = Hipótese`. Se a semana tinha registros sem desfecho, pergunte o desfecho de cada
um em uma linha e grave. Feche perguntando: "aceita a leitura, ajusta, ou discorda — e por quê?".
