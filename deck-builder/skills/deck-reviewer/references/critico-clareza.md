# Critico 1 — Clareza

Pergunta unica: **o deck tem clareza estrutural?**

Aplica 5 checagens. Cada falha vira issue com severidade conforme tabela ao fim deste arquivo.

---

## 1. Action titles vs titulos descritivos

**Regra:** todo slide (exceto capa) deve ter um title afirmativo com verbo, NAO um label descritivo.

| Action title (OK) | Titulo descritivo (FALHA) |
|---|---|
| "Mercado de endo cresce 12% a.a." | "Mercado endodontia" |
| "Premium ja paga mais por agenda livre" | "Comportamento do consumidor" |
| "Beauty Smile dobrou ticket em 18 meses" | "Resultados" |
| "Concorrencia foca volume; sobra premium" | "Analise competitiva" |
| "Ask: R$500k @ 8% / 6m" | "Investimento" |

**Como detectar:**
- Title tem verbo conjugado (cresce, paga, dobra, sobra)? Action title ✓
- Title tem so substantivo + adjetivo? Descritivo ✗
- Caso ambiguo (numero solto, sigla): considerar peso da mensagem-chave; se a Mensagem-chave salva, marca 🟢; se nao, 🟡

**Severidade:**
- Capa pode ser nominal — NAO marca
- 1-2 titles descritivos: 🟢 cada
- 3+ titles descritivos: 🟡 (padrao sistemico)
- Title fraco em slide CTA, problema ou Ask: 🟡 (alta consequencia)

**Fonte canonica (NB1):** Resonate (Duarte) — "Slide titles should make a complete point, not label a topic." McKinsey: "The reader should be able to read only the slide titles and get the story."

## 2. Uma ideia por slide

**Regra:** cada slide carrega 1 mensagem-chave. Slide com 3 bullets desconectados = 3 slides disfarcados de 1.

**Como detectar:**
- A Mensagem-chave do slide pode ser parafraseada em 1 frase sem perder nada? OK
- Se o slide tem 3+ bullets que nao se conectam a uma tese unica: FALHA
- Caso especial: slide `dados` com tabela e ate 3 colunas comparativas — OK se a Mensagem-chave amarrar

**Severidade:**
- 1-2 slides poluidos: 🟢 cada
- 3+ slides poluidos: 🟡 (padrao sistemico)
- Slide chave (problema / solucao / Ask / capa) poluido: 🟡

**Fonte:** Reynolds — Presentation Zen. Duarte — "If they're reading bullets, they're not listening to you."

## 3. Horizontal logic test

**Regra:** ler apenas os action titles em sequencia conta a historia inteira do deck.

**Como aplicar:**
1. Extrai titles de todos os slides em ordem
2. Le em voz alta como se fosse um paragrafo
3. Faz sentido como narrativa? OK
4. Precisa do conteudo dos slides pra entender? FALHA

**Severidade:**
- Salto narrativo isolado (1 slide nao conecta com vizinhos): 🟡
- Toda a sequencia incoerente (≥3 saltos): 🔴 (deck nao apresenta uma historia)

**Fonte canonica:** Minto Pyramid Principle + Barbara Minto via McKinsey.

## 4. CTA dentro do `max_ctas`

**Regra:** ver tabela de defaults por vertical no SKILL.md §max_ctas.

```
max_ctas_efetivo = Meta.max_ctas OR default_da_vertical
count_ctas = numero de slides com Tipo: CTA

Se count_ctas > max_ctas_efetivo:
  🟡 MAJOR: "{count_ctas} CTAs detectados, max_ctas={max_ctas_efetivo}. Reduzir OU aumentar limite na Meta com justificativa."

Se count_ctas == 0:
  Vertical exige CTA?
    fundraising / sales / proposal / equipment → 🔴 BLOCKER (vide tabela abaixo)
    teaching / scientific / internal → 🟢 (CTA pode estar implicito)
    clinical → 🟡 (CTA tipico = "agendar avaliacao")
```

### Sugestoes especificas por vertical quando CTA ausente

| Vertical | Sugestao |
|----------|----------|
| fundraising | "Adicionar slide 'Ask' com valuation + ticket + timeline + uso do capital" |
| sales | "Adicionar slide CTA com proxima etapa concreta (POC, contrato, demo)" |
| proposal | "Adicionar slide CTA com proximo passo + valor + prazo de validade da proposta" |
| equipment | "Adicionar slide CTA com proxima etapa (demo, teste in loco, contrato)" |

## 5. Tempo estimado por slide balanceado

**Regra:** somatorio dos `Tempo estimado` deve bater (±20%) com `Duracao` da Meta. Distribuicao nao deve ter outliers > 3x mediana.

**Como detectar:**
- Soma dos tempos / duracao da Meta esta entre 0.8 e 1.2? OK
- Algum slide com tempo > 3x mediana? Suspeito (provavelmente conteudo demais)
- Algum slide sem `Tempo estimado`? 🟢

**Severidade:**
- Soma fora da faixa: 🟢 (informacional)
- Outlier > 3x mediana: 🟢 (avisa autor)
- ≥5 slides sem tempo estimado: 🟢 (incompleto)

NUNCA 🔴 ou 🟡 — tempo e ajuste fino, nao bloqueante.

---

## Resumo de severidades — Critico Clareza

| Falha | Severidade |
|-------|------------|
| 3+ titles descritivos (sistemico) | 🟡 MAJOR |
| Title fraco em slide CTA/problema/Ask | 🟡 MAJOR |
| 3+ slides poluidos (sistemico) | 🟡 MAJOR |
| ≥3 saltos no horizontal logic | 🔴 BLOCKER |
| CTAs > max_ctas | 🟡 MAJOR |
| CTA inexistente em fundraising/sales/proposal/equipment | 🔴 BLOCKER |
| 1-2 titles descritivos isolados | 🟢 MINOR |
| Slides poluidos isolados (1-2) | 🟢 MINOR |
| Salto narrativo isolado (1 slide) | 🟡 MAJOR |
| Tempo estimado desbalanceado | 🟢 MINOR |
| Slide sem tempo estimado | 🟢 MINOR |

## Output do Critico Clareza (input pra consolidacao)

Lista de issues com schema:

```python
[
  {"slide_n": 4, "tipo_slide": "problema", "critico": "clareza",
   "severidade": "🟡",
   "problema": "Action title fraco: 'Mercado endodontia'",
   "sugestao": "Reescrever: 'Mercado de endo premium cresce 12%/ano com TAM R$2.4bi'"},
  ...
]
```
