---
name: laser-physics
description: Cálculos de física do laser (fluence, peak/avg power, irradiance, energia cumulativa) + dosimetria para pesquisa e artigos. Foco odontologia e LightWalker (Er:YAG 2940nm + Nd:YAG 1064nm).
intent: Skill para Fernando (dentista pesquisador) calcular física do laser de forma rigorosa, citar fontes (LAHA Master Dental + literatura), e produzir output pronto para uso em pesquisa, artigos, protocolos clínicos e estudos. Cobre o sistema LightWalker em profundidade e laser physics geral. NotebookLM 91c9d937-4319-4fbb-bf2a-232db4ceb3ea contém o corpus completo (cursos + manuais + tips/ponteiras) para deep search quando references locais não bastam.
effort: high
---

# Laser Physics — Skill

Calcula, justifica e reporta parâmetros físicos de laser para pesquisa e prática clínica, com profundidade especial em odontologia e no equipamento Fotona LightWalker.

## Quando usar esta skill

Sempre que o input mencionar:
- Cálculo de fluence, peak power, average power, irradiance, power density
- Energia cumulativa, energia por aplicação, energia por pulso
- Pulse mode (SSP, MSP, SP, LP, VLP, QSP, SMOOTH, SWEEPS)
- Handpiece / tip / ponteira (H02, R30A, R16, PS04, fiber 300 µm, etc)
- Wavelength específico (2940, 1064 nm) ou "Er:YAG", "Nd:YAG", "LightWalker"
- TRT (thermal relaxation time), ablation threshold, penetration depth
- Cromóforo (água, hemoglobina, melanina, hidroxiapatita)
- Justificativa de dosimetria, threshold térmico, pulpal safety, Zach & Cohen
- Revisão de artigo / Methods section / pergunta de revisor sobre dosimetria
- Class 4, MPE, NOHD, eyewear, LB rating
- Comparação Er:YAG vs Nd:YAG, biomodulação vs ablação, hemostasia

## Modos de operação

### Modo CÁLCULO (default)
Usuário fornece parâmetros parciais → skill calcula os derivados, mostra fórmulas, valida unidades, retorna tabela.

### Modo DOSIMETRIA-PESQUISA
Usuário pede para preparar/revisar dosimetria de artigo → skill aplica o checklist de 14 parâmetros + 4 pilares de justificativa de `references/dosimetry-reporting.md`, retorna tabela pronta para Methods.

### Modo COMPARAÇÃO Er:YAG vs Nd:YAG
Usuário pergunta qual λ usar para X → skill compara cromóforos, penetration depths, mecanismos, retorna recomendação justificada com base em `references/tissue-interaction.md`.

### Modo PROTOCOLO clínico
Usuário descreve procedimento (cárie, periodontia, biomod, endo, cirurgia) → skill propõe parâmetros baseados em ranges canônicos do material LAHA + tabela em `references/lightwalker-equipment.md`, com disclaimer de validação clínica.

### Modo SAFETY
Usuário pergunta sobre eyewear, NOHD, MPE, plume, classificação → skill consulta `references/safety-classification.md`.

## Protocolo de execução

### Passo 1 — Identificar modo
A partir do input, decidir qual modo (cálculo, dosimetria-pesquisa, comparação, protocolo, safety). Se ambíguo, perguntar.

### Passo 2 — Inventário de parâmetros conhecidos
Listar TODOS os parâmetros que o usuário forneceu:
- Wavelength (λ)
- Energia por pulso (E)
- Spot size / diâmetro (d)
- Pulse duration (t) + mode (SSP/MSP/etc)
- Frequency / repetition (ν)
- Average power (Pave) — se dado pelo display
- Tempo de aplicação (t_app)
- Número de aplicações (n)
- Handpiece / tip
- Wavelength selection (Er:YAG ou Nd:YAG)

Se faltar algum parâmetro CRÍTICO para o cálculo pedido, perguntar antes de assumir.

### Passo 3 — Converter unidades
Padrão: J, cm, s, W. Sempre converter ANTES de calcular (mm→cm, mJ→J, µs/ms→s).

### Passo 4 — Calcular na ordem
Usar sequência de `references/formulas-core.md`:
1. S = π/4 × d²
2. F = E/S (se tem E e d)
3. Ppeak = E/t
4. Pave = E × ν (validar contra display)
5. Power densities (Ppeak/S, Pave/S)
6. E_aplicação = Pave × t_app
7. E_cumulativa = E_aplicação × n

Sempre mostrar: fórmula → substituição → resultado com unidade.

### Passo 5 — Validação cruzada
Se o usuário forneceu valores derivados (ex: Pave do display), validar contra cálculo. Se discrepância > 5%, sinalizar e investigar (provavelmente erro de unidade).

