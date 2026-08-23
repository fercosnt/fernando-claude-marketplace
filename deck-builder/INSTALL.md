# Instalacao — deck-builder

O plugin tem **duas camadas** de dependencia, e elas nao se misturam:

| Camada | Precisa de que | Quem usa |
|--------|----------------|----------|
| **Skills de storyboard** (11 skills, `/deck`) | Nada. Sao markdown puro. | Todas as verticais, orchestrator, image-prompts, reviewer |
| **`deck-review-print`** (v2.0.0) | Binarios de sistema + 2 pacotes Python | So a skill de dossie |

Se voce so vai gerar `STORYBOARD.md`, **nao precisa instalar nada** — pule para "Instalar o plugin".

---

## TL;DR — maquina nova

**Use um venv.** E o caminho recomendado e o unico imune aos dois problemas que
derrubam instalacao no macOS: o bloqueio PEP 668 do Homebrew Python e a duvida
de "qual `python3` o script vai usar". O `check-print-deps.sh` procura
`<repo>/.venv` automaticamente — voce nao precisa ativar nada.

```bash
cd <raiz-do-repo>            # ex.: cd ~/code/fernando-claude-marketplace

# binarios de sistema
brew install poppler                              # macOS
brew install --cask chromium                      # ou use o Chrome que ja tiver
# sudo apt install -y poppler-utils chromium      # Debian / Ubuntu

# venv do projeto + pacotes Python
python3 -m venv .venv
./.venv/bin/python -m pip install -r deck-builder/scripts/requirements-print.txt

# conferir
./deck-builder/scripts/check-print-deps.sh
```

> **`cd` na raiz do repo primeiro.** Todos os caminhos acima sao relativos a ela.
> Rodar de `~` da `no such file or directory` — e o erro mais comum destes comandos.

```powershell
# Windows (PowerShell, como administrador)
winget install Google.Chrome                       # pule se ja tiver Chrome ou Edge
winget install oschwartz10612.Poppler              # ou: choco install poppler
winget install Python.Python.3.12                  # pule se ja tiver Python
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r deck-builder\scripts\requirements-print.txt

# conferir — no Git Bash ou WSL, nao no PowerShell
./deck-builder/scripts/check-print-deps.sh
```

Opcional, so se for ingerir `.pptx`:

```bash
brew install --cask libreoffice                    # macOS
sudo apt install -y libreoffice                    # Debian/Ubuntu
winget install TheDocumentFoundation.LibreOffice   # Windows
python3 -m pip install python-pptx                 # ou `py -m pip` no Windows
```

---

## Windows — o que muda

Funciona, com tres diferencas em relacao a macOS/Linux:

| Assunto | macOS / Linux | Windows |
|---------|---------------|---------|
| Interpretador Python | `python3` | **`py`** (o launcher oficial). `python3` costuma nao existir |
| Instalar pacote | `python3 -m pip install` | **`py -m pip install`** |
| Rodar `check-print-deps.sh` | terminal normal | **Git Bash ou WSL** — PowerShell nao executa `.sh` |
| Python do venv | `.venv/bin/python` | `.venv\Scripts\python.exe` (o script procura os dois) |

**O Edge serve como motor de PDF.** E Chromium por baixo, ja vem instalado, e o script o encontra automaticamente. Nao precisa instalar Chrome so por causa disso.

**Gerenciador de pacotes:** `winget` ja vem no Windows 10/11. Se preferir, `choco` e `scoop` tambem funcionam:

```powershell
choco install poppler googlechrome libreoffice-fresh
scoop install poppler
```

**Se o `poppler` nao estiver no `winget`** (o pacote muda de nome as vezes): baixe o release de `oschwartz10612/poppler-windows` no GitHub, extraia, e acrescente a pasta `bin` ao `PATH` do sistema. O `check-print-deps.sh` so procura o `pdftoppm` no PATH.

**Git Bash** vem junto com o Git for Windows (`winget install Git.Git`). E o caminho recomendado — os scripts do repositorio sao todos bash, inclusive o `lint-storyboard-schema.sh` que ja existia antes desta versao.

> A skill em si **nao depende de bash**. Quem executa o pipeline e o Claude, lendo o `SKILL.md`. Os dois scripts sao auxiliares: um diagnostica dependencias, o outro mede tinta. Num Windows sem Git Bash, a skill ainda funciona — voce so perde o diagnostico automatico e a medicao de TAC.

---

## Duas falhas de instalacao que parecem a mesma coisa

Ambas terminam em "instalei e o script diz que falta", mas a causa e o conserto sao diferentes. Leia o erro antes de escolher o remedio.

