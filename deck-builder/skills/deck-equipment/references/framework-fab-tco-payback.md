# Framework — FAB + TCO 5 anos + Payback + Sensitivity 3 cenarios

> Os 4 frameworks aplicados em TODOS os outputs `deck-equipment` modo `padrao`.
> Modo `comparativo` aplica os mesmos + expande o bloco de comparativo entre marcas.

---

## 1. FAB — Features → Advantages → Benefits

### Origem
Modelo classico de sales engineering aplicado a venda consultiva de equipamentos medicos. Diferente de listar "specs" (que sao tecnicas e abstratas), FAB amarra cada caracteristica a um beneficio concreto que o decisor (clinica, dentista, hospital) consegue mensurar.

### Estrutura por feature

| Bloco | Pergunta que responde | Audiencia primaria |
|-------|----------------------|--------------------|
| **Feature** | O que o equipamento tem? (caracteristica tecnica objetiva) | engenheiro / tecnico |
| **Advantage** | Por que isso e diferenciado vs alternativas no mercado? | comprador / decisor tecnico |
| **Benefit** | Que resultado concreto isso entrega? (clinico + economico) | decisor financeiro / clinico final |

### Regras de aplicacao

- **Maximo 3-4 features por deck.** Mais que isso dilui mensagem e cliente esquece.
- Cada feature ocupa **1 slide** (slides 5-7 do esqueleto).
- **Benefit DEVE ser quantificavel.** Frases como "melhora qualidade" ou "deixa o paciente satisfeito" sao fracas — preferir "reduz tempo de cadeira em X min", "evita aquisicao de segundo equipamento de R$Y", "expande indicacoes em N protocolos novos".
- **Advantage DEVE ser honesto.** Se a feature existe em outras marcas, diga isso e diferencie em outro vetor (preco, integracao, suporte, ergonomia).

### Exemplos canonicos

#### Exemplo A — Fotona LightWalker AT S (Er:YAG + Nd:YAG dual)

**Feature 1: Dual wavelength integrado (Er:YAG 2940nm + Nd:YAG 1064nm) em chassi unico**
- *Advantage:* Permite executar protocolos hard-tissue (Er:YAG: preparo cavitario, cirurgia ossea) E soft-tissue (Nd:YAG: cirurgia gengival, descontaminacao periodontal) sem trocar equipamento. Concorrentes especializados (Lumenis, BTL) tipicamente exigem 2 aparelhos para mesma cobertura.
- *Benefit:* Elimina aquisicao de 2o equipamento de R$120-180k. Reduz footprint de sala. Treinamento unificado.

**Feature 2: Modo TwinLight (Er:YAG + Nd:YAG na mesma sessao periodontal)**
- *Advantage:* Protocolo proprietario validado em literatura (citar paper Gaspirc & Skaleric 2007 + reviews recentes). Concorrentes nao oferecem combinacao integrada no fluxo.
- *Benefit:* Resultado clinico em periodontite cronica superior a SRP isolado em N pontos de profundidade de bolsa (citar evidencia + GRADE).

**Feature 3: Sistema VSP (Variable Square Pulse) para Er:YAG**
- *Advantage:* Permite ajustar tempo de pulso (50us a 1000us) — concorrentes oferecem 2-3 setpoints fixos. Diferencial em controle termico.
- *Benefit:* Indicacoes adicionais (corte preciso vs ablacao volumetrica) sem trocar configuracao do equipamento.

#### Exemplo B — Megagen AnyRidge (implante)

**Feature 1: Knife Thread (rosca cortante com pitch variavel)**
- *Advantage:* Geometria proprietaria que melhora estabilidade primaria em osso tipo IV (esponjoso). Concorrentes premium (Straumann SLActive, Neodent Drive) sao referencia em outros tipos osseos.
- *Benefit:* Permite carga imediata em maxila posterior com ISQ > 60 em maior porcentagem de casos (citar evidencia AAID).

#### Exemplo C — 3Shape Trios 5 (scanner intraoral)

**Feature 1: Wireless + ScanAssist IA**
- *Advantage:* Workflow sem cabo + algoritmo de fechamento de buracos automatico. iTero 5D Plus tem fio + algoritmo proprio Align.
- *Benefit:* Reduz tempo de escaneamento em 25-30% (benchmark Trios) e onboarding de assistente em 1 sessao menos.

---

## 2. TCO 5 anos — Total Cost of Ownership

### Por que 5 anos
Vida util tipica de equipamento medico/dental premium e 7-10 anos, mas analise de 5 anos:
1. cobre periodo de financiamento padrao (36-60 meses)
2. e horizonte de planejamento financeiro confortavel para clinica
3. permite comparar com payback (que tipicamente ocorre em 12-36 meses)

### Componentes obrigatorios

| Componente | Como estimar | Notas |
|------------|--------------|-------|
| **Aquisicao** | Preco a vista OU valor financiado total (principal + juros) | Se parcelado, distribuir nos anos correspondentes |
| **Consumiveis** | Custo por procedimento × volume anual | Inclui pecas de mao, brocas, fibras laser, descartaveis, contraste |
| **Manutencao** | Contrato preventivo anual + reserva corretiva (~3-5% do valor do equipamento/ano) | Anos 1-2 podem ter garantia inclusa |
| **Treinamento** | Inicial Ano 1 (custo de curso + viagem + horas paradas) + reciclagens Ano 3 e 5 | Importante para laser (CFO exige) |
| **Software/atualizacao** | Licencas anuais (scanner, planejamento, integracao DICOM) | Cresce com expansao do uso |

