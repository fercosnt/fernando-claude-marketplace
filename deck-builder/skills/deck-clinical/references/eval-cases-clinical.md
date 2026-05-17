# Eval cases — deck-clinical

Tres casos canonicos. Cobrem os dois modos + diferenciais regulatorios criticos. Fixtures executaveis em [../evals/evals.json](../evals/evals.json).

---

## Case 1 — Protocolo Er:YAG clareamento pra dentistas (peer-facing)

### Input

- **U1 Big Idea:** "Dentistas aprovam protocolo Er:YAG como alternativa ao peroxido em casos de hipersensibilidade severa"
- **U2 Audiencia:** dentistas clinico-gerais e esteticos, mix iniciantes/experientes
- **U3 Duracao:** 20min
- **U4 Formato:** call remota (curso pos-graduacao)
- **U6 Marca:** Fotona (auto-detect → injeta `anvisa-laser-classe-iii` + carrega `laser-physics` se disponivel)
- **C1 Protocolo:** Clareamento dental com Er:YAG 2940nm (off-label vs convencional peroxido)
- **C2 Indicacao:** Hipersensibilidade dental severa + recessao gengival (peroxido contraindicado)
- **C3 Evidencia:** 1 case series + 2 RCTs piloto → GRADE moderate para outcome clareamento; LOW para outcome cura sintomatica em 12 meses
- **C4 Audiencia:** especialista → modo `peer-facing`
- **C5 Antes-e-depois:** sim, COM TCLE assinado

### Esperado: 12 slides Calgary-Cambridge

| # | Tipo | Action title (exemplo) | Compliance |
|---|------|----------------------|-----------|
| 1 | capa | "Er:YAG clareamento — alternativa em hipersensibilidade severa" | CRO declarado |
| 2 | problema | "Caso: paciente 42a, hipersensibilidade grau IV, peroxido contraindicado" | — |
| 3 | problema | "Peroxido falha em 30-40% dos casos com recessao + sensibilidade" | — |
| 4 | conceitual (mecanismo) | "Er:YAG age na agua intracristalina — sem oxidacao quimica" | — |
| 5 | dados (evidencia) | "GRADE moderate clareamento / LOW cura sintomatica 12m" | GRADE explicito |
| 6 | conceitual (protocolo) | "Protocolo passo-a-passo — fluence 1.5-2.5 J/cm², 10Hz, 4 sessoes" | dosimetria conforme bula |
| 7 | demo | "Procedimento ao vivo — sequencia + parametros visiveis" | — |
| 8 | comparativo (antes-depois) | "Caso 1: 4 sessoes, delta SGU 6 unidades — TCLE assinado, finalidade educativa" | TCLE explicito ✅ |
| 9 | dados (outcome curto-prazo) | "Outcome imediato — N=8 pacientes, sucesso clinico 7/8" | — |
| 10 | dados (follow-up) | "Outcome 6 meses — recidiva 1/7 casos" | — |
| 11 | disclaimer | "Fotona LightWalker — registro Anvisa {REGISTRO}, classe III. COI: relator e consultor Fotona." | Anvisa + COI ✅ |
| 12 | CTA | "Discussao + Q&A — uso off-label, criterios de selecao" | off-label disclaimer presente |

### Bloco Compliance & Disclaimers (3 tiers) esperado

```
🔴 Issues bloqueantes (resolver antes de apresentar):
- (nenhum — TCLE assinado, COI declarado, GRADE citado, registro Anvisa marcado como placeholder pendente {REGISTRO}: preencher antes)

🟡 Verificar antes:
- Slide 12: confirmar que off-label esta explicito no body, nao apenas implicito no titulo
- Slide 6: dosimetria conforme bula Fotona LightWalker — confirmar parametros antes
- COI Fotona: confirmar se ha pagamento direto vs cortesia em equipamento (graduacao do COI muda)

✅ OK:
- TCLE mencionado (slide 8)
- GRADE citado por outcome (slide 5)
- COI Fotona declarado (slide 11)
- Anvisa Classe III referenciada (slide 11)
- Linguagem clinica adequada — nenhum termo proibido detectado
- Bloco evidencia presente (slide 5)
- Follow-up apresentado (slide 10)
```

### Assertions

- [ ] Frontmatter STORYBOARD tem `Modo: peer-facing`
- [ ] 12 slides gerados
- [ ] Slide tipo `comparativo` menciona TCLE no body
- [ ] Slide tipo `disclaimer` cita registro Anvisa + COI Fotona
- [ ] GRADE aparece em slide tipo `dados` (slide 5)
- [ ] Bloco final tem ≥1 item em cada tier (🔴 pode ser vazio)
- [ ] `anvisa-laser-classe-iii` tag injetada (verificavel no Meta header)

---

## Case 2 — Implante All-on-4 pra paciente 55 anos SEM TCLE (patient-facing)

### Input

