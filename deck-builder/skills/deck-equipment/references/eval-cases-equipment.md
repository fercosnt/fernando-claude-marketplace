# Eval cases — deck-equipment

3 cenarios canonicos cobrindo:
- Laser Classe III + auto-detection Fotona + comparativo respeitoso
- Implante Classe II + consultorio solo + comparativo multi-marca
- Scanner Classe II + ROI digital + comparativo respeitoso

Cada caso lista entrada, esperado e criterios de avaliacao.

---

## Case 1 — Fotona LightWalker pra Smile Premium SP (modo `padrao`)

### Input (resumido)

- **U1:** Smile Premium SP aprova compra LightWalker em 60 dias
- **U6:** Fotona (auto-detect via regex `\bFotona\b|LightWalker|Er:YAG|Nd:YAG`)
- **E1:** Fotona LightWalker AT S (Er:YAG + Nd:YAG dual) — Anvisa Classe III, numero registro pedir ao usuario
- **E2:** Clinica boutique SP, 4 cadeiras
- **E3:** R$280k a vista; R$320k financiado 36x
- **E4:** 18 pacientes/mes laser → payback alvo 18 meses
- **E5:** Lumenis LightSheer (alternativa unica) → **modo `padrao`**

### Esperado no STORYBOARD

- **Auto-detection:** tags `anvisa-laser-classe-iii` + `cfo-laser` injetadas
- **18 slides** (estrutura padrao)
- **FAB 3 features:** Dual wavelength integrado (slide 5), TwinLight periodontal (slide 6), VSP modulacao (slide 7)
- **Comparativo Lumenis respeitoso** (slide 8): cita Lumenis com respeito (referencia em fotodepilacao desde 2003), lista 2 forcas + 2 limites com fonte, posiciona LightWalker como superior em integracao Er:YAG + Nd:YAG (criterio especifico), fecha com "depende do mix de procedimentos"
- **TCO 5 anos** (slide 10): tabela 5 colunas (Ano 1-5) com aquisicao R$280k, consumiveis Er+Nd, manutencao a partir do Ano 3, treinamento Ano 1 e Ano 3, total acumulado
- **Payback** (slide 11): formula explicita, payback 18 meses no realista (18 pacientes/mes × margem) — bate com E4
- **Sensitivity** (slide 12): otimista 36/mes payback ~9m, realista 18/mes payback 18m, pessimista 10/mes payback ~30m; frase de fechamento "mesmo no pessimista paga em 30m"
- **Compliance Anvisa Classe III** (slide 14): numero registro citado (ou 🟡 se nao fornecido), habilitacao CFO/CFM declarada, COI verificavel
- **Checklist:** ✅ comparativo respeitoso; 🟡 numero registro a confirmar; 🟡 TCLE se caso clinico real

### Criterios de avaliacao (assertions)

1. Frontmatter STORYBOARD inclui `Skill geradora: deck-equipment` e `Marca: Fotona`
2. Tag de compliance `anvisa-laser-classe-iii` aparece no bloco compliance
3. Slide 5/6/7 cada um tem F-A-B explicitos (3 blocos por slide)
4. Slide 8 cita Lumenis pelo nome SEM frase proibida do anti-badmouth
5. Slide 10 tem tabela TCO com 5 anos + 5 componentes minimos
6. Slide 11 tem formula payback + 18 meses no realista
7. Slide 12 tem 3 colunas (otimista/realista/pessimista)
8. Slide 14 menciona Classe III + numero registro (ou 🟡 se faltante)
9. Checklist 3 tiers preenchido no rodape (🔴/🟡/✅)

---

## Case 2 — Megagen AnyRidge implante pra dentista solo (modo `comparativo`)

### Input (resumido)

- **U1:** Dentista solo adota AnyRidge como implante primario
- **U6:** generico (sem auto-detect Fotona)
- **E1:** Megagen AnyRidge Knife Thread — Anvisa Classe III (implantes osseointegraveis tem grau de risco maior), numero a confirmar
- **E2:** Consultorio solo, 1 dentista, 2 cadeiras
- **E3:** R$280/unidade, caixa de 10 = R$2.800; pacote inicial 5 caixas = R$14k
- **E4:** 5 implantes/mes para payback alvo 18-24 meses
- **E5:** Straumann (premium global) + Neodent (premium BR) → **modo `comparativo`**

### Esperado no STORYBOARD

- **16-18 slides** (modo comparativo expande slide 8 em 8a/8b/8c)
- **FAB 3 features:** Knife Thread geometria (slide 5), superficie XPEED tratamento Ca (slide 6), conexao interna hexagonal (slide 7)
- **Comparativo modo `comparativo`** (slides 8a/8b/8c):
  - 8a Forcas: tabela 3 colunas (Megagen / Straumann / Neodent) com 3 forcas cada, com fonte
  - 8b Limites: tabela 3 colunas com 2 limites cada, fonte explicita (bula, paper, benchmark)
  - 8c Criterio: "depende do mix de casos: maxila posterior tipo IV osseo → Megagen / casos complexos com necessidade de SLActive → Straumann / suporte local + parceria laboratorial regional → Neodent"
