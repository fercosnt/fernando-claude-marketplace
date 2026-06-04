# LightWalker Equipment — Specs Canônicas

Equipamento Fotona LightWalker (lançado 2011) — sistema dual-wavelength com Er:YAG + Nd:YAG no mesmo console.

## Comprimentos de onda

### Er:YAG — 2940 nm
- **Cristal:** Erbium-doped Yttrium Aluminium Garnet (Y₃Al₅O₁₂)
- **Cromóforo principal:** ÁGUA (pico de absorção ~2.94 µm — match perfeito com pico vibracional H₂O)
- **Coef. absorção em água:** ~1000/mm → penetration depth = 1 µm
- **Coef. absorção em esmalte:** ~150/mm → penetration depth = 6.7 µm
- **Coef. absorção em dentina:** ~200/mm → penetration depth = 5 µm
- **Uso primário:** ablação de tecido duro (cárie, esmalte, osso) e tecido mole superficial; mecanismo de microexplosão por vaporização da água trapeada
- **Scattering em hard tissue:** desprezível (alta absorção domina)

### Nd:YAG — 1064 nm
- **Cristal:** Neodymium-doped Yttrium Aluminium Garnet
- **Cromóforos principais:** hemoglobina + melanina (água absorve POUCO em 1064 nm)
- **Penetra muito mais que Er:YAG** — alcança alguns mm de profundidade no tecido mole
- **Uso primário:** biomodulação (PBM), descontaminação periodontal/endodôntica, hemostasia, soft tissue surgery profunda, despigmentação
- **Scattering relevante:** sim, devido à profundidade de penetração

### Diferença prática Er:YAG vs Nd:YAG (1 frase)
> "Er:YAG corta com água como ferramenta; Nd:YAG penetra com hemoglobina/melanina como alvo."

## Pulse Modes (duração de pulso)

Variable Square Pulse (VSP) technology — pulsos quadrados (controle preciso da energia entregue, sem cauda exponencial das tecnologias antigas PFN).

| Mode | Duração típica | Uso preferencial |
|------|---------------|------------------|
| **SSP** Super Short Pulse | ~50 µs | máximo peak power, ablação ultra-fina, mínimo dano térmico |
| **MSP** Micro Short Pulse | ~100 µs | ablação padrão tecido duro |
| **SP** Short Pulse | ~300 µs | ablação balanceada (eficiência + algum efeito térmico controlado) |
| **LP** Long Pulse | ~600-1000 µs | mais efeito térmico, hemostasia em soft tissue |
| **VLP** Very Long Pulse | >1000 µs | thermal effects dominantes |
| **XLP** Extra Long Pulse | >1500 µs | máximo efeito térmico |
| **QSP** Quantum Square Pulse | proprietário | pulsos sub-microssegundo para efeitos fotomecânicos (Nd:YAG) |
| **SMOOTH** | proprietário | suaviza entrega de energia para conforto/biomodulação |
| **SWEEPS** | proprietário | endodontia (Shock Wave Enhanced Emission Photoacoustic Streaming) |

**Princípio do mapeamento pulso → efeito:**
- Pulsos CURTOS (alto peak power) → efeitos MECÂNICOS (ablação, fotodisrupção)
- Pulsos LONGOS (baixo peak power) → efeitos TÉRMICOS (coagulação, biomod)

## Handpieces / Ponteiras conhecidas (do material LAHA)

### H02 / H14
- **Diâmetro do spot:** 1 mm
- **Surface:** 0.0075 cm²
- **Tipo:** focal, alta densidade de energia
- **Uso típico:** odontologia restauradora, ablação precisa de cárie

### R30A
- **Diâmetro do spot:** 5 mm
- **Surface:** ~0.196 cm²
- **Configuração específica:** Nd:YAG com pulse durations 15 ms ou 25 ms
- **Uso típico:** dermato-estética, smooth/soft tissue procedures

### R16 / PS04
- **Diâmetro do spot:** 7 mm
- **Surface:** ~0.385 cm²
- **Pulse durations comuns:** SP (300 µs)
- **Uso típico:** áreas amplas, fluences baixas (ex: SMOOTH mode periodontia)

### Fiber 300 µm
- **Diâmetro:** 300 µm = 0.3 mm
- **Surface:** ~0.00068 cm²
- **Delivery:** fibra óptica flexível (Nd:YAG)
- **Uso típico:** endodontia, periodontia (PIPS, SWEEPS), descontaminação intracanal

> **Nota:** o catálogo completo de tips/ponteiras LightWalker (R02, R14, X-Runner, etc) está na biblioteca NotebookLM `91c9d937-4319-4fbb-bf2a-232db4ceb3ea`. Consultar lá quando precisar de specs de ponteira não listada acima.

## Delivery systems

### Articulated arm (OPTOflex® patenteado)
- Espelhos high-reflectance
- Preserva qualidade do feixe (collimation, polarização)
- Usado para Er:YAG primariamente (Er:YAG não passa bem por fibra de sílica padrão)

### Optical fiber
- Reflexão total interna — luz só sai na ponta
- Usado para Nd:YAG primariamente
- Permite acesso a cavidades (canal radicular, bolsa periodontal)

## Ranges típicos do equipamento (referência rápida)

| Parâmetro | Range típico em odonto | Unidade |
|-----------|----------------------|---------|
| Energia por pulso | 20 — 500 | mJ |
| Spot size (diâmetro) | 0.2 — 10 | mm |
| Pulse duration | 50 — 250.000 | µs (= 50µs a 250ms) |
| Fluence | 0.05 — 40 | J/cm² |
| Pulse repetition (frequency) | 2 — 50 | Hz |
| Peak power | 200 — 3000 | W |
| Average power | 0.5 — 20 | W |

## Validação cruzada de parâmetros

Quando o display do equipamento mostra apenas alguns parâmetros, sempre validar consistência:

1. Se display mostra E + ν → calcular Pave = E × ν e comparar com display
2. Se display mostra Pave + ν → calcular E = Pave/ν
3. Se display mostra F + d → calcular E = F × S
4. Se houver inconsistência > 5%, suspeitar de:
   - Display desatualizado de versão de software
   - Conversão de unidade errada
   - Parâmetro real diferente do informado

## Combinações comuns por aplicação clínica

| Aplicação | λ | Mode típico | F típica | ν típica |
|-----------|---|-------------|----------|----------|
| Cárie (preparo cavitário) | Er:YAG | MSP/SP | 8-15 J/cm² | 10-20 Hz |
| Ablação de osso | Er:YAG | SSP/MSP | 20-30 J/cm² | 15-25 Hz |
| Endo SWEEPS/PIPS | Er:YAG fiber | SWEEPS/SSP | sub-ablativa | 10-15 Hz |
| Biomodulação intra-oral | Nd:YAG | SMOOTH/LP | <1 J/cm² | 10 Hz |
| Periodontia descontaminação | Nd:YAG fiber | LP/VLP | sub-ablativa | 10-20 Hz |
| Bleaching ativação | Er:YAG ou Nd:YAG | LP/SMOOTH | sub-ablativa | conforme protocolo |
| Cirurgia soft tissue | Er:YAG ou Nd:YAG | LP/VLP | acima do threshold ablação | 15-25 Hz |

> Estas são faixas de orientação extraídas do material LAHA. Para protocolos específicos validados em literatura, consultar NotebookLM ou referências peer-reviewed.
