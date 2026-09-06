# Sistema MKT Fotona no Notion — referência técnica das skills

Workspace **Beauty Smile**, teamspace **Marketing**. Este arquivo evita que cada skill descubra o
sistema do zero a cada conversa. Se um ID ou nome de campo aqui divergir do Notion, **o Notion
manda** — e vale corrigir este arquivo na mesma sessão, senão o erro volta amanhã.

## IDs dos bancos

| Banco | database_id | data_source (collection) |
|---|---|---|
| 👥 Time | 217d6ac5d83c446d8c442de4ac8d3467 | 300fa19f-88f4-4501-b23e-ad52ba0aa477 |
| 🧭 Áreas | 61123b65bf584de1abd4382a8a248d08 | 3ab4cf16-a805-4166-9c00-926a60a39ece |
| 🎯 Metas & OKRs | 394b0650d843442a9cd54368bd25008a | 8ae9d113-4f43-4084-8d4c-cbc0415a0933 |
| 🚀 Campanhas | 8d295a7efca44854b5913cc408abc8f8 | 009face8-b34b-4959-b814-96addba90ee5 |
| 🗂️ Projetos | 6c2a190b9e924a2ab456e9661db60e9c | 59546e7b-e06b-4254-a91c-e82edd9a0f2d |
| ✅ Tarefas | 907987aef1c54bf0b3e0a5a388fea57d | cffcee09-5386-4445-a171-b9a737b76975 |
| 📚 Base de Conhecimento | e1e460c59b8c493c88508a5892e671a6 | 89d718ed-e89a-42b0-9c3c-1b1a7ccc1b11 |
| 🤝 Reuniões & Atas | 670586fcbe0b4227909d5907881cc83f | c29b9367-f647-4867-ac63-2ccabbaedd81 |
| 🌟 Creators | 3b2081f048114cf08fa4c912a9a805a2 | af9a7622-338a-4970-a60a-c6086a8d2bf5 |
| 📜 Log de Status | 173831e4f45045d3bef2298ec40fa969 | 9aca1777-524b-4f91-a4bd-e571686dd644 |
| 💡 Ideias & Oportunidades | 889d24a37c3a4ce7a97b18e104936fa8 | 09a930da-c293-43b1-be94-6b111f985b81 |

Páginas: 🏠 Central de Comando `3d16049b-8baf-81be-bb5b-f140146e187f` · 🛰️ Painel Executivo
`3d16049b-8baf-8107-924a-cbbdbbe2350a` · 📘 Manual `3d16049b-8baf-81d3-ad1b-d29cb3c3d459`.

## Campos de ✅ Tarefas que as skills usam

**Título:** `Tarefa` · **Status** (Select): Triagem · A fazer · Em produção · Em aprovação ·
Parada/Bloqueada · Concluída · Arquivada · Cancelada.

| Campo | Tipo | O que é |
|---|---|---|
| `Responsável` | Pessoa | Dono único. Obrigatório para sair da triagem |
| `Prazo` | Data | O prazo que a **triagem** definiu |
| `Data desejada` | Data | O prazo que o **solicitante** pediu. Não são a mesma coisa |
| `Estimativa` | Select P/M/G | Vira `Pontos` (P=1 · M=3 · G=8) |
| `Tipo de trabalho` | Select | Planejado · Ad-hoc/Demanda extra · Fire-drill/P0 |
| `Origem` | Select | Quem pediu: LA&HA · Comercial · Diretoria · Eventos · Influencer/Imprensa · Produto · GTS · Beauty Smile · MKT |
| `Canal de entrada` | Select | Form · Manual · Agente · Reunião |
| `Empresa` | Select | Fotona · GTS · Beauty Smile · IC360 |
| `Categoria` | Select | Operacional · Conteúdo |
| `Área` | Relação → 🧭 Áreas | Uma área dona |
| `Prioridade` | Select | P0 · P1 · P2 · P3 |
| `Objetivo / Por quê` | Texto | Por que esta tarefa existe |
| `Motivo do bloqueio` | Texto | Obrigatório quando Parada/Bloqueada |
| `Link do post` | URL | É ele que define publicado, não o status |
| `Data planejada` / `Publicado em` | Data | Quando vai ao ar / quando foi |
| `Prazo interno` | Data | Quando a peça precisa estar pronta e aprovada |
| `Subtarefa de` / `Subtarefas` | Relação (auto) | As fases de uma peça de conteúdo |
| `🤖 Resumo (IA)` · `🤖 Sugestão de triagem (IA)` · `🤖 Analisado em` | Texto/Texto/Data | **Campos de sugestão.** É aqui que a IA escreve |