- **TCO 5 anos** (slide 10): compra incremental por caixa, 5 implantes/mes × 12 = 60 implantes/ano = 6 caixas/ano → custo consumo R$16.8k/ano + brocas/instrumentais
- **Payback** (slide 11): margem por implante (preco cobrado R$2.5-4k − custo R$280 − custo cadeira) = R$2k+; payback ~24m no realista
- **Sensitivity** (slide 12): otimista 10 implantes/mes / realista 5/mes / pessimista 3/mes
- **Compliance Anvisa Classe III** (slide 14): registro Megagen Brasil; sem habilitacao especial (implante nao e laser, mas Classe III por risco)
- **Caso clinico AAID** (slide 9): 1 caso real com TCLE OU caso da literatura citado

### Criterios de avaliacao (assertions)

1. Modo `comparativo` detectado a partir de E5 com 2+ marcas
2. Slides 8a, 8b, 8c presentes (slide 8 expandido)
3. Tabela 8a tem 3 colunas (Megagen / Straumann / Neodent) com 3 forcas cada
4. Tabela 8b tem 3 colunas com 2 limites cada, com fonte explicita
5. Slide 8c tem criterio NEUTRO de escolha (nao declara vencedor geral)
6. NENHUMA frase proibida do anti-badmouth nos slides 8a/8b/8c
7. TCO 5 anos calcula compra incremental por caixa (nao bloco unico)
8. Payback considera margem por implante e volume 5/mes
9. Sensitivity 3 cenarios com pessimista 3/mes (~50% do realista)

---

## Case 3 — Scanner Trios 5 pra ortodontista (modo `padrao`)

### Input (resumido)

- **U1:** Ortodontista compra Trios 5 e migra workflow para digital
- **U6:** generico
- **E1:** 3Shape Trios 5 — Anvisa Classe II
- **E2:** Consultorio ortodontico, 1 ortodontista, 3 cadeiras
- **E3:** R$110k aquisicao + assinatura Trios Care R$8.4k/ano + software 3Shape Communicate
- **E4:** 12 casos digitais/mes para payback 24 meses
- **E5:** iTero 5D Plus (Align) → **modo `padrao`** (1 alternativa unica)

### Esperado no STORYBOARD

- **17 slides** (estrutura padrao)
- **FAB 3 features:** Wireless + ScanAssist IA (slide 5), abertura ortodontica (Setup virtual / Communicate / integracao Invisalign + outros) (slide 6), workflow digital end-to-end (escanear → planejar → fabricar) (slide 7)
- **Comparativo iTero respeitoso** (slide 8): cita iTero como referencia em integracao Align (Invisalign), lista 2 forcas + 2 limites (vendor lock-in Align, custo de uso por aparelho proprio), posiciona Trios como aberto (multi-fabricante), fecha com "depende do volume Invisalign vs outros aparelhos"
- **TCO 5 anos** (slide 10): aquisicao R$110k Ano 1 + Trios Care R$8.4k/ano × 5 = R$42k + software 3Shape Communicate licenca anual + treinamento Ano 1 e Ano 3
- **Payback** (slide 11): margem por aparelho ortodontico digital ~R$500-1500 economizado vs analogico (sem moldagem alginato + sem envio gesso); 12 casos/mes × margem → payback ~24m
- **Sensitivity** (slide 12): otimista 24/mes payback 12m, realista 12/mes 24m, pessimista 8/mes 36m (no limite — sinalizar 🟡 se pessimista > 36m)
- **Workflow demo** (slide 4): foto fluxo Trios → setup virtual → aparelho (sem TCLE pois e mockup ou caso publicado pela 3Shape)
- **Compliance Anvisa Classe II** (slide 14): registro 3Shape; LGPD declarada (arquivos STL/PLY sao dados de saude); integracao DICOM/HL7 mencionada
- **Treinamento** (slide 13): destacar curva de aprendizado wireless + 3Shape Communicate

### Criterios de avaliacao (assertions)

1. Modo `padrao` detectado (1 unica alternativa em E5)
2. Slide 8 cita iTero pelo nome SEM frase proibida
3. Comparativo destaca abertura Trios vs vendor lock-in iTero/Align (com fonte ou contexto neutro)
4. TCO 5 anos inclui assinatura anual Trios Care
5. Payback considera economia por digitalizacao do fluxo (nao apenas margem direta)
6. Sensitivity 3 cenarios; pessimista 36m sinalizado 🟡 se ultrapassar
7. Slide 14 declara Classe II + LGPD para STL/PLY
8. Frontmatter STORYBOARD `Marca: 3Shape` ou `generico` (sem auto-detect Fotona)

---

## Roll-up — criterios comuns aos 3 cases

Para qualquer eval rodada:

- [ ] STORYBOARD header §10.2 completo (Meta + Estrutura Narrativa + Slides + Compliance 3 tiers)
- [ ] 4 frameworks aplicados: FAB (slides 5-7) + TCO 5 anos (10) + Payback (11) + Sensitivity 3 cenarios (12)
- [ ] Comparativo SEM frase proibida do anti-badmouth (verificar lista em compliance-anvisa-equipment.md secao 5)
- [ ] Compliance Anvisa: Classe declarada + numero registro citado ou 🟡 marcado
- [ ] Schema §10.2 valido
- [ ] `max_ctas: 1` respeitado
- [ ] Whitelist `deck-image-prompts` respeitada (slides 1/2/3/4/8/9 preenchem prompt; 10/11/12/14/15/16 skip)
