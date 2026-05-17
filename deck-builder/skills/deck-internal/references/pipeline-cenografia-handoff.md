# Pipeline `skill-cenografia` → `deck-internal concept-reveal` (D3)

Documenta o schema do handoff entre `skill-cenografia` (projeta espaco) e `deck-internal` modo `concept-reveal` (apresenta o conceito).

**Fronteira LOCKED (D3):** `deck-internal concept-reveal` **NAO projeta espaco**. Consome artefatos prontos.

---

## Fluxo correto

1. **Usuario invoca `skill-cenografia` PRIMEIRO** — fornece briefing de evento/stand/camarote
2. `skill-cenografia` (ARCHI + DECOR + VISION) gera artefatos em pasta dedicada
3. **Depois usuario invoca `deck-internal` modo `concept-reveal`** — fornece path da pasta de artefatos
4. `deck-internal concept-reveal` carrega artefatos + apresenta ao board/CEO em STORYBOARD 6-8 slides Sparkline

---

## Onde ficam os artefatos cenografia

Path default sugerido: `./cenografia/<slug>/` (relativo ao cwd) ou absoluto fornecido pelo usuario via pergunta vertical **C1**.

Exemplo Carnaval 360:
```
./cenografia/sala-vip-carnaval360-2026/
├── briefing.md
├── layout/
│   ├── planta-baixa.svg
│   ├── fluxo-visitantes.png
│   └── layout.json
├── renders/
│   ├── render-hero-sala-vip-v2.png
│   ├── render-detalhe-iluminacao.png
│   ├── render-bar-vip.png
│   └── render-area-foto.png
├── mood/
│   ├── mood-board-textura.png
│   ├── mood-board-iluminacao.png
│   └── mood-board-materiais.png
├── prompts/
│   └── nano-banana-pro-prompts.json
└── README.md  (manifesto do projeto cenografico)
```

---

## Artefatos esperados (schema do handoff)

| Artefato | Tipo | Uso no STORYBOARD concept-reveal | Obrigatorio? |
|----------|------|--------------------------------------|--------------|
| **renders/render-hero-*.png** | Imagem PNG/JPG | Visual do slide 4 "What could be" (reveal principal) | Sim |
| **renders/render-detalhe-*.png** | Imagem PNG/JPG | Visuais dos slides 5-6 (detalhes do conceito) | ≥2 imagens |
| **mood/mood-board-*.png** | Imagem PNG/JPG | Visuais auxiliares slides 5-6 (texturas, iluminacao) | ≥1 imagem |
| **layout/planta-baixa.svg** | Vetor SVG | Apendice (opcional, para perguntas board) | Opcional |
| **prompts/nano-banana-pro-prompts.json** | JSON | Campo `Prompt de imagem:` dos slides 3-6 (copiar verbatim) | Sim |
| **briefing.md** | Markdown | Big Idea sensorial (C2) + contexto narrativo | Recomendado |
| **README.md** | Markdown | Manifesto + lista de artefatos para validacao | Recomendado |

---

## Schema JSON dos prompts Nano Banana Pro (de skill-cenografia)

```json
{
  "projeto": "sala-vip-carnaval360-2026",
  "marca": "Carnaval 360",
  "data_geracao": "2026-05-XX",
  "prompts": [
    {
      "artefato": "render-hero-sala-vip-v2.png",
      "engine": "Nano Banana Pro",
      "aspect_ratio": "16:9",
      "prompt": "SUBJECT: Sala VIP de evento Carnaval 360...\nCOMPOSITION:...\nCAMERA: ...\nLIGHTING: ...\nSTYLE: ...",
      "constraints": "prohibit text overlay, prohibit artificial poses, prohibit cliche bar imagery",
      "uso_sugerido": "slide reveal principal"
    },
    {
      "artefato": "render-detalhe-iluminacao.png",
      ...
    }
  ]
}
```

`deck-internal concept-reveal` LE este JSON e usa o campo `prompt` verbatim no STORYBOARD — NAO regera prompts. Cenografia ja fez esse trabalho.

---

## Como `deck-internal concept-reveal` referencia os artefatos

Schema §10.2 do STORYBOARD tem campo `Visual:` por slide. Em modo concept-reveal:

```markdown
## Slide 4 — What Could Be (Reveal)

Tipo: conceitual
Action title: A nova sala VIP nao serve drinks — ela te reconhece
Mensagem-chave: A Eva, IA hospedeira, conhece preferencia, historia e momento de cada VIP
Speaker notes: {walk-through 1a pessoa de 2-3 paragrafos}
Visual: /Users/fernando/Cursor Repo/Eventos/cenografia/sala-vip-carnaval360-2026/renders/render-hero-sala-vip-v2.png
Prompt de imagem:
> **Nano Banana Pro** (mockup-aware, 16:9): {prompt verbatim do JSON de cenografia}
>   CONSTRAINTS: {constraints verbatim do JSON}
Tempo estimado: 90s
Objecao esperada: "IA hospedeira nao vai assustar o convidado?"
```

