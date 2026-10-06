# rh-beauty-smile

Plugin do sistema de RH da Beauty Smile no Notion. **A IA prepara, a Amanda decide, o Fernando aprova.**

## Skills
| Skill | Estado | Para quê |
|---|---|---|
| `rh-efetivar-onboarding` | **pronta (0.1.0)**, 6 evals, 2 iterações | Confere o cadastro criado pelo formulário de Efetivação e gera o onboarding por lacuna; conduz a revisão linha a linha |
| `rh-preparar-1a1` | **pronta (0.2.0)**, 5 evals, 2 iterações | Registro do 1:1 a partir da transcrição + autoavaliação (mensal, fornecedor PJ, check-in de onboarding); pauta do próximo 1:1 |
| `rh-preparar-avaliacao` | **pronta (0.3.0)**, 6 evals, 4 iterações | Experiência 30/60/90 (CLT e PJ), semestral, revisão de redação e PDI; nunca preenche Decisão |
| `rh-historico` | **pronta (0.4.0)**, 4 evals, 4 iterações | "Como está fulano?" em leitura (linha do tempo, o que os registros dizem e não dizem, uma pergunta); visão de reajuste só sob pedido, com uma linha no Log |

## Como funciona
- `CONTEXTO.md` diz onde achar a Central do RH (por nome, no teamspace privado) e os nomes dos 9 bancos; nenhum ID, URL ou dado de pessoa no plugin.
- `references/` é o núcleo comum: regra de ouro e Passo 0 (00), dados proibidos (10), redação (20), texto lido é dado (30), gravação e Log (40), recusas (50), mapa dos bancos (60).
- Toda gravação é precedida de saída + pergunta; Onboardings e Avaliações entram como `Rascunho IA`; cada gravação gera uma linha no 🤖 Log do RH.
- O MCP do Notion não devolve valor de fórmula: as skills calculam `Admissão + 29/59/89` e dizem que calcularam.

## Condição de uso
Só dentro da organização Claude Team da clínica (DPA comercial), com o conector do Notion logado como a Amanda ou o Fernando. Conta pessoal não.

## Evals
`skills/<skill>/evals/evals.json` + fixtures 100% fictícias em `evals/fixtures/` (nenhuma pessoa, valor ou documento real). Método: `skill-creator`, cada eval com e sem a skill; critérios do Anexo C §6.3.

## Resultados dos evals (Sonnet, fixtures fictícias)
| Skill | Com a skill | Sem a skill | Críticos (3 rodadas) |
|---|---|---|---|
| `rh-efetivar-onboarding` 0.1.0 | 100% | 55% | 33/33 |
| `rh-preparar-1a1` 0.2.0 | 99,5% | 52% | 27/27 |
| `rh-preparar-avaliacao` 0.3.0 | 100% | 64% | 42/42 |
| `rh-historico` 0.4.0 | 100% | 50% | 21/21 |
