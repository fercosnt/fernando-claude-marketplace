# Eval cases — `deck-sales` (3 cenarios canonicos)

> Cases que validam DoD da skill. Tres cases cobrem (1) equipamento medico premium / Fotona, (2) franchising consolidado / Beauty Smile, (3) plataforma corporativa B2B / Carnaval 360.

---

## Case 1 — Fotona LightWalker pra dentista premium SP

### Input

```yaml
prompt: "Preciso vender LightWalker pra clinica premium SP — fechar pedido R$280k em 60 dias. Dentista-proprietario decide. Perdemos deals para Lumenis as vezes. Cliente referencia: Smile Premium SP, payback 14 meses."

U1: "Vender LightWalker pra clinica premium SP — fechar pedido R$280k em 60 dias"
U2: "Dentista-proprietario, premium SP, 15+ anos de experiencia, ja referenciada na regiao"
U3: 4 (30-45min — presencial na clinica)
U4: 1 (pitch presencial)
U5: "Voce ja decidiu ser referencia. Hoje, ser referencia exige laser."
U6: Fotona (auto-detect via regex)
S1: R$ 280.000
S2: 60 dias
S3: "dentista-proprietario, dor = diferenciacao competitiva e perda de paciente premium"
S4: "ROI vs concorrente Lumenis"
S5: "Clinica Smile Premium SP, payback 14 meses, ampliou mix premium de 30% pra 52% em 8 meses"
```

### Esperado (assertions auto-verificaveis)

| # | Assertion | Pass criteria |
|---|-----------|---------------|
| 1.1 | Slide 1 = capa com action title = U5 ou variante (NAO "Apresentacao Fotona") | regex no slide 1: NOT contains "obrigado", "apresentacao", "agenda" |
| 1.2 | Slide 2 = insight provocador Challenger com dado de mercado | slide 2 contem: dado de mercado (% ou ano) + reframe + implicacao no cliente |
| 1.3 | Slide 2 NAO contem "obrigado pela reuniao" / "vamos apresentar" | strict regex |
| 1.4 | Slides 3-5 = Gap Selling (Current State quantificado / Custo do status quo em R$ / Future State) | slide 3 tem numero, slide 4 tem R$ e tempo, slide 5 tem numero |
| 1.5 | Slide 6 = Old World vs New World (Raskin) — visual lado a lado | slide 6 contem "Old World" e "New World" OU equivalente bilingue |
| 1.6 | Slides 12-13 = Payback (em meses) + Sensitivity 3 cenarios | slide 12 contem numero de meses; slide 13 contem 3 colunas (pess/base/otim) |
| 1.7 | Payback no cenario base = 14 meses (consistente com S5) | slide 12 menciona "14 meses" como cenario base |
| 1.8 | Slide 14 = comparativo responsavel SEM badmouth de Lumenis | NOT contains: "Lumenis e caro", "Lumenis e ruim", "Lumenis nao funciona"; CONTAINS: "Lumenis — forte em ..." OU equivalente que cita pelo que ELES fazem bem |
| 1.9 | Modo selecionado = `padrao` (NAO `demo-presentation`, pois input nao menciona demo) | cabecalho Meta: `Modo: padrao` |
| 1.10 | CTA unico no slide final (15-18) com data | slide final contem 1 acao + data/prazo concreto |
| 1.11 | Auto-detection Fotona acionou compliance tags ANVISA Classe III | tier 🟡 do compliance contem "ANVISA" |
| 1.12 | Slides whitelist D5 listados em "Storyboard de Imagens" (capa, 2, 6, 11, 14) | seccao "Storyboard de Imagens" contem ≥4 entries |
| 1.13 | Schema §10.2 valido (cabecalho Meta + Estrutura Narrativa + slides + Apendice + Storyboard de Imagens + Checklist de Revisao + Compliance 3 tiers) | grep todas as seccoes obrigatorias |
| 1.14 | `Skill geradora: deck-sales` no cabecalho | cabecalho Meta tem essa linha |
| 1.15 | NB1 + NB3 referenciados (cite 1-3 fontes por NB nas speaker notes ou apendice) | grep "NB1" + "NB3" OU IDs |

### Variacoes possiveis (eval bonus)

- **Case 1a:** mesmo input, mas usuario adiciona "ja apresentamos LightWalker — agora e demo presencial pra fechar" → modo deve mudar para `demo-presentation`
- **Case 1b:** input sem S5 → slide 11 (prova social) marca 🟡 "inserir case real com aprovacao do cliente"

---

## Case 2 — Beauty Smile franchising pra dentista empreendedor

### Input

