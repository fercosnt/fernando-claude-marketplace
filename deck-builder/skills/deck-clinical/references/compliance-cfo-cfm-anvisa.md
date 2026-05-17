# Compliance regulatorio — CFO + CFM + Anvisa

Referencia das resolucoes citaveis no bloco final do STORYBOARD. Carregado quando a skill precisa fundamentar um tier 🔴/🟡.

> Skill nao substitui parecer juridico. Cita resolucoes como base regulatoria; profissional/clinica e responsavel pela conformidade final.

---

## CFO — Conselho Federal de Odontologia

### Resolucao CFO 196/2019 — Codigo de Etica Odontologica

Atualiza Resolucao CFO 118/2012. Pontos diretamente relevantes para apresentacoes clinicas:

| Artigo | Conteudo (resumo) | Aplicacao em deck |
|--------|------------------|------------------|
| Art. 14, II e III | Vedacao de garantir resultado ou prometer cura | Linguagem proibida "cura" / "garantido" / "100%" — 🔴 BLOCKER |
| Art. 18, II, "g" | Vedacao de divulgar antes-e-depois sem TCLE escrito do paciente, com finalidade exclusivamente cientifica/educativa | 🔴 BLOCKER se C5 = "sim sem TCLE" |
| Art. 18, II, "h" | Vedacao de divulgar foto/imagem com finalidade promocional | TCLE precisa ser ESPECIFICO pro uso (didatico ≠ promocional) |
| Art. 18, II, "k" | Vedacao de promessa de resultado ou conceito sensacionalista | "Reverte completamente" / "transforma" → 🔴 |
| Art. 18, IV | Publicidade deve incluir nome + numero CRO do responsavel tecnico | Slide capa ou rodape deve ter |
| Art. 22 | Sigilo profissional — proteger identidade paciente | Rosto identificavel em antes-e-depois sem TCLE ESPECIFICO → 🔴 |

**Citacao curta no bloco compliance:** "CFO Res. 196/2019, art. 18, II, 'g' — TCLE escrito obrigatorio para uso de antes-e-depois."

---

## CFM — Conselho Federal de Medicina

### Resolucao CFM 1974/2011 (alterada pela 2336/2023)

Norma a publicidade medica. Aplicavel a apresentacoes que envolvam diagnostico/tratamento medico (cirurgias bucomaxilo com integracao medica, sedacao, anestesia geral, ortognatica).

| Artigo | Conteudo (resumo) | Aplicacao em deck |
|--------|------------------|------------------|
| Art. 3 | Vedacao de garantir resultado, anunciar tecnica "exclusiva", prometer cura | Mesmas regras CFO — 🔴 BLOCKER |
| Art. 13 | Antes-e-depois proibido com finalidade promocional. Permitido com finalidade educativa/cientifica + TCLE + sem identificacao | Antes-e-depois sempre crop boca/area + TCLE mencionado |
| Art. 14 | Divulgacao de equipamentos exige citacao do registro Anvisa | Equipamento Fotona/Er:YAG/Nd:YAG → declarar registro Anvisa |
| Art. 15 | Auto-referencia como "expert" / "especialista mundial" / "unico" proibida sem titulacao formal | "Pioneiro em laser dental" sem titulacao = 🟡 verificar |

**Citacao curta no bloco compliance:** "CFM Res. 1974/2011 (alt. 2336/2023), art. 13 — antes-e-depois com finalidade educativa exige TCLE e veda identificacao."

---

## Anvisa — Agencia Nacional de Vigilancia Sanitaria

### RDC 185/2001 + RDC 751/2022 (classificacao de equipamentos medicos)

Define classes I-IV por risco. Equipamentos relevantes:

| Equipamento | Classe Anvisa | Implicacao em deck |
|-------------|--------------|--------------------|
| Fotona LightWalker (Er:YAG 2940nm + Nd:YAG 1064nm) | **Classe III** (alto risco) | Mencionar = declarar registro Anvisa + dosimetria conforme bula |
| Lasers de baixa potencia (LLLT terapeutico) | Classe II | Declarar registro |
| Equipamentos cirurgicos ativos (eletrocauterio, ultrassonico) | Classe II/III | Variavel — verificar bula |

