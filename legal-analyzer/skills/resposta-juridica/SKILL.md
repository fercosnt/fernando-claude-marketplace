---
name: resposta-juridica
description: Gera respostas formais em portugues brasileiro para consultas juridicas comuns de rotina — pedido de NDA, duvida de fornecedor, notificacao de descumprimento contratual, solicitacao de dados sob LGPD, pedido de informacao contratual. Usar sempre que o usuario pedir ajuda para responder um e-mail juridico, redigir resposta formal, escrever comunicacao a fornecedor, responder notificacao, responder pedido de dados pessoais, ou qualquer comunicacao de natureza contratual/juridica com linguagem formal. Tambem ativar ao mencionar "resposta", "redigir e-mail juridico", "responder notificacao", "comunicacao formal a fornecedor", "responder titular de dados", "resposta padrao", "template de resposta" — mesmo sem usar a palavra "template". CRITICO: antes de redigir, rastrear gatilhos de escalacao (litigio, regulatorio, criminal, midia, executivo) — se detectados, bloquear template e recomendar advogado.
---

# Resposta Juridica Templated

Skill para redigir respostas formais a consultas juridicas de rotina. O foco e dar ao usuario — que nao e advogado — um texto pronto, em portugues brasileiro formal, que resolva situacoes comuns sem expor a empresa. Quando a situacao sai do rotineiro, a skill **bloqueia o template** e encaminha para um advogado.

## Jurisdicao e idioma

- Jurisdicao: Brasil (legislacao federal)
- Idioma: portugues brasileiro formal — tratamento por "Vossa Senhoria" ou "Prezado(a) Senhor(a)"; sem girias, sem contracoes informais
- Citacoes legais: apenas artigos reais — nunca inventar referencia legislativa

## Fluxo obrigatorio

Independentemente do tipo de resposta solicitado, seguir nesta ordem:

1. **Coleta minima** — entender a situacao (quem pediu, o que pediu, contexto)
2. **Rastreio de escalacao** — verificar os 5 gatilhos antes de qualquer redacao
3. **Se escalacao detectada** — bloquear, explicar o motivo, recomendar advogado, oferecer apenas comunicacao de "acuso recebimento"
4. **Se nao houver escalacao** — identificar o template aplicavel e redigir
5. **Entregar** com assunto sugerido, corpo formal e disclaimer

A etapa 2 e inegociavel. E o que diferencia esta skill de um gerador de texto generico — proteger o usuario de assinar algo que devia ter passado pelo juridico.

## Gatilhos de escalacao (bloqueiam template)

Se **qualquer** dos 5 gatilhos abaixo estiver presente na situacao, **nao redigir o template**. Responder com o bloco de escalacao (ver secao "Bloco de escalacao" abaixo).

### 1. Litigio potencial ou ativo
Sinais:
- Citacao judicial, intimacao, mandado, carta precatoria
- Menciona "processo", "acao judicial", "oficio de juiz", "vara civel/criminal/trabalhista"
- Notificacao extrajudicial com ameaca explicita de acao judicial
- Outra parte ja contratou advogado que se manifestou
- Conflito com valor relevante e risco concreto de judicializacao
- Pedido de preservacao de provas (litigation hold)

### 2. Regulatorio
Sinais:
- Oficio, notificacao ou requisicao de orgao publico (ANPD, CADE, Receita Federal, Ministerio do Trabalho, ANVISA, ANATEL, BACEN, CVM, PROCON, Ministerio Publico, TCU, CGU)
- Auto de infracao, termo de ajustamento de conduta (TAC), termo de compromisso
- Fiscalizacao ou investigacao administrativa em curso
- Pedido de informacoes com prazo legal definido por autoridade
- Incidente de dados pessoais reportavel a ANPD (prazo 48h — nao use template generico)

### 3. Criminal
Sinais:
- Suspeita ou alegacao de fraude, corrupcao, desvio, peculato, lavagem de dinheiro
- Investigacao policial, inquerito, termo circunstanciado
- Denuncia anonima sobre conduta ilicita
- Assedio moral/sexual, discriminacao
- Violacao a Lei Anticorrupcao (12.846/2013), Codigo Penal, Lei de Lavagem (9.613/1998)
- Conduta que possa caracterizar crime ambiental, tributario ou contra ordem economica

### 4. Midia / reputacional
Sinais:
- Jornalista contatou solicitando posicionamento
- Publicacao em imprensa ou midia social com potencial viral
- Reclamacao publica em Reclame Aqui, redes sociais com engajamento alto
- Crise envolvendo figuras publicas, celebridades, politicos
- Risco de boicote, cancelamento, exposicao negativa da marca