### Passo 6 — AUTO-VERIFICAÇÃO obrigatória (anti-erro)

**Antes de mostrar qualquer resultado, rodar este checklist mental.** Erro em cálculo dosimétrico em paper é defeito que mancha autoria — vale o esforço de duplicar o trabalho.

1. **Recalcular Pave por dois caminhos:**
   - Caminho A: `Pave = E × ν`
   - Caminho B: `Pave = Ppeak × duty_cycle` onde `duty_cycle = t × ν`
   - Os dois devem bater dentro de < 1%. Se divergem, há erro de unidade em algum lugar — voltar e refazer conversões.

2. **Verificar ordem de magnitude vs ranges típicos** (`references/lightwalker-equipment.md`):
   - F em odonto: 0.05 — 40 J/cm² (fora? sinalizar)
   - Pave: 0.5 — 20 W (fora? sinalizar)
   - Ppeak: 200 — 3000 W (fora? sinalizar)
   - ν: 2 — 50 Hz; t: 50 µs — 250 ms
   - Se algum resultado está MUITO fora do range típico, parar e investigar antes de apresentar — pode ser real (caso extremo) ou erro de cálculo. Não deixar o usuário descobrir.

3. **Sanity checks dimensionais:**
   - `Ppeak ≥ Pave` (sempre, exceto CW puro onde Ppeak = Pave)
   - `duty_cycle = t × ν < 1` (se ≥ 1, é CW ou erro)
   - `F × S = E` (se reverter, deve dar a energia original)
   - `Pave × t_app = E_aplicação` (idem)

4. **Verificar conversões críticas:**
   - mm → cm: dividir por 10 (NÃO por 100)
   - cm² é mm²/100
   - mJ → J: dividir por 1000
   - µs → s: dividir por 1.000.000
   - ms → s: dividir por 1000

5. **Re-fazer 1 cálculo crítico do zero** (sem olhar o anterior) — tipicamente Fluence ou Peak power. Se o resultado bate, OK. Se não bate, refazer todos.

6. **Validar contra os 6 exemplos canônicos LAHA** (`references/formulas-core.md`): se o caso é análogo a um deles (mesma handpiece + mesmo mode + parâmetros próximos), a ordem de magnitude do resultado deve ser similar.

Se passou nos 6 → output. Se algum falhou → corrigir e refazer a verificação inteira (não só o item que falhou).

### Passo 7 — Output
Sempre incluir:
- Tabela de parâmetros (input + derivados)
- Fórmulas usadas
- **Linha de auto-verificação** explícita ao final (ex: "Sanity check: Ppeak × duty_cycle = 2500 × 0.0015 = 3.75 W = Pave ✓"). Mostrar o trabalho de verificação ao usuário, não esconder — torna o erro detectável também por ele.
- Interpretação clínica (se aplicável): "Esta fluence está [acima/abaixo/no] threshold de ablação para [tecido]"
- Quando em modo pesquisa: tabela pronta para Methods + justificativa
- Citação da fonte (LAHA Master Dental, NotebookLM, paper se houver)

### Passo 8 — Disclaimer profissional
Para protocolos clínicos novos: lembrar que parâmetros do material didático/manufacturer não substituem validação em literatura peer-reviewed e julgamento clínico do operador. Tom direto, sem ser alarmista — Fernando é dentista pesquisador, não leigo.

## References disponíveis

Carregar conforme o caso:

| Arquivo | Quando consultar |
|---------|-----------------|
| `references/formulas-core.md` | Sempre que houver cálculo numérico — fórmulas + 6 exemplos resolvidos canônicos do LAHA |
| `references/lightwalker-equipment.md` | Specs Er:YAG/Nd:YAG, handpieces (H02/R30A/R16/fiber), modes (SSP→VLP), ranges típicos |
| `references/tissue-interaction.md` | Cromóforos, absorção, Beer-Lambert, scattering Mie/Rayleigh, TRT, ablação Er:YAG, thresholds |
| `references/dosimetry-reporting.md` | Quando o caso for revisão de artigo / preparação para publicação / pergunta de revisor — checklist de 14 parâmetros + 4 pilares de justificativa + thresholds térmicos canônicos |
| `references/safety-classification.md` | Class 4, MPE, NOHD, interpretação de eyewear specs (LB rating, modos D/I/R), plume, anatomia ocular vs λ |

## Fonte de deep search

NotebookLM ID: **`91c9d937-4319-4fbb-bf2a-232db4ceb3ea`**

Contém:
- PDFs completos de cursos LAHA Master Dental (Modules 1-N)
- Manuais LightWalker
- Specs detalhados de tips/ponteiras (catálogo completo, não só os listados em `lightwalker-equipment.md`)
- Papers e protocolos clínicos

