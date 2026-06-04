# Tissue Interaction — Cromóforos, Absorção, Scattering, Ablação

Como a luz laser interage com o tecido, com foco no que importa para odontologia.

## Os 4 modos de interação

Quando o feixe atinge o tecido, 4 fenômenos podem ocorrer (geralmente simultaneamente):

1. **Reflection** — luz é refletida na superfície
   - **Specular** (superfície polida, espelho/joia metálica) → feixe MANTÉM intensidade, propaga em nova direção → PERIGO
   - **Diffuse** (superfície rugosa) → luz redirecionada em todas as direções → ainda pode ser hazardous
2. **Transmission** — luz atravessa o tecido sem ser absorvida
   - Tecido mais transmissivo a luz visível/IR no corpo: **olho** (córnea/lente/humor aquoso transparentes até retina)
3. **Absorption** — luz é absorvida por moléculas (cromóforos), produzindo calor
4. **Scattering** — luz é desviada sem ser absorvida; encurta penetração efetiva e alarga o feixe

## Cromóforos principais e seus picos de absorção

| Cromóforo | Picos de absorção (nm) | Relevância clínica |
|-----------|------------------------|-------------------|
| **Água (H₂O)** | 1450, **2940** (Er:YAG), 6100, 10600 (CO₂) | dominante em tecidos biológicos no IR; alvo do Er:YAG |
| **Hemoglobina oxigenada (HbO₂)** | 415 (Soret), 542, 577 | alvo de lasers vasculares (KTP 532, PDL 585, diodo) |
| **Melanina** | curva decrescente do UV ao IR (sem picos discretos) | relevante para depilação, despigmentação, segurança ocular (retina) |
| **Hidroxiapatita** | UV, ~9.6 µm, ~10 µm | mineral do esmalte/dentina; pico CO₂ usado em remineralização |

### Comprimentos de onda LightWalker vs cromóforos

- **Er:YAG 2940 nm:** absorção MÁXIMA em água, alta em hidroxiapatita, baixa em hemoglobina/melanina
  - Penetration depth em água: **1 µm** (extremamente raso → ablação superficial precisa)
- **Nd:YAG 1064 nm:** absorção BAIXA em água, alta em hemoglobina e melanina
  - Penetration depth em pele: vários mm (alcança vasos, melanócitos)

## Penetration depth (profundidade de penetração)

```
L = 1/μ
```

Profundidade onde 63% da potência incidente é absorvida (Beer-Lambert).

### Tabela canônica Er:YAG (2940 nm)

| Tecido | μ (1/mm) | Penetration depth |
|--------|----------|-------------------|
| Água pura | 1000 | **1 µm** |
| Esmalte | 150 | **6.7 µm** |
| Dentina | 200 | **5 µm** |
| Osso cortical | ~150-250 | ~5-7 µm |

A penetração rasa do Er:YAG é a razão pela qual ele é o gold-standard para ablação dental — o calor não difunde para a polpa.

### Comparação Er:YAG vs Nd:YAG em tecido mole

| λ | Penetration depth típica em soft tissue |
|---|----------------------------------------|
| Er:YAG 2940 nm | ~50-100 µm |
| Nd:YAG 1064 nm | ~3-5 mm (comprimento de scatter-equivalent) |
| CO₂ 10600 nm | ~30-50 µm |
| Diodo 810/980 nm | ~2-4 mm |

## Scattering — Rayleigh vs Mie

| | Rayleigh | Mie |
|--|---------|-----|
| Tamanho da partícula (a) | a < λ/10 | a > λ |
| Direção predominante | TODAS direções | FORWARD |
| Dependência com λ | FORTE (azul espalha mais que vermelho) | FRACA (todas as cores espalham igual) |
| Exemplo cotidiano | céu azul, sunset laranja | nuvens cinzas |

### Scattering em tecidos moles (relevante para Nd:YAG)

Tipos celulares e tamanhos:
- Hair follicle: ~100 µm
- Adipócito: ~100 µm
- Célula humana típica: ~30 µm
- Hemácia: ~8 µm

Como todos são MAIORES que λ Nd:YAG (1.064 µm) ou Er:YAG (2.94 µm), o scattering é predominantemente **Mie (forward)** — a luz se espalha PARA FRENTE no tecido, não para trás.

**Implicação prática:** spot sizes maiores penetram MAIS profundamente que spot sizes pequenos com a mesma fluence — porque o scattering radial relativo é menor em spots grandes (efeito de borda menor proporcionalmente).

## Confinamento térmico e TRT (Thermal Relaxation Time)

### Princípio

```
xd ~ √(D × tp)
```

xd = profundidade de difusão térmica durante o pulso. D = constante de difusão do tecido. tp = duração do pulso.

