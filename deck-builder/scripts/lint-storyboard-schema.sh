#!/usr/bin/env bash
# lint-storyboard-schema.sh
#
# QA-3: valida STORYBOARD.md contra schema §10.2 (storyboard-schema.md).
# Stack: shell + grep (zero deps Python).
#
# v1.1 changelog:
#   - Aceita campos com OU sem bold (Tipo: e **Tipo:** ambos passam)
#   - Novo campo obrigatorio em Meta: "Modo de entrega:"
#   - Novo check (warning): bloco "Conteudo do slide" em slides
#   - Novo check (warning): bloco "Layout sugerido" em slides
#   - Novo check (warning): dados R$/% sem [VERIFICAR] flag nem footnote
#
# Uso:
#   ./lint-storyboard-schema.sh <storyboard.md> [<storyboard2.md> ...]
#
# Exit codes:
#   0 = todos PASS
#   1 = pelo menos 1 FAIL
#   2 = erro de uso (sem arquivo / arquivo nao existe)

set -u
set -o pipefail

# ----- cores -----
if [[ -t 1 ]] && [[ -z "${NO_COLOR:-}" ]]; then
  C_PASS=$'\033[32m'
  C_FAIL=$'\033[31m'
  C_WARN=$'\033[33m'
  C_DIM=$'\033[2m'
  C_RST=$'\033[0m'
else
  C_PASS=""; C_FAIL=""; C_WARN=""; C_DIM=""; C_RST=""
fi

# ----- campos obrigatorios em ## Meta (v1.1 adiciona "Modo de entrega:") -----
META_REQUIRED_FIELDS=(
  "Skill geradora:"
  "Objetivo .nico:"
  "Audi.ncia:"
  "Dura..o:"
  "Formato:"
  "Modo de entrega:"
  "Big Idea:"
  "Marca:"
  "Framework principal:"
  "max_ctas:"
  "Gerado em:"
  "Vers.o:"
  "Storyboard ID:"
)

# ----- tipos canonicos -----
CANONICAL_TYPES=(
  "capa" "problema" "contexto" "conceitual" "dados" "comparativo"
  "prova-social" "equipe" "demo" "financeiro" "CTA" "disclaimer"
  "agradecimento" "ap.ndice" "apendice"
)

# ----- helpers -----
pass()  { printf "  ${C_PASS}[PASS]${C_RST} %s\n" "$1"; }
fail()  { printf "  ${C_FAIL}[FAIL]${C_RST} %s\n" "$1"; FAILED=1; }
warn()  { printf "  ${C_WARN}[WARN]${C_RST} %s\n" "$1"; }
info()  { printf "  ${C_DIM}[INFO]${C_RST} %s\n" "$1"; }

