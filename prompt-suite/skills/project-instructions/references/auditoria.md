# Auditoria de instrucao de projeto

Referencia do modo AUDITAR. Use junto com o teste de permanencia (SKILL.md secao 2) e os fatos de plataforma (secao 7). Nomear a falha e metade do trabalho: usuario que sabe o nome da falha para de reintroduzi-la na proxima versao.

---

## 1. Catalogo de falhas nomeadas

### 1.1 Instrucao-curriculo

**Como reconhecer.** Paragrafo inicial que descreve credenciais em vez de trabalho: "voce e um especialista senior com 20 anos de experiencia", "voce e um estrategista de classe mundial", "voce domina profundamente". Costuma ocupar as primeiras 300-600 caracteres e nao contem nenhum verbo de acao dirigido ao Claude.

**Por que quebra.** Nao muda comportamento nenhum e ainda consome janela de contexto — que no Chat Project e disputada com o knowledge (secao 7). Pior: ensina o usuario a medir instrucao por tamanho. Reprova nos tres testes de permanencia de uma vez (nao e duravelmente acionavel, e obvia, e nao tem casa em lugar nenhum).

**RUIM**
```
Voce e um especialista senior em marketing digital com mais de 20 anos de
experiencia, reconhecido no mercado, com dominio profundo de performance,
branding e growth. Voce pensa como um CMO de classe mundial.
```

**BOM**
```
Este projeto produz briefings de campanha para a equipe de midia paga.
Quando eu descrever uma campanha, entregue: objetivo, publico, oferta,
3 angulos de mensagem, KPI primario. Sem introducao.
```

---

### 1.2 Regra morta

**Como reconhecer.** Regra cujo gatilho nunca aparece no trabalho real daquele projeto. Teste: peca ao usuario 3 tarefas tipicas do ultimo mes e pergunte em quantas a regra teria disparado. Zero ou uma = morta. Sintomas textuais: "se o usuario enviar codigo em Rust", "caso seja um contrato internacional", num projeto que so faz post de Instagram.

**Por que quebra.** Regra morta nao e neutra. Ela dilui as regras vivas: o modelo processa um bloco de condicoes em que a maioria nunca se aplica, e a instrucao inteira passa a ler como sugestao. Reprova no teste de durabilidade (8 em 10).

**RUIM**
```
Se eu pedir analise juridica, cite a legislacao aplicavel.
Se eu enviar planilha financeira, valide as formulas antes.
Se o material for em ingles, mantenha o idioma original.
```

**BOM**
```
(as tres cortadas — nenhuma disparou nas ultimas 20 tarefas do projeto)
Toda peca sai em portugues do Brasil. Se eu pedir outro idioma, pergunte
qual variante antes de escrever.
```

---

### 1.3 Enciclopedia

**Como reconhecer.** Fatos colados dentro da instrucao: tabela de precos, lista de produtos, codigos hex da marca, nomes de todos os clientes, historico da empresa, especificacoes tecnicas. Sinal facil: blocos que envelhecem sozinhos e que ninguem consegue revisar sem consultar outra fonte.

**Por que quebra.** Fato dentro da instrucao carrega em toda conversa, mesmo quando irrelevante, e desatualiza em silencio — ninguem lembra de editar a instrucao quando o preco muda. O lugar certo e o knowledge (Chat) ou uma folder/link (Cowork), consultado sob demanda. Em plano pago o knowledge ainda ganha RAG; a instrucao nunca ganha.

**RUIM**
```
Nossos planos: Starter R$ 490/mes (ate 3 usuarios), Pro R$ 1.290/mes
(ate 15), Enterprise sob consulta. Cores: #1B3A5C, #F2A03D, #FFFFFF.
Clientes ativos: Alfa, Beta, Gama, Delta, Epsilon...
```

**BOM**
```
Precos e paleta estao em `tabela-precos.pdf` e `guia-de-marca.pdf` no
knowledge. Consulte antes de citar qualquer numero; se o dado nao estiver
la, diga que nao tem e pergunte.
```

---

### 1.4 Tom sem exemplo

**Como reconhecer.** Adjetivos empilhados sem amostra: "envolvente e profissional", "tom leve mas autoridade", "humano, nao robotico", "direto ao ponto". Nenhuma linha de texto de exemplo em lugar nenhum da instrucao.

