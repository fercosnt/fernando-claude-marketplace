# Whitelist por Tipo de Slide (D5 — Regra Canonica do Plugin)

> Esta tabela e a **fonte unica de verdade** sobre quando o deck-image-prompts preenche prompt vs quando devolve skip. Toda skill vertical (`deck-fundraising`, `deck-sales`, etc.) consulta esta tabela.

## Os 14 tipos canonicos

Os tipos canonicos sao definidos em §10.2 do `SHARED.md`:

```
capa | problema | contexto | conceitual | dados | comparativo |
prova-social | equipe | demo | financeiro | CTA | disclaimer |
agradecimento | apendice
```

## Whitelist (preencher prompt automaticamente)

| Tipo | Por que preencher | Engine sugerida default |
|------|-------------------|-------------------------|
| **capa** | Hero do deck, prompt visual sempre necessario | MJ v7 (mood) + Imagen 4 + Higgsfield (cinematic) |
| **problema** | Ilustracao do "antes" / dor / status quo broken | MJ v7 (mood) + Imagen 4 + Nano Banana Pro |
| **conceitual** | Metafora visual de modelo/framework | MJ v7 + Ideogram 3.0 (se texto integrado) + Nano Banana Pro |
| **comparativo** | Antes/depois, com vs sem produto, split-screen | MJ v7 (--seed fixo 2 geracoes) + Imagen 4 (editorial) + DALL-E |
| **demo** | Produto/equipamento/procedimento sendo usado | Imagen 4 Ultra (especular) + MJ v7 + Nano Banana Pro (mockup) |
| **prova-social** | Cliente real, logo wall (mockup), testemunho framing visual | Nano Banana Pro (mockup-aware) + MJ v7 + Higgsfield Soul (Soul ID) |

## Skip por default (sem prompt — campo recebe `—`)

| Tipo | Por que skip | O que vai no slide em vez |
|------|--------------|---------------------------|
| **dados** | Graficos sao geometricos; IA imagem nao acerta valores numericos | Grafico no PowerPoint/Figma direto |
| **financeiro** | Tabelas/projecoes/cap table — precisao numerica > estetica | Tabela ou grafico estruturado |
| **CTA** | Call-to-action e tipografica (action title + ask) | Layout tipografico (Ideogram opcional se quiser hero) |
| **disclaimer** | Texto puro com tom legal/clinico | Caixa de texto, fonte sobria |
| **agradecimento** | Slide de fechamento minimal | Tipografia + contato; opcional Ideogram |
| **apendice** | Conteudo extra de suporte | Caso-a-caso pela vertical |

**Tipos sem categoria explicita no D5** (`contexto`, `equipe`) — aplicar regra:
- **contexto:** preencher (geralmente cabe na whitelist comportamental — mood/cenario)
- **equipe:** preencher quando ha pessoas a retratar (Higgsfield Soul ID se possivel); skip se a vertical preferir grid de fotos reais

## Overrides

### Override `deck-scientific` (canonico)

Inclui `dados` na whitelist, porque **graficos cientificos sao imagens** (microscopia, raio-X, infograficos de mecanismo, esquemas anatomicos).

```yaml
deck-scientific:
  whitelist_extra: [dados]
  engine_preferida: Ideogram 3.0 (esquema cientifico com texto)
  guardrail_extra: cite a fonte do dado no `<!-- comentario -->` abaixo do bloco
```

**Comportamento:** quando `deck-scientific` chama esta skill, ela preenche `dados` com prompt orientado a esquema cientifico (NAO a grafico de barras/linha — esse fica no PowerPoint).

### Override `--include-dados` (usuario)

Flag de invocacao manual. Ex: `/deck-image-prompts --include-dados` ou no input encadeado:

```yaml
flags:
  include_dados: true
```

Forca preenchimento de `dados` mesmo fora de `deck-scientific`. Use quando o slide de dados pede infografico ilustrativo (nao numerico).

### Override `--exclude-prova-social` (usuario)

Pula prova-social mesmo sendo whitelist. Use quando o usuario vai usar logo wall real / screenshot de cliente em vez de prompt gerado.

```yaml
flags:
  exclude_prova_social: true
```

### Outros overrides ad-hoc

O usuario pode passar `--exclude-{tipo}` ou `--include-{tipo}` para qualquer tipo. A skill aplica e marca no bloco:

```markdown
**Prompt de imagem:** —
<!-- skip via flag --exclude-prova-social -->
```

## Tabela resumo (referencia rapida)

```
                              DEFAULT  | SCIENTIFIC | FLAGS USUARIO
                              ---------+------------+----------------
capa                          ✅       | ✅         | flag override
problema                      ✅       | ✅         | flag override
contexto                      ✅       | ✅         | flag override
conceitual                    ✅       | ✅         | flag override
dados                         ❌ skip  | ✅ inclui  | --include-dados
comparativo                   ✅       | ✅         | flag override
prova-social                  ✅       | ✅         | --exclude-prova-social
equipe                        ✅       | ✅         | flag override
demo                          ✅       | ✅         | flag override
financeiro                    ❌ skip  | ❌ skip    | --include-financeiro
CTA                           ❌ skip  | ❌ skip    | --include-cta
disclaimer                    ❌ skip  | ❌ skip    | (raro)
agradecimento                 ❌ skip  | ❌ skip    | --include-agradecimento
apendice                      ❌ skip  | ❌ skip    | (raro)
```

## Output de skip

Quando a skill processa um slide de tipo skip, **sempre** devolve:

```markdown
**Prompt de imagem:** —
<!-- skip — tipo {tipo} fora da whitelist (D5){,se flag: " | flag {flag}"}{,se override scientific aplicavel mas nao usado: " | nota: deck-scientific incluiria"} -->
```

A vertical recebe esse bloco e cola no campo correspondente do STORYBOARD. NUNCA inventar prompt para tipo skip — quebra a regra canonica e induz o designer a usar imagem inadequada em vez de grafico/tabela/tipografia.