# ----- lint de 1 arquivo -----
lint_file() {
  local f="$1"
  FAILED=0

  printf "\n${C_DIM}─── %s ───${C_RST}\n" "$f"

  if [[ ! -f "$f" ]]; then
    fail "Arquivo nao encontrado"
    return 1
  fi

  # ----- check 1: cabeçalho Meta presente -----
  if ! grep -q '^## Meta' "$f"; then
    fail "Bloco '## Meta' ausente"
  else
    pass "Bloco '## Meta' presente"

    # ----- check 1.1: 13 campos obrigatorios em Meta (v1.1) -----
    # regex aceita: "- Campo:" OU "- **Campo:**" (bold opcional)
    local missing=0
    local field
    for field in "${META_REQUIRED_FIELDS[@]}"; do
      # busca dentro dos primeiros 80 linhas (Meta com bold ocupa mais espaço)
      if ! head -n 80 "$f" | grep -qE "^- (\*\*)?${field}(\*\*)?"; then
        fail "Meta sem campo: '${field}'"
        missing=$((missing + 1))
      fi
    done
    if [[ $missing -eq 0 ]]; then
      pass "Meta completa (${#META_REQUIRED_FIELDS[@]} campos)"
    fi
  fi

  # ----- check 2: tipos canonicos presentes -----
  # regex aceita "Tipo: X" OU "**Tipo:** X"
  local types_found
  types_found=$(grep -E '^(\*\*)?Tipo:(\*\*)?[[:space:]]+' "$f" \
    | sed -E 's/^\*\*Tipo:\*\*[[:space:]]+//; s/^Tipo:[[:space:]]+//; s/[[:space:]]+$//' \
    | sort -u)

  if [[ -z "$types_found" ]]; then
    fail "Nenhum 'Tipo:' encontrado (storyboard sem slides estruturados)"
  else
    local n_types
    n_types=$(echo "$types_found" | wc -l | tr -d ' ')
    pass "Slides com 'Tipo:' declarado ($n_types tipos distintos)"

    # checa se algum tipo NAO esta na whitelist
    local bad_types=0
    while IFS= read -r t; do
      [[ -z "$t" ]] && continue
      local found=0
      local c
      for c in "${CANONICAL_TYPES[@]}"; do
        if echo "$t" | grep -qiE "^${c}$"; then
          found=1
          break
        fi
      done
      if [[ $found -eq 0 ]]; then
        fail "Tipo nao-canonico: '$t'"
        bad_types=$((bad_types + 1))
      fi
    done <<< "$types_found"
    [[ $bad_types -eq 0 ]] && pass "Todos os tipos sao canonicos"
  fi

  # ----- check 3: slide 1 obrigatorio Capa -----
  # awk procura "Tipo: capa" OU "**Tipo:** capa"
  if grep -qE '^## Slide 1' "$f"; then
    if awk '/^## Slide 1/{flag=1; next} flag && /^(\*\*)?Tipo:(\*\*)?/{print; exit}' "$f" \
        | grep -qiE 'Tipo:(\*\*)?[[:space:]]+capa'; then
      pass "Slide 1 = capa"
    else
      fail "Slide 1 nao declara 'Tipo: capa'"
    fi
  else
    fail "Slide 1 ausente"
  fi

  # ----- check 4: bloco compliance 3 tiers -----
  local has_compliance_header has_red has_yellow has_green
  has_compliance_header=$(grep -cE '^## Compliance' "$f" || true)
  has_red=$(grep -cE '^🔴' "$f" || true)
  has_yellow=$(grep -cE '^🟡' "$f" || true)
  has_green=$(grep -cE '^✅' "$f" || true)

  if [[ "$has_compliance_header" -eq 0 ]]; then
    fail "Bloco '## Compliance & Disclaimers' ausente"
  else
    if [[ "$has_red" -ge 1 ]] && [[ "$has_yellow" -ge 1 ]] && [[ "$has_green" -ge 1 ]]; then
      pass "Bloco compliance 3 tiers (🔴 🟡 ✅)"
    else
      fail "Bloco compliance incompleto (🔴=$has_red 🟡=$has_yellow ✅=$has_green — precisa ≥1 de cada)"
    fi
  fi

  # ----- check 5: checklist de revisao presente -----
  if grep -qE '^## Checklist de Revis' "$f"; then
    local checks
    checks=$(grep -cE '^- \[ \]' "$f" || true)
    if [[ "$checks" -ge 5 ]]; then
      pass "Checklist de Revisao com $checks itens"
    else
      warn "Checklist de Revisao com apenas $checks itens (esperado >=5)"
    fi
  else
    warn "Bloco '## Checklist de Revisao' ausente (recomendado para handoff reviewer)"
  fi

  # ----- check 6: action titles (warning, nao fail) -----
  # regex aceita "Action title:" OU "**Action title:**"
  local action_titles
  action_titles=$(grep -cE '^(\*\*)?Action title:(\*\*)?' "$f" || true)
  if [[ "$action_titles" -ge 1 ]]; then
    pass "$action_titles 'Action title:' declarados"
  else
    warn "Nenhum 'Action title:' encontrado (slides podem ter titulos descritivos — anti-padrao)"
  fi

  # ----- check 7 (v1.1): bloco "Conteudo do slide" em slides -----
  local content_blocks
  content_blocks=$(grep -cE '^(\*\*)?Conte.do do slide' "$f" || true)
  local slide_count
  slide_count=$(grep -cE '^## Slide [0-9]+' "$f" || true)
  if [[ "$slide_count" -ge 1 ]]; then
    if [[ "$content_blocks" -ge 1 ]]; then
      if [[ "$content_blocks" -ge "$slide_count" ]]; then
        pass "Bloco 'Conteudo do slide' em todos os $slide_count slides (v1.1)"
      else
        warn "Bloco 'Conteudo do slide' em $content_blocks de $slide_count slides (v1.1 — esperado em todos)"
      fi
    else
      warn "Nenhum bloco 'Conteudo do slide' encontrado (v1.1 — slides ficam minimalistas demais para deck enviado-para-leitura)"
    fi
  fi

  # ----- check 8 (v1.1): bloco "Layout sugerido" em slides -----
  local layout_blocks
  layout_blocks=$(grep -cE '^(\*\*)?Layout sugerido' "$f" || true)
  if [[ "$slide_count" -ge 1 ]]; then
    if [[ "$layout_blocks" -ge 1 ]]; then
      if [[ "$layout_blocks" -ge "$slide_count" ]]; then
        pass "Bloco 'Layout sugerido' em todos os $slide_count slides (v1.1)"
      else
        warn "Bloco 'Layout sugerido' em $layout_blocks de $slide_count slides (v1.1 — handoff designer fica incompleto)"
      fi
    else
      warn "Nenhum bloco 'Layout sugerido' encontrado (v1.1 — designer/Gamma recebe deck sem instrucoes visuais)"
    fi
  fi

  # ----- check 9 (v1.1): [VERIFICAR] flag em dados fabricados -----
  # heuristica: linhas com R$Xk, X%, n=X, "RCT YYYY" SEM [VERIFICAR] proximo nem footnote
  # NOTA: warning soft — humano avalia. Detecta padrao mais comum de over-claiming.
  local suspect_data verified_flags
  # conta linhas com padroes de dado suspeito (R$NNk, NN%, n=NN, RCT YYYY)
  suspect_data=$(grep -cE '(R\$[0-9]+(k|M|mi|bi)|[0-9]+\.[0-9]+%|[0-9]+%|n=[0-9]+|RCT [A-Z][a-z]+ 20[12][0-9]|NPS [0-9]+|GRADE (high|moderate|low|very low))' "$f" || true)
  verified_flags=$(grep -cE '\[VERIFICAR' "$f" || true)
  if [[ "$suspect_data" -ge 5 ]] && [[ "$verified_flags" -lt 1 ]]; then
    warn "Possiveis dados fabricados (n=$suspect_data linhas com R\$/%/n=/RCT/NPS/GRADE) sem nenhum [VERIFICAR] flag — v1.1 recomenda marcar todos os dados nao-conferidos com [VERIFICAR: descricao]"
  elif [[ "$verified_flags" -ge 1 ]]; then
    pass "$verified_flags marcacoes [VERIFICAR] encontradas (v1.1 — dados sinalizados para auditoria)"
  fi

  # ----- veredicto -----
  if [[ $FAILED -eq 0 ]]; then
    printf "${C_PASS}OK${C_RST}: %s\n" "$f"
    return 0
  else
    printf "${C_FAIL}FAIL${C_RST}: %s\n" "$f"
    return 1
  fi
}

