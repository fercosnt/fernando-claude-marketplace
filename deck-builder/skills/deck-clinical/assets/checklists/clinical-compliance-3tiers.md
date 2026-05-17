# Checklist: bloco Compliance & Disclaimers (3 tiers)

Decisao explicita para cada issue → mapeia para 🔴 / 🟡 / ✅. Skill executa esta checklist ANTES de fechar o STORYBOARD. Reviewer pode reclassificar depois.

> **Princípio D7:** SKIll NUNCA bloqueia geracao. Issue 🔴 = "resolver ANTES de apresentar", mas o STORYBOARD sai pronto pro humano corrigir.

---

## 🔴 BLOCKER — sempre marca, resolver antes de apresentar

Issue 🔴 = nao apresentar nesse estado. Lista canonica:

| # | Issue | Detector (como a skill identifica) | Resolucao citavel |
|---|-------|----------------------------------|-------------------|
| 1 | Linguagem proibida nao removivel | C1/U1/U5 contem "cura", "garantido", "100%", "reverte completamente", "sem dor" (procedimento invasivo), "sem riscos", "tecnica exclusiva" — E substituicao traria a Big Idea | CFO 196/2019 art. 14, II e III; CFM 1974/2011 art. 3 |
| 2 | Antes-e-depois SEM TCLE | C5 = "sim sem TCLE" OU "nao mencionado" | CFO 196/2019 art. 18, II, "g"; CFM 1974/2011 art. 13 |
| 3 | Promessa resultado especifico sem disclaimer | Slide outcome quantificado sem "individual variation" mencionado em algum lugar | CFO 196/2019 art. 18, II, "k" |
| 4 | Equipamento Classe III sem registro Anvisa | Auto-detect Fotona/Er:YAG/Nd:YAG/laser ATIVO + slide compliance NAO menciona registro | Anvisa RDC 185/2001 + RDC 751/2022 |
| 5 | Patient-facing invasivo SEM alternativas | Modo = patient + C1 contem "implante", "cirurgia", "extracao", "ortognatica" + slide tipo `comparativo` ausente OU sem opcao "nao fazer nada" | Consentimento informado (CDC + CFO 196 art. 8) |
| 6 | Promessa cura/garantia/100% no body de slide | Grep no STORYBOARD final | CFO 196/2019 art. 14 |
| 7 | Off-label em patient-facing sem disclaimer | Modo = patient + C3 indica uso fora bula + slide sem mencao "uso fora da indicacao oficial" | RDC Anvisa + responsabilidade profissional |
| 8 | Registro Anvisa marcado como placeholder pendente | `{REGISTRO_ANVISA_FOTONA}` ou similar nao substituido | (precisa numero real) |

**Formato no bloco final:**
```
🔴 Issues bloqueantes (resolver antes de apresentar):
- {issue descrita objetivamente} → {resolucao citada}. Solucao: {acao concreta}.
```

Exemplo real (Case 2):
```
🔴 Issues bloqueantes (resolver antes de apresentar):
- TCLE pendente para antes-e-depois do caso de referencia → CFO Res. 196/2019, art. 18, II, "g". Solucao: (a) obter TCLE assinado do paciente do caso, OU (b) remover antes-e-depois e usar esquema anatomico generico.
```

---

## 🟡 VERIFICAR — revisar antes de apresentar

Issue 🟡 = nao bloqueia, mas humano precisa confirmar. Lista canonica:

