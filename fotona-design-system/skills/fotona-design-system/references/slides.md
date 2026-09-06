# Registro escuro — slides e decks

Os nove arquetipos que se repetem nas apresentacoes comerciais e institucionais da Fotona (Midia Kit, GLP1Tight, MelasmaRecovery, ATP Reboost, Meu Primeiro Fotona, Fotona4GLOW, Bem-vindo a Fotona). Medidas tiradas de exports em **1920 × 1080 px**. Use como contrato ao montar um deck no Canva, no Gamma ou em HTML.

Tokens em `assets/tokens.css` (bloco "registro de marca"); fotos em `references/prompts-imagem.md`.

---

## 0. Grade e elementos fixos (valem para todo slide)

| Elemento | Medida em 1920 × 1080 | Regra |
|----------|------------------------|-------|
| Margem lateral | 115–150 px | Logo e texto alinham na mesma margem esquerda |
| Margem superior | 72–78 px | Onde o logo assenta |
| Logo | 150–240 px de largura (52–72 px de altura), canto superior esquerdo | Negativo sobre escuro, positivo sobre claro. Em parcerias, lockup `Fotona \| Parceiro` separado por barra fina |
| Barra vermelha inferior | 24 px de altura, `#ED1C24`, largura total, rente a borda | Em todo slide escuro e claro, **exceto** capa com foto sangrada e slide de transicao |
| Coluna de texto | comeca entre x = 240 e x = 470; largura maxima ≈ 45% | Titulo e corpo alinhados a esquerda, nunca centralizados, exceto nos slides de frase unica |
| Rodape (quando existe) | 11–12 px, `rgba(255,255,255,.5)`, canto inferior esquerdo | "Fotona Brasil \| Estrategia Editorial" ou fonte do dado |
| Numeracao | canto inferior direito, mesmo tamanho do rodape | Opcional |

### Fundos

- **Escuro (padrao, ~70% dos slides):** `--brand-gradient` (preto → carmesim) com halo radial `--brand-halo` saindo de um canto ou do topo. Variante: preto puro com um unico cone de luz vermelha.
- **Claro (~30%):** `--stage-light` `#F5F4F1`, arcos finos vermelhos (quarto de circulo, 2 px, `#ED1C24`) sangrando por um ou dois cantos, mesma barra inferior.
- **Vermelho cheio (raro):** so em slide de transicao ou de convite.

### Tipografia dos slides

- **Titulo:** Montserrat caixa alta, 44–64 px, **duas batidas na mesma frase**: primeira em peso 300 (Light), segunda em 700 (Bold).
  Ex.: `O PACIENTE NAO QUER MUDAR O ROSTO.` / **`QUER VOLTAR A RECONHECER UMA PELE SAUDAVEL.`**
- **Subtitulo/lede:** 18–22 px, peso 400, `rgba(255,255,255,.85)` sobre escuro, `#4A4A4A` sobre claro, ate 60 caracteres por linha.
- **Corpo:** 14–16 px. Rotulos de eixo e legenda: 11–12 px, caixa alta, `letter-spacing: .06em`.
- **Nome de protocolo:** sempre com ® e com metade em bold — `GLP1`**`TIGHT`**`®`, `MELASMA`**`RECOVERY`**`®`, `Fotona`**`4GLOW`**`™`.

---

## 1. Capa

**Quando:** abertura de deck ou de capitulo.

- Foto sangrada ocupando a metade direita (ou 60%), fundida ao gradiente escuro por uma mascara suave a esquerda. Retrato editorial com luz vermelha, ou equipamento no palco.
- Logo no canto superior esquerdo. Em decks de parceria, lockup `Fotona | Nome do Medico`.
- Titulo em 2–3 linhas na coluna esquerda, alinhado ao terco inferior: batida 1 em 300, batida 2 em 700.
- Nome do protocolo abaixo em caixa alta 300/700 com ®, e uma linha de apoio de 18–20 px.
- **Sem barra inferior** quando a foto sangra ate a borda.

**Copy de exemplo:** `O PACIENTE PERDEU PESO.` / **`MAS A JORNADA NAO TERMINOU.`** — `GLP1TIGHT®` · Uma nova visao sobre o paciente pos-emagrecimento.

---

## 2. Dado grande

