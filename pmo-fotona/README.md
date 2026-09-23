# Plugin PMO Fotona — v2.1.0

O cérebro do agente de PMO do time de Marketing da Fotona. Cinco skills para a **coordenação**
(diretor, gerente de MKT, coordenador de criação) sobre o sistema no Notion — e os mesmos arquivos
alimentam os ritos agendados no n8n (`prompts/`).

| Skill | Nome antigo | Quem usa | Quando |
|---|---|---|---|
| **`pmo-triagem`** | `mkt-triagem` | gerente de MKT | Diariamente, na fila `Status = Triagem` — parte da análise que a IA já fez na entrada |
| **`pmo-status-semana`** | `mkt-status-semana` | coordenação | Segunda de manhã e sexta à tarde — com memória do que o PMO disse antes |
| **`pmo-relatorio-mensal`** | `mkt-relatorio-mensal` | diretor (MKT); coordenação (área, projeto, pessoa) | Fechamento do mês; andamento de projeto; 1:1 |
| **`pmo-briefing`** | — | coordenação | "Como está X?" — projeto, campanha, área, pessoa, sistema |
| **`pmo-replanejamento`** | — | diretor, gerente | Projeto estourou: pede seu palpite, mostra 2–3 cenários, não aplica |

Chame pelo nome (`/pmo-triagem`) ou simplesmente peça: "processa a fila de triagem", "como está a
semana", "relatório de setembro", "como está o CSBD", "o congresso estourou, o que eu corto".
Os gatilhos em linguagem natural das skills antigas continuam funcionando.

## Antes de usar: o contexto

Este plugin **não** carrega IDs de banco nem nomes de pessoas — isso é contexto privado, num
repositório separado. Clone-o uma vez e mantenha atualizado:

```
git clone <repo privado fotona-mkt-contexto> ~/fotona-mkt-contexto
cd ~/fotona-mkt-contexto && git pull      # antes de usar, sempre
```

`CONTEXTO.md` explica a ordem de busca. Sem o contexto, as skills param e dizem o que falta — nunca
inventam ID.

## Como funciona por dentro

- **Um cérebro, duas superfícies.** As skills são a fonte única do julgamento; o n8n carrega
  `prompts/*.md` + `shared/` do repositório e roda os ritos (segunda 8h, sexta 17h, dia 1º, entrada).
  O eval `evals/consistencia/` garante que as duas leem a mesma semana da mesma forma.
- **Memória no Notion**, no banco `🤖 Log do PMO` — nunca na sessão. Toda skill lê o que o PMO já
  disse sobre o alvo e grava o que disse agora, com `Status do fato` (hipótese / confirmado /
  superado) e pede o desfecho.
- **Dado bruto antes da leitura, uma pergunta no fim.** É forma de decisão, não estilo.

## O que estas skills não fazem

Não mudam status, prioridade, prazo ou dono (a triagem aplica em campo real **só** item a item,
depois de confirmação explícita). Não falam com o time — falam com a coordenação. Não comparam
pessoas, não calculam % de utilização, não leem o conteúdo de `Motivo do bloqueio`. Não citam
número que não veio de consulta.

## Pré-requisitos

- Conector do Notion autenticado **pela própria pessoa**, com acesso ao teamspace Marketing (é o
  que preserva a autoria no Log).
- Clone do contexto (acima).
- Para relatórios: skills `docx`, `pdf` e `dataviz` disponíveis; acesso ao GoHighLevel para o MKT.
- O banco `🤖 Log do PMO` criado (F0 do plano) — sem ele as skills só sugerem e avisam que não
  registraram.

## Evals

`evals/evals.json` — rodados com e sem skill sobre **fixtures fictícias** (`evals/fixtures/`), nunca
sobre o Notion real. Inclui evals negativos (escrita fora da classe, comparação entre pessoas,
"aplica tudo") e o de consistência plugin × n8n.

## Histórico

- **2.2.0 (21–22/09/2026)** — **`pmo-status-semana`** lê o status novo **`Refação`** (Q8b): contagem no
  "O que li", bloco 🔁 com a concentração por tipo de entrega/empresa/pilar — nunca por pessoa, e sem
  afirmar motivo —, "contador ausente" quando `Refações` vem vazio, e `Horas em aprovação` lida como da
  rodada atual. **`pmo-relatorio-mensal`** ganha a seção **aprovação sem × com refação** (denominador =
  concluídas que passaram por aprovação desde 21/09; faixas 1 · 2 · 3+; cortes por tipo de entrega,
  empresa e pilar), contada por `scripts/faixas_refacao.py`; no escopo Pessoa recusa refações também fora
  do arquivo. Prompts do n8n (`rito-segunda`, `rito-sexta`) acompanham. Evals 8, 9 e 10 novos
  (fixtures `semana-refacao.json` e `mes-outubro-refacao.json`): relatório 100% × 27%.

- **2.1.0 (09/09/2026)** — `pmo-triagem` lê `Entregas pedidas` e `Solicitante`, decide `Tipo de entrega`
  (uma só; entregas distintas viram sub-itens), lê `Origem` vazia como demanda do próprio MKT e propõe
  `Aprovação clínica = Aguardando` (select; nunca `Aprovada`). `prompts/enriquecimento-entrada.md`
  reescrito para a Onda A no n8n (`MKT — Enriquecimento na entrada`): mesmos campos, saída só-JSON,
  e o aviso ao coordenador de MKT por tarefa nova. Eval 0 ganhou 3 asserções.
- **2.0.0 (06/09/2026)** — primeira versão do cérebro do PMO (5 skills, prompts dos ritos, Log do PMO).