**TRT** ≈ tempo para o tecido alvo perder ~63% do calor por difusão para o tecido vizinho.

### Regra de seleção de pulso

- **tp < TRT** do tecido alvo → confinamento térmico → alvo é destruído sem aquecer significativamente o vizinho → seletividade
- **tp > TRT** → calor difunde → coagulação/dano térmico colateral

### TRT aproximados (referência rápida)

| Estrutura | Tamanho típico | TRT aproximado |
|-----------|----------------|----------------|
| Hemácia | 8 µm | ~50 µs |
| Vaso sanguíneo pequeno | 30-100 µm | ~1-10 ms |
| Vaso grande / hair follicle | 100-300 µm | ~10-100 ms |
| Melanossoma | 1 µm | ~1 µs (Q-switched necessário) |
| Tatuagem (partícula tinta) | 10-100 nm | ~10 ns (pico/Q-switched) |
| Esmalte (água trapeada) | µm scale | sub-ms |

> Estes são valores de orientação. Para TRT validado em literatura científica para um cromóforo/aplicação específica, consultar paper original (Anderson & Parrish 1983 é o seminal).

## Pulso curto vs longo — efeito mecânico vs térmico

### Pulso CURTO + alto Peak power
- Calor não tem tempo de difundir
- Temperatura local atinge threshold de ablação muito rápido
- Vaporização súbita → microexplosão → efeito MECÂNICO
- Ex: SSP/MSP Er:YAG para cárie

### Pulso LONGO + baixo Peak power
- Calor difunde para tecido adjacente
- Temperatura sobe gradualmente
- Coagulação, hemostasia, biomodulação → efeito TÉRMICO
- Ex: LP/VLP Nd:YAG para descontaminação periodontal

## Mecanismo de ablação Er:YAG em tecido dental

Sequência física (do material Fotona LAHA):

1. Luz Er:YAG (2940 nm) é altamente absorvida pelas moléculas de água presentes no esmalte/dentina
2. Moléculas de H₂O começam a vibrar mais intensamente
3. Vibrações dissipam energia em forma de CALOR para tecido circunvizinho
4. Temperatura da água sobe → água EVAPORA
5. Mas a água está TRAPEADA entre minerais (hidroxiapatita) e proteínas — não tem espaço para expandir
6. Pressão interna sobe até exceder a resistência mecânica do material
7. Pequena porção do tecido é ejetada por **MICROEXPLOSÃO**

Por isso Er:YAG corta osso/dente de forma "fria" relativa — o calor é levado embora junto com o material ejetado (mecanismo de "ablação a frio"), poupando o tecido subjacente. **Spray de água é fundamental** para dissipar calor residual e fornecer água de superfície para sustentar o mecanismo.

## Threshold de ablação

Para que ocorra ablação, é necessário atingir uma **fluence mínima** (J/cm²) específica para o tecido + λ + duração do pulso.

| Tecido + λ | Threshold de ablação aproximado |
|-----------|--------------------------------|
| Esmalte + Er:YAG | ~7-10 J/cm² (depende de hidratação) |
| Dentina + Er:YAG | ~3-5 J/cm² |
| Osso + Er:YAG | ~5-8 J/cm² |
| Soft tissue + Er:YAG | ~1-3 J/cm² |
| Soft tissue + Nd:YAG | varia muito; tipicamente sub-ablativo é o intencional |

**Abaixo do threshold:** efeitos sub-ablativos (limpeza, biomodulação, descontaminação)
**Acima do threshold:** ablação progressiva conforme fluence aumenta

> Os thresholds variam significativamente entre estudos por causa de diferenças em hidratação, técnica de medida, definição de "ablação" (mass loss vs depth). Citar fonte primária ao reportar.

## Heat shock proteins e dano térmico subletal

Para discussões de segurança pulpal/biomod:

- Aumento de **5.5°C** na polpa: limite clássico Zach & Cohen 1965 (43% de necrose pulpar acima desse limite em macacos) — citado em quase todo paper de bleaching/ablação dental
- Críticas modernas: limite pode variar com idade, espessura dentinária, tempo de exposição (não só pico)
- Aumento de **3°C** na superfície dentinária: usado em alguns protocolos como margem mais conservadora

## Reflection/Transmission — checklist de segurança

- Olho é o tecido mais transmissivo para visível e NIR (até 1400 nm) → ATINGE A RETINA
  - Acima de 1400 nm (incluindo Er:YAG 2940): luz é absorvida na córnea/cristalino antes de atingir retina (mas pode causar dano ocular anterior)
- Joias polidas, espelhos clínicos, instrumentos metálicos lustrosos = risco de reflexão especular
- Reflexões difusas (gengiva, esmalte) ainda podem ser perigosas em altas fluences

Ver `safety-classification.md` para classes de laser, MPE, NOHD e specs de eyewear.
