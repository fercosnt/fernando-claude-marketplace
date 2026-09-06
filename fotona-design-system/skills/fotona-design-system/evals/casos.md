# Evals — fotona-design-system

Casos de teste para verificar se a skill dispara na hora certa, roteia para o arquivo certo e aplica as regras inegociaveis.

## A. Ativacao

| # | Prompt | Deve ativar? | Por que |
|---|--------|--------------|---------|
| A1 | "Cria um dashboard de calendario editorial da Fotona" | Sim | Produto digital da marca |
| A2 | "Monta um slide de abertura pro deck do GLP1Tight" | Sim | Trigger de protocolo + slide |
| A3 | "Preciso de um carrossel pro @fotonalaser sobre lipedema" | Sim | Trigger de social |
| A4 | "Gera uma imagem de equipamento no padrao da marca" | Sim | Prompts de imagem |
| A5 | "Qual o vermelho da Fotona?" | Sim | Consulta de token |
| A6 | "Cria uma landing page pra Beauty Smile" | **Nao** | Outra marca — `beauty-smile-design-system` |
| A7 | "Escreve o roteiro do deck de vendas" | **Nao** (sozinha) | Conteudo e das skills `deck-*`; esta skill entra so na camada visual |

## B. Roteamento de registro

| # | Prompt | Registro esperado | Arquivo carregado |
|---|--------|-------------------|-------------------|
| B1 | "Painel interno de acompanhamento de metas" | Claro | `references/produtos-digitais.md` |
| B2 | "Capa do deck comercial em 1920×1080" | Escuro | `references/slides.md` |
| B3 | "Story de convite pro Review SP Line" | Escuro | `references/posts-social.md` |
| B4 | "Hero da LP institucional" | **Escuro dentro de pagina clara** | `produtos-digitais.md` (secao hero) + `slides.md` |
| B5 | "Prompt pra gerar retrato de paciente" | Escuro | `references/prompts-imagem.md` |

Falha comum a evitar: usar o gradiente preto-carmesim num dashboard, ou fundo branco com Instrument Serif num slide comercial.

## C. Regras inegociaveis (a saida deve passar)

| # | Verificacao | Falha se |
|---|-------------|----------|
| C1 | Um unico vermelho vivo por tela | Botao vermelho + chip vermelho + barra vermelha na mesma view |
| C2 | Neutros do logotipo no registro claro | Aparece `#000`, `#333`, `#666` ou cinza puro do Tailwind |
| C3 | Estado com cor **e** forma | Status comunicado so por cor de fundo |
| C4 | Fontes embutidas em artifact standalone | `<link>` para Google Fonts (bloqueado, cai em fallback silencioso) |
| C5 | Titulo de slide com duas batidas 300 + 700 | Titulo inteiro num peso so |
| C6 | Protocolo com ® e metade em bold | `GLP1Tight` sem ® ou sem o bold |
| C7 | Metrica com meta e barra de progresso | `Metric` sem `delta` nem `progress` |
| C8 | Antes/depois com foto real + credito + n. de sessoes | Antes/depois gerado por IA, ou sem credito |
| C9 | Nenhum concorrente, nome de paciente, valor ou promessa | Qualquer um dos quatro aparece |
| C10 | Dado com fonte | Numero de mercado sem "Fonte: ..." |
| C11 | Post em 4:5 ou 9:16 | Peca quadrada 1:1 |
| C12 | Logo inlinado mais de uma vez com `id` de `clipPath` unico | Ids duplicados — SVG quebra silenciosamente |

## D. Anti-defaults de IA

A saida nao pode conter: gradiente roxo/azul · cream com serif + terracota · luz azul, roxa ou teal na fotografia · tudo centralizado · emoji como marcador de secao · `rounded-lg`/`rounded-2xl` em card · glass morphism · stock photo sorrindo · ilustracao no lugar de gente real.

## E. Como rodar

1. Sessao limpa do Claude Code no diretorio de um projeto Fotona
2. Rodar os prompts da tabela A e verificar ativacao (a skill aparece no rastro de ferramentas)
3. Para B, conferir qual reference foi lido antes da resposta
4. Para C e D, revisar a peca gerada item a item
5. Registrar falhas e ajustar a secao correspondente do `SKILL.md` ou da reference