- **U1 Big Idea:** "Paciente aprova plano All-on-4 e agenda procedimento em 30 dias"
- **U2 Audiencia:** paciente 55 anos, perdeu 8 dentes superiores, prefere solucao definitiva
- **U3 Duracao:** 15min (consulta)
- **U4 Formato:** presencial em consultorio
- **U6 Marca:** Beauty Smile (auto-detect → carrega `beauty-smile-design-system`)
- **C1 Protocolo:** All-on-4 — reabilitacao total maxilar (4 implantes + protocolo carga imediata)
- **C2 Indicacao:** Edentulismo parcial avancado superior, paciente saudavel, expectativa de vida >20a
- **C3 Evidencia:** systematic review 2021 (Maló et al.) — 95% sobrevivencia 10a (HIGH GRADE)
- **C4 Audiencia:** paciente leigo → modo `patient-facing`
- **C5 Antes-e-depois:** SIM, mas **TCLE pendente** — paciente do caso original ainda nao assinou liberacao

### Esperado: 7 slides AIDET

| # | Tipo | Action title (linguagem leiga) | AIDET letra | Compliance |
|---|------|------------------------------|-------------|-----------|
| 1 | capa | "Seu plano de tratamento — Beauty Smile" | (capa) | — |
| 2 | problema | "Dr. Fernando + equipe Beauty Smile vao acompanhar voce" | A + I | — |
| 3 | problema | "Sua situacao hoje — perda de 8 dentes superiores" | E inicio | linguagem leiga ✅ |
| 4 | conceitual | "Plano proposto: 4 implantes que sustentam todos os dentes superiores" | E continuacao | — |
| 5 | dados | "Duracao — cirurgia 3-4h. Dentes provisorios no mesmo dia. Definitivos em 4 meses." | D | tempo realista |
| 6 | comparativo | "Suas opcoes — All-on-4 (proposto) | Protese removivel | Implantes unitarios | Nao fazer nada" | (alternativas) | alternativas obrigatorias ✅ |
| 7 | CTA | "Proximos passos — agendamento + estamos disponiveis pos-procedimento" | T | — |

### Bloco Compliance & Disclaimers (3 tiers) esperado

```
🔴 Issues bloqueantes (resolver antes de apresentar):
- TCLE pendente para antes-e-depois do caso de referencia → CFO Res. 196/2019, art. 18, II, "g". Solucao: (a) obter TCLE assinado do paciente do caso, OU (b) remover antes-e-depois e usar esquema anatomico generico.
- Procedimento invasivo apresentado a paciente → slide 6 ALTERNATIVAS deve incluir "nao fazer nada" como opcao legitima — confirmar que apresentacao verbal nao omite essa opcao.

🟡 Verificar antes:
- Slide 4: substituir "osseointegracao" e "carga imediata" caso aparecam no speaker notes — linguagem leiga
- Slide 5: confirmar tempos com cirurgiao responsavel (3-4h pode variar)
- Disclaimer "individual variation" precisa ser dito verbalmente quando mostrar duracao
- Sem GRADE explicito — modo patient-facing nao exige, mas estar preparado para pergunta do paciente

✅ OK:
- AIDET aplicado (A+I slide 2, D slide 5, E slides 3-4, T slide 7)
- Alternativas mostradas (slide 6) — consentimento informado
- Linguagem leiga em titulos
- Beauty Smile design system carregado
- Sem promessa de cura/garantia/100% detectada
```

### Assertions

- [ ] Frontmatter STORYBOARD tem `Modo: patient-facing`
- [ ] 7 slides gerados (faixa 6-8)
- [ ] Slide 6 tem 4 alternativas incluindo "nao fazer nada"
- [ ] Bloco final tem 🔴 BLOCKER mencionando TCLE pendente (CFO 196/2019)
- [ ] Nenhum dos action titles contem jargao tecnico (osseointegracao, carga imediata, etc.)
- [ ] Storyboard FOI gerado mesmo com 🔴 (D7 SEM hard-block — valida regra)
- [ ] Bloco final tem ≥1 item em cada tier

---

## Case 3 — Aula CIOSP "Laser na endodontia" (peer-facing)

### Input

- **U1 Big Idea:** "Dentistas do CIOSP saem entendendo quando aplicar Nd:YAG vs Er:YAG em endodontia"
- **U2 Audiencia:** dentistas endodontistas + clinico-gerais (mix), CIOSP plateia ~80 pessoas
- **U3 Duracao:** 45min + Q&A
- **U4 Formato:** presencial congresso
- **U6 Marca:** Fotona (auto-detect → `anvisa-laser-classe-iii` + `laser-physics`)
- **C1 Protocolo:** Laser na endodontia — descontaminacao do canal radicular (Nd:YAG 1064nm + Er:YAG 2940nm comparados)
- **C2 Indicacao:** Necrose pulpar com infeccao persistente, retratamento endodontico
- **C3 Evidencia:** 3 systematic reviews + 1 meta-analise para descontaminacao (GRADE HIGH); 1 RCT pequeno com alto risco vies para cura sintomatica 6m (GRADE LOW)
- **C4 Audiencia:** especialista → `peer-facing`
- **C5 Antes-e-depois:** sim, com TCLE; mais imagens radiograficas pre/pos

