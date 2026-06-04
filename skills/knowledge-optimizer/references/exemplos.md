# Exemplos Completos: Input → Output

**Updated:** 2026-02-19 | **Modes covered:** All 4 + Transcription Cleaning + Edge Cases

---

## Table of Contents

1. [Exemplo 1: Transcription Cleaning (Before/After)](#exemplo-1)
2. [Exemplo 2: RAG Standard (Input → JSON)](#exemplo-2)
3. [Exemplo 3: N8N Agent Knowledge (Input → JSON)](#exemplo-3)
4. [Exemplo 4: Claude Project (Input → XML+Markdown)](#exemplo-4)
5. [Exemplo 5: Hybrid Output (RAG + Claude combined)](#exemplo-5)
6. [Exemplo 6: Edge Case — Mixed Language Input (PT + EN)](#exemplo-6)
7. [Contra-Exemplo: Output Ruim vs Output Bom](#contra-exemplo)
8. [Validation Report Template](#validation-report-template)
9. [Output Metadata Schema](#output-metadata-schema)
10. [Metricas de Referencia](#metricas-de-referencia)

---

## Exemplo 1: Transcription Cleaning (Before/After)

### Input (transcricao bruta)

```
Então, hoje a gente vai falar sobre, né, os procedimentos de limpeza dental, tá? Tipo, é muito importante que o paciente entenda que, assim, a escovação correta ela tem que ser feita, né, pelo menos três vezes ao dia. Então é isso, basicamente.

Bom, passando para o próximo tópico... A gente tem que falar sobre o fio dental, né? Então, o fio dental ele é, tipo, essencial para remover, é... a placa bacteriana que fica entre os dentes, sabe? Muita gente não usa, mas é super importante, tá?

Voltando ao tema da escovação, é... a escova tem que ser trocada a cada três meses, basicamente. Então é isso que a gente recomenda, né, para manter a saúde bucal em dia.
```

### Output (cleaning moderado)

```
## Procedimentos de Limpeza Dental

### Escovacao Correta
A escovacao correta deve ser feita pelo menos tres vezes ao dia. E muito importante que o paciente entenda essa frequencia para manter a saude bucal.

### Uso do Fio Dental
O fio dental e essencial para remover a placa bacteriana que fica entre os dentes. Apesar de muitas pessoas nao utilizarem, e um complemento fundamental da higiene bucal.

### Troca de Escova
A escova deve ser trocada a cada tres meses para manter a eficacia da limpeza e a saude bucal em dia.
```

**Por que e bom:** Removeu fillers (entao, ne, tipo, assim, basicamente) mantendo 100% do conteudo. Reestruturou por topicos (eram 3 paragrafos misturados, agora 3 secoes claras). Detectou retorno ao tema da escovacao e agrupou corretamente. Reducao de ~40% no tamanho sem perda de informacao.

---

## Exemplo 2: RAG Standard (Input → JSON)

### Input (documento tecnico)

```
# Clareamento Dental

O clareamento dental e um procedimento estetico que pode ser realizado em consultorio ou em casa, sob supervisao do dentista.

## Tipos de Clareamento

### Clareamento a Laser
Realizado em consultorio, utiliza gel de peroxido de hidrogenio em concentracoes de 35-40%. O procedimento dura aproximadamente 1 hora por sessao, com resultados visiveis em 1-3 sessoes.

### Clareamento Caseiro
Utiliza moldeiras personalizadas com gel de peroxido de carbamida (10-22%). O tratamento dura 2-4 semanas com uso diario de 2-4 horas.

## Contraindicacoes
- Gestantes e lactantes
- Menores de 16 anos
- Pacientes com sensibilidade dental severa
- Restauracoes extensas nos dentes anteriores
```

### Output (RAG Standard JSON)

```json
{
  "document_id": "doc_clareamento_001",
  "source": "manual_procedimentos_esteticos",
  "created_at": "2025-02-18",
  "mode": "rag_standard",
  "total_chunks": 3,
  "chunks": [
    {
      "id": "doc_clareamento_001_chunk_000",
      "content": "Clareamento Dental — Visao Geral: O clareamento dental e um procedimento estetico que pode ser realizado em consultorio ou em casa, sob supervisao do dentista. Existem dois tipos principais: clareamento a laser (em consultorio) e clareamento caseiro (com moldeiras).",
      "token_count": 52,
      "metadata": {
        "section": "Clareamento Dental - Visao Geral",
        "keywords": ["clareamento dental", "procedimento estetico", "consultorio", "caseiro"],
        "content_type": "procedural",
        "confidence_score": 0.95,
        "chunk_index": 0
      }
    },
    {
      "id": "doc_clareamento_001_chunk_001",
      "content": "Tipos de Clareamento: Clareamento a Laser — Realizado em consultorio, utiliza gel de peroxido de hidrogenio em concentracoes de 35-40%. O procedimento dura aproximadamente 1 hora por sessao, com resultados visiveis em 1-3 sessoes. Clareamento Caseiro — Utiliza moldeiras personalizadas com gel de peroxido de carbamida (10-22%). O tratamento dura 2-4 semanas com uso diario de 2-4 horas.",
      "token_count": 89,
      "metadata": {
        "section": "Tipos de Clareamento",
        "keywords": ["clareamento a laser", "clareamento caseiro", "peroxido de hidrogenio", "peroxido de carbamida", "moldeiras"],
        "content_type": "procedural",
        "confidence_score": 0.93,
        "chunk_index": 1,
        "related_chunks": ["doc_clareamento_001_chunk_000", "doc_clareamento_001_chunk_002"]
      }
    },
    {
      "id": "doc_clareamento_001_chunk_002",
      "content": "Contraindicacoes do clareamento dental: gestantes e lactantes, menores de 16 anos, pacientes com sensibilidade dental severa, restauracoes extensas nos dentes anteriores. Estas condicoes devem ser avaliadas antes de iniciar qualquer procedimento de clareamento.",
      "token_count": 51,
      "metadata": {
        "section": "Contraindicacoes",
        "keywords": ["contraindicacoes", "gestantes", "sensibilidade dental", "restauracoes"],
        "content_type": "FAQ",
        "confidence_score": 0.96,
        "chunk_index": 2
      }
    }
  ]
}
```

**Por que e bom:** Cada chunk e auto-contido (compreensivel sem os outros). Chunk 0 adiciona contexto resumido (tecnica Anthropic contextual embeddings). Metadata inclui keywords relevantes para busca semantica e por palavra-chave. Related_chunks linkam chunks semanticamente proximos. Content_type classifica para filtragem. Confidence score alto porque o conteudo original era bem estruturado.

---

## Exemplo 3: N8N Agent Knowledge (Input → JSON)

### Input (FAQ de atendimento)

```
Pergunta: Quanto custa uma consulta de avaliacao?
A consulta de avaliacao tem valor de R$ 150,00. Esse valor pode ser abatido do tratamento caso o paciente inicie o procedimento em ate 30 dias.

Pergunta: Quais formas de pagamento voces aceitam?
Aceitamos cartao de credito (ate 12x), debito, PIX e boleto bancario. Para tratamentos acima de R$ 5.000, oferecemos condicoes especiais de parcelamento.
```

### Output (N8N Agent JSON)

```json
{
  "format": "n8n_agent",
  "document_id": "faq_atendimento_001",
  "knowledge_type": "FAQ",
  "created_at": "2025-02-18",
  "entries": [
    {
      "id": "faq_001",
      "question": "Quanto custa uma consulta de avaliacao?",
      "answer": "A consulta de avaliacao tem valor de R$ 150,00. Esse valor pode ser abatido do tratamento caso o paciente inicie o procedimento em ate 30 dias.",
      "keywords": ["preco", "valor", "consulta", "avaliacao", "custo"],
      "intent": "pricing_inquiry",
      "follow_up_actions": ["agendar_consulta", "informar_formas_pagamento"]
    },
    {
      "id": "faq_002",
      "question": "Quais formas de pagamento voces aceitam?",
      "answer": "Aceitamos cartao de credito (ate 12x), debito, PIX e boleto bancario. Para tratamentos acima de R$ 5.000, oferecemos condicoes especiais de parcelamento.",
      "keywords": ["pagamento", "cartao", "parcelamento", "PIX", "boleto"],
      "intent": "payment_methods",
      "follow_up_actions": ["calcular_parcelamento", "enviar_link_pagamento"]
    }
  ]
}
```

**Por que e bom:** Formato Q&A direto para agentes conversacionais. Intent classifica o tipo de pergunta para roteamento. Follow_up_actions sugere proximas acoes do agente. Keywords cobrem sinonimos que usuarios reais usariam (ex: "preco", "valor", "custo" para a mesma pergunta).

---

## Exemplo 4: Claude Project (Input → XML+Markdown)

### Input (manual de procedimento)

```
# Protocolo de Atendimento Inicial

O atendimento inicial segue um protocolo padrao para garantir qualidade e consistencia.

## Recepcao do Paciente
Ao chegar na clinica, o paciente deve ser recebido pela recepcionista que verifica os dados cadastrais e confirma o agendamento. Se for a primeira visita, solicitar preenchimento da ficha de anamnese.

## Anamnese
A ficha de anamnese coleta historico medico, alergias, medicamentos em uso e queixa principal. O dentista deve revisar a ficha antes da consulta.

## Exame Clinico
O exame clinico inclui inspecao visual, sondagem periodontal e radiografia panoramica quando indicada.
```

### Output (Claude Project XML+Markdown)

```xml
<document id="protocolo_atendimento_001" title="Protocolo de Atendimento Inicial" version="1.0">

<section level="1" id="overview">
# Protocolo de Atendimento Inicial
<context>Protocolo padrao para atendimento inicial de pacientes, cobrindo recepcao, anamnese e exame clinico. Aplicavel a todas as unidades.</context>

O atendimento inicial segue um protocolo padrao para garantir qualidade e consistencia.
</section>

<section level="2" id="recepcao">
## Recepcao do Paciente
<context>Primeiro contato do paciente com a clinica. Etapa critica para experiencia do paciente.</context>

Ao chegar na clinica, o paciente deve ser recebido pela recepcionista que verifica os dados cadastrais e confirma o agendamento. Se for a primeira visita, solicitar preenchimento da ficha de anamnese.

<cross-reference target="anamnese">A ficha de anamnese e detalhada na secao seguinte.</cross-reference>
</section>

<section level="2" id="anamnese">
## Anamnese
<context>Coleta de dados medicos do paciente. Obrigatorio antes de qualquer procedimento.</context>

A ficha de anamnese coleta historico medico, alergias, medicamentos em uso e queixa principal. O dentista deve revisar a ficha antes da consulta.
</section>

<section level="2" id="exame-clinico">
## Exame Clinico
<context>Avaliacao clinica que determina o plano de tratamento.</context>

O exame clinico inclui inspecao visual, sondagem periodontal e radiografia panoramica quando indicada.
</section>

</document>
```

**Por que e bom:** Hierarquia preservada com `<section level>`. Cada secao tem `<context>` que ajuda o Claude a entender o proposito antes de ler o conteudo. `<cross-reference>` conecta secoes relacionadas. IDs semanticos (nao numericos) facilitam referencia. Markdown preservado dentro do XML para legibilidade humana.

---

## Exemplo 5: Hybrid Output (RAG + Claude combined)

### Input (mesmo do Exemplo 4)

O mesmo protocolo de atendimento do Exemplo 4.

### Output — Arquivo 1: `protocolo_atendimento_claude.md`

Identico ao output do Exemplo 4 (formato Claude Project com XML tags).

### Output — Arquivo 2: `protocolo_atendimento_rag.json`

```json
{
  "document_id": "protocolo_atendimento_001",
  "source": "protocolo_atendimento_claude.md",
  "mode": "hybrid",
  "linked_document": "protocolo_atendimento_claude.md",
  "created_at": "2025-02-18",
  "total_chunks": 3,
  "chunks": [
    {
      "id": "protocolo_atendimento_001_chunk_000",
      "content": "Protocolo de Atendimento Inicial — Recepcao do Paciente: Ao chegar na clinica, o paciente deve ser recebido pela recepcionista que verifica os dados cadastrais e confirma o agendamento. Se for a primeira visita, solicitar preenchimento da ficha de anamnese.",
      "token_count": 55,
      "metadata": {
        "section": "Recepcao do Paciente",
        "keywords": ["recepcao", "paciente", "agendamento", "cadastro", "anamnese"],
        "content_type": "procedural",
        "confidence_score": 0.94,
        "chunk_index": 0,
        "claude_section_id": "recepcao"
      }
    },
    {
      "id": "protocolo_atendimento_001_chunk_001",
      "content": "Anamnese — Coleta de dados medicos: A ficha de anamnese coleta historico medico, alergias, medicamentos em uso e queixa principal. O dentista deve revisar a ficha antes da consulta. Dados obrigatorios antes de qualquer procedimento.",
      "token_count": 48,
      "metadata": {
        "section": "Anamnese",
        "keywords": ["anamnese", "historico medico", "alergias", "medicamentos", "ficha"],
        "content_type": "procedural",
        "confidence_score": 0.93,
        "chunk_index": 1,
        "claude_section_id": "anamnese",
        "related_chunks": ["protocolo_atendimento_001_chunk_000"]
      }
    },
    {
      "id": "protocolo_atendimento_001_chunk_002",
      "content": "Exame Clinico — Avaliacao que determina plano de tratamento: O exame clinico inclui inspecao visual, sondagem periodontal e radiografia panoramica quando indicada.",
      "token_count": 32,
      "metadata": {
        "section": "Exame Clinico",
        "keywords": ["exame clinico", "sondagem periodontal", "radiografia", "inspecao"],
        "content_type": "procedural",
        "confidence_score": 0.92,
        "chunk_index": 2,
        "claude_section_id": "exame-clinico"
      }
    }
  ]
}
```

**Por que e bom:** Ambos os arquivos compartilham `document_id`. O JSON inclui `claude_section_id` que mapeia cada chunk para a secao correspondente no Claude Project. `linked_document` conecta o RAG ao arquivo Claude. Isso permite: humanos navegam pelo Claude Project, automacao busca pelo RAG, e ambos referenciam o mesmo conteudo.

---

## Exemplo 6: Edge Case — Mixed Language Input (PT + EN)

### Input (documento bilingue)

```
## Dental Whitening Procedures

O clareamento dental pode ser feito de duas formas:

### In-Office Whitening
Uses hydrogen peroxide gel at 35-40% concentration. Each session takes approximately 1 hour.

### Clareamento Caseiro
Utiliza moldeiras personalizadas com gel de peroxido de carbamida (10-22%). Tratamento de 2-4 semanas.

Important: Always check for contraindications before proceeding.
Importante: Sempre verificar contraindicacoes antes de prosseguir.
```

### Output (RAG Standard — separated by language)

```json
{
  "document_id": "doc_whitening_bilingual_001",
  "source": "dental_whitening_procedures",
  "created_at": "2025-02-18",
  "mode": "rag_standard",
  "total_chunks": 4,
  "note": "Content separated by language for embedding quality. Original was bilingual.",
  "chunks": [
    {
      "id": "doc_whitening_bilingual_001_chunk_000",
      "content": "Dental Whitening Procedures — In-Office Whitening: Uses hydrogen peroxide gel at 35-40% concentration. Each session takes approximately 1 hour. Important: Always check for contraindications before proceeding.",
      "token_count": 38,
      "metadata": {
        "section": "In-Office Whitening",
        "keywords": ["dental whitening", "hydrogen peroxide", "in-office", "contraindications"],
        "content_type": "procedural",
        "language": "en",
        "confidence_score": 0.91,
        "chunk_index": 0
      }
    },
    {
      "id": "doc_whitening_bilingual_001_chunk_001",
      "content": "Procedimentos de Clareamento Dental — Clareamento Caseiro: Utiliza moldeiras personalizadas com gel de peroxido de carbamida (10-22%). Tratamento de 2-4 semanas. Importante: Sempre verificar contraindicacoes antes de prosseguir.",
      "token_count": 42,
      "metadata": {
        "section": "Clareamento Caseiro",
        "keywords": ["clareamento dental", "peroxido de carbamida", "moldeiras", "contraindicacoes"],
        "content_type": "procedural",
        "language": "pt-br",
        "confidence_score": 0.89,
        "chunk_index": 1
      }
    }
  ]
}
```

**Por que e bom:** Separou conteudo por idioma — cada chunk e monolingual, preservando qualidade de embeddings. Campo `language` na metadata permite filtragem por idioma na busca. `note` documenta que o original era bilingue. Confidence score ligeiramente menor (0.89) reflete a complexidade da separacao — transparente para o usuario.

---

## Contra-Exemplo: Output Ruim vs Output Bom

### Input

```
O tratamento ortodontico dura em media 18 a 24 meses. O paciente deve comparecer mensalmente para ajustes. E importante manter a higiene oral impecavel durante o tratamento para evitar caries e problemas gengivais.
```

### Output RUIM (o que NAO fazer)

```json
{
  "chunks": [
    {
      "content": "O tratamento ortodontico dura em media 18 a 24 meses. O paciente deve com",
      "metadata": {}
    },
    {
      "content": "parecer mensalmente para ajustes. E importante manter a higiene oral impecavel",
      "metadata": {}
    }
  ]
}
```

**Problemas:**
- Corte no meio da palavra ("com" / "parecer") — chunking fixo sem respeitar sentencas
- Metadata vazia — impossivel filtrar, buscar ou rastrear proveniencia
- Sem `document_id` — chunks orfaos sem contexto
- Sem overlap — perda de contexto na fronteira dos chunks
- Sem contextual embedding — chunks nao sao auto-contidos

### Output BOM (o que FAZER)

```json
{
  "document_id": "doc_ortodontia_001",
  "source": "guia_ortodontia",
  "created_at": "2025-02-18",
  "total_chunks": 1,
  "chunks": [
    {
      "id": "doc_ortodontia_001_chunk_000",
      "content": "Tratamento Ortodontico — Informacoes gerais: O tratamento ortodontico dura em media 18 a 24 meses. O paciente deve comparecer mensalmente para ajustes. E importante manter a higiene oral impecavel durante o tratamento para evitar caries e problemas gengivais.",
      "token_count": 52,
      "metadata": {
        "section": "Tratamento Ortodontico",
        "keywords": ["ortodontia", "tratamento", "ajustes mensais", "higiene oral"],
        "content_type": "informational",
        "confidence_score": 0.95,
        "chunk_index": 0
      }
    }
  ]
}
```

**Por que o bom e bom:** Texto curto demais para dividir — mantido como chunk unico (melhor do que forcar divisao). Contextual embedding adicionado ("Tratamento Ortodontico — Informacoes gerais:"). Metadata completa. Keywords cobrem termos de busca provaves.

---

## Validation Report Template

Use este template ao gerar o relatorio de validacao no Step 4:

```markdown
# Validation Report

**Source:** [nome do arquivo original]
**Mode:** [RAG Standard | Claude Project | N8N Agent | Hybrid]
**Date:** [YYYY-MM-DD]
**Version:** 1.0

## Metrics Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total chunks | [N] | — | — |
| Avg token count | [N] | 400-600 | [PASS/WARN/FAIL] |
| Min token count | [N] | >100 | [PASS/FAIL] |
| Max token count | [N] | <800 | [PASS/FAIL] |
| Overlap % | [N%] | 10-20% | [PASS/WARN/FAIL] |
| Metadata completeness | [N%] | 100% | [PASS/FAIL] |
| Chunks in target range | [N%] | >80% | [PASS/WARN/FAIL] |

## Quality Checks

- [ ] No encoding errors
- [ ] Consistent language (monolingual chunks)
- [ ] Proper capitalization
- [ ] All cross-reference IDs valid
- [ ] No circular references
- [ ] Contextual summaries present
- [ ] Keywords relevant and non-generic

## Issues Found

| # | Severity | Description | Chunk ID | Recommendation |
|---|----------|-------------|----------|----------------|
| 1 | [HIGH/MED/LOW] | [description] | [chunk_id] | [fix] |

## Before/After Comparison

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Word count | [N] | [N] | [N (-X%)] |
| Sections | [N] | [N] | [N] |
| Filler % (if transcription) | [N%] | [N%] | [-N%] |
| Quality score | [N/10] | [N/10] | [+N] |

## Conclusion

[PASS: Ready for deployment | WARN: Minor issues, review recommended | FAIL: Re-process required]
```

---

## Output Metadata Schema

Every output file MUST include these metadata fields:

```json
{
  "document_id": "string — unique ID, format: doc_{name}_{sequence}",
  "source": "string — original filename or description",
  "created_at": "string — ISO date YYYY-MM-DD",
  "mode": "string — rag_standard | claude_project | n8n_agent | hybrid",
  "version": "string — output version, e.g. 1.0",
  "total_chunks": "number — total chunk count (RAG/N8N modes)",
  "method": "string — chunking method used: recursive | semantic | fixed",
  "parameters": {
    "chunk_size": "number — target tokens per chunk",
    "overlap_pct": "number — overlap percentage used",
    "cleaning_level": "string — aggressive | moderate | light (if transcription)"
  }
}
```

**Required fields (all modes):** `document_id`, `source`, `created_at`, `mode`
**Required for RAG/N8N:** `total_chunks`, `method`, `parameters`
**Optional:** `version`, `linked_document` (for Hybrid mode)

---

## Metricas de Referencia

| Metrica | Valor Esperado | Sinal de Problema |
|---------|---------------|-------------------|
| Reducao de tamanho (transcricao) | 15-40% | >50% = provavel perda de conteudo |
| Chunks no range 400-600 tokens | >80% dos chunks | <60% = recalibrar chunk_size |
| Metadata completeness | 100% campos obrigatorios | Qualquer campo faltando = falha de validacao |
| Confidence score medio | >0.85 | <0.70 = input de baixa qualidade, considerar limpeza |
| Filler removal (PT-BR) | 50-90% dependendo do nivel | <30% = cleaning insuficiente |
| Chunks monolingual | 100% | Qualquer chunk bilingue = separar por idioma |