**Regras:**
- Campo `Visual:` SEMPRE com path **absoluto** (NAO relativo) para o render
- Campo `Prompt de imagem:` copia o bloco do JSON de cenografia verbatim
- NAO regerar prompt (deck-internal nao tem dominio de tecnica cinematografica de espaco — cenografia tem)

---

## Validacao dos artefatos (passo 8 do protocolo deck-internal)

Antes de gerar slides 3-6, validar:

```python
# Pseudo-codigo do passo de validacao
cenografia_dir = Path(C1)  # de pergunta vertical
if not cenografia_dir.exists():
    raise UserError(
        "Pasta de artefatos cenografia nao encontrada em {cenografia_dir}. "
        "Rode skill-cenografia primeiro, depois invoque deck-internal concept-reveal novamente."
    )

required = [
    "renders/render-hero-*.png",   # pelo menos 1
    "renders/render-detalhe-*.png", # pelo menos 2
    "mood/mood-board-*.png",        # pelo menos 1
    "prompts/nano-banana-pro-prompts.json",  # obrigatorio
]

faltantes = check_glob_patterns(cenografia_dir, required)
if faltantes:
    raise UserError(
        f"Artefatos cenografia incompletos: {faltantes}. "
        f"Rode skill-cenografia para completar antes."
    )
```

Se artefatos incompletos → **PARA e instrui usuario a rodar `skill-cenografia` primeiro**. NAO improvisar.

---

## Por que essa fronteira existe (D3)

Sem essa fronteira, `deck-internal` tentaria projetar espaco — algo que requer expertise de arquitetura efemera, materiais, iluminacao cenica, fluxo de visitantes. `skill-cenografia` ja faz isso bem (ARCHI + DECOR + VISION).

Duplicar trabalho seria:
- Ruim para qualidade (deck-internal nao tem references de Casacor, Balich, Bureau Betak)
- Caro para usuario (regerar prompts ja gerados)
- Confuso para fluxo (qual skill projeta? qual apresenta?)

**Solucao:** D3 LOCKED. Cenografia projeta; deck-internal apresenta.

---

## Quando usuario nao tem cenografia rodada ainda

Se usuario invoca `/deck preciso apresentar conceito da sala VIP` mas NAO rodou `skill-cenografia`:

1. `deck-orchestrator` detecta `conceito` + `sala` → roteia `deck-internal concept-reveal`
2. `deck-internal` pergunta C1 (path artefatos)
3. Usuario: "ainda nao gerei"
4. `deck-internal` PARA e sugere:
   > "Concept reveal precisa de renders/mood/layout prontos. Sugiro rodar `skill-cenografia` primeiro para projetar a sala VIP (eles geram renders Nano Banana Pro + mood + layout). Depois invoca `deck-internal concept-reveal` com o path da pasta. Quer que eu chame `skill-cenografia` agora?"
5. Se sim → delega para skill-cenografia; senao espera usuario rodar.

---

## Marcas suportadas pela cenografia (referencia cruzada)

- **Fotona** (compliance_tags `anvisa-laser-classe-iii`): estande premium, paleta preto/branco/vermelho. Concept-reveal apresenta como tecnologia elegante minimalista.
- **Beauty Smile**: design_system_skill `beauty-smile-design-system`. Cores deep blue/turquoise/gold. Concept-reveal puxa tokens automaticamente.
- **Carnaval 360**: cores quentes (vermelho ginga, amarelo samba) + frias (azul mare alta, verde agua coco). Concept-reveal apresenta como sofisticacao com energia.

---

## Exemplo de fluxo end-to-end (Case 2 do eval)

1. Usuario: "preciso apresentar conceito da Sala VIP Carnaval 360 com IA hospedeira pro board, eles precisam aprovar R$1.5M"
2. Orchestrator detecta `conceito` + `sala VIP` + `Carnaval 360` → `deck-internal concept-reveal` + auto-detect Carnaval 360
3. `deck-internal` roda U1-U6 + I1-I5 + **C1 + C2**
4. Usuario informa C1 = `/Users/fernando/Cursor Repo/Eventos/cenografia/sala-vip-carnaval360-2026/`
5. `deck-internal` valida artefatos (renders/mood/prompts) → OK
6. Consulta NB1 sobre Sparkline Duarte + Big Idea sensorial (C2)
7. Gera 8 slides STORYBOARD modo concept-reveal:
   - Slide 1: capa mood (visual = mood-board-iluminacao.png)
   - Slide 2: Big Idea sensorial (texto)
   - Slide 3: What is (sala VIP generica, sem visual de cenografia — gera prompt minimalista via deck-image-prompts)
   - Slide 4: What could be (visual = render-hero-sala-vip-v2.png, prompt copiado verbatim do JSON cenografia)
   - Slides 5-6: detalhes do conceito (visuais = render-detalhe-iluminacao.png + mood-board-textura.png + render-bar-vip.png)
   - Slide 7: Ask R$1.5M + cronograma
   - Slide 8: Proximos passos
8. Output STORYBOARD com paths absolutos nos campos Visual:
9. Sugere `/deck review` para validar Sparkline (2 vales antes do reveal slide 4)
