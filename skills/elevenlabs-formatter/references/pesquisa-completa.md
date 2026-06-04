# ElevenLabs TTS: Formatacao de Texto, Audio Tags e Otimizacao de Voz — Pesquisa Completa

> Compilado em 2026-04-01 a partir de 18+ fontes via deep-research
> Modo: Deep Research | Dominio: Voice AI / TTS / ElevenLabs

---

## Resumo Executivo

- **Audio Tags [brackets]** sao o sistema de controle principal do modelo v3 — substituem SSML. Mais de 1800 tags catalogadas em 15 categorias (emocoes, reacoes, efeitos sonoros, sotaques, archetypes)
- **Break tags SSML** (`<break time="x.xs" />`) funcionam em v2/Flash/Turbo, **NAO** no v3. No v3 use `[pause]`, `[short pause]`, `[long pause]`
- **Pontuacao e o controle de prosody mais confiavel**: ponto = pausa completa, reticencias = hesitacao, MAIUSCULAS = enfase, travessao = quebra forte
- **Pronunciation dictionaries** (.PLS ou .TXT) permitem alias e phoneme tags. Phoneme (IPA/CMU) so funciona com `eleven_flash_v2` e so em ingles
- **Truque de pronuncia manual**: reescrever palavras foneticamente (ex: "trapezIi", usar hifens, apostrofos, aspas simples)
- **Voice settings**: Stability ~0.5, Similarity ~0.75, Style 0.0 como ponto de partida. Narration: 0.6-0.8 stability. Characters: 0.3-0.5 stability
- **Normalizacao de texto e obrigatoria**: numeros, datas, moedas, siglas devem ser escritos por extenso para evitar ambiguidade multilingual
- **Speed control**: range 0.7 (lento) a 1.2 (rapido), default 1.0
- **Modelo v3 tem limite de 3000 caracteres** por geracao — scripts longos devem ser divididos por cenas/paragrafos
- **Gerar contexto narrativo** ao redor do dialogo melhora dramaticamente a entrega emocional

---

## Indice

