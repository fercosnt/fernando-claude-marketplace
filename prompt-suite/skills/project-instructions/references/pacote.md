# Modo PACOTE — montar o resto do projeto

A instrucao e uma camada. Sozinha ela nao faz o projeto funcionar. Este reference cobre tudo que fica **em volta** do texto: nome, descricao, knowledge, pastas, connectors, skills, memoria e — o mais dificil — como um time inteiro replica o mesmo projeto.

Regra que atravessa o documento: **cada item aqui e uma camada**, e passa pelo mesmo teste de permanencia da secao 2 do SKILL.md. Se um fato cabe num arquivo de knowledge, ele nao vai na instrucao. Se uma pasta ja da o contexto, a instrucao nao precisa descrever o conteudo dela.

---

## 1. Nome e descricao do projeto

Os dois campos que quase todo mundo preenche no automatico e que mudam comportamento.

| Campo | Quem le | Consequencia de errar |
|---|---|---|
| Nome | Voce e o time, na lista de projetos | Projeto duplicado, pessoa abre o errado |
| Description | **O Dispatch do Cowork le a Description ao escolher o projeto de uma tarefa** | Tarefa cai no projeto errado, ou nao cai em nenhum |

No Cowork, Description **nao e enfeite** — e roteamento. Descricao generica ("Projeto de marketing") nao distingue nada e o Dispatch escolhe mal. Escreva a Description como um **gatilho**: que tipo de tarefa pertence aqui, com as palavras que voce realmente usa ao pedir.

Formula: `[o que produz] a partir de [entrada tipica], para [publico]. Use para [gatilhos].`

### Tres exemplos, ruim → bom

| # | Ruim | Bom |
|---|---|---|
| 1 | `Marketing` · "Coisas de marketing" | `Decks Fotona` · "Monta e revisa storyboards de deck de equipamento laser (clinico, vendas, cientifico) a partir de briefing e material do fabricante, para clinicas e distribuidores. Use para: novo deck, revisar storyboard, ajustar slide, roteiro de apresentacao." |
| 2 | `Ads` · "Analise de campanhas" | `Relatorio mensal de midia paga` · "Gera o relatorio mensal de Meta e Google Ads por clinica, a partir de exports de plataforma, para o dono da clinica. Use para: fechar o mes, comparar periodos, explicar queda de resultado, montar recomendacao de verba." |
| 3 | `Contratos` · "Documentos juridicos" | `Revisao de contratos de fornecedor` · "Revisa e checa pre-assinatura contratos de fornecedor e NDAs em portugues, a partir do PDF enviado, para o time de compras. Use para: revisar minuta, checklist de assinatura, comparar versoes, avaliar risco de clausula." |

Sinal de descricao ruim: se ela serve igualmente bem para dois projetos seus, ela nao serve para nenhum.

---

## 2. Knowledge do Chat Project

Knowledge e a camada de **fatos**. Instrucao diz como trabalhar; knowledge diz o que e verdade.

### Criterios

| Anexar | Nao anexar |
|---|---|
| Documento estavel que voce cita sempre (tabela de preco, guia de marca, especificacao tecnica) | Regra de comportamento — isso e instrucao |
| Transcricao ou material de referencia longo demais para colar no chat | Arquivo que muda toda semana e ninguem vai reanexar |
| Exemplos de saida boa (2 ou 3 pecas aprovadas, marcadas como exemplo) | O repositorio inteiro "por garantia" |
| Glossario/vocabulario do time, se for longo | Sigla solta — cabe na instrucao |
| Dados que precisam sobreviver entre chats diferentes do projeto | Rascunho, versao antiga, duplicata |

Dois fatos de plataforma que decidem quase tudo aqui:

- **Contexto nao passa de um chat pro outro** dentro do mesmo projeto a menos que va para o knowledge base. Se o time precisa que a decisao de ontem valha amanha, ela vira arquivo — nao adianta ter sido dita num chat.
- **RAG do project knowledge (ate 10x mais capacidade) e so plano pago.** Em plano gratuito, knowledge grande compete com a janela. Se o time nao e pago, corte antes de anexar.