```yaml
prompt: "Recrutar dentista para abrir franquia Beauty Smile no interior SP — fechar contrato R$150k entrada. Dentista solo, 8 anos, quer escalar."

U1: "Recrutar dentista para abrir franquia Beauty Smile no interior SP — fechar contrato R$150k entrada"
U2: "Dentista empreendedor, 8 anos clinica solo no interior SP, atualmente 1-2 cadeiras, quer escalar mas nao tem brand"
U3: 3 (15-20min — call remota)
U4: 2 (call remota)
U5: "Voce queria empreender. Hoje virou administrador. Existe caminho diferente."
U6: Beauty Smile (auto-detect)
S1: R$ 150.000 entrada + royalty
S2: 60-90 dias
S3: "dentista empreendedor, dor = teto operacional / falta de brand / sozinho aprendendo gestao e marketing do zero"
S4: "medo de ser engolido pela operacao da franquia / perder autonomia clinica"
S5: "3 franquias ativas com retencao 18 meses+, ticket medio cresceu 40% no primeiro ano de uma delas"
```

### Esperado (assertions auto-verificaveis)

| # | Assertion | Pass criteria |
|---|-----------|---------------|
| 2.1 | Slide 1 = capa com action title = U5 ou variante | regex igual case 1 |
| 2.2 | Slide 2 = insight provocador (84% dentistas solo / crescimento virou jogo de brand OU similar) | slide 2 contem dado + reframe |
| 2.3 | Slide 2 NAO comeca cerimonial | NOT regex |
| 2.4 | Gap Selling explicito: solo (current) → solo com teto (custo) → brand consolidada (future) | slides 3-5 com numeros |
| 2.5 | Slide 6 = Raskin Old World (dentista solo) vs New World (dentista com brand) | slide 6 contem ambos |
| 2.6 | Payback no cenario base ≤ 12 meses (typical franquia consolidada premium SP) | slide 12 numero meses |
| 2.7 | Sensitivity 3 cenarios visiveis | slide 13 tabela |
| 2.8 | Slide 11 menciona "3 franquias ativas, retencao 18m+, ticket +40%" (S5) | grep S5 dados |
| 2.9 | Slide 14 (se presente) NAO faz badmouth de outras franquias odonto (Sorridents, OdontoCompany, etc.) | NOT contains adjetivo pejorativo sobre franquias concorrentes |
| 2.10 | Endereca objecao S4 (autonomia clinica) no slide 17 (FAQ antecipada) OU apendice | grep "autonomia" ou "decisoes clinicas" |
| 2.11 | CTA = "agendar call com COO" ou equivalente especifico com data | slide final |
| 2.12 | Auto-detection Beauty Smile acionou compliance CFO Resolucao 196/2019 | tier 🟡 menciona CFO ou publicidade odontologica |
| 2.13 | Schema §10.2 valido | grep seccoes |
| 2.14 | Modo = `padrao` | cabecalho Meta |
| 2.15 | Royalty fee mencionado como cost-of-revenue, NAO subtraido no payback do franqueado (premissa correta) | speaker notes do slide 12 explicam isso |

### Variacoes possiveis (eval bonus)

- **Case 2a:** input adiciona "decisor tambem e a esposa do dentista que vai gerir financeiro" → PAS deve ser ativado (decisor relacional/emocional adicional)

---

## Case 3 — Carnaval 360 plano corporativo pra agencia

### Input

```yaml
prompt: "Vender plano corporativo Carnaval 360 pra agencia multi-cliente — R$500k/ano. Diretor de cliente da agencia decide. Casos: marca de bebida ativou em 2024 NPS 9.2."

U1: "Vender plano corporativo Carnaval 360 pra agencia (multi-cliente, R$500k/ano)"
U2: "Diretor de cliente da agencia (atende 6+ marcas, ticket medio R$2-5M/ano por cliente)"
U3: 3 (15-20min — call remota inicial; presencial depois)
U4: 2 (call remota)
U5: "Ativacao virou ciencia. Patrocinio passivo virou prejuizo."
U6: Carnaval 360 (auto-detect)
S1: R$ 500.000/ano (multi-cliente)
S2: 90 dias
S3: "diretor de cliente da agencia, dor = entregar experiencias diferenciadas multi-marca, KPI = sentimento e LTV nao mais GRP/share-of-voice"
S4: "agencias ja tem fornecedores 'preferenciais' / risco de comoditizacao da plataforma na cabeca do cliente"
S5: "Marca de bebida X ativou no Carnaval 360 2024, NPS 9.2, UGC +47%, brand consideration +18pp"
```

### Esperado (assertions auto-verificaveis)

