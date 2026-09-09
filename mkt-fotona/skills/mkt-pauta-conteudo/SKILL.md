---
name: mkt-pauta-conteudo
description: Monta a pauta de conteúdo do mês para o time de MKT da Fotona (Instagram, LinkedIn, YouTube, e-mail, blog, por empresa) e, depois que a pessoa confirma a tabela e os donos, cria no Notion as tarefas-mãe com as fases datadas (Roteiro · Arte/Edição · Legenda · Aprovação · Postagem; em vídeo entra Gravação) como sub-itens, com os prazos escalonados a partir da data planejada. Use sempre que alguém falar em "pauta", "calendário editorial", "planejamento de conteúdo do mês", "o que vamos postar em outubro", "monta o mês", "cria as peças/os posts no Notion", "distribui as fases", "quem faz a arte de cada post", ou pedir para planejar posts de um período — mesmo sem dizer pauta. Não use para uma demanda avulsa (isso é mkt-nova-demanda) nem para escrever o texto da peça (mkt-brief-conteudo).
---

# Pauta de conteúdo — do calendário às peças no Notion

Uma peça de conteúdo no sistema é uma **tarefa-mãe** (`Categoria = Conteúdo`) com as **fases como
sub-itens**, cada fase com um dono e um prazo. A mãe aparece no calendário editorial; o trabalho e
a métrica vivem nas fases. Montar um mês à mão são 6 páginas por peça — o tipo de digitação que
ninguém sustenta por mais de um mês. Esta skill faz a digitação; a pessoa decide a pauta e os donos.

Leia `../../CONTEXTO.md` e carregue o contexto. O arquivo que manda aqui é o `conteudo.md` do
contexto (fases por formato, prazos, pilares, cadência padrão, dono padrão por fase, regra da
aprovação clínica). O resumo operacional está em `assets/fases-de-conteudo.md`.

## O que esta skill escreve

Páginas novas em ✅ Tarefas — a mãe e as fases — **só depois de duas confirmações**: a da pauta e a
dos donos. Classe 3 do `contrato-de-escrita.md`. Fase com dono e prazo confirmados nasce em
`A fazer`; fase que a pessoa não confirmou nasce em `Triagem`, para o coordenador de MKT decidir.
Nunca cria peça sem `Data planejada`: é o campo que revela o furo no calendário, e uma peça sem
data é uma peça que ninguém vai cobrar.

Não mexe em peça que já existe (mover, reagendar, trocar dono) — isso é Kanban e triagem.

## O fluxo

### 1. Entenda o mês

Pergunte, ou leia do pedido: mês, empresa(s), canais. Em paralelo consulte:

- 🚀 Campanhas com `Status = Produção` ou `No ar` no período (**Q13** cobre projetos; para campanhas
  use o mesmo filtro no banco de campanhas) — campanha ativa puxa pelo menos 2 peças para si.
- O mês anterior de conteúdo (**Q12** para publicadas, **Q10** para o que está no calendário) — para
  propor cadência a partir do que a casa realmente faz, não de um ideal.
- Pilares e cadência: o padrão da casa está no `conteudo.md`; a pessoa pode mudar na conversa
  ("esse mês são 2 por semana"). Use o que ela disser.

Não leia carga de ninguém. Dono se propõe **por área e formato** (tabela do `conteudo.md`); carga é
leitura do PMO, e este plugin não olha o trabalho dos outros.

### 2. Proponha a pauta — e declare a regra que usou

Uma tabela, uma linha por peça: **data planejada · canal · formato · pilar · linha/produto ·
campanha · tema em uma frase · aprovação clínica? (sugerido)**. Antes da tabela, uma linha com a
regra: "Instagram 3/semana, 1 educativa a cada 3, 1 prova social por quinzena; a campanha X puxou 2
peças; LinkedIn 1/semana". A regra declarada é o que permite a pessoa discordar da pauta inteira
com uma frase ("não, esse mês é 2 por semana") em vez de editar linha por linha.

Datas: dias úteis, distribuídos na semana; não empilhe duas peças no mesmo canal no mesmo dia sem
motivo. `Aprovação clínica = Aguardando` sugerido quando `Pilar = Educativo/Clínico`, quando a
linha/produto é protocolo clínico, ou quando o tema fala de resultado, indicação ou paciente;
`Não requer` nos demais que forem claros; em dúvida, deixe como pergunta. (É um select — desde
09/09/2026 não existe mais o checkbox `Requer aprovação clínica?`.)