### 5. Executivo / societario
Sinais:
- Assunto envolve C-Level, conselho, socios, acionistas
- Disputa societaria, exclusao de socio, dissolucao
- M&A, reestruturacao, operacao de capital
- Comunicacao destinada a investidor, auditoria, due diligence
- Questao que envolve poderes de representacao, governanca, compliance corporativo
- Assunto classificado como material non-public information (MNPI)

### Como rastrear
Antes de redigir, fazer um check mental rapido:
- A situacao envolve um terceiro que ja acionou ou ameacou acionar a justica?
- Tem orgao publico envolvido ou prazo legal regulatorio?
- Ha qualquer mencao a conduta potencialmente ilicita?
- A imprensa ou redes sociais estao envolvidas?
- O assunto extrapola o nivel operacional?

Na duvida, **escalar**. O custo de escalar um caso rotineiro por excesso de cautela e baixo. O custo de tratar um caso critico com template padrao e alto.

## Bloco de escalacao

Quando qualquer gatilho for detectado, entregar esta estrutura (adaptar ao caso concreto):

```
# Escalacao recomendada — nao usar template padrao

## Gatilho(s) identificado(s)
- [Gatilho especifico encontrado na situacao]
- [Justificativa objetiva — o que na situacao disparou o gatilho]

## Por que isto exige advogado
[1-2 paragrafos explicando o risco concreto: exposicao, prazo legal, implicacao regulatoria, etc. Citar artigo de lei quando aplicavel, sem inventar.]

## O que voce pode fazer agora (sem advogado)
1. Nao responder ao merito — evitar confirmar fatos, reconhecer obrigacoes ou assumir responsabilidades
2. Preservar evidencias — guardar e-mails, mensagens, documentos relacionados
3. Nao destruir documentos — mesmo que rotineiramente descartaveis
4. Nao comentar publicamente nem em redes sociais

## Sugestao de comunicacao minima (apenas acuso de recebimento)
Se precisar responder para nao parecer omisso, use apenas:

"Prezado(a) Senhor(a),

Acuso o recebimento de sua comunicacao datada de [data], recebida em [data].

O assunto esta sendo encaminhado a area responsavel para analise. Retornaremos tempestivamente apos avaliacao interna.

Atenciosamente,
[nome]
[cargo]
[empresa]"

## Proximo passo
Acione imediatamente:
- Departamento juridico interno, OU
- Advogado externo especializado em [area: civel / regulatorio / criminal / societario / comunicacao de crise]

Leve ao advogado: a comunicacao original, contratos relacionados, historico do caso, e esta avaliacao.

---
⚠️ Esta analise nao constitui parecer juridico. O encaminhamento a advogado e obrigatorio dada a natureza do caso.
```

O tom do bloco de escalacao deve ser firme e claro — o usuario precisa entender que isto nao e um pedido, e uma recomendacao profissional baseada em risco real.

## Templates de resposta (quando nao ha escalacao)

Identificar qual template se aplica. Se o pedido combinar dois tipos (ex: fornecedor pergunta sobre NDA), usar o mais especifico ou combinar elementos.

### Template 1: Pedido de NDA

Quando: contraparte solicitou assinatura de NDA, ou usuario precisa propor NDA para iniciar conversas.

**Coleta minima antes de redigir:**
- Quem e a contraparte (empresa, pessoa fisica)?
- Objetivo da troca de informacoes?
- Quem proposta: a empresa do usuario ou a contraparte?
- Ha minuta ja em negociacao?

**Corpo da resposta:**

```
Assunto: Acordo de Confidencialidade — [projeto / tema]

Prezado(a) [nome],

Em atencao ao contato referente a [tema/projeto], confirmamos interesse em formalizar as conversas iniciais por meio de Acordo de Confidencialidade (NDA) previamente a qualquer troca de informacoes sensiveis.

[ESCOLHER UMA DAS OPCOES:]

[Opcao A — usuario vai enviar minuta]
Encaminharemos, na sequencia, nossa minuta padrao de NDA para avaliacao de Vossa Senhoria. A minuta contempla (i) obrigacao mutua de confidencialidade, (ii) prazo de vigencia de [2 a 5] anos, (iii) ressalvas de informacao publica, de posse previa, desenvolvida independentemente ou obtida de terceiros sem violacao, e (iv) foro da comarca de [cidade].

[Opcao B — recebeu minuta da contraparte]
Recebemos a minuta encaminhada e a submeteremos a revisao interna. Retornaremos com eventuais comentarios ou proposta revisada em ate [X] dias uteis.

[Opcao C — NDA padrao da contraparte e aceitavel]
Analisamos a minuta e informamos concordancia com os termos propostos. Seguimos para assinatura mediante [DocuSign / outro].

Permanecemos a disposicao para esclarecimentos.

Atenciosamente,
[nome]
[cargo]
[empresa]
```