**Por que quebra.** Adjetivo de tom nao tem referente compartilhado — "profissional" para o time juridico e outra coisa para o time de social. O modelo cai no default. Uma linha de amostra fixa o registro melhor que tres adjetivos.

**RUIM**
```
Escreva de forma envolvente e profissional, com tom leve mas mantendo
autoridade tecnica.
```

**BOM**
```
Tom: frase curta, sem adjetivo de venda, voce fala com dentista ocupado.
Assim: "O laser reduz o tempo de cadeira em 30%. O paciente sai no mesmo dia."
Nao assim: "Uma revolucao incrivel que vai transformar sua clinica!"
```

---

### 1.5 Conflito silencioso

**Como reconhecer.** Duas regras que nao podem ser obedecidas juntas — dentro da propria instrucao, contra o knowledge, ou contra o perfil global. Procure pares: tamanho x completude ("seja breve" + "sempre justifique cada escolha"), autonomia x fronteira ("nao pergunte, decida" + "confirme antes de qualquer entrega"), instrucao x arquivo ("use tom formal" com um guia de marca informal no knowledge).

**Por que quebra.** A Anthropic documenta precedencia apenas de organization > individual; entre project instructions, perfil, memoria e skills **nao ha ordem documentada** (secao 7). Ou seja: em conflito o resultado e imprevisivel e varia entre conversas — o que o usuario relata como "as vezes obedece, as vezes nao". A correcao nunca e escolher uma ordem inventada; e eliminar o conflito.

**RUIM**
```
Responda sempre em no maximo 3 bullets.
...
Para cada recomendacao, explique o raciocinio, cite as fontes do knowledge
e liste os riscos considerados.
```

**BOM**
```
Padrao: ate 3 bullets, sem justificativa.
Quando eu escrever "detalha", ai sim: raciocinio, fonte do knowledge e
riscos, sem limite de tamanho.
```

---

### 1.6 Negativa orfa

**Como reconhecer.** "Nao faca X" sem dizer o que fazer no lugar. Varredura rapida: grep mental por "nao ", "nunca ", "evite ", "jamais " — cada ocorrencia precisa de um substituto na mesma frase ou na seguinte.

**Por que quebra.** Negativa sozinha define o complemento do comportamento desejado, que e um espaco enorme. O modelo evita X e cai em Y, que muitas vezes e pior. Alem disso a negativa mantem o conceito proibido ativo no contexto.

**RUIM**
```
Nao seja prolixo. Nao use jargao corporativo. Nao invente dados.
```

**BOM**
```
Resposta padrao em ate 5 bullets; texto corrido so se eu pedir.
Escreva no vocabulario do time comercial (ticket, funil, agenda cheia)
e nao no de consultoria (sinergia, alavancar, end-to-end).
Numero so sai daqui se estiver no knowledge; se nao estiver, escreva
"sem dado" e diga qual arquivo faltou.
```

---

### 1.7 Cowork conversacional

**Como reconhecer.** Instrucao de Cowork Project escrita como se governasse a resposta do chat: tom, tamanho de mensagem, "explique seu raciocinio", "faca perguntas de acompanhamento", "seja proativo nas sugestoes". Falta o oposto: onde salvar, o que e "pronto", o que exige autorizacao.

**Por que quebra.** Cowork Project e agentico — governa o que e FEITO, nao como a fala sai. Instrucao conversacional produz o projeto que conversa bonito e nao entrega arquivo, ou entrega em lugar nenhum. Em tarefa agendada e pior: nao ha ninguem lendo a resposta, so o artefato importa. E tom pessoal ja tem casa: Global instructions do Cowork.

**RUIM**
```
Seja um parceiro estrategico. Explique seu raciocinio passo a passo,
faca perguntas de acompanhamento e sugira melhorias de forma proativa.
```

**BOM**
```
Entregavel: um .xlsx em `~/relatorios/[ano]/[mes]/`, nome `fechamento-YYYY-MM.xlsx`.
Pronto = todas as abas preenchidas, sem celula #N/A, e um resumo de 5 linhas
no topo da aba Resumo.
Nunca sobrescreva arquivo existente — crie `-v2` e me avise.
Pare e pergunte antes de: enviar e-mail, apagar arquivo, alterar planilha fonte.
```

---

### 1.8 Chat agentico

**Como reconhecer.** Instrucao de Chat Project mandando o Claude salvar em pasta, rodar sozinho, agendar, monitorar, "atualize o arquivo X ao final", "guarde isso para os proximos chats", "execute diariamente".

