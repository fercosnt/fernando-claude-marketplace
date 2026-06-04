# Laser Safety — Classes, MPE, NOHD, Eyewear

Conteúdo extraído do Module 1 LAHA Master Dental + IEC 60825 + ANSI Z136.

## Hazards de laser (visão geral)

1. **Elétrico** — alta voltagem na fonte
2. **Térmico** — hipertermia, coagulação não-intencional
3. **Mecânico** — plasma, vaporização, cavitação
4. **Explosão e fogo** — ignição de gases anestésicos, álcool, materiais inflamáveis
5. **Químico** — corrosão de proteções, plume com aldeídos/HPV
6. **Ocular** — o mais relevante e o mais subestimado

## Classificação de lasers (IEC 60825)

| Classe | Segurança | Limite | Exemplos |
|--------|-----------|--------|----------|
| **Class 1** | Seguro em todas condições | — | Mouse, impressora, CD player |
| **Class 1M** | Seguro exceto com óptica de magnificação | — | Sistemas de fibra óptica para comunicação |
| **Class 2** | Reflexo de piscar protege; só luz visível | ≤ 1 mW | Pointers vermelhos, leitores de código de barras |
| **Class 2M** | Reflexo de piscar + sem instrumentos ópticos | — | Pointers visíveis com divergência alta |
| **Class 3R** | Seguro com cuidado; MPE pode ser excedido | ≤ 5 mW | Pointers verdes, scanners de laser |
| **Class 3B** | Perigoso direto; visão de reflexão difusa OK | ≤ 500 mW | Oftalmologia, espectrometria, estereolitografia |
| **Class 4** | **Pode queimar pele e causar dano ocular permanente — direto, difuso ou indireto** | > 500 mW | **Lasers médicos (Er:YAG, Nd:YAG, CO₂, diodos cirúrgicos)** |

> Lasers odontológicos são **Class 4** sem exceção. Toda a discussão de safety neste documento assume Class 4.

## Requisitos obrigatórios para Class 4

Conforme normativas (variam por jurisdição mas são equivalentes):

- **Key switch** — controle de acesso físico
- **Door interlock** — switch remoto que desliga o laser se a porta abre
- **Sound** — quando sistema é ligado E quando emissão acontece
- **Attenuator (shutter)** — dispositivo para bloquear emissão sem desligar
- **Labels** — Caution Class 4, abertura, características, no laser head
- **Laser Safety Officer (LSO)** designado na clínica/instituição

## MPE (Maximum Permissible Exposure)

**Definição:** nível máximo de exposição (de olho ou pele) que NÃO causa lesão imediata ou após longo tempo.

Depende de:
- Wavelength
- Pulse duration / exposure time
- Tipo de tecido (córnea, retina, pele)

Tabelas oficiais: ANSI Z136.1 e IEC 60825.

## NOHD (Nominal Ocular Hazard Distance)

**Definição:** distância da abertura do laser onde a irradiância (W/cm²) ou exposição radiante (J/cm²) iguala o MPE.

```
Dentro da NOHD: PERIGOSO (acima do MPE)
Fora da NOHD: seguro para o olho desprotegido
```

### Pontos práticos

- NOHD depende do handpiece (handpiece com lente colimadora → NOHD muito maior; handpiece divergente → NOHD curta)
- **Para a maioria dos lasers odontológicos Class 4, a NOHD é MAIOR que o consultório** → todos na sala precisam de proteção ocular
- Manter apenas pessoal essencial na sala: paciente, operador, assistente

## Cautions essenciais para a sala

| Item | Ação |
|------|------|
| Manuais | Ler warnings, cautions, notes antes de operar |
| Isolamento | Sala não deve ser local de passagem |
| Avisos | Sinais nas portas: "Class 4 laser in use", "Eyewear mandatory" |
| Portas | Fechadas/trancadas durante operação |
| Superfícies refletivas | Remover joias, instrumentos espelhados (cuidado com espelhos clínicos!) |
| Janelas | Cortinas/persianas fechadas |
| Eyewear | Obrigatório para TODOS na sala (paciente incluído) |
| Key | Remover quando equipamento sem uso |
| Smoke | Plume de ablação → máscara N95+ + smoke evacuator dedicado |
| Warning | Avisar todos antes de cada disparo |

## Eyewear — interpretação de specs

Specs de óculos de proteção têm formato como: `815-1100 IR LB7`

Decompondo:

### Wavelengths protegidos
`815-1100` = nm (faixa de proteção para o filtro)

### Operating modes
- **D** — continuous wave (>0.25 s)
- **I** — pulsed (1 µs — 0.25 s) → onde se enquadra Er:YAG/Nd:YAG odonto típico
- **R** — Q-switched (1 ns — 1 µs) → relevante para QSP modes
- Combinações: `DIR` cobre os 3 modos

