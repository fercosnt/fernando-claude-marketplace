# §10.8 Fronteiras Explícitas (LOCKED)

> Contrato LOCKED — o que o plugin **NÃO faz**. Cada skill replica este bloco na sua description/SKILL.md para combater escopo creep.

## O plugin NÃO

1. **Não gera slides finais SEM PEDIDO EXPLÍCITO do usuário (D15 — emendado em v2.0.0).**
   O default continua sendo `STORYBOARD.md` (ou `POSTER.md` D8). Render para artefato visual final é atribuição **exclusiva** das skills nomeadas aqui — hoje, apenas **`deck-render-canva`** — e é sempre opt-in via `AskUserQuestion` (D16). Sem MCP do Canva conectado, o handoff nem é oferecido.

   **Permanece proibido:** PPTX, Google Slides, Figma, Gamma. E qualquer outra skill que queira gerar artefato visual final exige uma **nova decisão D** — a lista acima é enumerativa justamente para que isto continue sendo uma fronteira, e não um precedente.

   **Sem brand template, o render não gera (D19).** Quando um tipo de slide não tem brand template cadastrado para a marca, a skill **reporta e pula**. Nunca cai para geração livre. Isto não é preferência estética: no render manual de 2026-08-11, a geração livre do Canva descartou **em silêncio** o slide de disclaimer forward-looking (Res. CVM 160/22), o footnote de compliance cfo-cfm e o qualificador metodológico de um NPS — e inventou uma página de contato com placeholder de template. Base parcial e honesta é melhor que deck completo sem trava jurídica.

2. **Não busca dados em tempo real.**
   Números, métricas, citações de cases → usuário fornece. Skills perguntam quando precisam.

3. **Não faz design visual (D20).**
   `deck-image-prompts` gera **prompts** (MJ/Imagen/Nano Banana/etc.), mas designer/IA gera as imagens. `deck-render-canva` **preenche** um brand template que já existe — preencher campo não é desenhar. O output do render é explicitamente uma **base de trabalho**: o plugin entrega base, a designer entrega peça. Nenhuma skill deste plugin persegue acabamento visual final, e este é o critério objetivo de recusa a pedidos de "melhorar o design".

4. **Não chama APIs pagas sem confirmação.**
   Qualquer chamada externa (NotebookLM, MCP, API) é opt-in ou degradada quando falha.

5. **Não escreve post de redes sociais.**
   Carrossel/reel/legenda → delega `/copy` via routing matrix.

6. **Não projeta espaço/cenografia (D3).**
   Layout 3D / booth / camarote / set design → delega `skill-cenografia`.

7. **Não roda `/idea-to-brief` automaticamente.**
   Quando input é vago, orchestrator **sugere** via AskUserQuestion (D12). Usuário decide.

8. **Não cria documentação além do output.**
   STORYBOARD.md + (opcional) POSTER.md + (opcional) SIXPAGER.md + review.md + (v2.0.0) DOSSIE-*.pdf, DECKLINK-*.md e BRIEFING-*.md. Nada mais é escrito ao filesystem, e nada fora de `$DECKS_DIR`.

9. **Não imprime.**
   `deck-review-print` entrega um PDF. O plugin não tem — e não deve ter — acesso a periférico.

10. **Não publica, compartilha nem move de pasta no Canva.**
    O render entrega o link de edição ao usuário e para por aí. Nenhuma chamada de publicação, compartilhamento ou movimentação é feita. Dar acesso a outra pessoa é decisão humana.

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
- Não gera slides visuais finais — render é exclusividade de `deck-render-canva`, opt-in (D15/D16)
- Não delega automaticamente (rotas externas são opt-in)
- Não escreve fora de `$DECKS_DIR`

As 8 verticais e as 2 auxiliares **nunca passam a exigir** o MCP do Canva conectado. Com o conector desligado, elas funcionam igual e o handoff de render simplesmente não é oferecido — não aparece como opção quebrada.

## Cross-references

- `routing-matrix.md` — rotas externas (`/copy`, `skill-cenografia`, `culture-lab`, `/idea-to-brief`)
- `output-convention.md` — único filesystem location permitido (`$DECKS_DIR`)
- `nb-query-template.md` — degradação graciosa quando NB offline