| Sintoma no terminal | Causa | Conserto |
|---------------------|-------|----------|
| `pip` roda, diz **"Successfully installed"**, e o check continua acusando falta | Instalou em **outro interpretador** (pyenv/mise/asdf/venv) | `python3 -m pip install` (secao abaixo) |
| `pip` **explode com traceback** antes de instalar qualquer coisa | **Interpretador quebrado** — ex.: `pyexpat` do Homebrew Python contra `expat` do sistema | `brew reinstall python@3.x`, ou use outro Python (ver tabela de problemas comuns) |

O primeiro e erro de PATH. O segundo e build quebrado, e nenhum `-m pip` no mundo resolve.

---

## A armadilha do `pip` (leia antes de xingar o script)

**Use `python3 -m pip install`, nunca `pip install` solto.**

Em maquina com `pyenv`, `mise`, `asdf`, `conda` ou venv, o `pip` do PATH quase nunca e o pip do `python3` do PATH. O pacote instala, o `pip` diz "Successfully installed", e o script continua acusando que falta — porque instalou em outro interpretador.

`python3 -m pip` usa, por construcao, o mesmo interpretador que a skill vai usar.

Para descobrir onde voce esta:

```bash
which python3          # o interpretador que a skill usa
python3 -V
python3 -c "import PIL, numpy; print('ok')"
```

O `check-print-deps.sh` imprime o caminho do Python ativo na primeira linha, justamente para essa conferencia. Com o venv do projeto criado, ele passa a mostrar `<repo>/.venv/bin/python` — e a duvida acaba.

**Ordem de preferencia do script:** `$DECK_PY` (override) → `<repo>/.venv` → `python3` / `py` / `python` do PATH.

---

## Dependencias, uma a uma

### Nucleo — sem isto nenhum dossie e gerado

| Dependencia | Para que | macOS | Debian/Ubuntu | Windows |
|-------------|----------|-------|---------------|---------|
| **Chromium/Chrome/Edge** (headless) | Renderiza o HTML A4 em PDF | `brew install --cask chromium` | `sudo apt install chromium` | ja vem (Edge) |
| **Pillow** | Miniaturas e conversao CMYK da medicao de TAC | `python3 -m pip install Pillow` | idem | `py -m pip install Pillow` |
| **numpy** | Media por pixel na medicao de TAC | `python3 -m pip install numpy` | idem | `py -m pip install numpy` |

> Google Chrome ja instalado serve — o script procura em `/Applications/Google Chrome.app/...` no macOS e nos nomes `chromium`, `chromium-browser`, `google-chrome`, `google-chrome-stable`, `chrome` no PATH.

### Rota `.pdf` — ingerir PDF e conferir o PDF gerado

| Dependencia | macOS | Debian/Ubuntu | Windows |
|-------------|-------|---------------|---------|
| **pdftoppm** (poppler-utils) | `brew install poppler` | `sudo apt install poppler-utils` | `winget install oschwartz10612.Poppler` |

**Alternativa sem binario:** `python3 -m pip install pymupdf`. Com ele instalado, o `measure-tac.py` rasteriza PDF sozinho e o `pdftoppm` deixa de ser necessario para medicao. Recomendado no Windows, onde instalar poppler da mais trabalho.

Sem nenhum dos dois: a rota `.pdf` fica desabilitada e o `measure-tac.py` so aceita imagem. As demais rotas seguem funcionando.

### Rota `.pptx` — ingerir PowerPoint

| Dependencia | macOS | Debian/Ubuntu | Windows |
|-------------|-------|---------------|---------|
| **LibreOffice** (headless) | `brew install --cask libreoffice` | `sudo apt install libreoffice` | `winget install TheDocumentFoundation.LibreOffice` |
| **python-pptx** | `python3 -m pip install python-pptx` | idem | `py -m pip install python-pptx` |

Sem elas: so a rota `.pptx` fica desabilitada.

### Rota Canva — ingerir por URL de design

**Nao depende de binario nenhum.** Depende do **MCP do Canva conectado na conversa** onde a skill roda:

- Claude Code: `/mcp` ou `claude mcp`
- Claude Desktop / claude.ai: configuracoes de conectores

Sem o conector, a skill **nao tenta rota alternativa de download** — ela avisa e oferece receber o deck exportado como PDF ou PPTX.

---

## Verificar a instalacao

```bash
./deck-builder/scripts/check-print-deps.sh
```

Saida esperada numa maquina completa:

