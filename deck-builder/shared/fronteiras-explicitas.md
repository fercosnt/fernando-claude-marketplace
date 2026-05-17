# §10.8 Fronteiras Explícitas (LOCKED)

> Contrato LOCKED — o que o plugin **NÃO faz**. Cada skill replica este bloco na sua description/SKILL.md para combater escopo creep.

## O plugin NÃO

1. **Não gera slides finais (PPTX/Gamma/Figma).**
   Só gera `STORYBOARD.md` (ou `POSTER.md` D8). O usuário/designer/IA visual gera os slides a partir do storyboard.

2. **Não busca dados em tempo real.**
   Números, métricas, citações de cases → usuário fornece. Skills perguntam quando precisam.

3. **Não faz design visual.**
   `deck-image-prompts` gera **prompts** (MJ/Imagen/Nano Banana/etc.), mas designer/IA gera as imagens.

4. **Não chama APIs pagas sem confirmação.**
   Qualquer chamada externa (NotebookLM, MCP, API) é opt-in ou degradada quando falha.

5. **Não escreve post de redes sociais.**
   Carrossel/reel/legenda → delega `/copy` via routing matrix.

6. **Não projeta espaço/cenografia (D3).**
   Layout 3D / booth / camarote / set design → delega `skill-cenografia`.

7. **Não roda `/idea-to-brief` automaticamente.**
   Quando input é vago, orchestrator **sugere** via AskUserQuestion (D12). Usuário decide.

8. **Não cria documentação além do output.**
   STORYBOARD.md + (opcional) POSTER.md + (opcional) SIXPAGER.md + review.md. Nada mais é escrito ao filesystem.

## Pipeline cenografia → concept-reveal (D3)

Única exceção onde uma skill externa é parte integrante do fluxo do plugin:

```
1. Usuário: "/deck preciso apresentar conceito da Sala VIP Fotona pro CEO"
2. orchestrator detecta "conceito" + "sala" → roteia deck-internal modo concept-reveal
3. deck-internal SUGERE: "Antes do storyboard, /skill-cenografia para gerar
   renders + JSON Nano Banana Pro + mood board?"
4. Se sim: usuário roda /skill-cenografia ANTES, gera artefatos em
   ~/Documents/cenografia/{projeto}/
5. deck-internal CONSOME paths absolutos dos artefatos como `Prompt de imagem`
   verbatim (não regenera prompts — usa os do cenografia)
6. Output: STORYBOARD.md focado em vender o conceito visualmente pro board
```

**Inviolável (D3):** `deck-internal concept-reveal` não chama `skill-cenografia` direto — sempre via AskUserQuestion. Usuário roda manualmente.

## DoD por skill — fronteiras

Cada SKILL.md deve declarar explicitamente na seção "O que esta skill NÃO faz":
- Não gera slides visuais finais
- Não delega automaticamente (rotas externas são opt-in)
- Não escreve fora de `$DECKS_DIR`

## Cross-references

- `routing-matrix.md` — rotas externas (`/copy`, `skill-cenografia`, `culture-lab`, `/idea-to-brief`)
- `output-convention.md` — único filesystem location permitido (`$DECKS_DIR`)
- `nb-query-template.md` — degradação graciosa quando NB offline