### Como preparar o arquivo

1. **Nome falante.** `precos-laser-2026-Q1.md`, nao `doc final v3 (2).pdf`. O nome e o primeiro sinal de relevancia.
2. **Cabecalho de sumario** nas primeiras linhas: o que e, para que serve, data, dono. Tres linhas bastam.
3. **Um assunto por arquivo.** Preco num, tom de voz noutro, especificacao tecnica noutro. Arquivo misto e recuperado errado.
4. **Data no conteudo**, nao so no nome — o Claude nao ve a data de modificacao.
5. **Texto acima de imagem.** Tabela em markdown vale mais que print de planilha.

Modelo de cabecalho:

```
# Tabela de precos — linha X — 2026 Q1
Para que serve: valores de referencia para proposta e deck comercial.
Vale ate: 2026-03-31 · Dono: [nome] · Fora de escopo: condicao negociada caso a caso.
```

### Quando o material e grande demais

Em ordem: **resumir → fatiar → linkar**.

| Situacao | O que fazer |
|---|---|
| Documento longo, so uma parte importa | Extraia a parte e anexe so ela, com uma linha dizendo de onde veio |
| Varios assuntos num arquivo so | Fatie por assunto, um arquivo cada |
| Base viva (planilha, sistema) | No Chat Project, congele um recorte com data; no Cowork, prefira Folder ou Connector |
| Material enorme e realmente necessario | Escreva um **indice**: um arquivo curto que lista o que existe e onde, e anexe so os que o projeto usa de fato |

---

## 3. Folders / Links / Projects from Chat (Cowork)

No Cowork o projeto nao "anexa arquivo" — ele **monta o que voce autorizou**. A VM so enxerga as pastas dadas ao projeto. Pasta errada = trabalho travado no meio; pasta larga demais = risco desnecessario e mais ruido de contexto.

| Recurso | Quando usar | Cuidado |
|---|---|---|
| **Folders** | Onde os arquivos de trabalho vivem e onde o entregavel deve ser salvo | De a pasta **especifica do projeto**, nao a home nem o Drive inteiro |
| **Links** | Doc de referencia que vive na web/nuvem e muda sozinho (wiki, planilha viva, doc de processo) | Link nao e garantia de leitura offline; use para referencia, nao para o insumo critico |
| **Projects from Chat** | Ja existe um Chat Project com o knowledge curado do mesmo assunto | Importa o knowledge, nao a instrucao — o modelo mental do chat nao serve pro agentico |

Como escolher as pastas:

1. Liste o que a tarefa **le** e o que ela **escreve**.
2. De a pasta mais rasa que cubra os dois. Se leitura e escrita ficam longe uma da outra, de as duas — nao o ancestral comum.
3. Se uma pasta tem material sensivel que a tarefa nao usa, **nao inclua**: separe antes.
4. Use **Folder instructions** para regra que so vale ali (padrao de nome de arquivo, formato de export). Lembre: instrucoes de pasta **podem ser reescritas pelo proprio Claude durante a sessao** — nao coloque ali nada que precise ser imutavel.

Limite duro: **arquivos individuais de ate 50 MB**. PDF escaneado, video, PSD e export bruto estouram facil. Converta, fatie ou extraia o texto antes.

---

## 4. Connectors e permissao (Cowork)

Connector e capacidade. Permissao e o que separa "assistente util" de "incidente".

| Modo | Comportamento | Use para |
|---|---|---|
| **Manual** | Pede aprovacao a cada uso | Tudo que sai pra fora ou nao tem volta |
| **Auto** | Roda sem perguntar | Leitura e consulta interna, alto volume, baixo dano |
| **Skip** | Connector nao entra na sessao | Connector que o projeto nao usa — reduz ruido e superficie de erro |

