# Formulas Core — Laser Physics

Todas as fórmulas com unidades, conversoes e exemplos resolvidos do material Fotona LAHA Master Dental.

## Conversoes de unidades essenciais

| De | Para | Fator |
|----|------|-------|
| 1 mm | cm | 0.1 cm |
| 1 µm | cm | 0.0001 cm |
| 1 J | mJ | 1000 mJ |
| 1 s | ms | 1000 ms |
| 1 ms | µs | 1000 µs |
| 1 W | mW | 1000 mW |

**Atenção:** SEMPRE converter para unidades coerentes ANTES de aplicar formulas. Padrão recomendado para cálculos: J, cm, s, W.

## 1. Surface (área do spot)

```
S = (π/4) × d²
```

- **S** = surface (cm²)
- **d** = diâmetro do spot (cm) — converter de mm
- **π** ≈ 3.1416 (em cálculos rápidos pode usar 3)

**Exemplo H02 (d=1 mm):**
```
d = 1 mm = 0.1 cm
S = (π/4) × (0.1 cm)² = (3/4) × 0.01 cm² = 0.0075 cm²
```

**Exemplo R30A (d=5 mm):**
```
d = 5 mm = 0.5 cm
S = (π/4) × (0.5)² = 0.785 × 0.25 = 0.196 cm² ≈ 0.19 cm²
```

**Exemplo fiber 300 µm (d=0.3 mm):**
```
d = 0.3 mm = 0.03 cm
S = (π/4) × (0.03)² = 0.785 × 0.0009 = 0.000707 cm² ≈ 0.00068 cm²
```

## 2. Fluence (densidade de energia)

```
F = E / S
```

- **F** = fluence (J/cm²) — também chamada *energy density*
- **E** = energia por pulso (J) — converter de mJ
- **S** = surface (cm²)

**Exemplo H02 (E=300 mJ, d=1 mm):**
```
E = 300 mJ = 0.3 J
S = 0.0075 cm²
F = 0.3 J / 0.0075 cm² = 40 J/cm²
```

**Range típico em odonto:** 0.05 — 40 J/cm²

## 3. Peak power (potência por pulso)

```
Ppeak = E / t
```

- **Ppeak** = peak power (W)
- **E** = energia por pulso (J)
- **t** = duração do pulso (s) — converter de µs ou ms

**Exemplo (E=300 mJ, t=100 µs MSP):**
```
E = 300 mJ = 0.3 J
t = 100 µs = 0.0001 s
Ppeak = 0.3 J / 0.0001 s = 3000 W
```

**Range típico:** 200 — 3000 W

## 4. Average power (potência média)

```
Pave = E × ν
```

- **Pave** = average power (W)
- **E** = energia por pulso (J)
- **ν** = pulse repetition / frequency (Hz)

**Exemplo (E=300 mJ, ν=10 Hz):**
```
E = 0.3 J
Pave = 0.3 J × 10/s = 3 W
```

**Range típico em odonto:** 0.5 — 20 W

**Validação cruzada:** Pave também pode ser calculado como `Pave = Ppeak × duty_cycle` onde `duty_cycle = t × ν`.

## 5. Power density (irradiância)

Fundamental para reportar em pesquisa — exige tanto peak quanto average.

```
Peak power density    = Ppeak / S    [W/cm²]
Average power density = Pave  / S    [W/cm²]
```

Average power density é o que normalmente se chama **irradiance** em literatura biomédica.

**Exemplo continuando o caso H02 anterior (Pave=3 W, Ppeak=3000 W, S=0.0075 cm²):**
```
Average power density = 3 / 0.0075 = 400 W/cm²
Peak power density    = 3000 / 0.0075 = 400.000 W/cm²
```

A distância entre peak e average reflete o duty cycle baixíssimo de pulsos curtos — fundamental quando se discute efeitos térmicos vs mecânicos.

## 6. Energia por aplicação e cumulativa

Crítico para reporte em pesquisa (ver `dosimetry-reporting.md`).

```
E_aplicação = Pave × t_aplicação
E_cumulativa = E_aplicação × n_aplicações
```

**Exemplo (Pave=3 W, aplicação de 30 s, 3 irradiações):**
```
E_aplicação  = 3 W × 30 s = 90 J
E_cumulativa = 90 J × 3 = 270 J
```

## 7. Energia do fóton

Útil para discutir interação fundamental.

```
E_photon = h × ν = h × c / λ
```

- **h** = constante de Planck = 6.626 × 10⁻³⁴ J·s
- **c** = velocidade da luz = 3 × 10⁸ m/s
- **λ** = comprimento de onda (m)
- Comprimentos de onda menores → fótons mais energéticos → mais perigosos (UV, X-ray)