**Regra deck-clinical:** equipamento Classe III mencionado SEM declaracao de registro Anvisa = 🔴 BLOCKER. Bloco final precisa conter linha tipo:

> "Fotona LightWalker — registro Anvisa nº XXXXXXX, classe III. Uso conforme bula."

(Numero real do registro deve ser fornecido pelo profissional/clinica; a skill marca como `{REGISTRO_ANVISA_FOTONA}` placeholder se nao fornecido.)

### Bula e uso off-label

- Uso de laser para indicacao NAO listada na bula = off-label.
- Off-label NAO e proibido — mas precisa estar explicito no slide compliance + body do slide do protocolo.
- Em deck peer-facing: 🟡 verificar quando aplica.
- Em deck patient-facing: 🔴 BLOCKER se off-label nao for explicado ao paciente.

---

## Conflito de Interesse (COI)

Padrao academico/regulatorio: declarar relacao financeira/institucional com fabricante/patrocinador.

| Cenario | Tratamento no deck |
|---------|-------------------|
| Apresentacao patrocinada pela Fotona | Slide compliance: "COI: apresentacao apoiada pela Fotona — relator e KOL/consultor da marca" — 🔴 se ausente em peer |
| Equipamento da clinica do palestrante (sem patrocinio) | Slide compliance: "Equipamento utilizado e da pratica clinica do relator. Sem patrocinio externo." — 🟡 |
| Sem relacao financeira | "Sem conflito de interesse a declarar." — ✅ |

---

## Linguagem proibida (tabela canonica — espelha SKILL.md)

A skill substitui automaticamente OU marca 🔴 quando intencao seria traida pela substituicao:

| Termo proibido | Substituir por | Resolucao |
|----------------|---------------|-----------|
| "Cura" / "curar" | "tratamento", "manejo", "resolucao clinica" | CFO 196/2019 art. 14, II; CFM 1974/2011 art. 3 |
| "Garantido" / "garantia" | "tipicamente", "na maioria dos casos" | CFO 196/2019 art. 14, III; CFM 1974/2011 art. 3 |
| "100%" / "100 por cento" | "documentado em N% dos casos (literatura)" | CFO 196/2019 art. 18, II, "k" |
| "Reverte completamente" | "melhora documentada em..." | CFO 196/2019 art. 18, II, "k" |
| "Sem dor" (procedimento invasivo) | "anestesia local minimiza desconforto" | Desinformacao clinica |
| "Sem riscos" / "totalmente seguro" | "riscos minimizados conforme protocolo" | Viola consentimento informado |
| "Tecnica exclusiva" / "unico no Brasil" | omitir ou "tecnica usada por X grupos no mundo" | CFM 1974/2011 art. 15 |
| "Resultado imediato" (sem prazo definido em literatura) | "resultados visiveis em [X] sessoes/semanas conforme literatura" | Promessa inverificavel |

---

## Checklist rapido pra preencher bloco compliance

1. **Linguagem proibida** → grep nas substituicoes acima. Algum termo restante? → 🔴 ou 🟡.
2. **Antes-e-depois mencionado?** SIM → TCLE explicito mencionado? NAO → 🔴.
3. **Equipamento Classe III citado?** SIM → registro Anvisa declarado? NAO → 🔴.
4. **COI relevante (Fotona patrocinador)?** SIM → slide proprio? NAO → 🔴 (peer) / 🟡 (patient).
5. **Off-label?** SIM → disclaimer? NAO → 🟡 (peer) / 🔴 (patient).
6. **Modo patient + procedimento invasivo?** → slide alternativas presente? NAO → 🔴 (viola consentimento informado).
7. **Modo patient + jargao restante?** → 🟡 verificar slide-a-slide.
8. **Disclaimer "individual variation" em slide pos-procedimento?** SIM → ✅. NAO + outcome especifico prometido → 🟡.
