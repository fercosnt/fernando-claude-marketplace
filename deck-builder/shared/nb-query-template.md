# §10.6 NB Query Template

> Contrato LOCKED — todas as skills consultam NotebookLM via CLI subcomando `ask` (verificado, não é `chat`).

## Comando padrão

```bash
notebooklm use <NB_ID>             # set context
notebooklm ask "<pergunta>" --max-citations 5
```

## Os 3 NotebookLMs do plugin

| NB | ID | Sources | Cobertura |
|----|------|---------|-----------|
| **NB1 Core Transversal** | `7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da` | 243 | Frameworks gerais de comunicação, storytelling, design de slides — usado por TODAS as skills |
| **NB2 Verticais Densas** | `1635d16b-773c-480d-89c2-79c717f4b2e1` | 223 | Clínico, científico, ensino, equipamentos médicos — usado por `deck-clinical`, `deck-scientific`, `deck-teaching`, `deck-equipment` |
| **NB3 Verticais Comerciais** | `5a0aaabb-78c1-4d03-a400-e9ce1973737b` | 268 | Vendas, fundraising, proposta, pitch interno — usado por `deck-sales`, `deck-fundraising`, `deck-proposal`, `deck-internal` |

**Total:** 734 sources curados.

## Convenções

- Cada skill cita **até 3 NBs** — NB1 sempre + 1-2 verticais
- Toda query inclui a **Big Idea (U5)** para contextualizar
- Falha do NB **NÃO bloqueia** a skill — degrada com warning e segue com conhecimento base

## Template de query

```bash
notebooklm use $NB_ID
notebooklm ask "Para um pitch [vertical] com Big Idea '$U5', \
  audiência '$U2', duração $U3min, formato $U4: \
  qual o framework mais aplicável e quais slides são obrigatórios?" \
  --max-citations 5
```

## Exemplo concreto (deck-fundraising)

```bash
notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da   # NB1
notebooklm ask "Pitch anjo Beauty Smile R$500k, Big Idea \
  'crescemos 10x em 24 meses com 0,3% CAC', \
  audiência 'investidor anjo regional', formato 'pitch presencial 15min': \
  estrutura Sequoia ou YC? Andy Raskin se aplica?" \
  --max-citations 5

notebooklm use 5a0aaabb-78c1-4d03-a400-e9ce1973737b   # NB3
notebooklm ask "Slide 4 Promised Land (Andy Raskin) para pitch anjo \
  early-stage com tração comprovada: estrutura concreta?" \
  --max-citations 5
```

## Degradação sem NotebookLM

Se `notebooklm` não está instalado ou NB está offline:

```
[warn] NotebookLM offline (NB1: 7f1b2e2b...) — gerando com conhecimento base
```

Skill continua, mas:
- `Speaker notes` ficam menos densas
- Não cita papers/livros específicos
- Avisa usuário no final do storyboard

## Cross-references

- `skill-frontmatter.md` — declara `nb_ids:` por skill
- `fronteiras-explicitas.md` — NB não é pré-requisito (D11)