**Quando:** abrir um argumento com um numero de mercado.

- Fundo escuro com halo. Opcional: uma "barra de busca" ilustrativa acima do numero (pilula clara com lupa e o termo pesquisado: "Flacidez pos Tirzepatida").
- Numero em 120–160 px, peso 700, branco, alinhado a margem esquerda.
- Leitura do dado em 2–3 linhas de 22–26 px, caixa alta, com a parte importante em 700.
- Caixa de contexto a direita: pilula ou retangulo arredondado com borda fina vermelha, 13–14 px, 3 linhas.
- **Fonte do dado no rodape**, 11 px: "Fonte: McKinsey & Company (2024) · Fotona · Alem da Balanca (2025)".

**Copy de exemplo:** `62%` · `DOS PACIENTES EM GLP-1` / **`JA BUSCAM ESTETICA POS-EMAGRECIMENTO`**

---

## 3. Frase unica

**Quando:** transicao de raciocinio, o slide que "respira".

- Fundo escuro; frase centralizada em 44–56 px, caixa alta, 300/700, no maximo 3 linhas.
- Uma linha de apoio de 16–18 px centralizada abaixo, `rgba(255,255,255,.7)`.
- Variante fotografica: foto em preto e branco desaturada com a frase por cima e a palavra-chave repetida em pequeno no rodape ("a verdadeira", "algumas").
- Sem outros elementos alem do logo e da barra.

**Copy de exemplo:** `O PACIENTE NAO QUER MUDAR O ROSTO.` / **`QUER VOLTAR A RECONHECER UMA PELE SAUDAVEL.`**

---

## 4. Comparativo em duas colunas

**Quando:** contrastar o modelo antigo e o modelo Fotona.

- Fundo escuro com halo central. Titulo 300/700 no topo, centralizado ou a esquerda.
- Duas colunas de largura igual com uma linha vertical fina entre elas.
- Cabecalho de cada coluna em pilula com borda vermelha fina, caixa alta 700, 14 px: `CLINICA QUE FRAGMENTA` | `CLINICA QUE INTEGRA`.
- 4–6 itens por coluna, cada um em pilula escura (`rgba(255,255,255,.06)` com borda `rgba(237,28,36,.35)`), 13–14 px, altura 36–40 px, gap 10 px.
- **A coluna Fotona nunca ganha cor extra**: a hierarquia vem so do texto.

**Copy de exemplo**
Fragmenta: Trata uma queixa por vez · Vende sessoes isoladas · Facilita comparacao por preco · Tem menor recorrencia · Dispersa o paciente
Integra: Atua em diferentes necessidades · Estrutura uma jornada · Eleva a percepcao de valor · Favorece manutencao continua · Centraliza o cuidado na clinica

---

## 5. Lista em pilulas

**Quando:** enumerar sintomas, queixas, ganhos, frentes.

- Fundo claro (`#F5F4F1`) ou escuro.
- Titulo 300/700 a esquerda, 36–44 px, ocupando ≈ 35% da largura.
- A direita, 4–6 pilulas empilhadas, alinhadas a direita, largura variavel pelo texto, altura 40–44 px, gap 12 px, 15–16 px de texto.
  - Sobre claro: pilula preta `#111` com texto branco, ou vermelha `#ED1C24` sangrando pela borda direita.
  - Sobre escuro: pilula `--crimson-700` com borda `#ED1C24`.
- Variante "frentes": rotulo curto + protocolo em 700 (`Face: Fotona4D`).

**Copy de exemplo:** `E NECESSARIO ATUAR DE FORMA INTEGRADA PARA` **`ENTREGAR QUALIDADE GLOBAL DA PELE`** → Pigmentacao irregular · Vermelhidao difusa · Poros dilatados · Linhas finas · Perda de firmeza

---

## 6. Tabela operacional

**Quando:** estrutura de programa, cenarios de faturamento, agenda.