## 8. Atenuação no tecido (Beer-Lambert)

```
P(d) = P₀ × e^(−μ × d)
```

- **P(d)** = potência na profundidade d
- **P₀** = potência incidente
- **μ** = coeficiente de absorção+scattering (1/cm ou 1/mm)
- **d** = profundidade (cm ou mm — coerente com μ)

## 9. Penetration depth (profundidade de penetração)

```
L = 1 / μ
```

- **L** = profundidade onde 63% da potência incidente foi absorvida
- Mais usado clinicamente que μ por ser mais intuitivo

**Penetration depths para Er:YAG (2.94 µm):**

| Tecido | μ (1/mm) | L = penetration depth |
|--------|----------|----------------------|
| Água | 1000 | 1 µm |
| Esmalte | 150 | 6.7 µm |
| Dentina | 200 | 5 µm |

## 10. Heat diffusion depth (difusão térmica)

```
xd ~ √(D × tp)
```

- **xd** = profundidade de difusão térmica (m)
- **D** = constante de difusão térmica do material (m²/s)
- **tp** = duração do pulso (s)

**Pulso mais longo → calor difunde mais profundo.** É o conceito por trás do TRT (Thermal Relaxation Time):

- Pulsos < TRT do alvo → confinamento térmico → ablação eficiente, dano colateral mínimo
- Pulsos > TRT do alvo → calor difunde para tecido adjacente → coagulação/risco térmico

## Os 6 exemplos resolvidos do Fotona LAHA

Estes são os exercícios canônicos do curso — usar como gabarito.

### H02/H14 handpiece
| Input | | Cálculo | |
|-------|--|---------|--|
| λ | Erbium 2940 nm | F | **40 J/cm²** |
| d | 1 mm | Ppeak | **3000 W** |
| t | 100 µs (MSP) | | |
| E | 300 mJ | | |
| ν | 20 Hz | | |
| Pave | 6 W | | |

### Fiber 300 µm
| Input | | Cálculo | |
|-------|--|---------|--|
| λ | Neodymium 1064 nm | E | **43 mJ** |
| d | 300 µm = 0.3 mm | S | **0.00068 cm²** |
| t | 200 µs (SP) | F | **63 J/cm²** |
| ν | 70 Hz | Ppeak | **215 W** |
| Pave | 3 W | | |

### R16/PS04 handpiece
| Input | | Cálculo | |
|-------|--|---------|--|
| λ | Erbium 2940 nm | S | **0.37 cm²** |
| d | 7 mm | E | **296 mJ** |
| t | 300 µs (SP) | Ppeak | **987 W** |
| F | 0.8 J/cm² | | |
| ν | 5 Hz | | |
| Pave | 1.52 W | | |

### R30A handpiece
| Input | | Cálculo | |
|-------|--|---------|--|
| λ | Neodymium 1064 nm | S | **0.19 cm²** |
| d | 5 mm | E | **7.6 J** |
| t | 25 ms | Ppeak | **304 W** |
| F | 40 J/cm² | | |
| ν | 1 Hz | | |
| Pave | 7.85 W | | |

## Checklist de cálculo (ordem recomendada)

Quando receber parâmetros parciais, calcular nesta ordem:

1. **Converter unidades** (mm→cm, mJ→J, µs/ms→s)
2. **Surface** S = π/4 × d²
3. **Fluence** F = E/S (se tem E e d)
4. **Peak power** Ppeak = E/t
5. **Average power** Pave = E × ν (ou validar via display)
6. **Power densities** = Ppeak/S e Pave/S
7. **Energia por aplicação** = Pave × tempo
8. **Energia cumulativa** = E_aplicação × n_aplicações

Sempre mostrar fórmula → substituição numérica → resultado com unidade.

## Auto-verificação sistemática (anti-erro)

**Princípio:** todo cálculo dosimétrico entregue ao usuário passa por este checklist ANTES de aparecer no output. Erros de unidade são a causa #1 de cálculo dosimétrico errado em papers — quase sempre mm↔cm ou µs↔ms↔s.

### Sanity Check 1 — Recalcular Pave por dois caminhos

```
Caminho A:  Pave_A = E × ν
Caminho B:  duty_cycle = t × ν
            Pave_B = Ppeak × duty_cycle
```

Os dois resultados devem ser iguais dentro de < 1% (a única diferença vem de arredondamento). Se divergem em > 5%, há erro de unidade — voltar e refazer todas as conversões.

**Exemplo H02 / 250 mJ / 100 µs / 15 Hz:**
```
Pave_A = 0.25 × 15 = 3.75 W
duty_cycle = 0.0001 × 15 = 0.0015 (0.15%)
Pave_B = 2500 × 0.0015 = 3.75 W ✓
```

