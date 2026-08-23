# Eval cases — deck-review-print

Fixture de regressao: **W4 GLP1TIGHT v4** (design `DAHKNdTNVwI`, 17 slides, 1920x1080, marca Fotona).
Baseline medido no piloto de 2026-08-10: **6 paginas, 16,8% TAC medio**.
Execucao real de 2026-08-12 — **baseline oficial de regressao**: original 193% TAC x 17 paginas; dossie **7 paginas / 17,1% TAC**; reducao ~27x; **4 tabelas** (07, 12, 13, 15); 1 divergencia aritmetica (slide 13); slide 10 sem nenhum pixel.

---

## Case 1 — caminho feliz, Canva

**Dado** URL de design com 17 slides e MCP do Canva conectado
**Quando** `/deck-review-print {url}`
**Entao**

- [ ] PDF em `$DECKS_DIR/{YYYY-MM}/DOSSIE-glp1tight-{HHmm}.pdf`
- [ ] Exatamente **17 entradas**, numeradas 01..17, na ordem do original (D18)
- [ ] <= 7 paginas (execucao real: 7)
- [ ] TAC medio <= 25% (execucao real: 17,1%)
- [ ] Reporta ao usuario os 3 numeros: paginas, TAC medio, comparacao com o original
- [ ] O reporte de TAC vem **com a ressalva metodologica** (proxy, sem perfil ICC)
- [ ] Lista as **4** tabelas marcadas `[CONFERIR]` por numero de slide (07, 12, 13, 15)
- [ ] Comunica a divergencia aritmetica do slide 13 explicitamente, nao so no resumo

## Case 2 — MCP do Canva indisponivel

**Dado** URL do Canva e MCP desconectado
**Quando** `/deck-review-print {url}`
**Entao**

- [ ] **Nao** tenta rota alternativa de download
- [ ] Informa que precisa do conector ativo **nesta conversa**
- [ ] Oferece a alternativa de receber o deck exportado como PDF ou PPTX
- [ ] Nao grava arquivo nenhum

## Case 3 — deck grande

**Dado** design com 74 slides
**Quando** `/deck-review-print {url}`
**Entao**

- [ ] Avisa volume estimado (paginas e tempo) **antes** de processar
- [ ] Oferece 3 saidas: seguir · recortar intervalo · 3 slides por folha
- [ ] Nao comeca a processar sem resposta

## Case 4 — fidelidade de tabela (D17)

**Dado** slide 12 do GLP1TIGHT, classificado `tabela`
**Quando** transcreve
**Entao**

- [ ] A fonte da transcricao e a **imagem** do slide, nunca o texto corrido da API
- [ ] Miniatura do slide original ao lado da tabela transcrita
- [ ] `[CONFERIR]` visivel
- [ ] Todas as celulas numericas batem digito a digito com o original
- [ ] Unidades e separadores preservados
- [ ] Aparece no resumo final

### 4b — tabela ilegivel

- [ ] Re-exporta **aquele slide** em resolucao maior antes de desistir
- [ ] Se persistir: `[ILEGIVEL: linha N]`, sem inventar valor
- [ ] O trecho ilegivel aparece no resumo final

### 4c — divergencia apontada depois

- [ ] Corrige a celula e **regrava** o PDF (nao entrega errata)
- [ ] Registra slide, celula, valor transcrito e valor correto no log

## Case 5 — privacidade (RNF-06)

**Dado** GLP1TIGHT, slide 10 (7 pares antes/depois de pacientes)
**Quando** modo `revisao`
**Entao**

- [ ] **Zero** pixels da foto no PDF
- [ ] Entra como moldura tracejada: "Slide de cases (7 pares antes/depois)"
- [ ] Continua ocupando o numero 10 (D18)

**Quando** modo `handout`
**Entao**

- [ ] Pergunta **a cada execucao** se inclui as imagens de paciente
- [ ] Default e omitir
- [ ] Resposta afirmativa registrada no log
- [ ] Nunca por flag persistida

## Case 6 — classificacao (D24)

**Dado** os 17 slides do GLP1TIGHT
**Quando** classifica
**Entao**