**Regra de seguranca, sem excecao:** acao **irreversivel** ou que **sai pra fora** fica em **Manual**. Isso inclui:

- mandar email, mensagem, DM
- publicar, postar, comentar em canal com outras pessoas
- apagar, sobrescrever, mover em massa
- gastar dinheiro (anuncio, compra, upgrade) ou mudar permissao/compartilhamento de arquivo

Leitura de calendario, busca em drive, consulta de metrica: **Auto** e o ganho real de produtividade. O resto do que voce nao usa: **Skip**.

Em tarefa **agendada** o custo do Manual e alto (a tarefa para esperando voce). A saida certa nao e afrouxar para Auto: e desenhar a tarefa para **terminar em rascunho** — deixa o email como draft, o post como rascunho, o arquivo numa pasta de saida — e a instrucao do projeto declara isso na definicao de pronto.

---

## 5. Skills e plugins

Quando uma regra vira skill em vez de ficar na instrucao:

| Vira skill | Fica na instrucao |
|---|---|
| Processo de **uma** tarefa, com passos, que voce quer invocar | Regra que vale em quase toda tarefa do projeto |
| Passa de ~15 linhas e tem checklist proprio | Cabe em 2 ou 3 linhas |
| Usada em mais de um projeto | So faz sentido neste projeto |
| Tem material de apoio (templates, referencias, exemplos) | E so texto |
| Roda de vez em quando | Vale sempre |

Instrucao de projeto carrega **em toda tarefa**. Processo que roda em 1 de 10 tarefas dentro da instrucao e desperdicio de janela — e ensina o Claude a ignorar o resto. Mande pra skill.

**Fato critico:** o **Cowork nao le `~/.claude`**. Skill ou plugin que voce tem no Claude Code **nao aparece sozinho** no Cowork — precisa ser adicionado em **Customize**. Ao montar um pacote para o time, "instalar a skill X" nao e um passo opcional do checklist: sem ele o projeto se comporta diferente na maquina de cada pessoa.

Caminho oficial mais rapido para criar skill: rode o workflow inteiro uma vez, na mao, com o Claude junto — e depois peca:

```
Package what we just did into a skill.
```

Sai uma skill enraizada no processo real, nao no processo imaginado. Revise e versiona no repo.

---

## 6. Memoria

| Chat Project | Cowork Project |
|---|---|
| Memoria do projeto: o que o Claude aprendeu ao longo dos chats | Memory: store proprio do projeto, persiste entre sessoes |
| **Automatico. Nao se escreve.** | **Automatico. Nao se escreve.** |
| **Por projeto** — nao vaza de um projeto pro outro | **Por projeto** — nao vaza de um projeto pro outro |

Consequencias praticas:

- Memoria **nao substitui knowledge nem instrucao** — projeto novo comeca sem memoria, e o pacote precisa funcionar no dia 1 so com instrucao + knowledge/folders + connectors + skills.
- Como e por projeto, **cada pessoa do time tem a propria memoria**. Nada que o time dependa pode morar ali.
- Comportamento que precisa ser garantido vai na camada certa. Memoria e bonus, nao contrato.

---

## 7. Pacote para TIME

A parte mais importante, e a que mais quebra na pratica.

Os dois fatos que definem o problema:

- **Projeto Cowork vive so na maquina: nao sincroniza nem compartilha.**
- **Projeto do chat e compartilhavel apenas em Team/Enterprise.**

Logo: nao existe "mandar o projeto" pro time. O que existe e **um arquivo-fonte versionado** que cada pessoa cola, mais **um checklist de setup replicavel**. Sem isso, em duas semanas existem cinco versoes da instrucao e ninguem sabe qual e a certa.

### Layout do arquivo-fonte

Guarde no repo em `projetos/[nome]/INSTRUCOES.md`. Uma linha de PR muda a instrucao de todo mundo.

````markdown
# [Nome do projeto] — instrucoes de projeto
Alvo: Cowork Project        <!-- ou Chat Project -->
Dono: [nome] · Revisar em: [AAAA-MM-DD] · Versao: 1.2
Para que serve: [uma frase]