Quando consultar:
- Spec de ponteira não listada nas references locais
- Protocolo clínico específico (ex: "qual a recomendação Fotona para PIPS em retreatment endodôntico?")
- Validação de parâmetro fora dos exemplos canônicos
- Pergunta de aplicação clínica não coberta pelos ranges típicos

Forma de citar: "Per NotebookLM Laser Physics + LightWalker corpus, [fato/spec]". Não inventar specs — se não tem certeza, dizer que requer consulta ao NotebookLM ou ao manual oficial.

## Princípios

1. **Mostrar trabalho** — sempre fórmula → substituição → resultado, nunca só "F = 40 J/cm²".
2. **Unidades coerentes** — checar conversão antes de calcular, sinalizar se input ambíguo.
3. **Citar fonte** — LAHA, NotebookLM, ou paper. Não inventar valores nem thresholds.
4. **Validação cruzada** — se o display dá Pave e os outros parâmetros conferem matematicamente, dizer "consistente". Se diverge, sinalizar.
5. **Distinguir cálculo de protocolo** — calcular a física é uma coisa; recomendar parâmetros clínicos é outra. No segundo caso, sempre lembrar que reproducibility e julgamento clínico mandam.
6. **Direto e técnico** — Fernando é dentista, não leigo. Sem disclaimers excessivos, sem explicar conceitos básicos como se fosse aula introdutória, a menos que solicitado.
7. **Pesquisa-friendly** — quando o contexto é artigo/paper, oferecer tabela pronta para Methods + justificativa estruturada nos 4 pilares.
8. **AUTO-VERIFICAÇÃO inegociável** — todo cálculo passa pelo Passo 6 antes de virar output. Erro em dosimetria de paper = mancha em autoria. Sempre recalcular Pave por dois caminhos (E×ν vs Ppeak×duty), conferir ordem de magnitude vs ranges típicos, validar conversões de unidade, refazer 1 cálculo crítico do zero. Mostrar a linha de sanity check no output para o usuário enxergar o trabalho de verificação. Ver `references/formulas-core.md` seção "Auto-verificação sistemática" para o procedimento detalhado.

## Exemplo de fluxo (Modo Cálculo)

**Input:** "Calcula tudo aí: H02, MSP, 250 mJ, 15 Hz."

**Output esperado:**
```
Equipamento assumido: LightWalker Er:YAG (H02 é tip Er:YAG)
λ = 2940 nm (Er:YAG)

PARÂMETROS DE INPUT
- Handpiece: H02 → d = 1 mm
- Mode: MSP → t = 100 µs
- Energia/pulso: E = 250 mJ
- Frequency: ν = 15 Hz

CONVERSÕES
d = 1 mm = 0.1 cm
E = 250 mJ = 0.25 J
t = 100 µs = 0.0001 s

CÁLCULOS
S = π/4 × d² = (3.1416/4) × (0.1)² = 0.00785 cm²
F = E/S = 0.25 / 0.00785 = 31.8 J/cm²
Ppeak = E/t = 0.25 / 0.0001 = 2500 W
Pave = E × ν = 0.25 × 15 = 3.75 W
Avg power density = Pave/S = 3.75 / 0.00785 = 477.7 W/cm²
Peak power density = Ppeak/S = 2500 / 0.00785 = 318,471 W/cm²

INTERPRETAÇÃO
- Fluence 31.8 J/cm² está bem acima do threshold de ablação para esmalte (~10 J/cm²) — eficiente para preparo cavitário
- Pulse curto (MSP) prioriza efeito mecânico (microexplosão), minimizando dano térmico colateral
- Spray water deve estar ativo para sustentar mecanismo de ablação a frio

Fonte: fórmulas LAHA Master Dental Module 1, Fotona.
```

## Exemplo de fluxo (Modo Dosimetria-Pesquisa)

**Input:** "Revisora pediu pra eu reportar fluence/pulso, average power, irradiância, energia por aplicação de 30s e energia cumulativa de 3 irradiações. Eu usei R30A, 5 W, 25ms, 1 Hz, Nd:YAG, em estudo de bleaching."

**Output esperado:**
1. Reconstruir todos os 14 parâmetros do checklist
2. Tabela pronta para Methods (formato de `references/dosimetry-reporting.md`)
3. Sugestão de justificativa nos 4 pilares (literatura, manufacturer, piloto, threshold térmico)
4. Sanity check vs threshold pulpal Zach & Cohen 5.5°C
5. Lacunas potenciais que outros revisores podem cobrar

Ver `references/dosimetry-reporting.md` para o template completo.