- [ ] **Nenhuma decisao de classificacao usa TAC** — nem limiar absoluto, nem relativo
- [ ] Classifica por: estrutura tabular → densidade de texto → leitura visual
- [ ] Bate com a classificacao de referencia (`references/classificacao-slides.md`):
      `conteudo` 02,04,05,06,09,16 · `tabela` 07,12,13,15 · `foto` 03,08,10,11 · `misto` 01,14,17
- [ ] Detecta **4 tabelas**, nao 3 — o slide 07 e comparativo em duas colunas
- [ ] Rotulos apresentados ao usuario **antes** de compor, com override aceito
- [ ] Nenhum slide some da numeracao, qualquer que seja o rotulo

### 6b — regressao do bug de TAC

**Dado** o GLP1TIGHT (mediana 253% TAC, fotos medindo 65% e 273%)
**Entao**

- [ ] Slide 10 (65% TAC) classificado `foto` — TAC baixo **nao** impede
- [ ] Slide 05 (266% TAC) classificado `conteudo` — TAC alto **nao** obriga
- [ ] TAC aparece no relatorio como metrica de tinta, nunca como justificativa de rotulo

## Case 6c — auditoria aritmetica

**Dado** o slide 13 do GLP1TIGHT (programa masculino), que tem divergencia conhecida
**Quando** transcreve e audita
**Entao**

- [ ] Soma cada linha e cada coluna contra os totais declarados
- [ ] **Detecta** que a linha *Massa muscular (StarFormer)* soma **28** (`8+8+6+2+2+2`) mas declara **27X**
- [ ] Marca a celula `[DIVERGE: soma da linha = 28, total declarado = 27X]`
- [ ] **Transcreve 27X** — o valor do slide, como esta. O dossie reproduz, nao corrige
- [ ] A divergencia entra no resumo final e e comunicada explicitamente ao usuario
- [ ] Slide 12 (feminino) **nao** dispara falso positivo: linhas 6+9+5+6+6+36 = 68, colunas 14+14+14+9+8+9 = 68
- [ ] Slide 15 (financeiro) confere colunas derivadas: 180k x 4 = 720k, 720k x 12 = 8,64M

> Se este case passar batido, o checklist de conferencia nao esta sendo executado.

## Case 7 — modo apresentador (D22)

**Dado** deck com `DECKLINK` e paginas com bloco de briefing nas notas
**Quando** `--modo apresentador`
**Entao**

- [ ] Notas vem do `STORYBOARD.md` vinculado (precedencia 1)
- [ ] **Zero** ocorrencias de `▪ BRIEFING DE MONTAGEM` no PDF
- [ ] Marcador de abertura sem fechamento → **nao remove nada**, reporta a pagina

## Case 8 — degradacao (RNF-05 / RNF-09)

- [ ] Sem LibreOffice: rota `.pptx` desabilitada com mensagem acionavel; demais rotas vivas
- [ ] Sem `pdftoppm`: rota `.pdf` desabilitada; Canva segue funcionando
- [ ] Sem Chrome/Pillow/numpy: nucleo incompleto, bloqueia com instrucao de instalacao
- [ ] `brands.yaml` ausente ou malformado: tema cinza neutro, sem travar
- [ ] `$DECKS_DIR` nao gravavel: erro claro com o caminho tentado, e **nada** escrito em outro lugar

## Case 9 — contencao de escrita (RNF-07)

**Quando** qualquer execucao termina
**Entao**

- [ ] `find` fora de `$DECKS_DIR` retorna **0** arquivos novos
- [ ] Artefatos intermediarios (PNGs, HTML) removidos do diretorio temporario

## Case 10 — nao-regressao do contrato (RNF-10)

- [ ] `scripts/lint-storyboard-schema.sh` roda sobre W1-W3 **antes e depois** com resultado identico
- [ ] Nenhuma alteracao em `shared/storyboard-schema.md`

> **Estado conhecido:** W1-W3 falham no lint desde antes do v2.0.0, por `Meta sem campo: 'Modo de entrega:'` — campo que o schema v1.1 tornou obrigatorio e ao qual as fixtures nunca foram migradas. Baseline em `main`: 3 FAIL / 3 arquivos. O criterio aqui e **resultado identico**, nao "verde".
