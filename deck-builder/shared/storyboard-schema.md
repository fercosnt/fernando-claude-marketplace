# §10.2 STORYBOARD.md Schema

> Contrato LOCKED — schema único para todos os modos **EXCETO** `deck-scientific` poster (que usa `POSTER.md`, ver D8).
> Linter shell `scripts/lint-storyboard-schema.sh` valida outputs reais.

## Esqueleto canônico

```markdown
# Deck: {nome-deck}

## Meta
- Skill geradora: deck-{vertical}
- Objetivo único: {U1}
- Audiência: {U2}
- Duração: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: {ex: Sequoia + Andy Raskin}
- Modo: {se aplicável}
- max_ctas: {1 default; deck-teaching até 4; deck-scientific até 3 — D14}
- Gerado em: {ISO date}
- Versão: v1 | v2 | ...
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa
{2-3 parágrafos sobre o arco narrativo escolhido}

## Slide 1 — Capa
Tipo: capa
Action title: {headline assertivo, NÃO título descritivo}
Mensagem-chave: {1 frase}
Speaker notes: {2-3 parágrafos}
Visual: {descrição neutra}
Prompt de imagem: {SE tipo na whitelist D5 — deck-image-prompts preenche; senão skip}
Tempo estimado: {seg}
Objeção esperada: {se aplicável}

## Slide 2..N — {Tipo}
(tipos canônicos: capa | problema | contexto | conceitual | dados | comparativo |
 prova-social | equipe | demo | financeiro | CTA | disclaimer | agradecimento | apêndice)

## Apêndice (slides opcionais)

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide N: {brief}

## Checklist de Revisão (handoff pra deck-reviewer)
- [ ] Action titles (não títulos descritivos)
- [ ] 1 ideia por slide
- [ ] Horizontal logic test
- [ ] Hook do slide 1 testado contra /copy
- [ ] CTA único (ou até max_ctas)
- [ ] {se clínico} Compliance CFO/CFM/Anvisa
- [ ] {se científico} Citações com GRADE
- [ ] {se vendas/captação} ROI/payback explícito

## Compliance & Disclaimers (3 tiers — D7)
🔴 Issues bloqueantes (resolver antes de apresentar):
- {issues 🔴}

🟡 Verificar antes:
- {issues 🟡}

✅ OK:
- {confirmações}
```

## Tipos de slide canônicos

| Tipo | Quando usar | Whitelist image-prompts (D5) |
|------|-------------|------------------------------|
| `capa` | Slide 1 sempre | ✅ Preencher prompt |
| `problema` | Articular dor | ✅ Preencher prompt |
| `contexto` | Background/setup | Skip |
| `conceitual` | Apresentar tese/framework | ✅ Preencher prompt |
| `dados` | Números, gráficos, charts | Skip *(override scientific: ✅)* |
| `comparativo` | A vs B, antes/depois | ✅ Preencher prompt |
| `prova-social` | Logos, depoimentos, cases | ✅ Preencher prompt |
| `equipe` | Founders, team slide | ✅ Preencher prompt |
| `demo` | Demonstração funcional | ✅ Preencher prompt |
| `financeiro` | Pricing, projeções, unit economics | Skip |
| `CTA` | Call to action / ask | Skip |
| `disclaimer` | Forward-looking, compliance | Skip |
| `agradecimento` | Slide final relacional | Skip |
| `apêndice` | Backup material | Skip |

## Regras invioláveis

1. **Action titles** (não títulos descritivos). Errado: "Mercado". Certo: "Mercado dobra a cada 18 meses."
2. **1 ideia por slide.** Múltiplas ideias = mais slides, não mais texto.
3. **Hook do slide 1** testado contra a Escala de Schwartz (consciência da audiência).
4. **CTA único** (ou até `max_ctas` declarado no `## Meta`).
5. **Bloco compliance 3 tiers sempre presente** (mesmo que ✅ OK seja "Nenhuma issue").
6. **Versão `## Meta` completa** — linter rejeita Meta truncada.

## Cross-references

- `entrevista-universal-u1-u6.md` — origem dos campos `## Meta`
- `output-convention.md` — onde o arquivo é salvo
- `../scripts/lint-storyboard-schema.sh` — validação automática
- D8 (override): `deck-scientific` modo poster usa `POSTER.md`, não este schema