**Fórmulas prontas (não recalcule na mão):** `Pontos` · `É contêiner?` · `Aberta?` · `Concluída?` ·
`Pontos abertos` · `Pontos atrasados` · `Pontos próximos 7d` · `Pontos concluídos 30d` ·
`Sinal de prazo` (🔴 Atrasada / 🟡 / 🟢) · `Nesta semana?` · `Idade em produção (dias)` ·
`Horas em aprovação` · `Publicado?` · `No prazo editorial?` · `Reativa?` · `Sem dono ou prazo?` ·
`Taxa de engajamento`.

As 11 Áreas: Social Media · Performance · Produto/Lançamentos · Design · Audiovisual ·
Eventos & Congressos · Branding · Web · Comercial · Imprensa · Creators.

## Como consultar

Use `notion-query-data-sources` em **modo SQL** com a URL `collection://<data_source>` como nome da
tabela. Duas armadilhas que custam tempo:

- **Fórmulas não são legíveis por SQL.** Todas as colunas de fórmula estão em
  `notAvailableInQuerySql`. Para ler o valor de uma fórmula, use **modo view** sobre uma view que já
  a exibe, ou reconstrua a condição a partir dos campos crus (ex.: em vez de `Sinal de prazo`, use
  `date:Prazo:start < date('now')` combinado com `Status`).
- **Datas viram três colunas:** `date:Prazo:start`, `date:Prazo:end`, `date:Prazo:is_datetime`.
  `SELECT "Prazo"` não existe.

Pessoa e relação voltam como JSON: `Responsável` é um array de user IDs, `Área` um array de URLs de
página. Para mostrar nome de pessoa, cruze com o banco 👥 Time (campo `Pessoa`) ou com
`notion-get-users`.

## As regras do sistema que mudam a resposta

1. **Contêiner não é trabalho.** Uma peça de conteúdo é uma tarefa-mãe com as fases como
   sub-itens. A mãe agrupa; o trabalho e a métrica vivem nas fases. Filtre `Subtarefas IS EMPTY`
   (ou `É contêiner? = false` quando estiver em modo view) antes de contar qualquer coisa.
2. **`Tipo de trabalho` é classificação de entrada e não se reclassifica.** É o que responde
   "quanto do mês foi consumido por coisa que ninguém planejou". Reclassificar depois faz o número
   mentir.
3. **Cancelada sai de tudo. Arquivada conta como entregue.** São coisas diferentes.
4. **Publicado é o link, não o status.** `Publicado?` lê `Link do post`.
5. **`Data planejada` não se edita quando atrasa.** É ela que revela o furo no calendário.
6. **Percentual é 0–100** neste sistema, nunca 0–1. E contagem de dias usa o dia, não a hora.
7. **A IA sugere, o humano decide.** Escreva inferência nos campos `🤖 ...`; campo real só recebe o
   que uma pessoa confirmou. Erro de IA em campo real é invisível e contamina métrica.

## Quem é quem (banco 👥 Time)

Fernando Costa Neto (Diretor) → Leandro Lomeu (Gerente de MKT, faz a triagem, acumula
Performance/growth) e Amanda Reis Jordão (Growth das BUs externas — Beauty Smile e GTS).
Sob o Leandro: Avinho (Coord. de Criação) → Isabela Canário (Produtor de Mídia Jr) e Luana
(Designer Gráfico); Morena Manhães (Coord. de Eventos) → Marcos (Assistente); Sabrina Amorim
(Comunicação e Produto); Maria Clara Maruchi (Branding e PR); Beatriz (Social Media).

⚠️ **Nem todo mundo tem conta no Notion.** `Responsável` é campo de Pessoa e só aceita membros do
workspace. Quando a pessoa sugerida não tiver conta, diga o nome no texto e **não** tente gravar no
campo — gravar errado é pior que deixar vazio.
