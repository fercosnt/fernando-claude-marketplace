# Voice Cloning — Calibracao de Tom e Bloqueio de Cliches

Workflow para personalizar a voz da marca/perfil e eliminar tom sintetico de IA.

## Por Que Voice Cloning

54% dos consumidores ja identificam conteudo gerado por IA. O problema nao e usar IA — e soar como IA. Voice cloning resolve isso calibrando a geracao com o tom real do usuario.

## Workflow de Calibracao

### Passo 1: Coletar Amostras

Pedir ao usuario 3-5 textos que representam seu tom. Podem ser:
- Posts anteriores que performaram bem
- Textos do site/bio
- Mensagens de WhatsApp/DM (tom informal natural)
- Transcricoes de audio/video (tom falado)
- Emails para clientes

**Minimo:** 3 amostras. **Ideal:** 5 amostras variadas (formal + informal).

### Passo 2: Analisar Padroes

Extrair de cada amostra:

| Dimensao | O que observar | Exemplo |
|----------|---------------|---------|
| **Formalidade** | Nivel 1-5 (casual → formal) | "3 = conversa entre amigos profissionais" |
| **Humor** | Tipo e frequencia | "Ironia sutil, 1-2 por post, nunca no CTA" |
| **Vocabulario** | Palavras recorrentes, girias | "Sempre usa 'brabo', evita 'maravilhoso'" |
| **Tamanho de frase** | Curta/media/longa | "Frases curtas, max 15 palavras" |
| **Emojis** | Quais e onde | "🔥 e 👇 apenas, nunca mais de 2" |
| **Pontuacao** | Estilo | "Sem ponto final em frases curtas" |
| **Estrutura** | Como organiza ideias | "Sempre abre com pergunta" |
| **Girias/regionalismos** | Expressoes locais | "PT-BR informal, sem anglicismos" |

### Passo 3: Criar Voice Profile

Documento resumo com os padroes. Formato:

```
## Voice Profile — [Nome/Marca]

**Tom geral:** [descricao em 1 frase]
**Formalidade:** [1-5]
**Humor:** [tipo + frequencia]
**Vocabulario preferido:** [lista de palavras/expressoes que USA]
**Vocabulario proibido:** [lista de palavras/expressoes que NUNCA usa]
**Estrutura tipica:** [como organiza frases]
**Emojis:** [quais + onde]
**Pontuacao:** [estilo]

### Exemplo de Tom Ideal
[1 paragrafo que captura perfeitamente o tom]

### Exemplo de Tom a Evitar
[1 paragrafo que representa o oposto]
```

### Passo 4: Aplicar na Geracao

Ao gerar copy, incluir o voice profile como restricao:
- Antes de gerar, reler o voice profile
- Apos gerar, comparar com as amostras originais
- Se destoar, ajustar e regenerar

### Passo 5: Bloqueio de Cliches

Lista de frases PROIBIDAS — soam como IA generica:

**Nivel 1 — Cliches Mortais (nunca usar):**
- "Desbloqueie seu potencial"
- "Transforme sua vida"
- "Leve para o proximo nivel"
- "Descubra o segredo"
- "Revolucionario"
- "Game changer"
- "Potencialize seus resultados"
- "Jornada de transformacao"
- "Conteudo de valor"
- "Estrategia infalivel"
- "O guia definitivo"
- "Tudo que voce precisa saber"
- "Nao vai acreditar"
- "Imperdivel"
- "Exclusivo"

**Nivel 2 — Cliches de Abertura (evitar):**
- "Voce sabia que..."
- "Nos dias de hoje..."
- "Em um mundo cada vez mais..."
- "Nao e segredo que..."
- "A verdade e que..."
- "Confesso que..."

**Nivel 3 — Cliches de CTA (substituir):**
- "Clique no link da bio" → "Comenta [PALAVRA] que eu te mando"
- "Compartilhe com seus amigos" → "Manda pra quem precisa ouvir isso"
- "Siga para mais conteudo" → "Tem mais [topico] vindo essa semana"
- "Deixe seu like" → [nao pedir like, foco em save/comment]

## Tecnica de Comandos Negativos

Ao gerar copy, alem de dizer O QUE fazer, especificar O QUE NAO FAZER:
- "NAO use adjetivos superlativos sem dados"
- "NAO abra com pergunta retorica cliche"
- "NAO use mais de 2 emojis por paragrafo"
- "NAO termine com 'E voce, o que acha?'" (cliche de IA)

## Recalibracao

Revisitar voice profile a cada 30 dias ou quando:
- Feedback do usuario indica que tom mudou
- Posts nao estao performando como esperado
- Mudanca de estrategia de conteudo
