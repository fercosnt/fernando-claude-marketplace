# Modos de Entrada — Detalhamento

> Referencia detalhada para os modos de coleta de contexto do PRD.

---

## Modo A: Entrevista Guiada

Maximo 5 perguntas. Numerar com opcoes em letras (A/B/C/D) para resposta rapida ("1A, 2C, 3B"). Pare quando clareza >= 80%.

**ESSENCIAIS** (sempre perguntar):

1. **Problema**: "Qual problema especifico voce quer resolver? Quem sofre com ele hoje?"
   - A) Tenho o problema claro e evidencia
   - B) Tenho uma ideia mas preciso refinar o problema
   - C) Tenho uma solucao em mente, preciso extrair o problema

2. **Escopo**: "O que deve estar DENTRO e FORA do v1?"
   - A) Ja tenho escopo definido (descreva)
   - B) Preciso de ajuda para delimitar
   - C) Quero MVP minimo possivel
   - D) Quero produto completo

**IMPORTANTES** (se complexidade >= Standard):

3. **Usuarios**: "Quem sao os usuarios e quais roles/permissoes?"
   - A) Um tipo de usuario apenas
   - B) Multiplos roles (descreva)
   - C) Multi-tenant com isolamento de dados

4. **Tecnico**: "Stack ja definida ou restricoes tecnicas?"
   - A) Stack livre
   - B) Stack definida no CLAUDE.md (usar detectada)
   - C) Precisa integrar com sistema externo (descreva)

**OPCIONAIS** (se complexidade = Comprehensive):

5. **Timeline/Metricas**: "Prazo e como medir sucesso?"
   - A) Tenho metricas e prazos
   - B) Preciso de ajuda para definir
   - C) Sem prazo rigido, qualidade > velocidade

**Estrategia:** processar respostas e decidir se precisa de mais perguntas. Se usuario forneceu descricao rica, pular perguntas ja respondidas.

---

## Modo B: Context Dump

O usuario cola todo o contexto disponivel (briefing, notas, docs, mensagens). A skill analisa e pergunta APENAS sobre gaps.

**Fluxo:**

1. Receber material do usuario (texto colado, links, arquivos referenciados)
2. Usar thinking cuidadoso para categorizar: o que foi fornecido vs o que falta
3. Apresentar analise de gaps no formato abaixo
4. Fazer perguntas APENAS sobre gaps (pode ser 0 a N perguntas)
5. Prosseguir para construcao do PRD

**Formato de apresentacao da analise de gaps:**

```markdown
## Analise do Material Fornecido

| Aspecto | Status | Detalhe |
|---------|--------|---------|
| Problema | Coberto / Gap | [resumo do que foi detectado ou o que falta] |
| Personas/Usuarios | Coberto / Gap | [resumo] |
| Escopo v1 | Coberto / Gap | [resumo] |
| Fora do Escopo | Coberto / Gap | [resumo] |
| Metricas de sucesso | Coberto / Gap | [resumo] |
| Stack/Tecnico | Coberto / Gap | [resumo] |
| Riscos | Coberto / Gap | [resumo] |

[Se 0 gaps: "Material completo! Vou gerar o PRD diretamente."]
[Se N gaps: "Preciso de mais informacao sobre os gaps acima:" + perguntas focadas]
```

**Importante**: NAO e modo cego. A skill deve analisar profundamente o material antes de prosseguir. Se tudo estiver coberto, gerar o PRD sem perguntas adicionais.

---

## Modo C: Best Guess

A skill gera o PRD completo fazendo suposicoes razoaveis para tudo que falta. O usuario valida depois.

**Fluxo:**

1. Analisar todo contexto disponivel (docs do projeto, material fornecido, CLAUDE.md, codebase)
2. Gerar PRD completo fazendo suposicoes razoaveis para tudo que falta
3. Marcar CADA suposicao feita com tag `[ASSUMIDO]` inline no PRD
4. Ao final, apresentar lista consolidada de todas as suposicoes para validacao rapida
5. Usuario confirma, corrige ou rejeita suposicoes
6. Skill ajusta o PRD conforme feedback

**Formato da lista de suposicoes (ao final do PRD):**

```markdown
## Suposicoes Feitas

Marquei X suposicoes no PRD com [ASSUMIDO]. Revise e corrija:

1. [ASSUMIDO] Metrica primaria: reducao de tempo de processo manual (correto? qual metrica?)
2. [ASSUMIDO] Apenas 2 roles: admin e usuario (ha outros?)
3. [ASSUMIDO] Sem integracao externa no v1 (precisa integrar com algo?)
...

Responda com numeros e correcoes: "1: correto, 2: tem tambem role parceiro, 3: precisa integrar com Stripe"
```

**Regra**: Suposicoes devem ser razoaveis e baseadas em evidencia do contexto disponivel. NAO inventar dados quantitativos — marcar como `[ASSUMIDO][TBD]` quando nao ha base para estimar.

---

## Modo D: From Brief

Quando existe `BRIEF/BRIEF.md` (produzido pela skill `idea-to-brief`), este modo e auto-detectado. O brief ja contem pesquisa, frameworks e recomendacao — o PRD herda e aprofunda.

**Fluxo:**

1. Ler `BRIEF/BRIEF.md` integralmente
2. Usar thinking cuidadoso para mapear sections do brief ao PRD (ver tabela de handoff abaixo)
3. Apresentar analise de cobertura + gaps restantes
4. Fazer perguntas APENAS sobre gaps (tipicamente: detalhe tecnico, metricas quantitativas, criterios de aceite)
5. Gerar PRD com rastreabilidade ao brief (marcar `[DO BRIEF]` nas secoes herdadas)

**Mapa de Handoff — BRIEF.md → PRD:**

| Secao do BRIEF | Secao do PRD | Acao |
|----------------|-------------|------|
| Problema (MITRE) | Problema & Contexto | Herdar e aprofundar com evidencia adicional |
| Oportunidades (OST) | Escopo (v1/v2/out) | Mapear oportunidades → features; priorizar com MoSCoW |
| Suposicoes (Lean UX) | Riscos & Mitigacoes | Converter suposicoes em riscos formais |
| Pesquisa de mercado | Problema & Contexto (evidencia) | Usar como evidencia/citacao |
| Analise de plataformas | Consideracoes Tecnicas | Herdar constraints e stack recommendation |
| Abordagem recomendada | Requisitos Funcionais | Detalhar em user stories com criterio de aceite |
| Riscos do brief | Riscos & Mitigacoes + Questoes em Aberto | Manter e expandir |

**Regra**: Quando no modo From Brief, a entrevista guiada e DESNECESSARIA — o brief ja fez esse trabalho. Perguntar apenas sobre gaps especificos (tipicamente detalhe tecnico e metricas).

---

## Deteccao Automatica de Modo

| Sinal | Modo sugerido |
|-------|---------------|
| `BRIEF/BRIEF.md` existe no projeto | **D) From Brief** |
| Usuario colou texto extenso ou referenciou docs | **B) Context Dump** |
| "faz o PRD com best guess", "chuta" | **C) Best Guess** |
| "faz o PRD completo" sem material | **A) Guiado** |
| Material insuficiente para detectar | Perguntar qual modo |