- Fundo claro para tabelas de faturamento; escuro para estrutura de programa.
- Titulo 300/700 com a palavra-chave em destaque (`ESTRUTURA OPERACIONAL DO PROGRAMA` **`FEMININO`**, com "FEMININO" em caixa vermelha).
- Tabela centralizada, largura 60–70%, linhas de 36–40 px, cabecalho em 700 com fundo `#111` (claro) ou `rgba(255,255,255,.08)` (escuro).
- **Ultima linha de total** com fundo `#ED1C24` e texto branco 700.
- Numeros alinhados a direita, tabulares. Valores em R$ com separador de milhar.
- Uma linha de conclusao abaixo da tabela em 700, 15 px: "Programa Feminino entrega 68 sessoes em 12 meses contratualizados."
- Selo de vantagem com icone de check: `Sem consumivel por sessao`.

---

## 7. Antes e depois

**Quando:** cases clinicos. **Sempre foto real cedida, nunca gerada.**

- Fundo dividido: 60% off-white a esquerda, 40% vermelho/carmesim a direita (ou fundo preto com halo).
- Rotulo pequeno `ANTES&DEPOIS` em caixa alta 300, e o protocolo em 700 com ® abaixo (`GLP1TIGHT®`), 24–28 px, alinhados a margem esquerda.
- Linha tecnica de 11 px: handpiece, modo, plataforma (`T-Runner · T-Runner com HC6 · NX-Runner`).
- Duas fotos em molduras arredondadas (raio 16–20 px), mesma altura (~520 px), lado a lado; a "depois" avanca sobre a area vermelha.
- Pilula branca `ANTES` e pilula vermelha `DEPOIS` centralizadas na base de cada foto, caixa alta 700, 11 px.
- `QUANTIDADE DE SESSOES: 4` em 11 px no canto superior direito. Credito `Cortesia de: Dra. Nome` abaixo em 10 px.
- Variante mosaico: 6–8 pares pequenos em grade para "Cases reais · Cortesia de quem aplica".

---

## 8. Equipamento em destaque

**Quando:** apresentar SP Dynamis NX, StarWalker PICO Pro, StarFormer 4.0, TimeWalker.

- Fundo preto com 1–3 cones de luz vermelha vindo do alto, nevoa baixa, chao refletivo. O equipamento ocupa 40–50% da largura, a direita ou ao centro.
- Nome do equipamento em 40–48 px 700, com a variante do modelo em vermelho: `StarWalker` **`Pico Pro`**.
- Linha de posicionamento em 18–20 px 400 abaixo do nome.
- Lista de 4–6 specs em 13–14 px com bullet simples, ou pares "valor + rotulo" em duas linhas (`2,7 GW` / `Alta potencia de pico`).
- Selos com check no rodape: `Nao invasivo` · `Sem downtime` · `Sem consumivel por sessao`.

---

## 9. Transicao e encerramento

**Transicao (esfera)**
- Fundo preto; esfera translucida vermelha ocupando 70% da altura, deslocada a esquerda, com o wordmark "Fotona" em branco dentro dela (ou logo completo).
- Frase de 3–4 linhas a direita, 22–26 px, caixa alta 300/700.
- **Sem barra inferior.**

**Encerramento**
- Fundo escuro. Logo completo com tagline centralizado, 400–480 px de largura.
- Bloco de contato no canto inferior esquerdo em 12 px, com icones de linha: WhatsApp comercial · Showroom (endereco) · Instagram @fotonalaser.
- Barra inferior presente.

---

## Sequencia tipica de um deck comercial (17–31 slides)

1. Capa → 2. Dado grande → 3. Frase unica → 4. Lista em pilulas (sintomas) → 5. Comparativo (fragmenta × integra) → 6. Transicao esfera ("E neste cenario que a Fotona entra") → 7. Equipamento em destaque (×1–3) → 8. Lista em pilulas (frentes/protocolos) → 9. Antes e depois (×3–6) → 10. Tabela operacional (programa) → 11. Tabela operacional (faturamento) → 12. Credenciais ("60 anos Fotona + protocolo nao replicavel") → 13. Encerramento.

## Checklist antes de exportar

- [ ] Um unico vermelho vivo por slide; o resto e preto e carmesim
- [ ] Logo na margem de 115–150 px; barra de 24 px em todo slide que nao seja capa sangrada ou transicao
- [ ] Titulo com as duas batidas (300 + 700), caixa alta, alinhado a esquerda
- [ ] Protocolos com ® e metade em bold
- [ ] Antes e depois so com foto real e credito do medico
- [ ] Nenhum concorrente citado; nenhum dado sem fonte