### Esperado: 14 slides Calgary-Cambridge + apendice

| # | Tipo | Foco | Compliance |
|---|------|------|-----------|
| 1 | capa | "Laser na endodontia — quando Nd:YAG vence Er:YAG" | CRO + CIOSP |
| 2 | problema | "Caso clinico: dente 36, necrose, 2 retratamentos falhados" | — |
| 3 | problema | "Limitacoes da irrigacao convencional (NaOCl + EDTA)" | — |
| 4 | conceitual | "Mecanismo Nd:YAG vs Er:YAG — penetracao + interacao tecidual" | — |
| 5 | dados (evidencia 1) | "Descontaminacao bacteriana: GRADE HIGH (3 SR + 1 meta-analise)" | GRADE explicito ✅ |
| 6 | dados (evidencia 2) | "Cura sintomatica 6m: GRADE LOW (1 RCT pequeno, alto vies)" | GRADE explicito ✅ |
| 7 | dados (evidencia 3) | "Sumario dos outcomes — adoptar para descontaminacao, cautela para outcome clinico" | — |
| 8 | conceitual | "Protocolo Nd:YAG — fibra 200um, 1.5W, 4 pulsos/canal" | dosimetria bula |
| 9 | conceitual | "Protocolo Er:YAG — PIPS/SWEEPS, 0.3W, 20Hz" | dosimetria bula |
| 10 | demo | "Demonstracao procedural — Nd:YAG canal mesial" | — |
| 11 | comparativo | "Antes-e-depois radiografico — caso 1, 6m follow-up — TCLE assinado" | TCLE ✅ |
| 12 | disclaimer | "Fotona LightWalker — registro Anvisa {REGISTRO}, Classe III. COI: relator KOL Fotona." | Anvisa + COI ✅ |
| 13 | CTA | "Discussao + Q&A — selecao de caso, custo-beneficio, curva aprendizado" | — |
| 14 | apendice | "Papers de referencia (off-stage): 5 references completas" | — |

### Bloco Compliance & Disclaimers (3 tiers) esperado

```
🔴 Issues bloqueantes (resolver antes de apresentar):
- Registro Anvisa marcado como placeholder {REGISTRO} no slide 12 — preencher numero real antes do CIOSP

🟡 Verificar antes:
- COI Fotona — CIOSP exige declaracao escrita no inicio. Confirmar que slide 12 + verbalizacao no inicio cobrem
- Slide 8-9: dosimetria precisa estar dentro de bula Fotona LightWalker — confirmar com fabricante
- Off-label se algum parametro for fora de bula → adicionar disclaimer

✅ OK:
- TCLE mencionado (slide 11)
- GRADE explicito por outcome (slides 5, 6) — descontaminacao HIGH separada de cura sintomatica LOW
- COI Fotona declarado (slide 12)
- Anvisa Classe III referenciada (slide 12)
- Bloco evidencia tem 3 slides dedicados (5-7)
- Apendice com 5 papers (slide 14)
- Linguagem clinica adequada
```

### Assertions

- [ ] Frontmatter STORYBOARD tem `Modo: peer-facing`
- [ ] 14 slides gerados
- [ ] GRADE aparece DUAS vezes em slides distintos (slides 5, 6) — uma para cada outcome
- [ ] Apendice com 5 papers (slide 14)
- [ ] Slide tipo `comparativo` (slide 11) menciona TCLE no body
- [ ] COI Fotona em slide proprio + bloco final
- [ ] `anvisa-laser-classe-iii` tag injetada

---

## Sumario das regras validadas pelos 3 cases

| Regra | Validada por |
|-------|-------------|
| Modo peer-facing gera 10-14 slides Calgary-Cambridge | Case 1 (12), Case 3 (14) |
| Modo patient-facing gera 6-8 slides AIDET | Case 2 (7) |
| Compliance D7 SEM hard-block — STORYBOARD sai mesmo com 🔴 | Case 2 (TCLE pendente, deck gerado) |
| Antes-e-depois COM TCLE → ✅ | Cases 1, 3 |
| Antes-e-depois SEM TCLE → 🔴 BLOCKER | Case 2 |
| GRADE por outcome quando multiplos outcomes | Case 3 (HIGH vs LOW) |
| Linguagem leiga em patient-facing | Case 2 |
| Alternativas obrigatorias em patient-facing invasivo | Case 2 (4 alternativas) |
| Equipamento Fotona → registro Anvisa declarado | Cases 1, 3 |
| Auto-detect Fotona injeta tag `anvisa-laser-classe-iii` | Cases 1, 3 |
| Auto-detect Beauty Smile carrega design system | Case 2 |
| Linguagem proibida (cura/garantido/100%) substituida ou marcada | Todos (verificado por ausencia) |
