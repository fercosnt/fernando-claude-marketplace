---
name: mkt-relatorio-mensal
description: Escreve o relatório mensal de Marketing da Fotona para a diretoria e o CEO, puxando os números do Notion (projetos, tarefas, campanhas, conteúdo, carga, metas) e do GoHighLevel, no template da casa, e entrega como .docx. Use sempre que pedirem "relatório mensal", "relatório da diretoria", "fechamento do mês do marketing", "como foi o mês", "números para o CEO", "consolidar o mês", "apresentação de resultados do MKT", ou quando for dia de fechar o mês. Também use para preparar a leitura de um trimestre ou de uma campanha encerrada.
---

# Relatório mensal de MKT

Este relatório é lido por quem não acompanha o Notion. Ele funciona quando responde três coisas em
uma página: **o que o marketing fez avançar no negócio, o que está em risco, e o que precisa de
decisão.** Número que não muda nenhuma decisão é ruído — e ocupa o lugar do que importa.

Leia `../../shared/sistema-mkt.md` antes de consultar. O template está em
`assets/template-relatorio.md` e a definição de cada KPI, em `assets/kpis.md` — **leia os dois antes
de escrever**, porque quase todo erro neste relatório é de definição, não de conta.

## Ordem de trabalho

### 1. Fixe o período e confirme

Padrão: mês anterior fechado. Diga qual período está usando na primeira frase e siga — se estiver
errado, é barato corrigir; parar para perguntar o óbvio custa mais.

### 2. Colete os números

Do **Notion**, sempre excluindo contêineres (`Subtarefas IS EMPTY`) e `Cancelada`:

| O que | Onde |
|---|---|
| Entregas: contagem **e** pontos das concluídas no período | ✅ Tarefas, `Data de conclusão` no mês |
| % no prazo | concluídas com `Data de conclusão` ≤ `Data desejada` (e `Prazo` quando não houver data desejada) |
| Atrasadas no fim do mês, e o que travou | ✅ Tarefas |
| Projetos concluídos, em andamento, farol RAG | 🗂️ Projetos |
| Conteúdo publicado, por canal e por pilar; aderência ao calendário | ✅ Tarefas `Categoria = Conteúdo`, `Link do post` |
| Investimento, leads, CPL, ROI por campanha | 🚀 Campanhas |
| Carga e capacidade | 👥 Time + pontos abertos por responsável |
| % reativo (em pontos) | 🧭 Áreas e ✅ Tarefas |
| Progresso dos OKRs | 🎯 Metas & OKRs |

Do **GoHighLevel**: leads, qualificados, oportunidades, receita influenciada. Se o GHL não estiver
acessível, escreva "não disponível nesta rodada" no lugar — deixar a linha em branco faz o leitor
achar que o resultado foi zero.

### 3. Trate os números com honestidade

Isto é o que separa um relatório confiável de um bonito:

- **Nunca preencha uma célula com estimativa sem marcar.** Se um número foi inferido, ele leva um
  asterisco e uma nota. Um número inventado descoberto uma vez contamina o relatório inteiro para
  sempre.
- **Contagem e pontos andam juntos, sempre.** Contagem sozinha trata um story e um vídeo de três
  dias como iguais; pontos sozinhos criam incentivo a inflar estimativa. E **não chame pontos de
  "throughput"** — throughput é contagem de itens.
- **Não publique métrica individual.** Capacidade se reporta no nível do time e da área. A visão por
  pessoa existe, é ferramenta do coordenador, e não vai para a diretoria.
- **Não reporte média de lead time.** Média esconde a cauda, que é onde mora o problema. Enquanto não
  houver histórico para calcular percentil, esta linha simplesmente não existe no relatório.
- **Mês sem base de comparação:** escreva "primeiro mês de medição" em vez de deixar a coluna vazia.

### 4. Escreva

Siga `assets/template-relatorio.md` sem reordenar as seções — a diretoria já sabe onde olhar.

O **resumo executivo** é a única parte que muitos vão ler inteira. Um parágrafo, começando pelo
resultado de negócio e terminando pelo risco principal. Atividade ("publicamos 34 conteúdos") entra
como sustentação, nunca como manchete.

Em **riscos**, cada linha precisa de uma decisão pedida a alguém com nome. "Criação sobrecarregada"
não é risco, é sintoma; "Criação entrou em outubro com mais pontos abertos que a capacidade de duas
semanas — repriorizar o lançamento ou contratar freelancer, decisão do Fernando até dia 10" é risco.

Em **prioridades do próximo mês**, três a cinco, cada uma amarrada a um OKR. Se não amarra, ou o OKR
está errado ou a prioridade está.

### 5. Entregue

Gere o `.docx` seguindo a skill `docx`. Nomeie `Relatorio-MKT-<AAAA-MM>.docx`. Entregue o arquivo e,
no chat, escreva **três linhas**: o resultado do mês, o risco principal, e a decisão que você precisa.
Quem abriu o chat no celular deve conseguir agir sem abrir o anexo.

Ofereça registrar o relatório na 📚 Base de Conhecimento do Notion — é o que constrói a série
histórica que, daqui a dois meses, permite falar de tendência com lastro.

## Sinais de que o relatório está errado

- Todos os KPIs verdes. Ou o mês foi excepcional, ou as metas não são metas.
- Nenhum risco. Um time de 10 pessoas com 4 marcas sempre tem um.
- Mais de 9 KPIs no corpo. O resto é apêndice.
- Um número que você não consegue apontar de onde veio. Tire.