Peça a **confirmação da pauta**: a pessoa corta, troca, move; você reapresenta a tabela final e
pergunta "essa é a pauta?". Só então passe aos donos.

### 3. Proponha donos e prazos por fase

Para cada peça, as fases do formato (5; **6 com Gravação quando o formato é vídeo** — reels, vídeo
curto/longo, YouTube, institucional) com dono padrão **por área** (`conteudo.md`) e prazo
escalonado a partir da `Data planejada`. Para os prazos, rode o script — é determinístico e trata
fim de semana e feriado (pergunte os feriados do período, ou use os que a pessoa ou a consulta
informarem; feriado recua para o dia útil anterior, como o fim de semana):

```
python3 scripts/escalonar_prazos.py 2026-10-19 carrossel
python3 scripts/escalonar_prazos.py 2026-10-19 reels --feriados 2026-10-12
```

Se a própria `Data planejada` cair em fim de semana ou feriado, confirme com a pessoa antes de
seguir — postar no domingo pode ser intencional; entregar no domingo, não.

Apresente por peça, ou em bloco quando a pessoa preferir ("todas as artes com a designer, todas as
legendas com a social media"). Bloco explícito conta como confirmação **daquelas** fases; "ok"
depois de uma lista de 30 linhas não conta como 30 decisões — percorra por peça. Dono que não está
no banco 👥 Time não é gravado: escreva o nome no texto e deixe a fase em `Triagem`.

Aprovação clínica confirmada (`Aguardando`) → a fase Aprovação vai para o dono clínico (LA&HA) e o
prazo da fase respeita o D-1; se a pessoa quiser folga, aumente a Data planejada, não encurte as
outras fases. A aprovação em si acontece no grupo de WhatsApp da clínica; quem aprova muda o select
para `Aprovada` (ou `Reprovada`) e a automação carimba `Aprovação clínica em`.

### 4. Crie — mãe primeiro, fases depois

Para cada peça confirmada:

1. **Mãe:** `Tarefa` = "<formato> · <tema>" · `Categoria = Conteúdo` · `Tipo de trabalho = Planejado`
   · `Canal de entrada = Agente` · `Empresa` · `Canal` · `Formato` · `Pilar de conteúdo` ·
   `Linha/Produto` · `Data planejada` · `Prazo interno` (D-1, do script) · `Campanha` (quando
   houver) · `Aprovação clínica` (`Aguardando` ou `Não requer`) · `Objetivo / Por quê` (o tema em uma
   frase + a campanha).
   Sem `Responsável`, sem `Prazo`, `Status = A fazer`. A mãe é contêiner.
2. **Fases:** uma página por fase, `Tarefa` = "<fase> — <tema>", `Subtarefa de` = a mãe, `Categoria =
   Conteúdo`, `Tipo de trabalho = Planejado`, `Canal de entrada = Agente`, `Empresa`, `Prazo` =
   prazo da fase, `Responsável` = o dono confirmado, `Status = A fazer` (ou `Triagem` sem dono
   confirmado). `Estimativa` fica vazia — é decisão de triagem.

Crie em lote, mas **só depois da tabela final**: criar 30 peças erradas de uma vez é o risco número
um desta skill. Confira ao final que cada mãe tem `Subtarefas` preenchido (virou contêiner) e que
cada fase tem `Subtarefa de`; uma fase solta vira tarefa órfã no Kanban.

Em **modo fixture**, liste as páginas que criaria (mãe + fases, campo a campo, com os prazos do
script) sem tocar no Notion.

### 5. Resumo

N peças · N fases · quem ficou com o quê (por pessoa, contagem) · o que ficou em `Triagem` e por
quê · link do calendário editorial. Uma frase de alerta se algum dia útil ficou com mais de uma
peça no mesmo canal, ou se alguma peça clínica ficou sem dono de aprovação.

## O que esta skill não faz

Não escreve o texto da peça (é `mkt-brief-conteudo`), não abre demanda avulsa (`mkt-nova-demanda`),
não muda peça existente, não decide estimativa, não olha carga. Se a pessoa pedir "reorganiza o mês
que já está no Notion", mostre o que existe (Q10) e diga que mover é na UI ou com o coordenador.
