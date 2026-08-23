# Eval cases — deck-render-canva

Fixture: **Beauty Smile pitch anjo** (design `DAHSC1Q6iNA`, 13 paginas) e o
storyboard `STORYBOARD-beauty-smile-pitch-anjo.md`.

---

## Case 1 — modo `anotar`, caminho feliz

**Dado** um design de 13 paginas e o storyboard de 13 slides
**Quando** roda `--modo anotar`
**Entao**

- [ ] Confere que a contagem de paginas bate com a de slides **antes** de escrever
- [ ] Cada pagina recebe bloco com os 4 rotulos, na ordem, <= 900 chars
- [ ] O bloco e **prefixado**: nota preexistente permanece abaixo do marcador de fim
- [ ] Publica **um** comentario-indice, <= 1.000 chars
- [ ] Grava `DECKLINK-*.md` com storyboard ↔ design_id ↔ mapa ↔ hash por pagina
- [ ] Nada e publicado, compartilhado ou movido de pasta

### 1b — contagem nao bate

**Dado** design de 12 paginas e storyboard de 13 slides
**Entao**

- [ ] **Nao escreve nada** antes de confirmar
- [ ] Mostra o mapeamento proposto e pede confirmacao
- [ ] Aceita override do usuario

> Aconteceu de verdade: `generate-design-structured` transformou 13 slides em 12
> paginas, partindo um e fundindo outros.

## Case 2 — o briefing e especifico da pagina

**Dado** uma pagina cujo conteudo divergiu do storyboard
**Entao** o `ESCREVER` aponta a divergencia concreta, nao instrucao generica:

- [ ] "veio com dois blocos quando o storyboard pedia um"
- [ ] "FALTA o tailwind dos 78%"
- [ ] "os titulos vieram em INGLES"

> Se todos os `ESCREVER` de um deck forem intercambiaveis, a skill nao olhou as
> paginas.

## Case 3 — item bloqueante

**Dado** o slide com quote de paciente sem TCLE confirmado
**Entao**

- [ ] `BLOQUEANTE` em caixa alta, **no topo** do `NAO MEXER`
- [ ] Diz o que fazer sem o TCLE ("montar sem ela")
- [ ] Aparece tambem no comentario-indice
- [ ] **Nao** cria um 5º rotulo (D23)

## Case 4 — limpeza (D26)

**Dado** design com briefing em todas as paginas e 3 blocos editados a mao
**Quando** roda `--limpar-briefing`
**Entao**

- [ ] Blocos identicos ao hash: removidos em silencio
- [ ] Blocos divergentes: **arquivados** em `## Recados arquivados` no `DECKLINK`, com nº de slide e data, **antes** de remover
- [ ] Reporta "N paginas limpas, M recados arquivados"
- [ ] Notas do apresentador voltam **byte a byte** iguais
- [ ] Zero ocorrencias de marcador restantes

### 4b — marcador quebrado

- [ ] **Nao remove nada** naquela pagina
- [ ] Reporta a pagina para revisao manual

### 4c — design sem briefing

- [ ] Informa que nao havia briefing
- [ ] **Nenhuma transacao e commitada**

## Case 5 — nao-destrutividade (RNF-13)

- [ ] Diff limitado ao bloco entre marcadores
- [ ] Thumbnails antes/depois identicos — anotacao **nao** altera a camada visual
- [ ] `height` de nenhum elemento de texto mudou

## Case 6 — atomicidade (RNF-14)

**Dado** falha injetada na pagina 7 de 13
**Entao**

- [ ] `finalize: "cancel"` — transacao inteira descartada
- [ ] Nenhuma pagina fica anotada
- [ ] Reporta a falha e a pagina

## Case 7 — modo `render` sem template (D19)

**Dado** `search-brand-templates` devolve lista vazia
**Entao**

- [ ] **Nao renderiza**
- [ ] Informa que falta brand template da marca
- [ ] Oferece o modo `anotar` sobre deck existente
- [ ] **Nao** cai para geracao livre

> Regressao do achado de 2026-08-12: a geracao livre descartou em silencio o
> slide de disclaimer CVM 160/22, o footnote cfo-cfm e o qualificador do NPS.

## Case 8 — formatacao no modo `render`

**Dado** template com elementos de regiao unica e de regioes mistas
**Entao**

- [ ] Regiao unica: `replace_text` **seguido de** `format_text` + `position_element`
- [ ] Regioes mistas: `find_and_replace_text`
- [ ] `height` de cada elemento editado conferida contra a original **antes** do commit
- [ ] Nenhum `listMarker` aparece onde nao havia

## Case 9 — tabela

- [ ] Slide com tabela e reportado como exigindo template que ja a contenha
- [ ] **Nunca** tenta escrever em `sheet-element`
- [ ] **Nunca** simula tabela com retangulos + caixas de texto
- [ ] O comentario-indice avisa que o preenchimento da tabela e humano

## Case 10 — degradacao (US-10)

**Dado** MCP do Canva desconectado
**Entao**

- [ ] As 8 verticais geram `STORYBOARD.md` normalmente
- [ ] O handoff **nao e oferecido** — nem como opcao quebrada
- [ ] Nenhum aviso intrusivo
