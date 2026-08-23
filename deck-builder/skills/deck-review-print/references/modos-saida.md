# Modos de saida

Um motor, tres destinos. O que muda entre eles nao e estetica — e **quem le e o que essa pessoa pode ver**.

## `revisao` (default)

**Quem le:** a presidencia, com caneta na mao. Caso de uso dominante.

| | |
|---|---|
| Slides por folha | 2, A4 retrato |
| Pauta de anotacao | Sim — 3-4 linhas em slide simples, 2-3 em slide denso |
| Miniatura | Sim (exceto `foto`) |
| Marcacoes internas | Sim — `[CONFERIR]`, `[ILEGIVEL]`, rotulo de tipo |
| Imagem de paciente | **Nunca** |
| TAC alvo | <= 25% |

O rotulo de tipo fica visivel de proposito: o revisor precisa saber **por que** um slide entrou sem imagem, ou vai achar que faltou pagina.

## `handout`

**Quem le:** o cliente, depois da reuniao. Leave-behind.

| | |
|---|---|
| Slides por folha | 2, com respiro maior |
| Pauta de anotacao | **Nao** |
| Marcacoes internas | **Nao** — sem `[CONFERIR]`, sem rotulo de tipo |
| Imagem de paciente | So com **confirmacao explicita a cada execucao** |
| TAC alvo | <= 25% |

Marcacao de processo em peca que circula fora da casa e vazamento de bastidor. `[CONFERIR]` significa "ainda nao conferimos este numero" — nao e coisa que se entrega a cliente.

### A confirmacao de imagem de paciente e por execucao (Questao 4 do PRD)

Nunca por flag persistida, nunca por default, nunca "lembrar da ultima vez". A pergunta e feita **toda vez**:

```
Este deck tem 1 slide com imagem clinica de paciente (slide 10, 7 pares antes/depois).
Incluir as imagens neste handout?

  [Nao, omitir] (default)   [Sim, incluir]
```

Motivo: CFO 196/2019 e LGPD. Material impresso que sai da clinica nao volta, e o consentimento de uso em prontuario nao e consentimento de uso em peca comercial. A resposta afirmativa fica registrada no log da execucao.

## `apresentador`

**Quem le:** quem vai apresentar, antes de subir ao palco.

| | |
|---|---|
| Slides por folha | 2 |
| Pauta de anotacao | Sim |
| Speaker notes | **Sim** — e a razao de existir do modo |
| Imagem de paciente | **Nunca** |

### Precedencia da fonte das notas (Questao 6 do PRD)

1. `STORYBOARD.md` vinculado via `DECKLINK` — as notas originais, escritas com o arco em mente
2. Notas da propria pagina no Canva
3. Nenhuma — a entrada sai so com o texto do slide

### Filtro do briefing de montagem (Questao 7 do PRD)

As notas passam por filtro que **remove** tudo entre `▪ BRIEFING DE MONTAGEM` e `▪ FIM DO BRIEFING` (D22).

Esse bloco e instrucao para quem **monta** o deck — "o que nao mexer", "o que decidir". Nao tem uso nenhum para quem **apresenta**, e ainda ocupa espaco que deveria ser da nota real. Marcador de abertura sem o de fechamento: **nao remove nada** e reporta a pagina, porque apagar por heuristica arrisca comer a nota do apresentador.

## `aplicar` (Fase 3 — D25)

Nao gera PDF. Consome correcoes enderecadas por numero de slide e grava no Canva via `edit-design`.

Trava que os outros modos nao tem: **dry-run obrigatorio** mostrando o diff por slide antes de qualquer commit — o commit do `edit-design` e irreversivel.

Vive aqui, e nao numa skill propria, porque opera sobre o **mesmo artefato** e o **mesmo contrato de enderecamento** (numeracao espelhada D18 + `DECKLINK`). Separar duplicaria a logica de enderecamento em dois SKILL.md e criaria duas fontes de verdade para a mesma numeracao.

## Matriz de decisao rapida

| O usuario disse | Modo |
|-----------------|------|
| "para o presidente revisar", "corrigir", "anotar" | `revisao` |
| "deixar com o cliente", "leave-behind", "material de apoio" | `handout` |
| "minhas notas", "vou apresentar", "cola" | `apresentador` |
| "aplicar as correcoes", "ja corrigi no papel" | `aplicar` |
| Nao disse | `revisao` — e o caso dominante |
