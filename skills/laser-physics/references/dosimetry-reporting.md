# Dosimetry Reporting — Checklist Completo para Pesquisa e Publicação

Esta reference é o "modo pesquisa" da skill. Quando o usuário tem um artigo a ser revisado/escrito ou um protocolo a ser publicado, usar este checklist.

## Por que isso importa

Um revisor de revista científica de odontologia/laser tipicamente cobra:

> "Authors should clarify that the selected settings correspond to a defined fluence per pulse and should additionally provide the resulting average power, irradiance, energy delivered per 30-second application, and cumulative energy across the three irradiations. More importantly, they should explain why this specific dosimetry was chosen."

Não basta listar "5 W, 30 s" — é preciso reportar TODOS os parâmetros derivados E justificar a escolha.

## Checklist de 14 parâmetros para reporte completo

Sempre reportar TODOS os 14 abaixo (mesmo que alguns sejam "implícitos" no equipamento). Marcar com ✅ os reportados; falta = LACUNA a corrigir.

### Parâmetros DIRETOS do equipamento

| # | Parâmetro | Símbolo | Unidade | Notas |
|---|-----------|---------|---------|-------|
| 1 | Wavelength | λ | nm | Er:YAG 2940 nm; Nd:YAG 1064 nm |
| 2 | Energia por pulso | E | mJ | display do equipamento |
| 3 | Spot size (diâmetro) | d | mm | tem que vir do handpiece/tip usado |
| 4 | Pulse duration | t | µs ou ms | citar mode também (SSP/MSP/SP/LP/VLP) |
| 5 | Repetition frequency | ν | Hz | display do equipamento |
| 6 | Tempo de aplicação | t_app | s | tempo total de cada irradiação |
| 7 | Número de aplicações | n | — | quantas vezes a irradiação foi repetida (mesmo ponto) |

### Parâmetros DERIVADOS (que devem ser CALCULADOS e reportados)

| # | Parâmetro | Símbolo | Fórmula | Unidade |
|---|-----------|---------|---------|---------|
| 8 | Spot area | S | π/4 × d² | cm² |
| 9 | Fluence per pulse | F | E / S | J/cm² |
| 10 | Peak power | Ppeak | E / t | W |
| 11 | Average power | Pave | E × ν | W |
| 12 | Irradiance (avg power density) | I | Pave / S | W/cm² |
| 13 | Energia por aplicação | E_app | Pave × t_app | J |
| 14 | Energia cumulativa | E_cum | E_app × n | J |

> Em literatura biomédica de laser, "irradiance" geralmente = average power density (W/cm²). Em literatura mais física pode aparecer como fluence rate. Reportar a fórmula para evitar ambiguidade.

## Exemplo completo: caso bleaching dental

**Cenário:** revisor cobrou em paper de bleaching ativado por laser. Operador reportou apenas "5 W, 30 s, 3 aplicações com handpiece R30A em modo XYZ".

**Reconstrução completa:**

```
Equipment:    Fotona LightWalker
Wavelength:   1064 nm (Nd:YAG)
Handpiece:    R30A
Spot diameter: d = 5 mm = 0.5 cm
Pulse mode:   25 ms (LP equivalent)
Frequency:    ν = 1 Hz
Average power (display): Pave = 5 W
Application time: t_app = 30 s/aplicação
Number of applications: n = 3

DERIVED:
S       = π/4 × (0.5)² = 0.196 cm²
E       = Pave / ν = 5 W / 1 Hz = 5000 mJ = 5 J por pulso
F       = E / S = 5 / 0.196 = 25.5 J/cm² por pulso
Ppeak   = E / t = 5 J / 0.025 s = 200 W
I (avg) = Pave / S = 5 / 0.196 = 25.5 W/cm²
E_app   = Pave × t_app = 5 × 30 = 150 J por aplicação
E_cum   = 150 × 3 = 450 J total entregue na área

REPORTING TABLE pronta para Methods:
| Parameter            | Value      |
|----------------------|------------|
| Wavelength           | 1064 nm    |
| Pulse duration       | 25 ms      |
| Frequency            | 1 Hz       |
| Energy per pulse     | 5 J        |
| Spot diameter        | 5 mm       |
| Spot area            | 0.196 cm²  |
| Fluence per pulse    | 25.5 J/cm² |
| Peak power           | 200 W      |
| Average power        | 5 W        |
| Irradiance           | 25.5 W/cm² |
| Application time     | 30 s       |
| Energy per application | 150 J    |
| Number of applications | 3        |
| Cumulative energy    | 450 J      |
```

## Justificativa científica — os 4 pilares

Toda escolha de dosimetria deve ser justificada por pelo menos UMA das fontes abaixo (idealmente várias):

### 1. Literatura prévia (PRIMARY)
Citar protocolo previamente publicado e validado.
- Formato: "Os parâmetros foram baseados em [Autor et al., ano], que demonstraram [efeito desejado] sem [evento adverso] em [condição similar]."
- Quando a literatura cobre um análogo mas não exato: "Adaptado de [paper], com ajuste de [X] para acomodar [Y]."

### 2. Manufacturer guidance
Recomendação oficial do fabricante (Fotona, no caso do LightWalker).
- Citar: nome do protocolo (ex: "Fotona TouchWhite protocol"), versão do manual.
- Limitação: protocolo do fabricante não substitui validação clínica/literatura.

