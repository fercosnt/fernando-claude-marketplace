# Changelog

Todas as mudanças notáveis do plugin `deck-builder` são documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/) e versionamento [SemVer](https://semver.org/).

## [2.0.0] - 2026-08-23

> **Breaking change sem mudanca de schema.** O que quebrou foi um contrato LOCKED de **comportamento**: a Fronteira nº 1 (`shared/fronteiras-explicitas.md`) dizia que o plugin nunca gera slides finais. Passa a dizer "nao gera **sem pedido explicito**", nomeando as skills autorizadas. Nenhuma alteracao no schema `STORYBOARD.md` v1.1, que segue LOCKED.
>
> **Estado:** Blocos C, A e D implementados e exercitados em deck real. Do Bloco B, o modo `anotar` entra; o modo `render` fica para o 2.1 (bloqueado por conta do Canva). Ver "Escopo do 2.0.0" no fim desta entrada.

### Added — `deck-review-print` (Bloco A, RF-01..RF-19)

Skill nova, **12ª do plugin**. Unica skill que **consome** um deck em vez de produzir um: pega Canva/PPTX/PDF e devolve `DOSSIE-{slug}-{HHmm}.pdf` — copia A4 preto sobre branco, numerada e anotavel a caneta.

- **`skills/deck-review-print/SKILL.md`** — pipeline de 5 passos (dependencias → ingestao → classificacao → transcricao → composicao/medicao), 3 modos de saida, fronteiras proprias.
- **`shared/print-dossie-schema.md`** (NOVO) — contrato do artefato: estrutura da entrada em 4 zonas, regra de numeracao espelhada (D18), marcacao `[CONFERIR]` (D17), tematizacao por marca, e o que o numero de TAC significa e o que nao significa.
- **`scripts/measure-tac.py`** (NOVO) — mede TAC de PDF/imagem, compara original vs dossie e reporta o fator de reducao. Exit 1 acima do alvo, para uso em eval. Repete a ressalva metodologica no proprio output.
- **`scripts/check-print-deps.sh`** (NOVO) — diagnostico de dependencias por rota. Ausencia de dep exclusiva de uma rota desabilita **apenas** aquela rota (RNF-09); nucleo incompleto bloqueia e instrui a instalacao.
- **`assets/templates/dossie-layout.html`** (NOVO) — template A4 com `@page`, 2 entradas por folha, miniatura <= 62 mm, moldura tracejada para slide `foto`, pauta proporcional, tabela em fio fino, resumo final. Degrada em cinza neutro quando `brands.yaml` falta.
- **`assets/checklists/conferencia-tabelas.md`** (NOVO) — checklist obrigatorio pre-entrega. Existe por causa do Risco nº 1 do PRD: um digito trocado chega ao presidente como se fosse o original.
- **3 references** — `ingestao-3-fontes.md`, `classificacao-slides.md`, `modos-saida.md`.
- **`evals/review-print-cases.md`** (NOVO) — 10 cases sobre a fixture **W4 GLP1TIGHT** (baseline: 6 paginas, 16,8% TAC).

- **`INSTALL.md`** (NOVO) — instrucoes de instalacao por plataforma (macOS / Debian-Ubuntu), dependencia a dependencia, com a distincao entre nucleo e rotas opcionais. Documenta a armadilha do `pip` solto em maquinas com pyenv/mise/asdf/venv, que foi como a primeira instalacao falhou silenciosamente.
- **`scripts/requirements-print.txt`** (NOVO) — pacotes Python, instalaveis com `python3 -m pip install -r`.
- **`check-print-deps.sh`** agora imprime o caminho do `python3` ativo na primeira linha e sugere `python3 -m pip` em vez de `pip`.
- **`README.md`** — secao de instalacao para maquina nova + `deck-review-print` na tabela de skills (11 → 12).

- **Instalacao via venv do projeto** — `check-print-deps.sh` procura `<repo>/.venv` automaticamente (ordem: `$DECK_PY` → `.venv` → `python3`/`py`/`python`). Resolve de uma vez os dois modos de falha reais encontrados no setup: o bloqueio **PEP 668** do Homebrew Python e a ambiguidade de qual `python3` o script usa quando a maquina tem pyenv/mise/asdf. `INSTALL.md`, `README.md` e `requirements-print.txt` passam a documentar o venv como caminho principal.

### Changed — correcoes da primeira execucao real (2026-08-12)

Primeira passagem completa da skill sobre a fixture GLP1TIGHT. Tres correcoes vindas do confronto com o deck de verdade:

- **D24 reescrito pela terceira vez — o TAC saiu do classificador.** A v1 usava limiar absoluto (150%), a v2 baseline relativa a mediana do deck. As duas estavam **erradas, nao mal calibradas**: na execucao, fotos mediram 65% e 273% e conteudo mediu 37% e 266%. Num fundo escuro chapado a foto e frequentemente mais clara que o fundo, e o sinal se inverte. A v2 chegou a classificar **zero** slides como foto. Classificacao passa a ser estrutura tabular → densidade de texto → leitura visual; o TAC continua medido e reportado como metrica de tinta, funcao na qual reproduziu o piloto quase slide a slide (193% x 17 paginas).
- **Auditoria aritmetica entra no contrato, com marcacao `[DIVERGE]`.** A execucao encontrou erro real no deck do cliente: slide 13, linha *Massa muscular*, celulas somam 28 e o total declara 27X. Achado por habito, nao por exigencia da skill — agora e item obrigatorio do checklist. A skill **transcreve o valor do slide como esta** e sinaliza; corrigir e decisao de quem escreveu o deck.
- **Sao 4 tabelas, nao 3.** O slide 07 e comparativo em duas colunas e nao era contado.

**Execucao real de ponta a ponta (2026-08-12), fixture GLP1TIGHT (`DAHKNdTNVwI`, 17 slides):**

| | Resultado |
|---|---|
| Ingestao | 17 PNGs via `read-design` → `get-export-formats` → `export-design` |
| Original | **193% TAC medio x 17 paginas** — reproduziu o piloto quase slide a slide |
| Dossie | **7 paginas · 17,1% TAC medio** (alvo <= 25%) |
| Reducao | produto 3.281 → 120 — aproximadamente **27x** menos tinta |
| Tabelas | 4 transcritas por leitura visual, todas `[CONFERIR]` |
| Divergencia | 1 encontrada e marcada `[DIVERGE]` (slide 13) |
| Privacidade | slide 10 (antes/depois de pacientes) entrou sem nenhum pixel, mantendo o numero |
| Numeracao | 17 entradas, 01..17, D18 respeitado |

O piloto manual de 2026-08-10 tinha registrado 6 paginas / 16,8%. A execucao real deu 7 / 17,1% porque inclui **4 tabelas** (o piloto contava 3) e os blocos de auditoria aritmetica, que nao existiam.

- **`measure-tac.py` ganhou fallback PyMuPDF** — rasteriza PDF sem o binario `pdftoppm`. Alternativa util onde instalar poppler e trabalhoso (notadamente Windows). Preferencia: `pdftoppm` → `pymupdf` → erro acionavel.

### Added — `deck-render-canva` e a camada de anotacao (Blocos B e D)

Skill nova, **13ª do plugin**, com dois modos independentes:

- **`anotar`** — escreve o briefing de montagem nas notas de cada pagina de um design existente e publica o comentario-indice. **Nao depende de brand template.** Foi por aqui que a hipotese do Epico C foi validada em campo: a redatora recebeu o deck anotado, montou em cima e respondeu **"nao abri o markdown"**.
- **`render`** — preenche brand template. **Bloqueado**: a conta nao tem brand template e `publish-brand-template` falha (escopo `brandtemplate:content:write` ausente, ou recurso de plano Teams/Enterprise).

Separar os dois foi decisao de realidade — a metade que funciona nao podia ficar refem da que esta travada.

- **`shared/briefing-annotation-contract.md`** (NOVO) — formato v2 do bloco, os 4 rotulos, limites duros do canal, campo compartilhado (D22), limpeza com arquivamento (D26), comentario-indice.
- **`shared/canva-render-contract.md`** (NOVO) — regras de edicao programatica, medidas em execucao real.
- **2 references + 10 eval cases** sobre a fixture Beauty Smile.

### Changed — formato do briefing (v2), a pedido da usuaria

A redatora pediu "tamanhos de letra diferentes e pular linhas" nas notas. Quebra de linha e hierarquia foram atendidas: rotulo em linha propria, corpo indentado, linha em branco entre blocos. **Tamanho de fonte e impossivel** — `replace_speaker_notes` aceita texto puro. Os 13 briefings foram reescritos e regravados no Canva (517–713 chars, teto 900).

### Added — baseline de regressao

- **`evals/baselines/W4-glp1tight-review-print.md`** (NOVO) — registro da execucao real: 17 entradas, 7 paginas, 17,1% TAC, ~27x de reducao, 4 tabelas, 1 divergencia aritmetica, TAC por slide, classificacao de referencia e as 7 falhas que o fixture pega.
- **`evals/baselines/` e um diretorio novo**, separado de `evals/fixtures/`. Motivo empirico: o `lint-storyboard-schema.sh` casa com `W*.md`, e o baseline colocado em `fixtures/` era capturado pelo glob e contado como FAIL, mudando o guardrail de 3 para 4 arquivos. Fixture de storyboard e baseline de execucao sao artefatos diferentes e nao dividem diretorio.

### Escopo do 2.0.0 — o que entra e o que fica para depois

**Entra:** Blocos C (contratos), A (`deck-review-print`) e D (camada de anotacao), mais o modo `anotar` do `deck-render-canva`. Os tres foram exercitados em deck real e o Bloco D teve a hipotese **validada em campo**.

**Fica para o 2.1:** o modo `render` do `deck-render-canva`. Esta bloqueado por conta, nao por codigo — a conta nao tem brand template e `publish-brand-template` falha por escopo `brandtemplate:content:write` ausente (ou por ser recurso de plano Teams/Enterprise). Publicar 2.0.0 com uma skill declarada e inoperante seria anunciar capacidade inexistente, que e exatamente o erro que este ciclo passou corrigindo.

O `SKILL.md` do `deck-render-canva` declara o modo `render` como bloqueado e nao o oferece quando nao ha template — degradacao explicita, nao falha silenciosa.

### Fixed — divida pre-existente do lint

- **As fixtures W1-W3 voltaram a passar no `lint-storyboard-schema.sh`.** As tres falhavam por `Meta sem campo: 'Modo de entrega:'`, campo que o schema v1.1 tornou obrigatorio e ao qual nunca foram migradas. O linter estava certo; os arquivos e que ficaram para tras.

  Resultado: **3 FAIL / 3 → 0 FAIL / 3**. Contando o `BAD-incomplete-meta.md`, que deve falhar por design: **1 FAIL / 4 arquivos**, exatamente o teste negativo.

  Os valores nao foram derivados do campo `Formato` — foram lidos das versoes completas dos mesmos storyboards, que declaram `hibrido` nos tres casos. Derivar do formato teria produzido `apresentado-ao-vivo` no W2 e no W3, que seria errado: a aula distribui material pos-aula e o pitch ao CEO entrega um 6-pager impresso.

  O guardrail do PRD ("lint passa em 100% das fixtures") volta a significar alguma coisa. Enquanto estava em 0%, o criterio real era "mesmo numero de falhas antes e depois", que detecta regressao nova mas nao valida nada.

### Escopo do 2.0.0 — o que entra e o que fica para depois

**Entra:** Blocos C (contratos), A (`deck-review-print`) e D (camada de anotacao), mais o modo `anotar` do `deck-render-canva`. Os tres foram exercitados em deck real e o Bloco D teve a hipotese **validada em campo**.

**Fica para o 2.1:** o modo `render` do `deck-render-canva`. Esta bloqueado por conta, nao por codigo — a conta nao tem brand template e `publish-brand-template` falha por escopo `brandtemplate:content:write` ausente (ou por ser recurso de plano Teams/Enterprise). Publicar 2.0.0 com uma skill declarada e inoperante seria anunciar capacidade inexistente, que e exatamente o erro que este ciclo passou corrigindo.

O `SKILL.md` do `deck-render-canva` declara o modo `render` como bloqueado e nao o oferece quando nao ha template — degradacao explicita, nao falha silenciosa.

### Conhecido — divida pre-existente, nao introduzida aqui

- **As fixtures W1-W3 nao passam no lint desde antes desta mudanca.** As tres falham por `Meta sem campo: 'Modo de entrega:'`, campo que o schema v1.1 tornou obrigatorio e ao qual as fixtures nunca foram migradas. Baseline em `main` verificado antes e depois: **3 FAIL / 3 arquivos, identico**. Esta entrega nao introduziu regressao — o diff nao toca fixtures, script de lint nem `storyboard-schema.md`.

### Changed — contratos compartilhados

- **`shared/fronteiras-explicitas.md`** — Fronteira nº 1 emendada conforme **D15**, em redacao **enumerativa**: render e atribuicao exclusiva de `deck-render-canva`, sempre opt-in (D16), e qualquer nova skill de render exige nova decisao D. PPTX/Google Slides/Figma/Gamma seguem proibidos. Fronteira nº 3 esclarecida com **D20** (preencher template ≠ desenhar; o plugin entrega base, a designer entrega peca). Fronteira nº 8 estendida aos 3 artefatos novos. Duas fronteiras novas: nº 9 (nao imprime — entrega PDF) e nº 10 (nao publica, compartilha nem move de pasta no Canva).
- **`shared/output-convention.md`** — 3 artefatos novos na tabela de anexos: `DOSSIE-{slug}-{HHmm}.pdf`, `DECKLINK-{slug}-{HHmm}.md` e `BRIEFING-{slug}-{HHmm}.md`. Nota explicita de que **STORYBOARD e documento de autoria, nao de execucao** — quem revisa e monta precisa de view reduzida, e o schema v1.1 nao deve ser amputado para resolver isso.
- **`shared/routing-matrix.md`** — 2 rotas internas de ciclo (`deck-review-print`, `deck-render-canva`) + secao propria documentando a degradacao obrigatoria sem MCP do Canva.
- **11 SKILL.md** — bloco de fronteiras atualizado com D15 nas 11 skills. `deck-scientific` ganhou secao `## Fronteiras (§10.8)`, que nao tinha.

### Added — handoff opt-in

- **Bloco `## Handoff: render no Canva`** nas **8 verticais** (fundraising, sales, clinical, equipment, teaching, proposal, internal, scientific): 13 linhas, oferta via `AskUserQuestion`, nunca automatica. Com o MCP do Canva desconectado o handoff **nao e oferecido** — nem como opcao quebrada. As 8 verticais continuam funcionando sem Canva.

### Decisoes novas (D15–D26)

| # | Decisao |
|---|---------|
| D15 | Fronteira nº 1 emendada, de forma enumerativa — render so por pedido explicito, so pelas skills nomeadas |
| D16 | Render e sempre opt-in via `AskUserQuestion`; sem MCP conectado, nem e oferecido |
| D17 | Transcricao de tabela e sempre visual (imagem do slide, nunca o texto corrido da API); toda tabela sai `[CONFERIR]` |
| D18 | Numeracao espelhada — todo artefato derivado preserva a numeracao do deck de origem |
| D19 | Sem brand template, sem geracao livre — reporta e pula |
| D20 | O plugin entrega base, a designer entrega peca |
| D21 | Nenhum artefato de handoff sai sem a instrucao de como usa-lo |
| D22 | Speaker notes sao campo compartilhado, delimitado por marcador (briefing de montagem + notas do apresentador) |
| D23 | A camada de anotacao e uma view, nao uma copia — teto de 900 chars, 4 rotulos fixos (`PROVAR`/`ESCREVER`/`NAO MEXER`/`DECIDIR`) |
| D24 | **O TAC mede tinta, nao classifica slide** — classificacao e estrutura tabular → densidade de texto → leitura visual |
| D25 | `deck-review-apply` e modo (`--modo aplicar`) do `deck-review-print`, nao skill propria |
| D26 | O briefing e editavel; a limpeza arquiva no `DECKLINK` o que foi escrito a mao antes de remover |

### Evidencia de campo para D19

Render manual em 2026-08-11 (design `DAHSC1Q6iNA`): a geracao livre do Canva, sem brand template, **descartou em silencio** o slide de disclaimer forward-looking (Res. CVM 160/22), o footnote de compliance cfo-cfm ("autoreporte, nao auditada por terceiros nesta fase"), o qualificador metodologico do NPS ("n=131, metodologia Bain") e 3 numeros do storyboard — e inventou uma pagina de contato com placeholder de template (`hello@reallygreatsite`). D19 deixa de ser preferencia estetica e vira trava de compliance.

## [1.2.0] - 2026-05-17

### Added

- **`deck-reviewer` Critico 4 — VERIFICAR Auditor** — quarto critico adversarial dedicado a absorver as marcações `[VERIFICAR: descricao]` introduzidas em v1.1. Workflow expandido de 3 para 4 passes sequenciais.
- **`shared/.../skills/deck-reviewer/references/critico-verificar.md`** (NOVO) — documenta:
  - Algoritmo de coleta via regex `\[VERIFICAR:[^]]+\]`
  - Mapeamento ao slide (incluindo tipo + bloco interno onde flag aparece)
  - Classificação automática de severidade baseada no tipo do slide:
    - `CTA` / `disclaimer` / `compliance` → 🔴 BLOCKER (decisor)
    - `dados` / `financeiro` / `prova-social` / `problema/comparativo com número` → 🟡 MAJOR
    - `equipe` / `conceitual` / `contexto` / `capa` / `demo` → 🟢 MINOR
    - `apêndice` / `agradecimento` → ignorado
  - Ajustes contextuais (modo_entrega=enviado-para-leitura escala 🟢→🟡; compliance tags clínicas escalam 🟡→🔴; flag em Speaker notes downgrade em modo enviado)
- **Bloco `## Audit [VERIFICAR] flags` no review.md** — dedicado, alem do bloco geral de severidade. Lista flags por severidade com slide afetado + texto da flag + sugestão concreta de fonte/ação + totais + densidade.
- **Caso especial: 0 flags** — bloco gera warning de potencial over-claiming (skill pode ter inventado dados sem flagar).
- **Eval case 5** — W1 v1.1 Beauty Smile pitch anjo (22 flags reais) como fixture viva, valida 3 🔴 + 14 🟡 + 5 🟢 com classificação esperada documentada.
- **Recommended next action consolidada (4 críticos)** — regra v1.2 considera flags VERIFICAR:
  - 1+ 🔴 em CTA/disclaimer → "Resolver N blocker(s) E confirmar dado(s) decisor(es) com fonte antes de apresentar"
  - Total flags ≥ 10 sem 🔴 → "Confirmar N dados com fonte antes de apresentar — alta densidade de inferencias"

### Changed

- **`deck-reviewer/SKILL.md`** workflow de 3 para 4 passes; novo schema do output com Meta expandida (modo_entrega, total flags por severidade) + bloco dedicado.
- **`shared/verificar-flag.md`** seção "O que o reviewer faz com flags" reescrita para refletir o Critico 4 com algoritmo completo (coleta → mapeamento → classificação automática → bloco dedicado → ajustes contextuais → contribuição para recommended action).
- **DoD `deck-reviewer`** atualizado: 5 eval cases (era 4); 4 críticos como passes sequenciais (era 3); leitura de `modo_entrega` da Meta; bloco `## Audit [VERIFICAR]` no output.

### Validation

Prova de conceito: `STORYBOARD-beauty-smile-pitch-anjo.review.md` gerado aplicando os 4 críticos contra W1 v1.1 (22 marcações [VERIFICAR] reais). Resultado:
- 3 🔴 BLOCKER (TCLE quote slide 9 + SAFE BR slide 12 + Res. CVM 160/22 slide 13)
- 14 🟡 MAJOR (dados de problema/dados/financeiro/prova-social/roadmap)
- 5 🟢 MINOR (KPIs capa + bios equipe)
- Critico 1 (Clareza): 0 issues — STORYBOARD v1.1 estruturalmente impecável
- Critico 2 (Persuasão): 0 issues estruturais — hook + CTA passam filtros
- Critico 3 (SUCCESs): 0 issues — todos os 6 elementos cobertos
- Recommended action: "Resolver 3 blockers E confirmar 14 dados com fonte antes de apresentar — alta densidade de inferências"

### Why v1.2

Em v1.1, as skills verticais ganharam disciplina `[VERIFICAR]` para flagar dados inferidos (NPS, %, R$, papers, registros regulatórios). Mas o `deck-reviewer` ainda ignorava essas flags — passava direto sem capturar. v1.2 fecha a alça: agora o reviewer absorve as flags, classifica severidade automaticamente baseado no tipo do slide, e produz um bloco dedicado no review.md listando exatamente o que precisa ser confirmado antes da apresentação. Combinado com os outros 3 críticos, o usuário tem uma audit list completa para resolver entre a geração do STORYBOARD e a apresentação real.

## [1.1.0] - 2026-05-17

### Added

- **`modo_entrega` em `## Meta`** — derivado de U4. Valores: `apresentado-ao-vivo` (U4=1/2), `enviado-para-leitura` (U4=3), `hibrido` (U4=4). Adapta densidade dos slides (minimalista para apresentado vs denso para enviado).
- **Bloco `Conteúdo do slide (visível na projeção)`** em cada slide — separa o que aparece no slide do que o apresentador fala (speaker notes). Densidade calibrada ao `modo_entrega`. Resolve issue: slides minimalistas demais quando deck é enviado para leitura.
- **Bloco `Layout sugerido`** em cada slide — handoff explícito para designer / Gamma / Claude Design / PowerPoint com grid + tipografia + componentes visuais + animação. Resolve issue: instruções vagas para construção visual.
- **Formato `Imagens sugeridas` reformatado** — Quantidade declarada explicitamente (1 imagem hero com 3 variações vs N imagens distintas) + cada variação em bloco markdown separado com 6 campos labeled (Aspect ratio / Estilo / Composição / Prompt / Negative / Mood ref). Resolve issue: prompts confusos com config misturada com prompt.
- **`[VERIFICAR]` flag** — disciplina anti-fabricação. Toda data específica inferida (R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa) sem fonte conferida pela skill marca `[VERIFICAR: descrição]`. Documentado em novo `shared/verificar-flag.md`. Lint v1.1 emite WARN quando ausente. Reviewer converte flags em 🟡 ou 🔴.
- **Bold opcional nos rótulos** (`**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**`, etc.) — facilita scan visual ao revisar STORYBOARD. Lint aceita ambos formatos (texto puro e bold).
- **Adendo v1.1 em todas as 8 verticais** — cada SKILL.md das skills verticais documenta as 4 disciplinas novas (modo_entrega / Conteúdo do slide / Layout sugerido / [VERIFICAR]).

### Changed

- **Lint script `lint-storyboard-schema.sh`** atualizado:
  - Regex aceita campos com bold opcional (`\*?\*?Field:\*?\*?`)
  - Adicionado check obrigatório: `Modo de entrega:` em Meta (13 campos no total agora)
  - Adicionado check (WARN): bloco `Conteúdo do slide` em cada slide
  - Adicionado check (WARN): bloco `Layout sugerido` em cada slide
  - Adicionado check (WARN): dados R$/%/n=/RCT/NPS/GRADE sem `[VERIFICAR]` flag
  - Header de usage atualizado para refletir validações v1.1
- **Schema `storyboard-schema.md`** reformulado com 3 regras adicionais (7, 8, 9):
  - Regra 7: Conteúdo do slide adaptado ao `modo_entrega`
  - Regra 8: Layout sugerido obrigatório em cada slide
  - Regra 9: `[VERIFICAR]` em dados fabricados
- **`deck-image-prompts/SKILL.md`** seção "Formato de output" reformulada com novo bloco `Imagens sugeridas:` (Quantidade + 3 variações em blocos separados). Formato v1.0 deprecated mas ainda aceito pelo lint para retrocompatibilidade.
- **`entrevista-universal-u1-u6.md`** documenta como `modo_entrega` deriva de U4 + impacto explícito no STORYBOARD (densidade vs speaker notes).

### Migration v1.0 → v1.1

STORYBOARDs gerados em v1.0 ainda passam o lint v1.1 EXCETO no novo campo obrigatório `Modo de entrega:` em Meta. Para migrar manualmente:

1. Adicionar `- Modo de entrega: <apresentado-ao-vivo|enviado-para-leitura|hibrido>` em `## Meta` (derive de U4 / Formato).
2. Para cada slide, adicionar bloco `Conteúdo do slide` extraindo bullets implícitos da Mensagem-chave + Speaker notes.
3. Para cada slide, adicionar bloco `Layout sugerido` (grid + tipografia + componentes + animação).
4. Reformatar bloco `Prompt de imagem` em `Imagens sugeridas` com Quantidade explícita + variações em blocos.
5. Marcar dados fabricados com `[VERIFICAR: descrição]`.
6. (Opcional) Bold nos rótulos: `Tipo:` → `**Tipo:**`.

### Why v1.1

Após o build v1.0 ser validado por simulação com lint PASS em 3 walkthroughs, o usuário forneceu feedback substantivo (UAT humano real) apontando 4 issues estruturais:

1. Speaker notes dominam o conteúdo, slide visual fica vazio
2. Falta pergunta "deck será apresentado ou enviado?" — densidade adaptativa ausente
3. Instruções para handoff visual (Claude Design / Gamma / PowerPoint) fracas
4. Prompts de imagem confusos (quantidade, config vs prompt, qualidade)

Adicionalmente, durante o feedback foi identificado que skills inventam números plausíveis (NPS 91 n=131, "40% fecharam", papers RCT fabricados) sem flag — risco de over-claiming em apresentação real. v1.1 introduz `[VERIFICAR]` para resolver.

Esse é exatamente o "ponto de falsificação do trade-off D1" previsto no PRD §9 risco #1 — input humano real captou o que a simulação determinística não pegou.

## [1.0.0] - 2026-05-17

### Added

- **11 skills** completas: `deck-orchestrator` (entrypoint) + 8 verticais (`deck-fundraising`, `deck-sales`, `deck-clinical`, `deck-equipment`, `deck-teaching`, `deck-proposal`, `deck-scientific`, `deck-internal`) + 2 auxiliares (`deck-image-prompts`, `deck-reviewer`).
- **8 contratos compartilhados** (§10 SHARED.md) em `shared/`:
  - Entrevista universal U1-U6
  - STORYBOARD.md schema
  - Routing matrix (16 rotas)
  - Output convention (`$DECKS_DIR` + slug + versionamento)
  - Auto-detection brands.yaml
  - NotebookLM query template
  - Skill frontmatter padrão
  - Fronteiras explícitas (o que o plugin NÃO faz)
- **4 templates** em `templates/`:
  - `storyboard-skeleton.md` — esqueleto canônico
  - `poster-skeleton.md` (D8) — schema próprio para `deck-scientific` modo poster
  - `brands.yaml.example` (D6) — 3 marcas pré-povoadas (Beauty Smile / Fotona / Carnaval 360)
  - `env-decks-dir.example` (D4) — configuração de `$DECKS_DIR`
- **3 walkthroughs end-to-end** documentados no README:
  - W1: Pitch Beauty Smile pra investidor anjo (deck-fundraising + Sequoia + Andy Raskin)
  - W2: Aula Fotona Er:YAG (deck-teaching + laser-physics + chunks ≤7min)
  - W3: Pitch CEO política viagens com ROI (deck-internal pitch-to-leadership + BLUF + 6-pager)
- **Pipeline `skill-cenografia` → `deck-internal concept-reveal` (D3)** documentado com exemplo de paths e regra "consome verbatim".
- **Suporte a 3 NotebookLMs** (734 sources curados):
  - NB1 Core Transversal (243 sources)
  - NB2 Verticais Densas (223 sources)
  - NB3 Verticais Comerciais (268 sources)
- **Lint script shell+grep** em `scripts/lint-storyboard-schema.sh` validando:
  - Bloco `## Meta` completo (12 campos)
  - Tipos de slide na whitelist canônica
  - Bloco compliance 3 tiers (🔴 🟡 ✅)
- **Distribuição dupla (D13):**
  - Marketplace `fercosnt/fernando-claude-marketplace` (Claude Code via `/plugin install`)
  - Cowork Desktop nativo (suporte confirmado com legal-analyzer)
- **11 decisões LOCKED** declaradas em `plugin.json` metadata.
- **Tabela de overrides por vertical** (whitelist image-prompts D5 / max_ctas D14 / compliance D7).
- **Frameworks embutidos** por skill (resumo):
  - Sequoia, Andy Raskin, Klaff, TED, Heath Brothers (SUCCESs), Pyramid Minto, Working Backwards Amazon, Calgary-Cambridge, AIDET, GRADE, CONSORT, STROBE, IMRAD, Tufte, Doumont, Better Poster Morrison, Andragogy (Knowles), Bloom, Mayer, Sparkline Duarte, Win Without Pitching (Enns), 5X Rule, Challenger, Gap Selling, SPIN, Great Demo (Cohan), Sinek, Kotter.

### Inviolable Rules (LOCKED)

- D3 — Pipeline `skill-cenografia` → `deck-internal concept-reveal` (sempre via AskUserQuestion, nunca auto-delega)
- D4 — `$DECKS_DIR` env var default `~/Documents/decks/`
- D5 — Whitelist image-prompts por tipo de slide (override scientific: +dados)
- D6 — `brands.yaml` extensível com 3 marcas pré-povoadas
- D7 — Compliance 3 tiers (🔴 🟡 ✅) **sem hard-block** (bloco final sempre preenchido)
- D8 — `poster-skeleton.md` schema próprio para `deck-scientific` modo poster
- D10 — Routing-first 90% (2+ keywords mesma rota → roteia direto sem perguntar U1-U3)
- D11 — NotebookLM **NÃO** é pré-requisito (degrada com warning)
- D12 — **NUNCA** auto-delega `/idea-to-brief` (sempre AskUserQuestion)
- D13 — Distribuição dupla marketplace + Cowork Desktop nativo
- D14 — `max_ctas` override (`teaching:4` / `scientific:3` / demais:`1`)

### Boundaries (Fronteiras explícitas)

- Não gera slides finais (PPTX/Gamma/Figma) — só STORYBOARD.md
- Não busca dados em tempo real
- Não faz design visual (prompts sim, imagens não)
- Não chama APIs pagas sem confirmação
- Não escreve post de redes sociais (delega `/copy`)
- Não projeta espaço/cenografia (delega `skill-cenografia`)
- Não roda `/idea-to-brief` automaticamente

### Build summary

- **Ondas paralelas:** 4 (Onda 1: 2 auxiliares / Onda 2: 8 verticais / Onda 3: orchestrator / Onda 4: este plugin packaging)
- **Total linhas SKILL.md:** 2.594 linhas em 11 skills
- **Eval cases:** 32 casos em 11 evals/*.json
- **References:** 41 arquivos
- **Assets:** 16 arquivos (templates, checklists, exemplos)
- **NotebookLM:** 734 sources em 3 NBs
- **Modelo:** Opus 4.7 (1M context)
- **Duração:** 3 dias

### Compatibility

- Claude Code: `>= 2.0.10`
- Cowork Desktop: instalação nativa via marketplace (testado com legal-analyzer)
- Sistemas: macOS (testado), Linux (esperado funcionar — sem deps platform-specific)
- Dependências externas opcionais: `notebooklm` CLI, `yq`, `jq`

### Known limitations

- `notebooklm` CLI não é distribuído com o plugin — usuário instala separadamente
- Walkthroughs assumem usuário tem acesso aos 3 NBs (IDs fixos podem ser substituídos por NBs próprios via override futuro)
- Lint script é Bash 4+ (testado bash 5.x)

---

## [Unreleased]

### Planned (v1.1.0 candidate)

- Refinamento de 1-2 skills baseado em feedback dos 5 primeiros decks reais (D1)
- v1.1.0 candidato apenas se walkthroughs §12 revelarem problemas sistemáticos
- Possível adição de skill `deck-summary` (resumo 1-slide para emails)

### Potential (v2.0.0)

- Integração nativa com Gamma API (opt-in, hoje só prompts)
- NotebookLM override via brands.yaml (NBs próprios por marca)
- Multi-language support (hoje só PT-BR)