```
python3 ativo: /usr/local/bin/python3 (Python 3.12.x)

NUCLEO (sem isto nao ha dossie)
  [OK]   Chromium/Chrome headless — HTML A4 -> PDF (...)
  [OK]   Python: Pillow — miniaturas e medicao de TAC
  [OK]   Python: numpy — medicao de TAC
...
NUCLEO OK — 5 checagens passaram.
Rotas de ingestao disponiveis: Canva (se MCP conectado), .pdf, .pptx
```

| Exit | Significado |
|------|-------------|
| `0` | Nucleo OK. Ao menos uma rota de ingestao viva. |
| `1` | Nucleo incompleto — nenhum dossie pode ser gerado. |

`[AVISO]` desabilita **apenas** aquela rota. `[FALTA]` bloqueia tudo.

---

## Instalar o plugin

### Claude Code — via marketplace

```bash
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install deck-builder
```

### Claude Code / Desktop — copia local

```bash
cp -r deck-builder/skills/* ~/.claude/skills/
```

Claude Desktop (pasta do skills-plugin):

```bash
cp -r deck-builder/skills/* \
  "$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<id>/<id>/skills/"
```

### Configurar `$DECKS_DIR` (D4)

Todo output vai para `$DECKS_DIR/{YYYY-MM}/`. Default: `~/Documents/decks/`.

```bash
echo 'export DECKS_DIR=~/Documents/decks/' >> ~/.zshrc
```

Override por contexto, util para cliente especifico:

```bash
cd ~/Clientes/Fotona/
export DECKS_DIR=./decks/
```

### Configurar marcas (D6, opcional)

```bash
mkdir -p ~/.config/deck-builder
cp deck-builder/templates/brands.yaml.example ~/.config/deck-builder/brands.yaml
```

Sem esse arquivo o plugin nao quebra: cai em tema cinza neutro.

---

## Problemas comuns

| Sintoma | Causa provavel | Solucao |
|---------|----------------|---------|
| "instalei Pillow e continua FALTA" | `pip` instalou em outro interpretador | `python3 -m pip install Pillow`; confira a 1ª linha do check |
| `[FALTA] Chromium/Chrome` com Chrome instalado | Chrome fora do path padrao | Instale o Chromium via brew/apt, ou ajuste `acha_chrome()` no script |
| PDF sai com cabecalho e rodape do navegador | Faltou a flag | Use `--no-pdf-header-footer` |
| PDF sai em branco | Caminho relativo no `file://` | Use caminho absoluto |
| `externally-managed-environment` no pip (Debian 12+, **ou Homebrew Python no macOS**) | PEP 668 — o gerenciador protege a instalacao dele | **Use o venv do projeto** (secao TL;DR). Evite `--break-system-packages`: o proprio Homebrew avisa que pode quebrar a instalacao |
| macOS: `pip` explode com `ImportError ... pyexpat ... Symbol not found: _XML_SetAllocTrackerActivationThreshold` | **Python do Homebrew quebrado** — o `pyexpat` foi compilado contra um `expat` mais novo que o `/usr/lib/libexpat.1.dylib` do sistema. Nao e problema de interpretador errado nem de venv | `brew reinstall python@3.14` (ou a versao que o traceback citar). Se persistir, use outro Python: `python3.12 -m pip install Pillow numpy` ou `brew install python@3.13 && python3.13 -m pip install Pillow numpy` |
| Instalei com `brew` mas o Claude nao acha o binario | O shell do agente pode ter visao de filesystem diferente da do seu terminal | **Rode `check-print-deps.sh` no SEU terminal**, nao peca para o agente conferir |
| Windows: `python3: command not found` | No Windows o launcher e `py` | Use `py -m pip install ...` |
| Windows: `.sh` nao executa | PowerShell nao roda bash | Abra o **Git Bash** ou WSL |
| Windows: `pdftoppm` nao encontrado apos instalar | Pasta `bin` do poppler fora do PATH | Acrescente a pasta `bin` ao PATH do sistema e reabra o terminal |
| Dossie sai colorido demais | `brands.yaml` com cor forte | O corpo e sempre preto sobre branco; so titulo e fio usam a marca. Se nao for isso, e bug |

---

## Cross-references

- [`scripts/check-print-deps.sh`](scripts/check-print-deps.sh) — diagnostico
- [`scripts/requirements-print.txt`](scripts/requirements-print.txt) — pacotes Python
- [`shared/print-dossie-schema.md`](shared/print-dossie-schema.md) — contrato do dossie
- [`shared/output-convention.md`](shared/output-convention.md) — `$DECKS_DIR` e paths