## Description do projeto (colar no campo Description)
[uma frase de roteamento — ver secao 1]

## Instrucao (colar em Project instructions)
```
[texto exato da instrucao, pronto pra colar, sem comentario]
```

## Setup replicavel
### Folders / Knowledge
- [ ] Pasta `~/...` adicionada como Folder     <!-- Cowork -->
- [ ] `precos-2026Q1.md` anexado ao knowledge   <!-- Chat -->

### Connectors
| Connector | Modo | Por que |
|---|---|---|
| Google Drive | Auto | so leitura da pasta do projeto |
| Gmail | Manual | envia pra fora |
| [nao usados] | Skip | |

### Skills / Plugins (Customize)
- [ ] `nome-da-skill` — Cowork nao le `~/.claude`, precisa adicionar aqui

## Fora da instrucao (e onde foi parar)
| Regra levantada | Camada |
|---|---|
| [regra] | knowledge / skill / perfil / chat |

## Changelog
- 2026-09-06 · v1.2 · [o que mudou e por que]
````

### Regras de operacao do pacote de time

1. **Fonte unica.** A instrucao no app e **copia**. Alterou no app e funcionou? Volta pro repo no mesmo dia, senao vira divergencia silenciosa.
2. **Versao e changelog** no arquivo — e como alguem descobre que sua copia esta velha.
3. **Sem contexto tacito.** Nada de "como sempre fazemos". Time novo entra sem o historico.
4. **Setup e parte do pacote.** Instrucao identica com connectors diferentes produz resultados diferentes; a pessoa culpa o texto.
5. **Um dono, uma data de revisao.** Instrucao sem dono apodrece.
6. **Teste de replicacao:** peca a alguem que nunca montou o projeto para seguir so o arquivo. O que ela perguntar e o que esta faltando escrever.

---

## 8. Checklist de montagem

### Chat Project

- [ ] Nome distingue de todos os outros projetos seus
- [ ] Description diz o que produz e para quem
- [ ] Instrucao dentro do orcamento (1.500–2.500 caracteres) e com cabecalho de dono/data
- [ ] Nenhum fato dentro da instrucao que deveria ser knowledge
- [ ] Knowledge: um assunto por arquivo, nome falante, cabecalho de sumario, data no conteudo
- [ ] Material grande foi resumido/fatiado, nao despejado
- [ ] Confirmado se o plano e pago (RAG) — se nao for, knowledge foi cortado
- [ ] O que precisa valer entre chats esta no knowledge, nao so dito num chat
- [ ] Processo de tarefa unica virou skill, nao paragrafo da instrucao
- [ ] Se o time vai usar: existe `projetos/[nome]/INSTRUCOES.md` versionado (compartilhamento so em Team/Enterprise)

### Cowork Project

- [ ] Description escrita como gatilho de roteamento — o Dispatch le ela
- [ ] Instrucao cobre: proposito, workflow, definicao de pronto, onde salvar, fronteira de permissao
- [ ] Global instructions enxutas e so sobre voce — nao sobre o projeto
- [ ] Folders: a pasta mais rasa que cobre leitura e escrita; nada sensivel a mais
- [ ] Nenhum arquivo de insumo acima de 50 MB
- [ ] Links usados para referencia viva; Projects from Chat so para importar knowledge curado
- [ ] Folder instructions so com regra local, nada imutavel (o Claude pode reescrever)
- [ ] Connectors: Manual em tudo irreversivel ou que sai pra fora; Auto so leitura; Skip no resto
- [ ] Tarefa agendada termina em rascunho, e a instrucao diz isso
- [ ] Skills e plugins locais adicionados em **Customize** (Cowork nao le `~/.claude`)
- [ ] Projeto funciona no dia 1, sem depender de memoria
- [ ] Se o time vai usar: arquivo-fonte versionado + checklist de setup (projeto Cowork e local, nao compartilha)