### Optical density (LB rating)
| LB | Transmissão |
|----|-------------|
| LB1 | 10% |
| LB2 | 1% |
| LB3 | 0.1% |
| LB4 | 0.01% |
| LB5 | 0.001% |
| LB6 | 0.0001% |
| LB7 | 0.00001% |
| LB8 | 0.000001% |

> Quanto MAIOR o LB, MAIOR a proteção. Verificar que o LB nas wavelengths do equipamento é suficiente para a potência usada.

## Combinações típicas para LightWalker (dual-λ)

Como LightWalker emite Er:YAG (2940 nm) E Nd:YAG (1064 nm), o eyewear precisa cobrir AMBAS as faixas. Exemplos válidos (do material LAHA):

### Exemplo 1 (multi-spec):
```
995-1100 DIR LB6 + M LB6Y
1010-1090 D LB6 + IR LB7 + M LB7Y
1050-1080 D LB6 + IR LB8 + M LB7Y
1420-1585 DI LB2
1585-1660 DI LB3
1660-3000 DI LB4
10000-11000 DI LB4
```
→ cobre Nd:YAG (1064) com LB7-LB8 e Er:YAG (2940 dentro de 1660-3000) com LB4. ✅

### Exemplo simples LightWalker:
```
DIR 1064 L7
DI 2800-3000 L5
```
→ cobre Nd:YAG (1064) com LB7 em modo DIR e Er:YAG (2940 dentro de 2800-3000) com LB5 em modo DI. ✅

### Erros comuns na seleção
- Óculos só para Nd:YAG → desprotege para Er:YAG (e vice-versa)
- LB insuficiente para potência do equipamento (verificar com fabricante do equipamento + fabricante do óculos)
- Modo R (Q-switched) faltando quando se usa QSP

## Olho — anatomia e penetração de λ

| Wavelength range | Penetra até | Tecido em risco |
|-----------------|-------------|-----------------|
| UV (< 400 nm) | Córnea/cristalino | Catarata, fotoceratite |
| Visível (400-700 nm) | RETINA (transmite ~90%) | Lesão retiniana, dano térmico, escotomas |
| Near-IR (700-1400 nm) | RETINA (transmite ~70%) | Dano retiniano sem dor (perigoso!) |
| Mid-IR (1400-3000+ nm) | Córnea/aquoso | Queimadura corneana, catarata térmica |
| Far-IR (3000+ nm, CO₂) | Córnea | Queimadura corneana superficial |

### Implicação para LightWalker
- **Nd:YAG 1064 nm**: Near-IR → ATINGE A RETINA → dano retiniano possível, sem dor (paciente pode não notar até dias depois)
- **Er:YAG 2940 nm**: Mid-IR → absorvido na CÓRNEA → queimadura corneana imediata e dolorosa, mas geralmente reversível

## Reflexões — o risco silencioso

- **Especular** (mirror-like): preserva potência do feixe, só muda direção → MESMA fluence em ângulo imprevisível
- **Difusa** (rugosa): luz redirecionada em todas direções → ainda perigosa em fluences altas (Class 4 por definição)
- Joias, espelhos clínicos, instrumentos polidos = fontes ocultas de risco

## Plume e fumaça (ablação)

Ablação Er:YAG cria plume com:
- Vapor d'água
- Partículas micrométricas de tecido
- Compostos voláteis (aldeídos, formaldeído, HCN em alguns casos)
- Vírus (HPV documentado em ablação verrucosa) e bactérias viáveis

**Mitigação:**
- Smoke evacuator dedicado (não aspirador convencional — pressão e filtragem específicas)
- Máscara N95 ou superior (cirúrgica simples NÃO filtra partículas <5 µm)
- Distância de aspiração ≤ 2 cm da fonte de plume
- Filtro do evacuador: trocar conforme protocolo do fabricante

## Checklist pré-operatório de safety (rápido)

Antes de cada sessão Class 4:

1. ☐ Key inserida, equipamento em standby (não armado)
2. ☐ Door interlock verificado/conectado
3. ☐ Sinal "laser in use" na porta
4. ☐ Eyewear correto para λ + modo + LB suficiente — para todos: operador, assistente, paciente
5. ☐ Sala isolada, janelas cobertas
6. ☐ Sem superfícies refletivas no campo
7. ☐ Smoke evacuator preparado (se ablação)
8. ☐ Spray water testado (se Er:YAG ablação)
9. ☐ Calibração de potência verificada (se sessão crítica)
10. ☐ Aviso verbal a todos antes do primeiro disparo