**Ressalvas:**
- Se contraparte exigir unilateral (so o usuario se obriga), sinalizar para negociar mutuo
- Se prazo for > 5 anos ou survival > 5 anos, sinalizar como atipico
- Se houver non-compete embutido, ESCALAR (gatilho: assunto envolve restricao concorrencial — exige advogado)

### Template 2: Duvida de fornecedor

Quando: fornecedor enviou pergunta sobre contrato, processo, documentacao, prazo.

**Coleta minima:**
- Qual a duvida especifica?
- Ha contrato vigente entre as partes?
- Ha prazo associado a resposta?
- E informacao que o usuario pode responder ou precisa validar com outra area?

**Corpo da resposta:**

```
Assunto: Re: [assunto original]

Prezado(a) [nome],

Em atencao a sua mensagem referente a [tema], prestamos os seguintes esclarecimentos:

[CORPO — escolher formato conforme caso:]

[Se resposta direta possivel]
1. Sobre [ponto 1]: [resposta clara, objetiva, baseada em fato ou clausula contratual — ex: "conforme Clausula X.Y do contrato firmado em [data], o prazo de entrega e de [N] dias a contar do pedido"]
2. Sobre [ponto 2]: [resposta]

[Se precisa validar internamente]
A questao esta em avaliacao pela area responsavel. Retornaremos em ate [X] dias uteis com posicionamento.

[Se depende de informacao do fornecedor]
Para que possamos prosseguir com a analise, solicitamos:
- [informacao 1]
- [informacao 2]

Permanecemos a disposicao.

Atenciosamente,
[nome]
[cargo]
[empresa]
```

**Ressalvas:**
- Nunca confirmar valores, prazos ou obrigacoes sem verificar contrato — pedir validacao se necessario
- Nao reconhecer inadimplemento ou culpa da empresa usuaria sem analise — neste caso, ESCALAR se houver ameaca de cobranca formal

### Template 3: Notificacao de descumprimento contratual (enviar)

Quando: usuario precisa notificar fornecedor/contraparte de inadimplemento ou violacao contratual.

**Coleta minima:**
- Qual contrato? (tipo, partes, data)
- Qual a obrigacao descumprida? (clausula especifica)
- Ha prazo de cura previsto no contrato?
- Valor ou impacto envolvido?
- Ja houve tentativa amigavel anterior?

**Importante:** Esta e uma notificacao *formal com efeitos juridicos* (constituir em mora, interromper prescricao, abrir prazo de cura). Se a situacao evoluir, sera prova documental. Na duvida sobre efeitos juridicos, ESCALAR.

**Corpo da resposta:**

```
Assunto: Notificacao — Descumprimento Contratual — Contrato [numero/identificador]

[empresa], pessoa juridica de direito privado, inscrita no CNPJ sob n. [XX.XXX.XXX/XXXX-XX], com sede em [endereco], vem, por meio desta, NOTIFICAR [contraparte], inscrita no CNPJ sob n. [XX.XXX.XXX/XXXX-XX], nos seguintes termos:

1. As partes celebraram, em [data], o Contrato de [tipo] cujo objeto consiste em [resumo do objeto].

2. Nos termos da Clausula [X.Y] do referido instrumento, V.Sa. assumiu a obrigacao de [descricao da obrigacao].

3. Constata-se, contudo, que [descrever o descumprimento com fatos objetivos, datas, valores quando cabivel].

4. Diante do exposto, fica V.Sa. NOTIFICADA a, no prazo de [N] dias a contar do recebimento desta, [sanear a mora / cumprir a obrigacao / apresentar justificativa / pagar o valor de R$ XXX], sob pena de [consequencia prevista no contrato — multa, rescisao, execucao das garantias].

5. A presente notificacao tem por finalidade constituir V.Sa. em mora, na forma do art. 397, paragrafo unico, do Codigo Civil, e resguardar todos os direitos desta parte notificante.

Atenciosamente,
[cidade], [data].

[nome]
[cargo]
[empresa]
```