# ----- main -----
if [[ $# -eq 0 ]]; then
  cat <<EOF
lint-storyboard-schema.sh — valida STORYBOARD.md (schema §10.2 v1.1)

Uso:
  $0 <storyboard.md> [<storyboard2.md> ...]

Validacoes (FAIL):
  - Bloco ## Meta com 13 campos obrigatorios (v1.1 adiciona "Modo de entrega:")
  - Slide 1 = capa
  - Tipos de slide na whitelist canonica
  - Bloco ## Compliance & Disclaimers com 3 tiers (🔴 🟡 ✅)

Validacoes (WARN — v1.1):
  - Bloco "Conteudo do slide" em cada slide (handoff visual)
  - Bloco "Layout sugerido" em cada slide (handoff designer)
  - [VERIFICAR] flag em dados fabricados (R\$, %, n=, RCT, NPS, GRADE)
  - Checklist de Revisao
  - Action titles

Formatos aceitos:
  - Texto puro: "Tipo: capa"
  - Bold opcional: "**Tipo:** capa"

Exit codes:
  0 = todos PASS
  1 = pelo menos 1 FAIL
  2 = erro de uso
EOF
  exit 2
fi

TOTAL=0
FAILS=0
for f in "$@"; do
  TOTAL=$((TOTAL + 1))
  if ! lint_file "$f"; then
    FAILS=$((FAILS + 1))
  fi
done

printf "\n${C_DIM}═══════════════════════════════════════${C_RST}\n"
if [[ $FAILS -eq 0 ]]; then
  printf "${C_PASS}TODOS PASS${C_RST} (%d/%d arquivos)\n" "$TOTAL" "$TOTAL"
  exit 0
else
  printf "${C_FAIL}%d FAIL${C_RST} / %d arquivos\n" "$FAILS" "$TOTAL"
  exit 1
fi
