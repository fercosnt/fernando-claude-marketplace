#!/usr/bin/env bash
# check-print-deps.sh — valida dependencias de sistema do deck-review-print.
#
# Principio (RNF-09): ausencia de dependencia EXCLUSIVA de uma rota desabilita
# APENAS aquela rota, com mensagem acionavel — nunca o comando inteiro.
#
# Exit: 0 = ao menos uma rota de ingestao viva e o motor de PDF presente
#       1 = nucleo quebrado (nao da para gerar dossie nenhum)

set -uo pipefail

VERDE=$'\033[0;32m'; VERM=$'\033[0;31m'; AMAR=$'\033[0;33m'; ZERO=$'\033[0m'
ok=0; falta=0

diz_ok()    { printf "  ${VERDE}[OK]${ZERO}   %s\n" "$1"; ok=$((ok+1)); }
diz_falta() { printf "  ${VERM}[FALTA]${ZERO} %-22s %s\n" "$1" "$2"; falta=$((falta+1)); }
diz_avisa() { printf "  ${AMAR}[AVISO]${ZERO} %-22s %s\n" "$1" "$2"; }

tem_cmd() { command -v "$1" >/dev/null 2>&1; }
tem_py()  { "$PY" -c "import $1" >/dev/null 2>&1; }

# Chromium/Chrome headless — nomes variam por plataforma e forma de instalacao
acha_chrome() {
  local c
  for c in chromium chromium-browser google-chrome google-chrome-stable chrome; do
    if tem_cmd "$c"; then echo "$c"; return 0; fi
  done
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium" \
           "/c/Program Files/Google/Chrome/Application/chrome.exe" \
           "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
           "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
           "/c/Program Files/Microsoft/Edge/Application/msedge.exe"; do
    if [[ -x "$c" ]]; then echo "$c"; return 0; fi
  done
  return 1
}

# Qual Python usar, em ordem de preferencia:
#   1. $DECK_PY            — override explicito
#   2. <repo>/.venv        — venv do projeto (recomendado: imune a PEP 668 e
#                            a ambiguidade de "qual python3" entre shells)
#   3. python3 / py / python  — o que estiver no PATH
# Windows: `python3` costuma nao existir; o launcher e `py`.
RAIZ_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
py_bin() {
  if [[ -n "${DECK_PY:-}" ]] && command -v "$DECK_PY" >/dev/null 2>&1; then echo "$DECK_PY"; return 0; fi
  for v in "$RAIZ_REPO/.venv/bin/python" "$RAIZ_REPO/.venv/Scripts/python.exe"; do
    if [[ -x "$v" ]]; then echo "$v"; return 0; fi
  done
  if command -v python3 >/dev/null 2>&1; then echo "python3"
  elif command -v py     >/dev/null 2>&1; then echo "py"
  elif command -v python >/dev/null 2>&1; then echo "python"
  else return 1; fi
}
PY="$(py_bin || echo python3)"

echo "═══ deck-review-print — dependencias de sistema ═══"
echo
# Mostrar QUAL python3 esta ativo evita o erro mais comum de setup:
# "eu instalei com pip e continua dizendo que falta". Quase sempre o pip
# instalou em outro interpretador (pyenv, mise, venv, brew, /usr/bin).
if command -v "$PY" >/dev/null 2>&1; then
  printf "Python ativo: %s (%s)\n\n" "$(command -v "$PY")" "$("$PY" -V 2>&1)"
else
  printf "${VERM}Python nao encontrado no PATH (procurei python3, py, python).${ZERO}\n\n"
fi

echo "NUCLEO (sem isto nao ha dossie)"

CHROME_MOTOR=""
if CHROME_MOTOR=$(acha_chrome); then
  diz_ok "Chromium/Chrome headless — HTML A4 -> PDF ($CHROME_MOTOR)"
else
  diz_falta "Chromium/Chrome" "macOS: brew install --cask chromium | Debian: sudo apt install chromium"
fi

if tem_py PIL; then diz_ok "Python: Pillow — miniaturas e medicao de TAC"
else diz_falta "Python Pillow" "$PY -m pip install Pillow"; fi

if tem_py numpy; then diz_ok "Python: numpy — medicao de TAC"
else diz_falta "Python numpy" "$PY -m pip install numpy"; fi

nucleo_falta=$falta

echo
echo "ROTA PDF  (ingestao .pdf + conferencia do PDF gerado)"
if tem_cmd pdftoppm; then
  diz_ok "pdftoppm (poppler-utils)"
  ROTA_PDF=1
else
  diz_avisa "pdftoppm" "macOS: brew install poppler | Debian: sudo apt install poppler-utils"
  echo "         -> rota .pdf DESABILITADA; medicao de TAC so aceita imagem"
  ROTA_PDF=0
fi

echo
echo "ROTA PPTX (ingestao .pptx)"
ROTA_PPTX=1
if tem_cmd libreoffice || tem_cmd soffice; then
  diz_ok "LibreOffice headless — renderiza slides de PPTX"
else
  diz_avisa "LibreOffice" "macOS: brew install --cask libreoffice | Debian: sudo apt install libreoffice"
  ROTA_PPTX=0
fi
if tem_py pptx; then
  diz_ok "Python: python-pptx — extrai texto de PPTX"
else
  diz_avisa "Python python-pptx" "$PY -m pip install python-pptx"
  ROTA_PPTX=0
fi
[[ $ROTA_PPTX -eq 0 ]] && echo "         -> rota .pptx DESABILITADA"

echo
echo "ROTA CANVA (ingestao por URL de design)"
echo "  Nao depende de binario local — exige o MCP do Canva conectado NESTA conversa."
echo "  Sem o conector: a skill NAO tenta rota alternativa de download; pede o deck"
echo "  exportado como PDF ou PPTX (RF-01, cenario 2)."

echo
echo "═══════════════════════════════════════════════════"
if [[ $nucleo_falta -gt 0 ]]; then
  printf "${VERM}NUCLEO INCOMPLETO${ZERO} — %d dependencia(s) essencial(is) faltando.\n" "$nucleo_falta"
  echo "Nenhum dossie pode ser gerado ate resolver o bloco NUCLEO acima."
  echo "Instrucoes completas por plataforma: deck-builder/INSTALL.md"
  echo
  echo "Caminho recomendado (imune a PEP 668 e a ambiguidade de interpretador):"
  echo "  cd $RAIZ_REPO"
  echo "  python3 -m venv .venv"
  echo "  ./.venv/bin/python -m pip install -r deck-builder/scripts/requirements-print.txt"
  echo "Windows: rode este script no Git Bash ou WSL (PowerShell nao executa .sh)."
  exit 1
fi

rotas=("Canva (se MCP conectado)")
[[ $ROTA_PDF  -eq 1 ]] && rotas+=(".pdf")
[[ $ROTA_PPTX -eq 1 ]] && rotas+=(".pptx")
printf "${VERDE}NUCLEO OK${ZERO} — %d checagens passaram.\n" "$ok"
printf "Rotas de ingestao disponiveis: %s\n" "$(IFS=', '; echo "${rotas[*]}")"
exit 0