**Ressalvas:**
- Se contraparte ja respondeu com ameaca de acao judicial, ESCALAR (gatilho litigio)
- Se houver divida liquida, certa e exigivel e o usuario pretender protestar ou executar — ESCALAR
- Recomendar envio por meio com prova de recebimento (AR, cartorio de titulos, e-mail registrado)

### Template 4: Pedido de dados sob LGPD

Quando: titular de dados pessoais (cliente, funcionario, fornecedor PF, visitante do site) exerce direito previsto nos arts. 17-22 da LGPD — confirmacao de tratamento, acesso, correcao, anonimizacao, portabilidade, eliminacao, informacao sobre compartilhamento, revogacao de consentimento.

**Prazo legal:** 15 dias (art. 19, caput — confirmacao e acesso). Nao ignorar. Se exigir analise complexa, comunicar prazo ao titular.

**Coleta minima:**
- Qual direito o titular exerce (acesso, correcao, eliminacao, etc.)?
- E titular identificado (cliente, funcionario)?
- Ha base legal para o tratamento (consentimento, contrato, obrigacao legal, etc.)?
- Os dados ainda existem / estao sob tratamento?

**Corpo da resposta:**

```
Assunto: Re: Solicitacao — Direitos do Titular — LGPD

Prezado(a) [nome],

Confirmamos o recebimento de sua solicitacao, datada de [data], referente ao exercicio do direito de [confirmacao de tratamento / acesso / correcao / eliminacao / portabilidade / revogacao de consentimento / informacao sobre compartilhamento], previsto no art. [17/18] da Lei n. 13.709/2018 (Lei Geral de Protecao de Dados Pessoais).

[ESCOLHER CONFORME O CASO:]

[Se pode atender diretamente — confirmacao / acesso]
Em atencao ao seu pedido, informamos que:
- Confirmamos o tratamento de seus dados pessoais em nossa base.
- Os dados tratados sao: [categorias — ex: nome, CPF, e-mail, endereco].
- Finalidade do tratamento: [ex: execucao de contrato de prestacao de servicos firmado em DD/MM/AAAA].
- Base legal: [art. 7, [inciso] — ex: inciso V, execucao de contrato].
- Compartilhamento: [listar operadores/controladores, ou informar que nao ha].
- Periodo de retencao: [ex: pelo prazo do contrato + 5 anos para fins fiscais].

[Se pedido de eliminacao e ha base legal concorrente]
Registramos seu pedido de eliminacao. Informamos, contudo, que parte de seus dados sera mantida com fundamento em [obrigacao legal — art. 16, I / exercicio regular de direitos em processo — art. 16, III], especificamente [detalhar]. Os dados nao sujeitos a essa retencao serao eliminados no prazo de [N] dias.

[Se pedido exige prazo adicional]
Seu pedido foi registrado. Dada a complexidade da solicitacao, informamos que a resposta definitiva sera encaminhada em ate [15 dias / prazo prorrogado com justificativa], conforme art. 19 da LGPD.

[Se precisa confirmar identidade]
Para resguardar seus direitos e evitar acesso indevido por terceiros, solicitamos confirmacao de identidade mediante [envio de documento oficial / validacao por canal autenticado]. Apos confirmacao, sua solicitacao sera processada em ate [N] dias.

Qualquer duvida, nosso Encarregado de Dados (DPO) esta a disposicao pelo e-mail [dpo@empresa.com].

Atenciosamente,
[nome]
[cargo]
[empresa]
```

**Ressalvas:**
- Se o pedido envolver dados de crianca/adolescente, exigir validacao de responsavel legal
- Se o pedido foi feito via ANPD (requerimento de autoridade), ESCALAR (gatilho regulatorio)
- Se houver incidente de seguranca relacionado, ESCALAR (prazo 48h ANPD)

### Template 5: Pedido de informacao contratual

Quando: contraparte ou area interna pede copia, status, detalhes de contrato vigente.

**Coleta minima:**
- Quem solicita (interno, contraparte, terceiro)?
- Qual informacao especifica pedida?
- Tem legitimidade para acessar?
- Ha clausula de confidencialidade que limite o compartilhamento?

**Corpo da resposta:**