### Template tabela TCO

| Componente | Ano 1 | Ano 2 | Ano 3 | Ano 4 | Ano 5 | Total 5a |
|------------|-------|-------|-------|-------|-------|---------|
| Aquisicao | R$X | — / R$X (se financiado) | ... | ... | ... | R$X total |
| Consumiveis | R$X | R$X | R$X | R$X | R$X | R$X |
| Manutencao | (garantia) | R$X | R$X | R$X | R$X | R$X |
| Treinamento | R$X | — | R$X (reciclagem) | — | R$X | R$X |
| Software | R$X | R$X | R$X | R$X | R$X | R$X |
| **Total ano** | **R$X** | **R$X** | **R$X** | **R$X** | **R$X** | **R$X** |
| Acumulado | R$X | R$X | R$X | R$X | R$X | — |

### Regras de honestidade

- NUNCA omitir manutencao corretiva (mesmo se equipamento "nao quebra")
- NUNCA usar preco promocional como base de aquisicao se nao esta vigente
- NUNCA esquecer reajuste de consumiveis (inflacao + cambio se imp.)
- Se estimativa tem alta incerteza, marcar com nota de rodape "estimativa baseada em [fonte]"

---

## 3. Payback Analysis

### Formula base

```
Margem por procedimento = Preco cobrado - Custo variavel - (Depreciacao + manutencao alocada por procedimento)

Procedimentos para payback = Investimento total / Margem por procedimento

Tempo de payback = Procedimentos para payback / (Procedimentos por mes × 12)
```

### Componentes

| Item | Como estimar |
|------|--------------|
| **Preco cobrado** | Pesquisa de mercado regional + posicionamento da clinica (premium / intermediario / popular) |
| **Custo variavel** | Consumiveis por procedimento + tempo de cadeira × custo hora-profissional + insumos descartaveis |
| **Depreciacao alocada** | (Investimento / vida util em meses) / procedimentos esperados por mes |
| **Manutencao alocada** | (Custo anual manutencao / 12) / procedimentos por mes |

### Output esperado no slide 11

Frase canonica: **"No cenario realista (X procedimentos/mes, R$Y preco medio, R$Z margem), o equipamento se paga em N meses."**

Sempre indicar:
- N meses de payback
- Volume mensal assumido
- Margem por procedimento usada
- Comparacao com volume historico ou projetado da clinica (E2/E4)

### Sinalizar 🟡 se

- Volume necessario para payback > capacidade atual da clinica (clinica nao consegue absorver)
- Payback > 36 meses (longo demais para equipamento de vida util 7-10 anos)
- Margem por procedimento < 30% do preco cobrado (precificacao insustentavel)

---

## 4. Sensitivity Analysis — 3 cenarios

### Por que 3 cenarios

Decisor financeiro precisa enxergar **range** de resultado, nao apenas ponto otimo. 3 cenarios cobrem psicologicamente:
- Otimista: argumento de upside para vencedor entusiasmado
- Realista: base de decisao
- Pessimista: defesa para CFO/socio ceticista — **se o pessimista ainda paga, a decisao e robusta**

### Template tabela Sensitivity

| Variavel | Otimista | Realista | Pessimista |
|----------|----------|----------|------------|
| Volume/mes | (1.5-2× realista) | (E4 do usuario) | (50-70% do realista) |
| Preco medio cobrado | (premium do mercado) | (mediana mercado regional) | (preco minimo defensivel) |
| Margem por procedimento | R$X | R$Y | R$Z |
| Payback (meses) | N meses | N meses | N meses |
| ROI 5 anos | X% | Y% | Z% |

### Regras de construcao

- **Realista = E4 do usuario.** NAO inventar — usar o numero que o cliente forneceu.
- **Otimista = realista × 1.5 a 2.0** em volume, + preco no terco superior do mercado regional.
- **Pessimista = realista × 0.5 a 0.7** em volume, + preco no minimo defensivel (sem perder margem).
- **Pessimista DEVE pagar.** Se nao paga em 5 anos: ou equipamento esta superdimensionado para o cliente (recomendar revisitar E2/E4), ou o cliente nao e perfil — skill deve sinalizar isso explicitamente em texto livre depois da tabela.

### Frase canonica de fechamento (slide 12)

**"Mesmo no cenario pessimista — volume de X/mes a R$Y por procedimento — o equipamento se paga em N meses e gera ROI de Z% em 5 anos. No realista, payback em N meses. No otimista, payback em N meses."**

---

## 5. Como amarrar os 4 frameworks no STORYBOARD

| Slide | Framework primario | Conteudo |
|-------|-------------------|----------|
| 5 | FAB | Feature 1 |
| 6 | FAB | Feature 2 |
| 7 | FAB | Feature 3 |
| 10 | TCO 5 anos | Tabela componentes × anos |
| 11 | Payback | Formula + meses no cenario realista |
| 12 | Sensitivity | Tabela 3 cenarios + frase de fechamento |

Os 4 frameworks juntos respondem as 4 perguntas do decisor:
- "O que diferencia este equipamento?" → FAB
- "Quanto vou gastar ao todo nos proximos 5 anos?" → TCO
- "Quando recupero o investimento?" → Payback
- "E se as coisas nao saem como o esperado?" → Sensitivity

Faltar qualquer um deles deixa a decisao **vulneravel a objecao** que aparece sempre no momento da assinatura do contrato.
