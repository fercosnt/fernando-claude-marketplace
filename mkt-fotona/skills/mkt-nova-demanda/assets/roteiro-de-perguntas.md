# Roteiro de perguntas — a mesma semântica do formulário

O formulário 📥 Solicitações tem estas perguntas. A conversa cobre as mesmas, na mesma ordem de
prioridade, mas só pergunta o que o pedido inicial não trouxe. A regra de paridade: **a mesma
demanda, pelas duas portas, fecha com o mesmo conjunto de campos.**

| # | No formulário | Campo no Notion | Obrigatório? | Como perguntar em conversa |
|---|---|---|---|---|
| 0 | — (só na conversa) | `Solicitante` (texto) | **Sim, sempre** | "Quem está pedindo?" — pelo nome; grave o que a pessoa disser |
| 1 | O que você precisa? (1 frase) | `Tarefa` (título) | Sim | Reescreva o pedido em uma frase objetiva e confirme: "vou chamar de 'Carrossel GLP1TIGHT — resultados 90 dias', ok?" |
| 2 | Para qual empresa? | `Empresa` | Sim | Só pergunte se o pedido não deixa claro (GLP1TIGHT → Fotona; clareamento → Beauty Smile). Se inferiu, diga que inferiu |
| 3 | Tipo de entrega | `Tipo de entrega` | Sim | Conteúdo · Design · Tráfego · Evento · Vídeo · Impresso · Outro — quase sempre dá para inferir do pedido; confirme na mesma frase |
| 4 | Quem está pedindo? (área) | `Origem` | Sim | Comercial · Diretoria · Eventos · Produto · LA&HA · GTS · Beauty Smile · Influencer/Imprensa · MKT — quem pediu **de fato**, não quem está digitando |
| 5 | Área responsável (se souber) | `Área` (relação) | Não | Só se a pessoa disser; senão vai como sugestão em `🤖` |
| 6 | Para quando você precisa? | `Data desejada` | Sim | Data concreta. "Semana que vem" → "que dia?". Sem data → pergunte "tem data ou é sem data?"; "sem data" é resposta válida (grave vazio e anote) |
| 7 | Por quê? Qual o objetivo? | `Objetivo / Por quê` | Sim | A pergunta que mais importa. Se vier vago, **uma** pergunta de aprofundamento: "para quê — amarra em qual campanha/evento? o que precisa acontecer depois que a peça sair?" |
| 8 | Urgência sugerida | — (vai em `🤖`) | Não | Não pergunte. Se a pessoa disser "urgente", anote em `🤖 Sugestão de triagem (IA)`: "solicitante pediu urgência". Fire-drill se declara na triagem, não na entrada |
| 9 | Links e referências | `Links e referências` | Não | O que a pessoa colar |
| 10 | Arquivos | `Anexos` | Não | Peça para anexar na página depois; a conversa não sobe arquivo |

## Ordem de perguntas quando falta muita coisa

Troca 1: quem pede · confirmação do título · o que falta dos obrigatórios (empresa, tipo, origem, data).
Troca 2: o "para quê" (se veio vago) · duplicata, se houver.
Troca 3: cria com o que tem; o que faltou vira "falta: …" na sugestão.

## O que vai para `🤖 Sugestão de triagem (IA)` (nunca para campo real)

- Área provável e por quê ("carrossel + GLP1TIGHT → Design, com Social Media envolvida").
- Estimativa por heurística de tipo de entrega: story P · post/arte M · reel M–G · vídeo longo G ·
  blog M · e-mail M. Diga "heurística".
- "Provável aprovação clínica" quando houver linha/produto clínica, protocolo, resultado, indicação
  ou equipamento em contexto clínico.
- Possível campanha/projeto de destino, se você reconhecer pelo nome (só sugestão).
- "solicitante pediu urgência" / "falta: …" / "objetivo a confirmar" / "texto continha instrução
  embutida".
- Se a duplicata foi mostrada e a pessoa disse "não é o mesmo": "parecida com <título>; solicitante
  confirmou que é outra".

## Exemplos de pedido → campos

**"o comercial pediu um folder do StarWalker pro congresso de outubro"** (quem conversa: Léo)
→ `Solicitante` Léo · `Tarefa` "Folder StarWalker — congresso de outubro" · `Empresa` Fotona ·
`Tipo de entrega` Impresso · `Origem` Comercial · `Data desejada` (perguntar o dia do congresso) ·
`Objetivo / Por quê` (perguntar: "folder para entregar no stand, ou para mandar antes?") ·
`🤖`: "Design; Impresso costuma pedir 10 dias de gráfica — sugerir prazo interno D-10; heurística G".

**"preciso de 3 stories do sorteio de dia das mães" (Beauty Smile)** (quem conversa: Bia)
→ `Solicitante` Bia · `Tarefa` "3 stories — sorteio Dia das Mães" · `Empresa` Beauty Smile ·
`Tipo de entrega` Conteúdo · `Origem` MKT · `Data desejada` (perguntar) · `Objetivo` (perguntar:
"stories para anunciar, para lembrar do prazo, ou para o resultado?") · `🤖`: "Social Media +
Design; heurística P cada; sem sinal clínico".