```
Assunto: Re: Solicitacao de Informacao — Contrato [identificador]

Prezado(a) [nome],

Em atencao a sua solicitacao referente ao Contrato de [tipo] celebrado em [data], informamos:

[ESCOLHER CONFORME O CASO:]

[Se atende — informacao compartilhavel]
- Numero/identificador do contrato: [XXX]
- Partes: [qualificacao resumida]
- Objeto: [resumo]
- Vigencia: [data inicial] a [data final / indeterminado]
- Situacao atual: [vigente / em renovacao / rescindido em DD/MM/AAAA]
- [Outras informacoes pedidas, conforme caso]

Copia integral do contrato segue em anexo [se aplicavel e autorizado].

[Se negativa — por confidencialidade]
Informamos que o contrato em referencia contem clausula de confidencialidade que veda o compartilhamento com terceiros sem autorizacao expressa da contraparte. Caso haja interesse legitimo, sugerimos formalizar solicitacao com justificativa, a qual sera submetida a avaliacao.

[Se negativa — por falta de legitimidade do solicitante]
Para que possamos atender sua solicitacao, solicitamos esclarecimentos quanto a (i) legitimidade do interesse no acesso a informacao, e (ii) finalidade do uso pretendido. Apos essa avaliacao, retornaremos com posicionamento.

Permanecemos a disposicao para esclarecimentos.

Atenciosamente,
[nome]
[cargo]
[empresa]
```

**Ressalvas:**
- Se o solicitante for advogado da contraparte, verificar procuracao — e considerar ESCALAR (possivel pre-litigio)
- Se for requisicao judicial ou administrativa, ESCALAR (gatilho regulatorio/litigio)
- Nunca enviar contrato com dados pessoais de terceiros sem validar LGPD

## Diretrizes transversais

### Linguagem formal
- Tratamento: "Prezado(a) [nome]", "Vossa Senhoria", "V.Sa."
- Fechamento: "Atenciosamente," ou "Cordialmente,"
- Evitar: "ok", "valeu", "abracos", abreviacoes informais, emojis
- Preferir: "em atencao a", "conforme", "tendo em vista", "nos termos de"
- Frases curtas e diretas — formalidade nao exige prolixidade

### Citacoes legais
- Citar apenas artigos reais e vigentes
- Na duvida, consultar `../references/legislacao-base.md`
- Artigos mais comuns:
  - Mora: CC art. 397
  - Clausula penal: CC art. 408-416
  - LGPD acesso/direitos: Lei 13.709/2018 arts. 17-22
  - LGPD prazo resposta: Lei 13.709/2018 art. 19
  - Confidencialidade: CC arts. 421-422 (boa-fe)

### Assunto do e-mail
Sempre sugerir linha de assunto clara:
- "Notificacao — [tema] — Contrato [ID]"
- "Re: [assunto original]"
- "Acordo de Confidencialidade — [projeto]"
- "Resposta — Solicitacao LGPD — [protocolo]"

### O que NUNCA colocar no template
- Confissao de culpa ou responsabilidade
- Reconhecimento de divida sem analise previa
- Promessa de indenizacao, desconto ou compensacao sem autorizacao
- Informacoes confidenciais nao solicitadas
- Dados pessoais de terceiros
- Valores, prazos ou clausulas extraidos de memoria — sempre verificar contrato

### Disclaimer obrigatorio
Toda saida da skill (tanto template como bloco de escalacao) deve terminar com:

```
---
⚠️ Este texto nao constitui parecer juridico. Revise com sua area juridica ou advogado antes de enviar, especialmente se houver valor financeiro relevante, terceiros nao identificados ou dual em relacao aos fatos.
```

Quando o caso for escalado, o disclaimer e mais firme:

```
---
⚠️ Esta analise nao constitui parecer juridico. O encaminhamento a advogado e obrigatorio dada a natureza do caso.
```

### Tom
- Firme e profissional — nao servil, nao defensivo
- Claro sobre o que a empresa vai fazer, o que espera, e em que prazo
- Sem ameacas veladas nem agressividade
- Deixar porta aberta para dialogo, salvo em caso de notificacao formal de descumprimento

## Verificacao antes de entregar

Checklist mental antes de apresentar a resposta ao usuario:
- [ ] Rastreei os 5 gatilhos de escalacao?
- [ ] Se ha gatilho, bloqueei o template e recomendei advogado?
- [ ] Se redigi template, identifiquei o tipo correto (1 a 5)?
- [ ] Coletei as informacoes minimas para personalizar o texto?
- [ ] Todos os artigos de lei citados sao reais e aplicaveis?
- [ ] Linguagem e formal em portugues brasileiro?
- [ ] Assunto do e-mail esta sugerido?
- [ ] Disclaimer obrigatorio esta ao final?
- [ ] Nao confessei culpa, nao reconheci divida, nao prometi nada sem autorizacao?

Se qualquer item falhar, corrigir antes de entregar.
