# fotona-design-system

Design system da Fotona Brasil — fonte unica de verdade visual para qualquer peca da marca.

## O que faz

Entrega, na hora de construir, a decisao visual que a Fotona ja tomou: qual registro usar, qual vermelho, qual fonte, qual medida, qual componente. O objetivo e que dashboard, slide e post parecam feitos pelo mesmo time — porque foram.

## Quando usar

- Construir dashboard, LP, app interno ou artifact da Fotona
- Montar slide ou deck comercial (Canva, Gamma, HTML)
- Criar post, carrossel ou story do @fotonalaser
- Gerar imagens no padrao visual da marca
- Consultar cor, tipografia, logo, medida ou componente
- Revisar se uma peca esta na marca antes de publicar

## Os dois registros

A marca tem duas identidades quase opostas. Escolher errado e o erro mais caro que existe aqui.

| Registro | Quando | Base visual | Titulo |
|----------|--------|-------------|--------|
| **Claro** — produto digital | Dashboard, LP, app, ferramenta, artifact | Branco, neutros do logotipo, vermelho so na acao primaria | Instrument Serif + Instrument Sans |
| **Escuro** — marca | Slide, deck, capa, post, story, hero | Preto + carmesim, luz de palco vermelha | Montserrat caixa alta 300 + 700 |

Heuristica: **se a peca vai ser usada, e clara; se vai ser mostrada, e escura.** O registro e por peca, nao por projeto — um hero escuro dentro de uma LP clara e o caso normal.

## O que vem dentro

| Arquivo | Conteudo |
|---------|----------|
| `SKILL.md` | Decisao de registro, tokens essenciais, 6 regras de ouro, tipografia, logotipo, checklist |
| `references/produtos-digitais.md` | 14 componentes `@fotona/ui` com props e classes `.ftn-*`, temas, layout, setup |
| `references/slides.md` | Grade 1920 × 1080 e 9 arquetipos com anatomia, medidas e copy de exemplo |
| `references/posts-social.md` | 7 formatos de feed, carrossel e stories, grade semanal, regras de legenda |
| `references/prompts-imagem.md` | Prompt-base, 6 variacoes prontas, prompt negativo, aprendizados de teste |
| `assets/` | `tokens.css`, `components.css`, `fonts.css` + 3 fontes woff2, logo SVG oficial, dashboard de exemplo |
| `evals/casos.md` | Ativacao, roteamento de registro, 12 regras inegociaveis, anti-defaults de IA |

## Regras inegociaveis

1. **Um vermelho vivo por tela.** `#ED1C24` marca a acao primaria, "hoje", "ao vivo", a palavra em destaque. Nada mais.
2. **Neutros vem do logotipo** — grafite `#414042` e cinza `#808285`, nunca preto ou cinza puros.
3. **Cor pertence ao pilar**, nunca ao responsavel.
4. **Estado nunca so por cor** — sempre cor + forma.
5. **Antes e depois so com foto clinica cedida**, com credito do medico e numero de sessoes. Nunca gerada.
6. **Nunca**: concorrente, nome de paciente, valor de procedimento, promessa de resultado, dado sem fonte.

## Gotchas que a skill ja resolve

- **Fonte via CDN e bloqueada em artifact** e cai em fallback silencioso — as tres woff2 vem embutidas para virar `@font-face` data URI.
- **Inlinar o logo SVG duas vezes na mesma pagina quebra a renderizacao** se os `id` do `clipPath` nao forem renomeados.
- `assets/exemplo-dashboard.html` tem 152KB: abrir no browser ou consultar com `grep`, nunca ler inteiro.

## Instalacao

```bash
/plugin install fotona-design-system@fernando-claude-marketplace
```

Reinicie o Claude Code apos instalar. No Cowork: Settings → Plugins → Install from GitHub → `fercosnt/fernando-claude-marketplace`.

## Relacao com outras skills

Complementa as skills `deck-*` do plugin **deck-builder** sem sobrepor: elas sao donas do conteudo e do storyboard; esta e da camada visual. Para outra marca, ver a skill avulsa `beauty-smile-design-system`.

## Origem

Extraida de `fotona/design-system` (DESIGN-SYSTEM.md, BIBLIOTECA-SLIDES.md, BIBLIOTECA-POSTS.md, PROMPTS-IMAGEM.md, pacotes `@fotona/tokens` e `@fotona/ui`). Paleta do registro escuro medida por amostragem de 6 apresentacoes do Canva e da grade do Instagram em set/2026.

**Autocontida**: os assets sao copias, nao referencias. Ao mudar o design system na origem, recopie `assets/` e suba uma versao nova.
