# Classificacao de slide (D24)

Decide se cada slide entra no dossie **com miniatura** (`conteudo`), **sem imagem nenhuma** (`foto`), ou **com tabela redesenhada** (`tabela` / `misto`).

## Algoritmo

```
se estrutura tabular presente          → tabela   (misto, se houver foto de fundo)
senao se densidade_texto >= 220 chars  → conteudo
senao                                  → leitura visual decide: foto ou conteudo
```

Tres sinais, em ordem de precedencia:

1. **Estrutura tabular** — por leitura visual do slide. Precedencia maxima.
2. **Densidade de texto** — nº de caracteres extraidos da fonte, quando disponivel.
3. **Leitura visual** — voce olhando o que a pagina e.

## O TAC nao entra aqui

Esta secao ja teve duas versoes que usavam TAC como classificador. As duas estavam erradas.

| Versao | Regra | Como morreu |
|--------|-------|-------------|
| v1 | `TAC >= 150%` → foto | Num deck de fundo escuro **todas** as paginas passam de 150%. Um slide de citacao virava `foto` por acidente |
| v2 | `TAC >= mediana_do_deck + 25 p.p.` → foto | Na execucao real, classificou **zero** slides como foto: a mediana ja era 253% e nenhuma pagina chegava a 278% |

O que a execucao da GLP1TIGHT (2026-08-12) mostrou:

| Slide | TAC | O que e de fato |
|-------|-----|-----------------|
| 09 | 37% | conteudo — fundo branco |
| 10 | 65% | **foto** — cases de pacientes |
| 05 | 266% | conteudo — fundo vermelho |
| 17 | 273% | **foto** — encerramento |

Fotos em 65% **e** em 273%. Conteudo em 37% **e** em 266%. O TAC nao separa em direcao nenhuma, porque num fundo escuro chapado a foto costuma ser **mais clara** que o fundo.

O erro de origem foi tratar uma **metrica de saida** como **criterio de entrada**. O TAC continua sendo medido e reportado — e nisso funciona bem: a execucao reproduziu o piloto quase slide a slide (media 193% x 17 paginas).

## Como fazer a leitura visual

Monte uma folha de contato e classifique olhando. Uma imagem com as N paginas em grade custa uma leitura, contra N leituras individuais:

```python
from PIL import Image, ImageDraw
import glob
ps = sorted(glob.glob("png/pag-*.png"))
cw, ch, cols = 300, 169, 5
rows = (len(ps)+cols-1)//cols
folha = Image.new("RGB", (cols*cw, rows*(ch+18)), "white")
d = ImageDraw.Draw(folha)
for i, p in enumerate(ps):
    with Image.open(p) as im:
        im = im.convert("RGB").resize((cw-4, ch-4))
    x, y = (i % cols)*cw, (i//cols)*(ch+18)
    d.text((x+3, y+2), f"slide {i+1:02d}", fill="black")
    folha.paste(im, (x+2, y+16))
folha.save("contato.png")
```

## Casos de borda

| Situacao | Rotulo | Por que |
|----------|--------|---------|
| Fundo claro + muito texto | `conteudo` | Densidade tem precedencia |
| Foto de fundo **e** tabela por cima | `misto` | Sem foto, com tabela redesenhada e `[CONFERIR]` |
| Foto sem nenhum texto | `foto` | Entrada minima: numero + descricao + pauta |
| Foto com texto que importa (capa com KPIs, encerramento com contatos) | `misto` | A foto sai, o texto fica |
| Grafico nativo / SmartArt | `tabela` ou `misto` | Leitura visual + `[CONFERIR]` |
| Slide de secao/transicao | `foto` | Pouco texto |

## Override do usuario e obrigatorio (RF-04)

**Sempre apresente os rotulos antes de compor**, com o TAC ao lado como informacao de tinta — nunca como justificativa da classificacao:

```
Classificacao dos 17 slides (leitura visual + densidade)

  01 misto      02 conteudo   03 foto       04 conteudo   05 conteudo
  06 conteudo   07 tabela     08 foto       09 conteudo   10 foto (PACIENTE)
  11 foto       12 tabela     13 tabela     14 misto      15 tabela
  16 conteudo   17 misto

  Confirma, ou quer sobrescrever algum?
```

Nenhum slide **some** por classificacao errada: `foto` continua ocupando seu numero (D18). O pior erro possivel e um slide entrar sem miniatura quando deveria ter uma — recuperavel com override e nova composicao.

## Classificacao de referencia — GLP1TIGHT v4

17 slides, 1920x1080, marca Fotona. Media do deck: **193% TAC** (metrica de tinta, nao de classificacao).

| Slide | Tipo | Slide | Tipo |
|-------|------|-------|------|
| 01 | misto (capa, foto + KPIs) | 10 | **foto — imagem clinica de paciente (RNF-06)** |
| 02 | conteudo | 11 | foto (transicao) |
| 03 | foto | 12 | **tabela** — programa feminino |
| 04 | conteudo | 13 | **tabela** — programa masculino |
| 05 | conteudo | 14 | misto (marca + texto) |
| 06 | conteudo | 15 | **tabela** — cenarios financeiros |
| 07 | **tabela** — comparativo 2 colunas | 16 | conteudo |
| 08 | foto | 17 | misto (encerramento + contatos) |
| 09 | conteudo | — | — |

**4 tabelas, nao 3.** O Apendice B do PRD nao contava o slide 7.