| # | Issue | Detector | Acao humana |
|---|-------|----------|------------|
| 1 | COI Fotona presente mas graduacao nao clara | Auto-detect Fotona + relator nao especifica "consultor/KOL/cortesia/sem patrocinio" | Especificar tipo de relacao |
| 2 | Sem GRADE em slide evidencia (modo peer) | Modo = peer + C3 informado + slide tipo `dados` sem string "GRADE" | Adicionar GRADE por outcome |
| 3 | Off-label sem disclaimer explicito (peer) | Modo = peer + C3 fora bula + body do slide sem mencao "uso off-label" | Adicionar disclaimer body |
| 4 | Sem disclaimer "individual variation" pos-outcome | Slide outcome especifico (delta SGU, taxa sucesso, etc.) + body sem mencao | Adicionar 1 linha disclaimer |
| 5 | Jargao restante em patient-facing | Modo = patient + grep no STORYBOARD encontra: osseointegracao, carga imediata, hipersensibilidade, periodontite, etc. | Revisar slide por slide e substituir |
| 6 | Tempos procedimento/recuperacao nao validados | Modo = patient + slide Duration com valores nao confirmados pelo cirurgiao | Confirmar com responsavel clinico |
| 7 | Auto-referencia ambigua ("pioneiro", "expert") | Grep encontra "pioneiro", "expert", "unico" sem titulacao formal documentada | Remover ou documentar titulacao |
| 8 | Citacao paper sem journal | Mencao a paper sem formato "Autor, ano, journal" | Completar citacao |
| 9 | Follow-up ausente (peer) | Modo = peer + sem slide outcome ≥6m | Adicionar OU declarar "follow-up em andamento" |
| 10 | Dosimetria nao alinhada com bula | Equipamento detectado + parametros fora do recomendado pela bula | Confirmar com fabricante + declarar off-label se aplicavel |

**Formato no bloco final:**
```
🟡 Verificar antes:
- {issue} — {acao humana sugerida}
```

---

## ✅ OK — confirmacoes do que esta correto

Lista canonica de checks que passaram:

| # | Check | Quando marcar |
|---|-------|--------------|
| 1 | TCLE mencionado | C5 = "sim com TCLE" + slide `comparativo` body contem mencao TCLE |
| 2 | GRADE citado por outcome | Modo = peer + slide(s) `dados` contem GRADE com nivel por outcome |
| 3 | COI declarado | Slide compliance contem declaracao COI explicita |
| 4 | Anvisa Classe N referenciada | Slide compliance cita "Classe N" + numero registro (ou placeholder marcado pra preencher) |
| 5 | AIDET aplicado (patient) | Modo = patient + slides 2/3-4/5/7 mapeam A+I/E/D/T |
| 6 | Alternativas mostradas | Modo = patient + slide `comparativo` lista ≥2 opcoes + "nao fazer nada" se invasivo |
| 7 | Linguagem leiga em titulos (patient) | Modo = patient + grep titulos sem jargao tecnico |
| 8 | Sem promessa cura/garantia detectada | Grep no STORYBOARD nao encontra linguagem proibida |
| 9 | Bloco evidencia presente (peer) | Modo = peer + ≥1 slide tipo `dados` dedicado a evidencia |
| 10 | Follow-up apresentado (peer) | Modo = peer + slide outcome ≥6m presente |
| 11 | Apendice com papers (peer) | Modo = peer + slide tipo `apendice` com refs |
| 12 | Auto-detect equipamento OK | Tag `anvisa-laser-classe-iii` injetada quando aplicavel |
| 13 | Design system carregado | Auto-detect marca + skill design system disponivel |

**Formato no bloco final:**
```
✅ OK:
- {check confirmado de forma curta}
```

---

## Ordem de execucao pela skill

1. Carregar todos os inputs (U1-U6, C1-C5) + outputs (STORYBOARD gerado)
2. Rodar grep de linguagem proibida → preencher 🔴 #1 e #6
3. Verificar C5 → preencher 🔴 #2 OU ✅ #1
4. Verificar auto-detect equipamento → preencher 🔴 #4 OU ✅ #4
5. Verificar modo + C1 invasivo + slide alternativas → preencher 🔴 #5 OU ✅ #6
6. Verificar GRADE em slides dados (peer) → preencher 🟡 #2 OU ✅ #2
7. Verificar AIDET (patient) → preencher ✅ #5
8. Verificar jargao restante (patient) → preencher 🟡 #5 OU ✅ #7
9. Verificar follow-up (peer) → preencher 🟡 #9 OU ✅ #10
10. Verificar COI → preencher 🟡 #1 OU ✅ #3
11. Verificar off-label disclaimer → preencher 🟡 #3 OU 🔴 #7 (patient)
12. Listar restantes ✅ aplicaveis
13. Gravar bloco final no STORYBOARD entre tags `## Compliance & Disclaimers (3 tiers — D7)` e fim do documento

**Regra dura:** cada tier deve ter pelo menos 1 linha (mesmo que seja "(nenhum)" em 🔴 quando tudo OK). Bloco vazio = STORYBOARD invalido.