**Por que quebra.** Chat Project nao tem essas capacidades. Alem disso o contexto **nao e compartilhado entre chats** do mesmo projeto a menos que va para o knowledge base (secao 7) — entao "lembre disso nos proximos chats" nao acontece por instrucao. A memoria de projeto existe, mas e automatica: nao se escreve, nao se comanda. Instrucao que pede o impossivel treina o usuario a desconfiar de todo o resto do texto.

**RUIM**
```
Ao final de cada conversa, salve o resumo em /projetos/atas/ e atualize
o arquivo de decisoes. Lembre-se disso nas proximas conversas.
```

**BOM**
```
Ao final, entregue o resumo em bloco de codigo com o titulo
`ata-AAAA-MM-DD`. Eu colo no knowledge — o que nao esta no knowledge
nao chega ao proximo chat.
```
> Se o usuario precisa mesmo de salvar/rodar sozinho: o alvo dele e Cowork Project, nao Chat. Diga isso na auditoria em vez de so reescrever a linha.

---

### 1.9 Instrucao-prompt

**Como reconhecer.** Uma tarefa especifica congelada na instrucao permanente: "analise a campanha de Black Friday 2025", "compare estes tres fornecedores", "revise o contrato da Acme". Datas, nomes proprios de um caso unico, e passo-a-passo de algo que aconteceu uma vez.

**Por que quebra.** Reprova no teste de durabilidade e ainda contamina todas as outras conversas do projeto com o enquadramento de um caso morto — o modelo passa a puxar Black Friday em fevereiro. Se o processo se repete e tem passos, a casa e uma skill; se acontece uma vez, e mensagem de chat.

**RUIM**
```
Analise a campanha de Black Friday 2025 da Acme: compare CPA de novembro
com outubro, avalie os 4 criativos e recomende o corte de verba.
```

**BOM**
```
(vira mensagem de chat, ou skill `analise-campanha` se repetir todo mes)
Na instrucao fica so o duravel:
Toda analise de campanha compara o periodo pedido com o periodo anterior
equivalente e termina com uma recomendacao de verba (manter/cortar/escalar).
```

---

## 2. Diagnostico por sintoma

O usuario relata sintoma, nao falha. Esta tabela traduz. Cheque a coluna 3 **antes** de reescrever qualquer texto.

| Sintoma relatado | Causa mais provavel | O que checar primeiro |
|---|---|---|
| "ele ignora as instrucoes" | Instrucao longa demais, ou conflito silencioso, ou regra que na verdade precisava de knowledge/skill | Conte caracteres e regras. Acima do orcamento (Chat: 1.500-2.500), corte antes de qualquer coisa. Depois varra pares contraditorios (1.5) e regra morta (1.2) |
| "responde generico" | Instrucao-curriculo no lugar de regra de trabalho, ou tom sem exemplo | Tem exemplo concreto de output em algum lugar? Tem publico e entregavel nomeados? Se a instrucao so descreve quem o Claude e, ela nao tem conteudo |
| "inventa dado" | Fato deveria estar no knowledge e nao esta — ou esta na instrucao, desatualizado (enciclopedia) | Onde vive o numero que ele inventou? Se em lugar nenhum: falta arquivo, nao falta regra. Se na instrucao: mova e adicione a regra de "sem dado, diga sem dado" |
| "responde longo demais" | Negativa orfa ("nao seja prolixo") ou conflito tamanho x completude | Procure "nao seja prolixo"/"seja conciso" sem numero. Substitua por limite contavel e um gatilho de escape ("quando eu escrever 'detalha'") |
| "esquece o que combinamos entre chats" | Expectativa de memoria que a plataforma nao da por instrucao | Contexto nao e compartilhado entre chats a menos que va para o knowledge base. O que precisa persistir vira arquivo no knowledge — nao linha de instrucao |
| "no Cowork ele conversa em vez de entregar" | Cowork conversacional: instrucao sem definicao de pronto nem destino | A instrucao diz ONDE salva, COM QUE NOME e o que conta como pronto? Se nao, nao ha o que obedecer. Tom pessoal, se existir, migra para Global instructions |
| "escolhe o projeto errado" | Description generica — o Dispatch le a Description ao rotear a tarefa | Leia a Description como se fosse a unica coisa que o roteador ve. Vale para varios projetos = generica. Reescreva com o objeto de trabalho e o gatilho tipico |
| "num projeto funciona, no outro nao" | Regra vive na camada errada (projeto vs global vs pasta) | Cowork empilha global > projeto > pasta. Regra que deveria valer sempre esta so num projeto, ou o inverso. Note tambem: instrucao de pasta pode ser reescrita pelo proprio Claude durante a sessao |
| "o time nao ve as mesmas instrucoes" | Projeto Cowork vive so na maquina — nao sincroniza nem compartilha | Confirme o alvo. Cowork exige arquivo-fonte versionado como origem da verdade. Projeto de chat so e compartilhavel em Team/Enterprise |
| "ignora os arquivos que anexei" | Volume de knowledge vs plano, ou instrucao que nao manda consultar | Ha uma regra explicita de quando consultar cada arquivo? RAG do project knowledge e so plano pago. No Cowork, cheque tambem o limite de 50 MB por arquivo |

