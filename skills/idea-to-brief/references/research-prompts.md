# Prompts para Sub-Agentes de Pesquisa

Referencia para a Fase 3 do idea-to-brief. Cada sub-agente recebe um prompt especifico com contexto limitado (bounded context).

## Instrucoes gerais para todos os sub-agentes

Ao disparar sub-agentes com o Agent tool:
- Envie todos no **mesmo turno** para execucao paralela
- Use `subagent_type: "general-purpose"` para todos
- Cada sub-agente recebe APENAS: (1) a descricao da ideia, (2) o contexto especifico para sua missao
- Resultados devem ser concisos — resumo + fontes, nao dumps de pesquisa bruta

---

## Sub-Agente 1: Mercado & Tendencias

```
Voce e um analista de mercado. Pesquise sobre o seguinte tema:

**Ideia**: [descricao da ideia em 2-3 frases]
**Setor/dominio**: [setor identificado na captura]

Pesquise e retorne:

1. **Panorama do setor**: Tamanho do mercado, crescimento, players principais
2. **Tendencias recentes (12-24 meses)**: 3 tendencias relevantes com fontes
3. **Sinais de timing**: Por que agora? O que mudou que torna essa ideia viavel/necessaria?
4. **Demanda observada**: Evidencias de demanda — discussoes em comunidades, volume de busca, pedidos de usuarios

Use WebSearch para pesquisar. Cite TODAS as fontes com URLs.
Seja conciso: maximo 300 palavras no total.
Foque em FATOS e DADOS, nao opinioes.
Se nao encontrar dados concretos, diga explicitamente "Nao encontrei dados sobre X".
```

---

## Sub-Agente 2: Concorrentes & Alternativas

```
Voce e um analista competitivo. Mapeie o cenario competitivo para esta ideia:

**Ideia**: [descricao da ideia em 2-3 frases]
**Setor/dominio**: [setor identificado na captura]

Pesquise e retorne:

1. **Solucoes existentes**: Ate 5 produtos/ferramentas/servicos que resolvem problema similar
   Para cada: nome, tipo (produto/tool/OSS), pontos fortes, pontos fracos, preco
2. **Projetos open-source**: Ate 3 repositorios GitHub relevantes
   Para cada: nome, stars, ultima atualizacao, relevancia
3. **Workarounds atuais**: Como usuarios resolvem o problema hoje sem solucao dedicada? (3 exemplos)
4. **Gaps nao atendidos**: O que nenhuma solucao existente resolve bem?

Use WebSearch para pesquisar. Cite TODAS as fontes com URLs.
Seja conciso: maximo 400 palavras no total.
Se uma categoria nao tem resultados relevantes, diga "Nao identificado".
```

---

## Sub-Agente 3: Melhores Praticas

```
Voce e um consultor de melhores praticas. Identifique como especialistas abordam este tipo de problema:

**Ideia**: [descricao da ideia em 2-3 frases]
**Dominio tecnico**: [stack/plataforma identificada na captura]

Pesquise e retorne:

1. **Frameworks e metodologias**: Ate 3 frameworks relevantes para este tipo de problema/solucao
2. **Padroes de design/arquitetura**: Padroes aplicaveis ao tipo de solucao proposta
3. **Licoes aprendidas**: Erros comuns e melhores praticas de projetos similares
4. **Recursos recomendados**: 2-3 artigos/guias de referencia

Use WebSearch para pesquisar. Cite TODAS as fontes com URLs.
Seja conciso: maximo 300 palavras no total.
Foque em praticas ACIONAVEIS, nao teoria generica.
```

---

## Sub-Agente 4: Analise de Plataformas

```
Voce e um arquiteto de solucoes. Analise o ecossistema tecnologico do usuario e avalie o fit para esta ideia:

**Ideia**: [descricao da ideia em 2-3 frases]

**Tarefa**:

1. Leia os seguintes arquivos para detectar plataformas do usuario:
   - CLAUDE.md (na raiz do projeto e no home directory)
   - package.json (se existir)
   - Verifique se existem: vercel.json, docker-compose.yml, .github/workflows/

2. Liste as plataformas detectadas em formato:
   | Plataforma | Detectada via | Status |

3. Para cada plataforma, avalie:
   - Fit para a ideia (1-5)
   - Como poderia ser usada
   - Limitacoes para este caso

4. Se uma plataforma que o usuario NAO usa seria significativamente melhor, mencione qual e por que.

NAO use WebSearch — esta analise e baseada apenas em leitura de arquivos locais.
Seja conciso: maximo 300 palavras no total.
```

---

## Como consolidar resultados

Apos receber os 4 resultados:

1. **Sintetize convergencias**: O que multiplos sub-agentes confirmaram?
2. **Identifique contradicoes**: Algum sub-agente contradiz outro?
3. **Destaque gaps**: O que nenhum sub-agente conseguiu responder?
4. **Organize por relevancia**: Descarte informacao de baixa qualidade
5. **Mantenha fontes**: Cada achado deve ter sua fonte original

Os resultados consolidados alimentam diretamente:
- Pesquisa de mercado -> Secao 2 do brief
- Concorrentes -> Secao 3 do brief
- Melhores praticas -> Informa frameworks (Fase 4) e abordagens (Fase 5)
- Plataformas -> Secao 8 do brief
