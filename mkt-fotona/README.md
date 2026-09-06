# Plugin MKT Fotona — onda 1

Três skills que põem o Claude dentro da rotina do time de Marketing da Fotona, já sabendo os IDs dos
bancos do Notion, os nomes dos campos e as regras que não são óbvias.

| Skill | Quem usa | Quando |
|---|---|---|
| **`mkt-triagem`** | Leandro | Diariamente, na fila `Status = Triagem` |
| **`mkt-status-semana`** | Coordenação | Segunda de manhã (e sexta, para o fechamento da semana) |
| **`mkt-relatorio-mensal`** | Fernando | No fechamento do mês |

Chame pelo nome (`/mkt-triagem`) ou simplesmente peça: "processa a fila de triagem", "como está a
semana", "monta o relatório de setembro".

## Como funciona por dentro

`shared/sistema-mkt.md` é o mapa do sistema — IDs dos 11 bancos, campos de ✅ Tarefas, as fórmulas
que já existem (não recalcule na mão), as duas armadilhas de SQL do conector do Notion e as sete
regras do sistema. As três skills leem esse arquivo antes de consultar qualquer coisa.

## Pré-requisitos

- **Conector do Notion** autenticado, com acesso ao teamspace **Marketing** do workspace Beauty
  Smile. Idealmente **cada pessoa autentica o próprio** — é o que preserva a autoria do que for
  criado.
- **Conta no Notion** para quem vai aparecer como `Responsável`: é campo de Pessoa e só aceita
  membros do workspace.
- Para o relatório mensal: acesso ao **GoHighLevel** (leads, oportunidades, receita influenciada) e
  a skill `docx` disponível.

## O que estas skills não fazem

Não mudam status de tarefa fora da triagem, não repriorização de board, não falam com o time e não
escrevem inferência em campo real — inferência vai nos campos `🤖 ...`, e a decisão fica com a
pessoa. Erro de IA em campo real é invisível e contamina métrica.

Ondas 2 e 3 (pauta de conteúdo, briefing, entrada conversacional, ata, resultados, vigia) estão
planejadas em `01-blueprint-notion/14-plano-plugin-e-skills.md`.