---

## 3. Formato do relatorio de auditoria

Entregue exatamente nesta ordem. Sem elogio de abertura, sem resumo do que o usuario ja sabe.

### 3.1 Contagem

Tres linhas, numeros reais:

```
Tamanho: 4.180 caracteres (orcamento Chat Project: 1.500-2.500)
Regras identificadas: 14
Passam no teste de permanencia: 5 · Reprovam: 9 (4 mortas, 3 enciclopedia, 2 sem casa)
```

Se o alvo for Cowork, troque a linha de orcamento por: definicao de pronto presente? destino de arquivo presente? fronteira de permissao presente? (sim/nao para cada).

### 3.2 Tabela trecho -> veredito

Uma linha por trecho, na ordem em que aparecem no original. Veredito e uma das quatro palavras: `manter`, `reescrever`, `mover para X`, `cortar`. Toda linha que nao seja `manter` cita a falha nomeada.

| # | Trecho (primeiras palavras) | Veredito | Falha | Motivo em uma linha |
|---|---|---|---|---|
| 1 | "Voce e um especialista senior..." | cortar | instrucao-curriculo | Nao muda comportamento e come contexto |
| 2 | "Planos: Starter R$ 490..." | mover para knowledge | enciclopedia | Fato que desatualiza sozinho; vira `tabela-precos.pdf` |
| 3 | "Nao seja prolixo" | reescrever | negativa orfa | Sem substituto contavel |
| 4 | "Se eu pedir analise juridica..." | cortar | regra morta | Nao disparou em nenhuma das tarefas citadas |
| 5 | "Toda peca cita a fonte" | manter | — | Duravel, nao-obvia, sem casa melhor |

Nunca use `cortar` sozinho para regra que o usuario claramente quer: use `mover para X` e diga o X.

### 3.3 Versao reescrita completa

A instrucao inteira, nova, em bloco de codigo pronto pra colar — nao trechos avulsos, nao diff. Com o cabecalho de time:

```
Dono: [nome] · Revisar em: [data]
Para que serve: [uma frase]
```

Logo abaixo do bloco, tres linhas fixas:

- **Onde colar:** [Project instructions do projeto X / Settings > Cowork > Global / Folder instructions de ~/pasta]
- **O que saiu e para onde foi:** lista curta `trecho -> camada` (knowledge, skill, perfil, Description, ou "virou mensagem de chat")
- **O que voce precisa criar:** arquivos de knowledge, skill ou connector que a nova instrucao pressupoe e ainda nao existem

### 3.4 Testes concretos

Dois ou tres pedidos reais que devem se comportar diferente agora. Cada um em uma linha: o pedido, e o que muda. Sem "verifique se ficou melhor".

```
1. Cole a transcricao da ultima reuniao e peca o resumo.
   Antes: 8 paragrafos com introducao. Agora: 5 bullets, sem introducao,
   terminando em action items com dono.

2. Pergunte "quanto custa o plano Pro?".
   Antes: inventava um numero. Agora: cita `tabela-precos.pdf` ou responde
   "sem dado" e diz qual arquivo faltou.

3. Peca "detalha" logo apos uma resposta curta.
   Antes: nao existia esse gatilho. Agora: abre raciocinio, fontes e riscos.
```

Se algum teste depende de arquivo que ainda nao foi para o knowledge, diga isso na propria linha do teste — o usuario vai rodar e achar que a instrucao falhou.
