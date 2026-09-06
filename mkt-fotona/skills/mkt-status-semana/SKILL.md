---
name: mkt-status-semana
description: Monta a leitura da semana do time de Marketing da Fotona a partir do Notion — atrasadas, foco dos próximos 7 dias, aprovações estouradas, travadas e carga por pessoa — e entrega um texto pronto para a reunião de segunda e para mandar no grupo. Use sempre que pedirem "status da semana", "como estamos", "o que está atrasado", "resumo pra reunião de time", "o que temos essa semana", "prepara a segunda", "manda no grupo o que está pendente", ou qualquer pedido de panorama do que o time de MKT está tocando. Também use para a leitura de sexta (o que fechou na semana).
---

# A semana do MKT em um texto

Uma reunião de time que começa com "o que cada um tem?" gasta os primeiros 20 minutos
reconstruindo o que o Notion já sabe. Esta skill produz o texto que substitui essa reconstrução —
e, mais importante, aponta as **três coisas que precisam de decisão** em vez de listar tudo.

Leia `../../shared/sistema-mkt.md` antes de consultar: IDs, campos e as armadilhas de SQL.

## Duas leituras, escolha pelo contexto

- **Segunda (padrão):** olha para frente. O que vence, o que já venceu, o que está travando.
- **Sexta:** olha para trás. O que fechou, o que escorregou para a semana que vem, o que entrou sem
  ter sido planejado.

Se o pedido não disser, use o dia de hoje para decidir e diga qual escolheu.

## O que consultar

Sempre excluindo contêineres (`Subtarefas IS EMPTY`) e `Cancelada`, porque contêiner não é trabalho
e cancelada não é atraso:

1. **Atrasadas** — abertas com `date:Prazo:start` anterior a hoje.
2. **Foco da semana** — abertas com prazo nos próximos 7 dias.
3. **Em aprovação** — `Status = 'Em aprovação'`, ordenadas pelo mais antigo
   (`date:Entrou em aprovação em:start`). Acima de 48h é fila, não aprovação.
4. **Travadas** — `Status = 'Parada/Bloqueada'`, com `Motivo do bloqueio`. Sem motivo escrito é um
   achado por si só.
5. **Carga** — pontos abertos por `Responsável`, para comparar com a capacidade do banco 👥 Time.
6. **Conteúdo da semana** — `Categoria = 'Conteúdo'` com `Data planejada` nos próximos 7 dias, e as
   que passaram da data planejada sem `Link do post` (furo de calendário).
7. **Na leitura de sexta**, troque 1 e 2 por: concluídas nos últimos 7 dias, e o que tinha prazo na
   semana e não fechou.

## Como escrever

Este texto vai ser lido no celular, em pé, antes da reunião. Ele funciona se a pessoa entender a
situação nos primeiros 10 segundos.

```
📊 Semana do MKT — <data>

<Uma frase com o estado geral: o número que mais importa esta semana e o que ele significa.>

🔴 Precisa de decisão hoje
• <item> — <quem> — <o que está travando e o que resolveria>
(no máximo 3; se não houver nenhum, escreva "nada travado" e siga)

📅 Vence nesta semana (N)
• <agrupado por pessoa, no máximo 2 linhas por pessoa>

✋ Aprovação parada
• <item> — <Xh> com <aprovador>

⚖️ Carga
<Uma linha por pessoa que está fora da faixa, para mais ou para menos. Não liste o time todo.>

📣 Conteúdo
<O que vai ao ar esta semana e o que já passou da data sem link.>
```

Regras de escrita que fazem diferença:

- **Nunca liste mais de 5 itens por bloco.** Acima disso, dê o número e o link da view. Lista de 30
  linhas não é informada, é ignorada.
- **Diga o que fazer, não só o que está errado.** "Aprovação do carrossel parada há 3 dias com a
  Marina" é um fato; "…— vale cobrar hoje ou passar para o backup" é uma leitura.
- **Não compare pessoas por pontos.** Funções diferentes têm ritmos diferentes; comparar vira
  ranking e ranking mata o preenchimento honesto. Compare cada pessoa com a própria capacidade.
- **Fale de tendência quando tiver base.** "Terceira semana seguida com aprovação estourando o SLA"
  vale mais que qualquer número isolado. Sem histórico, não invente tendência.
- **Português do time.** Sem "throughput", sem "WIP" — a não ser que quem pediu use esses termos.

## Entrega

Devolva o texto direto na conversa, pronto para copiar. Se pedirem para mandar no Teams ou no
WhatsApp, ofereça — mas mostre o texto antes; mensagem para o time inteiro não se manda sem alguém
ler.

Se for para a reunião, acrescente no fim **três perguntas** que a leitura levantou e que só uma
pessoa pode responder. É o que transforma o relato em pauta.