| # | Assertion | Pass criteria |
|---|-----------|---------------|
| 3.1 | Slide 1 = capa com action title = U5 ou variante | regex |
| 3.2 | Slide 2 = insight provocador (ativacao 2024 cresceu Y%, KPI mudou de GRP pra NPS/LTV OU similar) | slide 2 dado + reframe |
| 3.3 | Slide 2 NAO comeca cerimonial | NOT regex |
| 3.4 | Gap Selling: status quo (patrocinio passivo) → custo (ROI commoditizando) → future (ativacao participativa) | slides 3-5 |
| 3.5 | Slide 6 = Raskin Old World (logo na arena, GRP) vs New World (CO-CRIACAO participativa, NPS+LTV) | slide 6 contem ambos lados |
| 3.6 | Slide 11 menciona case marca de bebida 2024 com NPS 9.2 + UGC +47% + brand consideration +18pp (S5) | grep dados S5 |
| 3.7 | Slides 12-13 = ROI/payback para AGENCIA (nao para marca cliente final) | slide 12 explicita que beneficiario do payback e a agencia que vende plano corporativo |
| 3.8 | Cenario base mostra payback ≤ 8 meses no ano fiscal | slide 12 |
| 3.9 | Sensitivity 3 cenarios = clientes/ano que ativam (4/6/9) | slide 13 |
| 3.10 | Slide 14 (se presente) NAO faz badmouth de produtoras / agencias / outros eventos | NOT contains adjetivo pejorativo |
| 3.11 | CTA especifico para diretor de cliente da agencia (workshop / piloto / ativacao demo) | slide final |
| 3.12 | Sem compliance tag obrigatoria (Carnaval 360 nao tem compliance_tags) | tier 🟡 vazio ou apenas ✅ |
| 3.13 | Schema §10.2 valido | grep |
| 3.14 | Modo = `padrao` | cabecalho |
| 3.15 | Speaker notes mencionam que "marca de bebida X" deve ser substituida no slide 11 SE NDA do cliente impedir nominar | grep nota sobre NDA/anonimizacao |

### Variacoes possiveis (eval bonus)

- **Case 3a:** input vira "demo da plataforma Carnaval 360 pra diretor da agencia" → modo `demo-presentation`, slide 5 mostra output final (dashboard NPS/UGC da plataforma)

---

## Cobertura DoD pela suite de 3 cases

| DoD especifico (bundle 04) | Coberto por | Como |
|----------------------------|--------------|------|
| Frontmatter §10.7 com `intent: action`, `effort: high`, NB1 + NB3 | Todos 3 (1.14, 2.13, 3.13) | grep cabecalho Meta + frontmatter SKILL.md |
| 3 eval cases passando | Este arquivo | 1, 2, 3 |
| 2 modos (`padrao` / `demo-presentation`) | Cases 1a / 3a (variacoes) + assertions 1.9 / 3.14 | seleccao automatica testada |
| Insight provocador Challenger no slide 2 — NUNCA "obrigado" | 1.2, 1.3, 2.2, 2.3, 3.2, 3.3 | regex negativo + presenca de dado/reframe |
| Comparativo responsavel sem badmouth | 1.8, 2.9, 3.10 | regex negativo de adjetivos pejorativos |
| ROI/payback explicito em todos 3 cases | 1.6, 1.7, 2.6, 2.7, 3.7, 3.8, 3.9 | presenca de slide payback + sensitivity |
| Auto-detection §10.5 | 1.11, 2.12, (3.12 = nenhuma tag — caso negativo controle) | compliance tier confere |
| Schema §10.2 valido | 1.13, 2.13, 3.13 | grep seccoes obrigatorias |

## Como rodar manualmente (quick check)

1. Abra Claude Code numa janela limpa
2. Invoque `/deck-sales` com prompt do case
3. Aguarde STORYBOARD ser gerado em `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`
4. Aplique assertions deste arquivo:
   - 🟢 Pass: assertion atendida
   - 🟡 Partial: parcial / requer ajuste cosmetico
   - 🔴 Fail: ausente ou contraria → iterar SKILL.md ou references
5. Repetir ate 3 cases com ≥80% pass rate em assertions auto-verificaveis

## Fixtures suggestion (futuro)

Quando rodando via `skill-creator` em modo evals automatizado, criar fixtures:

```
evals/
├── eval-cases-sales.md  (este arquivo)
├── fixtures/
│   ├── case-1-fotona-lightwalker.json   (input estruturado)
│   ├── case-2-beauty-smile-franchising.json
│   └── case-3-carnaval-360-corporativo.json
└── expected-outputs/
    ├── case-1-expected-storyboard.md
    ├── case-2-expected-storyboard.md
    └── case-3-expected-storyboard.md
```