### Sanity Check 2 — Ordem de magnitude vs ranges típicos odonto

Comparar cada resultado com os ranges em `lightwalker-equipment.md`:

| Parâmetro | Range típico | Se fora → ação |
|-----------|--------------|---------------|
| Energia/pulso (E) | 20 — 500 mJ | Acima: parâmetro extremo, confirmar com usuário |
| Fluence (F) | 0.05 — 40 J/cm² | Fora: provavelmente erro de unidade ou caso muito extremo |
| Peak power (Ppeak) | 200 — 3000 W | Acima: pulse mode muito curto ou erro de t |
| Average power (Pave) | 0.5 — 20 W | Acima: ν muito alta ou E muito alta para uso clínico |
| Frequency (ν) | 2 — 50 Hz | Fora: confirmar (alguns modos especiais excedem) |
| Pulse duration (t) | 50 µs — 250 ms | Fora: confirmar mode |

**Se algum resultado está fora:** sinalizar explicitamente no output ("F = 78 J/cm² está acima do range típico em odontologia — confirmar parâmetros") em vez de apresentar como se fosse normal.

### Sanity Check 3 — Coerência dimensional

Quatro identidades que sempre devem valer:

```
✓  Ppeak ≥ Pave         (sempre; igualdade só em CW puro)
✓  duty_cycle = t×ν < 1 (se ≥ 1, é CW ou erro de unidade em t)
✓  F × S = E            (reverter Fluence × área deve dar a energia)
✓  Pave × t_app = E_app (potência média × tempo = energia entregue)
```

### Sanity Check 4 — Re-conferir conversões (causa #1 de erro)

| De | Para | Operação | Erro comum |
|----|------|----------|-----------|
| mm | cm | ÷10 | **dividir por 100 (errado!)** |
| mm² | cm² | ÷100 | confundir com linear |
| µm | cm | ÷10.000 | esquecer fator |
| mJ | J | ÷1000 | tratar como J direto |
| µs | s | ÷1.000.000 | esquecer um zero |
| ms | s | ÷1000 | confundir com µs |
| min | s | ×60 | esquecer |

**Regra prática:** depois de converter, escrever explicitamente: `1 mm = 0.1 cm` (não 0.01). Verificar visualmente antes de usar nos cálculos.

### Sanity Check 5 — Re-fazer 1 cálculo do zero

Pegar o cálculo mais crítico (geralmente Fluence ou Peak power) e refazer SEM olhar o resultado anterior. Se bate → OK. Se não bate → refazer todos.

Para o exemplo H02 / 250 mJ / 100 µs / 15 Hz / d=1mm:
```
Refazer Fluence do zero:
  d = 1 mm → 0.1 cm
  S = (π/4) × (0.1)² = 0.7854 × 0.01 = 0.007854 cm²
  E = 250 mJ → 0.250 J
  F = 0.250 / 0.007854 = 31.83 J/cm²
Bate com primeiro cálculo (31.85)? ✓ (diferença = arredondamento de π)
```

### Sanity Check 6 — Comparar com exemplo canônico LAHA mais próximo

Os 6 exemplos resolvidos acima são gabaritos. Se o caso é parecido com um deles:

- Mesma handpiece + mesmo mode → ordem de magnitude do resultado deve ser similar
- Diferenças explicáveis por mudanças proporcionais (ex: dobrar E → dobra F e Pave; dobrar d → S quadruplica → F cai 4×)

**Exemplo de aplicação:**
> "H02 / MSP / E=250 mJ / 15 Hz" — comparar com canônico H02/MSP "E=300 mJ / 20 Hz" (F=40 J/cm², Pave=6 W).
> Esperado: F_novo ≈ 40 × (250/300) = 33.3 J/cm² (calculado: 31.8 — bate dentro do erro de π)
> Esperado: Pave_novo ≈ 6 × (250/300) × (15/20) = 3.75 W ✓

### Quando algo falha no checklist

1. **Não apresentar resultado errado** — sinalizar imediatamente
2. **Voltar à conversão de unidades** (causa #1) e refazer
3. **Refazer TODOS os cálculos**, não só o que falhou (erros de unidade se propagam)
4. **Mostrar ao usuário** que a verificação foi rodada (linha "sanity check" no output) — torna o trabalho transparente e o erro detectável também por ele

### Output: linha de verificação obrigatória

Sempre incluir no final do output uma linha mostrando que o sanity check foi feito:

```
✓ Sanity check: Pave via E×ν = 0.25×15 = 3.75 W; via Ppeak×duty = 2500×0.0015 = 3.75 W. Consistente.
```

Isso protege contra erro silencioso e dá ao usuário um marcador visual de que o cálculo passou pela verificação.
