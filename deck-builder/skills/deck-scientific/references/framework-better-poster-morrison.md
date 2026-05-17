# Better Poster Morrison — framework do modo `poster` (D8)

> Mike Morrison ("How to create a better research poster in less time", #BetterPoster). Aplicado **exclusivamente** no modo `poster` que gera **POSTER.md** (D8 — schema proprio, NAO STORYBOARD).

## Tese central

Posters cientificos tradicionais sao **muros de texto** que ninguem le. Better Poster inverte:

> A pessoa caminhando no corredor entende o achado principal em ≤5 segundos. Quem quiser detalhe, le o paper completo via QR code.

## Os 6 elementos visuais (Better Poster Morrison)

### 1. Centro — Key Finding (GRANDE)

- **1 frase + 1 numero chave** centralizado, em fonte gigante (≥ 100 pt em painel A0)
- Visivel a 3-5 metros
- Esta e a "manchete" — deve responder: **o que descobriram?**

Exemplo:
> "Er:YAG sustenta clareamento por 6 meses em 92% dos pacientes (n=50)"

### 2. Painel Esquerdo — Background

- Contexto + research question
- 2-3 paragrafos curtos
- Fonte 24-32 pt
- Termina com a pergunta de pesquisa em destaque

### 3. Painel Inferior Esquerdo — Methods (small)

- Design + sample + outcome + analise + reporting guideline
- Fonte 18-22 pt (deliberadamente menor — para quem quiser detalhe)
- Conciso, bullets

### 4. Painel Direito — Results (figuras)

- **1-2 figuras principais** + tabela resumida
- Tufte aplicado (data-ink ratio alto, sem chartjunk)
- Legenda autossuficiente
- IC95% + effect size + p-value + GRADE level visiveis

### 5. Painel Inferior Direito — Conclusion (small)

- Discussion destilada (1-2 paragrafos)
- Significado clinico
- Limitacoes (1-2 frases)
- Implicacoes para pratica

### 6. Rodape — References + COI + Acknowledgments + QR Code

- **QR code centralizado** para paper completo (DOI ou link estavel)
- **COI declarado** explicitamente
- Acknowledgments (financiamento, instituicao)
- 3-5 referencias principais
- ORCID dos autores

## Layout visual (A0 ou A1)

```
┌─────────────────────────────────────────────────────────────────┐
│  Titulo do estudo (TOPO — fonte 60 pt)                          │
│  Authors + affiliations + COI + congresso (linha menor)         │
├──────────────────┬──────────────────────────────────────────────┤
│                  │                                              │
│   Painel         │      CENTRO — Key Finding GRANDE             │
│   Esquerdo       │      (1 frase + 1 numero)                    │
│                  │      [≥ 100 pt em A0]                        │
│   Background     │                                              │
│   (2-3 paragr.)  │                                              │
│                  ├──────────────────────────────────────────────┤
│                  │                                              │
├──────────────────┤      Painel Direito                          │
│                  │      Results (figuras Tufte)                 │
│   Painel         │      [2 figuras + 1 tabela]                  │
│   Inferior       │                                              │
│   Esquerdo       │                                              │
│                  ├──────────────────────────────────────────────┤
│   Methods        │                                              │
│   (small, 18 pt) │      Painel Inferior Direito                 │
│                  │      Conclusion (small) + Implicacoes        │
│                  │                                              │
├──────────────────┴──────────────────────────────────────────────┤
│  Rodape: References + COI + Acknowledgments + QR Code           │
└─────────────────────────────────────────────────────────────────┘
```

## CTAs no poster (D14 — max 3)

1. **Read paper** — QR code centralizado para DOI ou OSF preprint
2. **Replicate** — protocolo + dataset/codigo aberto (Zenodo / OSF / Figshare)
3. **Contact author** — email ou ORCID do autor responsavel

## Anti-patterns (Morrison)

- **Muro de texto** — densidade alta em todos os paineis (le-se nada)
- **Key finding pequeno** — invertendo a tese: detalhe grande, achado pequeno
- **Sem QR code** — quem se interessa nao tem como aprofundar
- **Logo institucional gigante** — ego sobre ciencia
- **Cor decorativa** — gradientes, fundos azuis, etc. (Tufte: data-ink)
- **>3 figuras** — perde foco
- **Pizza chart** — sempre (Tufte: humanos nao leem areas de setores)

## Validacao do poster (passa em 4 testes)

1. **Teste de 5 segundos** — leitor a 3 metros entende o key finding?
2. **Teste de QR code** — leitor que escaneia chega no paper completo?
3. **Teste de COI** — COI esta declarado e visivel?
4. **Teste de GRADE** — outcome primario tem GRADE level explicito?

Se algum teste falha, poster nao esta pronto.

## Cross-refs

- IMRAD adaptado para layout 2D → `framework-imrad-grade.md`
- Tufte aplicado nas figuras do painel direito → `framework-tufte-doumont.md`
- Compliance (COI, reporting guideline) → `compliance-consort-strobe-prisma-coi.md`
- Schema completo POSTER.md → `assets/templates/poster-skeleton.md`
