# §10.1 Entrevista Universal (U1–U6)

> Contrato LOCKED — todas as 8 skills verticais (`deck-fundraising`, `deck-sales`, `deck-clinical`, `deck-equipment`, `deck-teaching`, `deck-proposal`, `deck-scientific`, `deck-internal`) **FAZEM** estas 6 perguntas **antes** de divergir para perguntas próprias da vertical.

## As 6 perguntas

| # | Pergunta | Tipo | Default inferido |
|---|----------|------|-----------------:|
| **U1** | Qual o objetivo único deste deck? (ação que a audiência deve tomar após assistir) | texto | — |
| **U2** | Quem é a audiência? (perfil + nível de senioridade + conhecimento prévio) | texto | inferir de CLAUDE.md |
| **U3** | Quanto tempo de apresentação? | (1) 3–5min (2) 7–12min (3) 15–20min (4) 30–45min (5) 60min+ | inferir do contexto |
| **U4** | Formato de entrega? | (1) pitch presencial (2) call remota (3) envio para leitura (4) híbrido | (2) call remota |
| **U5** | Big Idea em 1 frase (tese central que vai ficar quando esquecerem tudo) | texto curto | gerar 3 opções pro usuário escolher |
| **U6** | Marca/cliente? | (auto-detect §10.5) | regex + keywords |

## Saídas obrigatórias

Cada skill DEVE produzir as variáveis abaixo a partir das respostas:

```yaml
objetivo: <U1>
audiencia: <U2>
duracao_min: <U3>
formato: <U4>
big_idea: <U5>
marca: <U6>
```

Estas variáveis preenchem o cabeçalho `## Meta` do `STORYBOARD.md` (ver `storyboard-schema.md`).

## Regras de eficiência

- Se `routing-matrix.md` aplicou **routing-first** (D10 — 2+ keywords de mesma rota), pule U1–U3.
- Se auto-detection de marca (§10.5) já resolveu U6, **não pergunte**.
- Se 1-2 keywords ambíguas, **pergunte U1-U3** antes de re-classificar.
- Entrevista universal deve consumir **≤ 2 minutos** do usuário.

## Big Idea (U5) — geração assistida

Se o usuário hesitar em U5, **gere 3 opções** baseadas no que já sabe (objetivo + audiência + marca) e peça para ele escolher/ajustar. Big Idea é a única frase que precisa "ficar" — não pode ser vago.

Exemplos de Big Idea bem-feita:
- "Crescemos 10x em 24 meses com 0,3% CAC sobre receita." (fundraising)
- "Er:YAG não é laser de corte — é instrumento de precisão biológica." (teaching)
- "Cada R$1 em viagens precisa devolver R$3 ou não autorizamos." (internal pitch)

## Cross-references

- `routing-matrix.md` — algoritmo que decide quando pular U1-U3
- `auto-detection-brands.md` — resolve U6 automaticamente
- `storyboard-schema.md` — onde as saídas viram cabeçalho `## Meta`