### 3. Pilot testing
Estudo piloto in vitro ou in situ que estabeleceu a janela segura.
- Reportar: n de amostras, faixa testada, critério de seleção (ex: aumento de temperatura medido com termopar < limite).
- Forma: "Os parâmetros foram estabelecidos em estudo piloto (n=X) que demonstrou aumento de temperatura intra-pulpar de [valor]°C, abaixo do limiar crítico de 5.5°C estabelecido por Zach & Cohen (1965)."

### 4. A priori thermal threshold
Cálculo/argumento explícito de que os parâmetros ficam abaixo de um limite térmico conhecido.
- Forma: "A irradiância de [X] W/cm² × [t] s entrega [E] J/cm², mantendo o aumento térmico esperado abaixo de [limite] com base em [modelo de difusão térmica / paper de termografia]."

## Lacunas comuns que revisores cobram

| Lacuna | Como prevenir |
|--------|---------------|
| Reportar só "potência média" | Adicionar fluence/pulso + peak power + irradiância |
| Não citar tempo total de exposição | Sempre reportar t_app E número de aplicações E energia cumulativa |
| Não justificar parâmetros | Sempre adicionar referência (paper, manufacturer, piloto) — pelo menos UMA |
| Confundir Peak vs Average power | Reportar AMBOS, com fórmula explícita |
| Não reportar spot size | Sem isso, fluence não é calculável → reproducibility = zero |
| Não reportar pulse mode (SSP/MSP/etc) | Em VSP technology, pulse duration é fixa por mode — citar mode + duração |
| Esquecer wavelength em estudo dual-λ | Sempre explicitar qual λ foi usado em cada etapa |
| Não reportar uso de spray water | Para Er:YAG ablação isso ALTERA o mecanismo significativamente |
| Não reportar tip wear / calibração | Especialmente em estudos in vitro longos |

## Thresholds térmicos canônicos (para argumento de safety)

### Pulpa dental
- **Zach & Cohen 1965**: ΔT > 5.5°C → 15% das polpas com necrose; ΔT > 11°C → 60% necrose
- **Pohto & Scheinin 1958**: limite mais conservador, ΔT 4-5°C
- **Discussão moderna**: limite pode ser específico para idade dentária, espessura dentinária remanescente, tempo de exposição (não só pico). Citar com cautela mas é o standard de fato.

### Tecido mole intra-oral
- **Coagulação reversível**: ~50-60°C
- **Coagulação irreversível**: > 60°C
- **Vaporização**: > 100°C (água)
- **Carbonização**: > 200°C (perda de tecido + risco de plume tóxico)

### Osso
- **Osteonecrose induzida**: > 47°C por > 1 min (Eriksson & Albrektsson 1983)
- Implicação para implantodontia: spray water OBRIGATÓRIO

### Cementum/periodonto
- Aumento sustentado > 10°C → risco de dano periodontal
- Para Nd:YAG endo: discussão sobre superficial vs apical, com termografia

## Validação cruzada antes de publicar

Antes de submeter, rodar este sanity check:

1. ✅ Todos os 14 parâmetros listados na tabela?
2. ✅ Pelo menos 1 dos 4 pilares de justificativa citados?
3. ✅ Threshold térmico relevante para a aplicação foi mencionado?
4. ✅ Wavelength explícito em cada etapa do protocolo?
5. ✅ Fluence calculada bate com display do equipamento (se aplicável)?
6. ✅ Energia cumulativa razoável vs literatura (não está ordens de magnitude diferente)?
7. ✅ Spot size + spot área + handpiece model reportados?
8. ✅ Pulse mode (não só duração) citado?
9. ✅ Spray water usage reportado (sim/não, fluxo se medido)?
10. ✅ Distância de trabalho (tip-to-tissue) se contact-free?

Se algum item falhar, reescrever Methods antes de submeter — reduz drasticamente os "major revisions" cobrados por revisores de laser.

## Formato sugerido de tabela "Laser Parameters" para Methods

Para inserir direto em Methods de paper:

```
Table X. Laser irradiation parameters.

| Parameter                          | Value          |
|------------------------------------|----------------|
| Laser system                       | [Modelo, Fabricante, País] |
| Active medium / Wavelength         | [Er:YAG 2940 nm] |
| Pulse mode                         | [MSP] |
| Pulse duration                     | [100 µs] |
| Repetition rate (frequency)        | [10 Hz] |
| Energy per pulse                   | [200 mJ] |
| Spot diameter (handpiece)          | [1 mm — H02] |
| Spot area                          | [0.0075 cm²] |
| Fluence per pulse                  | [26.7 J/cm²] |
| Peak power                         | [2000 W] |
| Average power                      | [2 W] |
| Irradiance (avg power density)     | [266.7 W/cm²] |
| Application time per cycle         | [20 s] |
| Number of cycles per session       | [3] |
| Energy per cycle                   | [40 J] |
| Cumulative energy per session      | [120 J] |
| Coolant                            | [Air-water spray, X mL/min] |
| Working mode                       | [Contact / Non-contact distance Y mm] |
| Operator                           | [Single experienced operator] |
| Calibration                        | [Pre-experiment power meter check] |

Justification: Parameters selected based on [reference/manufacturer/pilot], 
designed to maintain pulpal temperature increase below the 5.5°C threshold 
established by Zach & Cohen (1965).
```

Este template resolve preventivamente ~80% das críticas dosimétricas de revisores.