1. [Fundamentos e Modelos](#1-fundamentos-e-modelos)
2. [Audio Tags (v3)](#2-audio-tags-v3)
3. [Controle de Pausas](#3-controle-de-pausas)
4. [Pontuacao e Prosody](#4-pontuacao-e-prosody)
5. [Pronuncia Customizada](#5-pronuncia-customizada)
6. [Voice Settings](#6-voice-settings)
7. [Normalizacao de Texto](#7-normalizacao-de-texto)
8. [Tecnicas Avancadas de Script](#8-tecnicas-avancadas-de-script)
9. [Troubleshooting](#9-troubleshooting)
10. [Videos Relevantes](#10-videos-relevantes)
11. [Fontes Completas](#11-fontes-completas)

---

## 1. Fundamentos e Modelos

### Modelos disponiveis e suas capacidades

| Modelo | Melhor para | Latencia | Linguas | Limite chars | Tags suportadas |
|--------|-------------|----------|---------|--------------|-----------------|
| **Eleven v3** | Emocao/storytelling | 1-2s | 70+ | 3.000 | Audio tags `[brackets]` |
| **Flash v2.5** | Real-time/chatbots | 75ms | 32 | 40.000 | SSML break, phoneme |
| **Turbo v2.5** | Uso geral | ~300ms | 32 | 40.000 | SSML break, phoneme |
| **Multilingual v2** | Qualidade premium | 1-2s | 29 | 5.000 | SSML break |
| **Flash v2** | Velocidade + phoneme | Rapido | 32 | 40.000 | SSML break, phoneme (IPA/CMU) |

**Fonte**: [ElevenLabs Best Practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) | [Webfuse Cheat Sheet](https://www.webfuse.com/elevenlabs-cheat-sheet)

### Escolha rapida

- **Velocidade** → Flash v2.5
- **Qualidade maxima** → Multilingual v2
- **Emocao e performance** → v3
- **Equilibrio** → Turbo v2.5

---

## 2. Audio Tags (v3)

O modelo v3 introduziu **audio tags** — palavras entre colchetes `[tag]` que direcionam tom, emocao, pausas e efeitos sonoros. NAO sao case-sensitive mas sao escritas em maiuscula por convencao.

**Fonte**: [Medium - Victor Kh.](https://medium.com/@v-jur-kh/on-text-markup-for-the-elevenlabs-v3-text-to-speech-2b0a330110e1) | [ElevenLabs Blog - Audio Tags](https://elevenlabs.io/blog/v3-audiotags)

### 2.1 Categorias de Tags

#### Emocoes e Estados
```
[SAD] [ANGRY] [HAPPILY] [SORROWFUL] [EXCITED] [NERVOUS]
[FRUSTRATED] [TIRED] [CALM] [CHEERFULLY] [FLATLY] [DEADPAN]
[PLAYFULLY] [ANNOYED] [FLUSTERED] [CASUAL] [RESIGNED TONE]
[DELIBERATE] [CURIOUS] [SARCASTIC] [MISCHIEVOUSLY] [CRYING]
```

#### Reacoes Humanas e Nao-Verbais
```
[LAUGHS] [GIGGLE] [LAUGHS SOFTLY] [LAUGHS HARDER] [STARTS LAUGHING]
[WHEEZING] [SIGH] [SIGHING] [EXHALES] [GULPS] [GASPS]
[CLEARS THROAT] [BREATHES] [SNORTS] [SWALLOWS]
```

#### Controle de Volume e Entrega
```
[WHISPERS] [WHISPERING] [LOUDLY] [SHOUTS]
```

#### Controle de Ritmo/Pacing
```
[PAUSE] [SHORT PAUSE] [LONG PAUSE]
[CONTINUES AFTER A BEAT] [CONTINUES SOFTLY]
[RUSHED] [SLOWS DOWN] [RAPID-FIRE] [DRAWN OUT]
[TIMIDLY] [EMPHASIZED] [STRESS ON NEXT WORD] [UNDERSTATED]
```

#### Tom Narrativo
```
[DRAMATIC TONE] [WISTFUL] [SERIOUS TONE] [MATTER-OF-FACT]
[CONVERSATIONAL TONE] [SARCASTIC TONE] [AWE] [LIGHTHEARTED]
[REFLECTIVE]
```

#### Hesitacao e Repeticao
```
[HESITATES] [STAMMERS] [REPEATS]
```

#### Sotaques e Dialetos
```
[FRENCH ACCENT] [GERMAN ACCENT] [SPANISH ACCENT] [ITALIAN ACCENT]
[RUSSIAN ACCENT] [AMERICAN ACCENT] [BRITISH ACCENT] [AUSTRALIAN ACCENT]
[INDIAN ENGLISH ACCENT] [IRISH ACCENT] [SOUTHERN US ACCENT]
[NEW YORK ACCENT] [SCOTTISH ACCENT]
[STRONG X ACCENT]  ← substituir X pelo sotaque desejado
[THICK IRISH ACCENT]  ← usar "thick" ou "strong" para intensificar
```

#### Archetypes de Personagem
```
[DEEP VOICE] [ROBOTIC TONE] [PIRATE VOICE] [EVIL SCIENTIST VOICE]
[CHILDLIKE TONE] [FANTASY NARRATOR] [SCI-FI AI VOICE]
[CLASSIC FILM NOIR]
```

#### Efeitos Sonoros
```
[GUNSHOT] [APPLAUSE] [CLAPPING] [EXPLOSION]
```

#### Multi-Personagem
```
[INTERRUPTING] [OVERLAPPING] [CUTS IN]
```

#### Experimentais
```
[SINGS] [WOO] [FART]
```

### 2.2 Regras de uso das tags

| Regra | Detalhe |
|-------|---------|
| **Posicionamento** | Tags no inicio da linha definem o tom geral; no meio da frase permitem mudancas dinamicas |
| **Layering** | Combinar tags de categorias diferentes: `[BRITISH ACCENT][EXCITED][PAUSE]` empilha instrucoes |
| **Terminacao** | Tags NAO tem fechamento — efeito termina quando contradito, no fim da frase, ou gradualmente |
| **Compatibilidade** | Algumas combinacoes enfraquecem o efeito vs uso individual — testar sempre |
| **Voz importa** | A voz escolhida e seus samples de treino afetam a efetividade de cada tag |

### 2.3 Exemplos praticos

```
[WHISPERING][PAUSE] Did you hear that? [RUSHED] Hide! Now!

[SARCASTIC] Oh, that's just wonderful. [SIGHS] I can't believe this.

"It was a VERY long day [SIGH] ... nobody listens anymore."

[DRAMATIC TONE] The kingdom had fallen. [PAUSE] And with it, all hope.

[PIRATE VOICE] Arrr, ye scallywags! [LAUGHS] Hand over the treasure!
```

### 2.4 Modos de Estabilidade (v3)

| Modo | Comportamento |
|------|---------------|
| **Creative** | Mais emocional e expressivo, mas propenso a "alucinacoes" sonoras |
| **Natural** | Mais proximo da gravacao original — equilibrado e neutro |
| **Robust** | Altamente estavel, menos responsivo a tags direcionais mas consistente |

---

## 3. Controle de Pausas

### Por modelo

| Metodo | Modelos compatveis | Syntax | Limite |
|--------|-------------------|--------|--------|
| **SSML Break tag** | v2, Flash v2/v2.5, Turbo v2.5, Multilingual v2 | `<break time="1.5s" />` | Ate 3 segundos |
| **Audio tags de pausa** | v3 apenas | `[PAUSE]`, `[SHORT PAUSE]`, `[LONG PAUSE]` | Sem limite numerico |
| **Pontuacao** | Todos | `.` `;` `...` `—` | Natural |

### Break tags SSML (v2/Flash/Turbo)

```xml
"Hold on, let me think." <break time="1.5s" /> "Alright, I've got it."
```

**CUIDADO**: Usar muitas break tags em uma unica geracao causa instabilidade — a IA pode acelerar, introduzir ruidos ou artefatos.

**Fonte**: [ElevenLabs - How to add pauses](https://help.elevenlabs.io/hc/en-us/articles/13416374683665-How-can-I-add-pauses) | [ElevenLabs Best Practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)

### Alternativas de pausa (todos os modelos)

| Tecnica | Efeito | Consistencia |
|---------|--------|-------------|
| **Travessao** (- ou —) | Pausa curta | Menos consistente |
| **Reticencias** (...) | Pausa hesitante, trailing off | Media |
| **Ponto final** (.) | Pausa completa entre sentencas | Alta |
| **Ponto e virgula** (;) | Pausa mais curta entre partes da sentenca | Alta |
| **Quebra de linha** | Funciona como pausa completa | Alta |
| **Novo paragrafo** | Pausa clara com reset de entonacao | Alta |

### Comportamento especial

Algumas vozes treinadas com "uh"s e "ah"s podem inserir esses maneirismos vocais durante as pausas, como um falante real faria.

---

## 4. Pontuacao e Prosody

A pontuacao e o sistema de controle de prosody MAIS CONFIAVEL e funciona em TODOS os modelos.

**Fonte**: [Medium - Victor Kh.](https://medium.com/@v-jur-kh/on-text-markup-for-the-elevenlabs-v3-text-to-speech-2b0a330110e1)

| Pontuacao | Efeito na voz |
|-----------|---------------|
| **Ponto (.)** | Pausa completa antes da proxima sentenca |
| **Ponto e virgula (;)** | Pausa mais curta, entre partes da sentenca |
| **Reticencias (...)** | Pausa notavel, sinaliza hesitacao ou continuacao |
| **Travessao (—)** | Quebra mais forte, especialmente com espacos ao redor |
| **Virgula (,)** | Micro-pausa natural, respiracao |
| **Ponto de interrogacao (?)** | Inflexao ascendente natural |
| **Ponto de exclamacao (!)** | Enfase e energia |
| **MAIUSCULAS** | Aumenta enfase vocal e volume |
| **Quebra de linha** | Funciona como pausa completa |
| **Novo paragrafo** | Pausa clara com reset de entonacao |

### Exemplos

```
Isso e MUITO importante.              ← enfase em "muito"
Eu pensei que... talvez nao.          ← hesitacao antes de "talvez"
Espera — eu ouvi algo.                ← quebra abrupta
Voce tem certeza? Absoluta?           ← inflexao ascendente dupla
```

---

## 5. Pronuncia Customizada

### 5.1 Pronunciation Dictionaries (.PLS)

Arquivos XML que mapeiam grafemas (escrita) para pronuncias customizadas.

**Fonte**: [ElevenLabs - Pronunciation Dictionaries](https://elevenlabs.io/docs/eleven-agents/customization/voice/pronunciation-dictionary)

#### Formato PLS (W3C standard)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
  xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
  alphabet="ipa" xml:lang="en-US">

  <lexeme>
    <grapheme>Claughton</grapheme>
    <alias>Cloffton</alias>
  </lexeme>

  <lexeme>
    <grapheme>UN</grapheme>
    <alias>United Nations</alias>
  </lexeme>

</lexicon>
```

#### Phoneme tags (IPA)

```xml
<lexeme>
  <grapheme>nginx</grapheme>
  <phoneme alphabet="ipa">/ˈɛndʒɪnˈɛks/</phoneme>
</lexeme>
```

#### Phoneme tags (CMU Arpabet) — RECOMENDADO

```xml
<phoneme alphabet="cmu-arpabet" ph="M AE1 D IH0 S AH0 N">Madison</phoneme>
```

**IMPORTANTE**: Phoneme tags so funcionam com `eleven_flash_v2`, `eleven_turbo_v2` e `eleven_english_v1`. Em outros modelos sao silenciosamente ignoradas.

**IMPORTANTE**: Phoneme tags (IPA/CMU) so funcionam para INGLES. Para outras linguas, use alias tags.

### 5.2 Regras dos dicionarios

- Busca e **case-sensitive**
- Apenas o **primeiro match** e usado (de cima para baixo)
- Multiplos dicionarios podem ser carregados simultaneamente
- Palavras fora do dicionario usam a pronuncia padrao do modelo
- Recomendado: criar entradas separadas para versao maiuscula e minuscula

### 5.3 Truques manuais de pronuncia

Quando NAO tem acesso a dicionarios ou o modelo nao suporta phoneme tags:

| Tecnica | Exemplo | Efeito |
|---------|---------|--------|
| **Escrita fonetica** | "trapezIi" em vez de "trapezii" | Enfase no "ii" |
| **Hifens** | "com-ple-ta-men-te" | Silabacao enfatica |
| **Apostrofos** | "re'al" | Enfase na silaba |
| **Aspas simples** | 'e' em vez de e | Pronuncia isolada da letra |
| **Maiusculas parciais** | "proDUcao" | Enfase na silaba em caps |
| **Alias simples** | "Zhee-Pee-Tee" em vez de "GPT" | Soletrar siglas |
| **Palavras substitutas** | "biu-ti" em vez de "beauty" | Aproximacao fonetica |

### 5.4 Ferramentas auxiliares de pronuncia

- **Sequitur G2P** — grapheme-to-phoneme automatico
- **Phonetisaurus** — conversor G2P
- **eSpeak** — sintetizador com output IPA
- **CMU Pronouncing Dictionary** — dicionario de referencia ingles

### 5.5 API Python para dicionarios

```python
# Criar dicionario via API
client.pronunciation_dictionaries.create_from_file(
    file=open("my_dictionary.pls", "rb"),
    name="My Custom Dictionary"
)

# Ou criar a partir de regras diretamente
client.pronunciation_dictionaries.create_from_rules(
    name="Brand Names",
    rules=[
        {"type": "alias", "string_to_replace": "ACME", "replacement": "ack-me"},
        {"type": "phoneme", "string_to_replace": "Nguyen", "phoneme": "W IH1 N", "alphabet": "cmu-arpabet"}
    ]
)
```

---

## 6. Voice Settings

### Parametros e ranges

| Parametro | Range | Default recomendado | Funcao |
|-----------|-------|---------------------|--------|
| **Stability** | 0.0 - 1.0 | 0.5 | Controla randomizacao entre geracoes. Baixo = expressivo/variado. Alto = monotono/consistente |
| **Similarity Boost** | 0.0 - 1.0 | 0.75 | Quanto a IA adere a voz original. Alto demais = reproduz ruidos/artefatos do audio original |
| **Style Exaggeration** | 0.0 - 1.0 | 0.0 | Amplifica o estilo natural da voz. Comecar em 0 e subir. 3-5% ja faz diferenca |
| **Speaker Boost** | on/off | on | Melhora clareza, reduz artefatos, mas adiciona latencia |
| **Speed** | 0.7 - 1.2 | 1.0 | Velocidade de fala. Extremos afetam qualidade |

**Fonte**: [Webfuse Cheat Sheet](https://www.webfuse.com/elevenlabs-cheat-sheet) | [ElevenLabs Voice Settings](https://elevenlabs-sdk.mintlify.app/speech-synthesis/voice-settings)

### Presets por caso de uso

| Caso de uso | Stability | Similarity | Style | Speed |
|-------------|-----------|------------|-------|-------|
| **Narracao** | 0.6-0.8 | 0.7 | 0.2-0.4 | 0.9-1.0 |
| **Atendimento/Suporte** | 0.7-0.9 | 0.9 | 0.0-0.2 | 1.0 |
| **Personagens dramaticos** | 0.3-0.5 | 0.8 | 0.7-1.0 | Variavel |
| **Audiobook** | 0.6-0.7 | 0.75 | 0.3-0.5 | 0.9 |
| **Clone de voz (natural)** | 0.5 | 0.75 | 0.0 | 1.0 |

### Importante: Nao-determinismo

A IA e **nao-deterministica** — os sliders funcionam como **ranges de randomizacao**, nao valores exatos. Mesma configuracao pode gerar resultados diferentes. Use a funcao "Regenerate" (3 versoes no web app) para escolher a melhor.

---

## 7. Normalizacao de Texto

### Por que normalizar

Numeros e simbolos sao escritos igual em muitas linguas mas pronunciados diferentemente. Escrever por extenso **elimina ambiguidade**.

**Fonte**: [ElevenLabs Best Practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)

### Tabela de conversoes obrigatorias

| Original | Normalizado | Motivo |
|----------|-------------|--------|
| `$42.50` | "forty-two dollars and fifty cents" | Moeda |
| `R$ 150,00` | "cento e cinquenta reais" | Moeda BR |
| `555-555-5555` | "five five five, five five five, five five five five" | Telefone |
| `2024-01-01` | "January first, twenty twenty-four" | Data |
| `15:30` | "three thirty PM" ou "quinze e trinta" | Hora |
| `Ctrl + Z` | "control z" | Atalho |
| `100km` | "one hundred kilometers" | Unidade |
| `#1` | "number one" | Simbolo |
| `@user` | "at user" | Simbolo |
| `50%` | "fifty percent" ou "cinquenta por cento" | Porcentagem |
| `CEO` | "C.E.O." ou "chief executive officer" | Sigla |

### Funcao Python de normalizacao

```python
import inflect
import re

p = inflect.engine()

def normalize_text(text: str) -> str:
    """Normaliza texto para TTS — converte numeros, moedas, simbolos"""
    
    def money_replacer(match):
        currency_map = {"$": "dollars", "£": "pounds", "€": "euros"}
        currency_symbol, num = match.groups()
        num_clean = num.replace(',', '')
        if '.' in num_clean:
            dollars, cents = num_clean.split('.')
            return f"{p.number_to_words(int(dollars))} {currency_map.get(currency_symbol, 'units')} and {p.number_to_words(int(cents))} cents"
        return f"{p.number_to_words(int(num_clean))} {currency_map.get(currency_symbol, 'units')}"
    
    text = re.sub(r"([$£€])(\d+(?:,\d{3})*(?:\.\d{2})?)", money_replacer, text)
    return text
```

### ElevenLabs auto-normalizacao

O parametro `apply_text_normalization` esta habilitado por default na API e normaliza automaticamente numeros, datas e texto complexo. Para japones, use `apply_language_text_normalization`.

---

## 8. Tecnicas Avancadas de Script

### 8.1 Contexto narrativo para emocao

Em vez de confiar apenas em tags, **escreva contexto emocional ao redor do dialogo**:

```
"You're leaving?" she asked, her voice trembling with sadness.

"That's it!" he exclaimed triumphantly, slamming his fist on the table.

"I... I thought you'd understand," he said, his voice slowing with disappointment.
```

**CUIDADO**: O modelo FALA os descritores emocionais ("her voice trembling with sadness"). Voce precisa remover essas partes em pos-producao, ou usar audio tags v3 que nao sao faladas.

### 8.2 Geracao segmentada

- **Gerar paragrafos/cenas completas** — a IA precisa de contexto para pacing natural
- **Dividir scripts longos** por cenas naturais, nao no meio de frases
- **v3 limite: 3.000 caracteres** — planejar divisoes com antecedencia
- **Combinar segmentos** em editor de audio para resultado final

### 8.3 Chunk sizing (streaming/API)

| Tamanho | Chars | Quando usar |
|---------|-------|-------------|
| Minimo | 50 | Nunca ideal |
| Recomendado | 200-400 | Uso geral |
| Maximo | 1.000 | Narrativa longa |

**Flush** no fim de sentencas para naturalidade: `ws.send(JSON.stringify({ flush: true }))`

### 8.4 Feature "Enhance" (UI)

O ElevenLabs tem um botao **Enhance** que usa um LLM para auto-gerar audio tags contextuais sem alterar o texto original. Util para adicionar emocao automaticamente.

### 8.5 Dicas de formatacao para a skill

Ao preparar scripts para ElevenLabs:

1. **Escrever numeros por extenso** — sempre
2. **Expandir siglas** — "CEO" → "C.E.O." ou "chief executive officer"
3. **Usar pontuacao estrategica** — reticencias para hesitacao, CAPS para enfase
4. **Adicionar audio tags v3** se usando modelo v3 — `[PAUSE]`, `[SIGHS]`, etc.
5. **Quebrar em chunks** de 200-400 chars para streaming, ate 3000 para v3
6. **Testar e regenerar** — gerar 2-3 versoes e escolher a melhor
7. **Contextualizar emocao** via narrativa ou tags, nao confiar em texto seco
8. **Remover markup narrativo** em pos-producao se usou estilo "she said sadly"

---

## 9. Troubleshooting

| Problema | Solucao |
|----------|---------|
| **Voz robotica/artificial** | Baixar stability (0.3-0.5), aumentar similarity boost, adicionar contexto narrativo |
| **Output inconsistente** | Aumentar stability (0.7-0.8), usar Turbo v2 em vez de v3, remover excess de breaks |
| **Artefatos/glitches** | Habilitar speaker boost, reduzir style exaggeration, corrigir pontuacao |
| **Pronuncia errada** | Usar phoneme tags (CMU), pronunciation dictionary, ou reescrever foneticamente |
| **Pausas inconsistentes** | Usar syntax correta `<break time="x.xs" />`, nao abusar de breaks |
| **Emocao flat** | Adicionar cues contextuais, descricoes narrativas, baixar stability, usar tags v3 |
| **Emocao exagerada** | Aumentar stability, reduzir style exaggeration, linguagem mais calma |
| **Palavras estrangeiras** | Definir `language_code`, usar contexto narrativo, tags de sotaque, quebrar em silabas |
| **Texto longo cortado** | Flash/Turbo: 40k limit, Multilingual: 5k, v3: 3k — dividir por sentencas |

**Fonte**: [Webfuse Cheat Sheet](https://www.webfuse.com/elevenlabs-cheat-sheet)

---

## 10. Videos Relevantes

| # | Video | Canal | Views | Data | Relevancia |
|---|-------|-------|-------|------|------------|
| 1 | [How to make AI Voiceovers that sound Human](https://youtube.com/watch?v=Vs6vJwmJL0Y) | ElevenLabs | 83K | 2025-07 | Alta — canal oficial, foco em naturalidade |
| 2 | [How To Use ElevenLabs - Master in 23 min](https://youtube.com/watch?v=s7p6OLwV_50) | Dan Kieft | 342K | 2025-05 | Alta — tutorial completo, 342K views |
| 3 | [How To Add Emotions In ElevenLabs](https://youtube.com/watch?v=JjY1F9h1IeU) | Artificial Quotient | 30K | 2025-03 | Alta — foco em voice settings e emocao |
| 4 | [How to Create Audiobooks with ElevenLabs](https://youtube.com/watch?v=KI7fb8_XCd0) | ElevenLabs | 14K | 2026-02 | Media — audiobooks, formatacao longa |
| 5 | [FREE AI Voice Generator Tutorial](https://youtube.com/watch?v=08cp19pf5nc) | Saddam Kassim | 40K | 2026-03 | Media — tutorial recente e basico |

---

## 11. Fontes Completas

### Tier 1 — Essenciais

| # | Fonte | Tipo | URL |
|---|-------|------|-----|
| 1 | ElevenLabs Best Practices | Docs oficial | https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices |
| 2 | ElevenLabs Cheat Sheet (Webfuse) | Guia completo | https://www.webfuse.com/elevenlabs-cheat-sheet |
| 3 | Text Markup for v3 (Victor Kh.) | Blog tecnico | https://medium.com/@v-jur-kh/on-text-markup-for-the-elevenlabs-v3-text-to-speech-2b0a330110e1 |
| 4 | ElevenLabs Pronunciation Dictionaries | Docs oficial | https://elevenlabs.io/docs/eleven-agents/customization/voice/pronunciation-dictionary |
| 5 | ElevenLabs Blog - v3 Audio Tags | Blog oficial | https://elevenlabs.io/blog/v3-audiotags |
| 6 | ElevenLabs Blog - Precision Delivery Control | Blog oficial | https://elevenlabs.io/blog/eleven-v3-audio-tags-precision-delivery-control-for-ai-speech |

### Tier 2 — Complementares

| # | Fonte | Tipo | URL |
|---|-------|------|-----|
| 7 | ElevenLabs - How to add pauses | Help center | https://help.elevenlabs.io/hc/en-us/articles/13416374683665-How-can-I-add-pauses |
| 8 | ElevenLabs - Force pronunciation | Help center | https://help.elevenlabs.io/hc/en-us/articles/16712320194577-How-can-I-force-a-certain-pronunciation-of-a-word-or-name |
| 9 | Using pronunciation dictionaries (cookbook) | Docs oficial | https://elevenlabs.io/docs/eleven-api/guides/cookbooks/text-to-speech/pronunciation-dictionaries |
| 10 | ElevenLabs - Emotional Context in Speech | Blog oficial | https://elevenlabs.io/blog/eleven-v3-audio-tags-expressing-emotional-context-in-speech |
| 11 | ElevenLabs - Character Performance | Blog oficial | https://elevenlabs.io/blog/eleven-v3-character-direction |
| 12 | ElevenLabs - Accent Emulation | Blog oficial | https://elevenlabs.io/blog/eleven-v3-audio-tags-emulating-accents-with-precision |
| 13 | ElevenLabs - Narrative Intelligence | Blog oficial | https://elevenlabs.io/blog/eleven-v3-audio-tags-enabling-narrative-intelligence-in-speech |
| 14 | LearnPrompting - Complete Guide to ElevenLabs | Tutorial | https://learnprompting.org/blog/guide-elevenlabs |
| 15 | Audio Generation Plugin - v3 Tag Library | Referencia | https://audio-generation-plugin.com/eleven-v3-tag-library/ |

### Tier 3 — Referencia

| # | Fonte | Tipo | URL |
|---|-------|------|-----|
| 16 | ElevenLabs Python SDK | Repo oficial | https://github.com/elevenlabs/elevenlabs-python |
| 17 | ElevenLabs Voice Settings (Mintlify) | Docs | https://elevenlabs-sdk.mintlify.app/speech-synthesis/voice-settings |
| 18 | SSML tags issue #175 | GitHub issue | https://github.com/elevenlabs/elevenlabs-python/issues/175 |
| 19 | ElevenLabs IPA Vowel Chart | Blog oficial | https://elevenlabs.io/blog/ipa-chart |
| 20 | Do pauses and SSML tags work with API? | Help center | https://help.elevenlabs.io/hc/en-us/articles/24352686926609-Do-pauses-and-SSML-phoneme-tags-work-with-the-API |

---

## Gaps Identificados

- **Lista completa dos 1800+ tags v3**: O site audio-generation-plugin.com tem a biblioteca mas carrega via AJAX — nao foi possivel extrair programaticamente. Recomendacao: acessar manualmente https://audio-generation-plugin.com/eleven-v3-tag-library/
- **Tags em portugues**: Nao encontrei documentacao especifica sobre como tags funcionam com vozes em portugues brasileiro — necessario testar empiricamente
- **Pronunciation dictionary para PT-BR**: Alias tags funcionam, mas phoneme tags (IPA/CMU) sao oficialmente so para ingles
- **Comparativo v3 Creative vs Natural vs Robust com exemplos de audio**: A documentacao menciona os modos mas sem exemplos A/B para ouvir
- **Reddit/Discord community tips**: Nao foi possivel acessar threads especificos do Reddit/Discord com dicas avancadas da comunidade

---

> Documento gerado por deep-research skill | 20 fontes | Pesquisa direta (subagentes hit rate limit)
> Marcacoes: [PESQUISADO] = dados de fontes verificadas | [INFERIDO] = deduzido do contexto
