# Cowork Project — instrucoes para projetos do Claude Cowork

Alvo agentico. O Cowork planeja, quebra em subtarefas, roda codigo, mexe em arquivos reais nas suas pastas e produz entregaveis (xlsx, pptx, docs). A instrucao **nao governa como ele fala — governa o trabalho que ele faz**.

A orientacao do proprio produto: *"Tell Claude what you need, not how."* Instrucao de Cowork descreve **resultado, definicao de pronto, onde salvar, formato e fronteira de permissao**. Se voce escrever tom de resposta aqui, ganhou um projeto que conversa bem e nao entrega.

## 1. As tres camadas

O Cowork empilha instrucoes. Escrever na camada errada e o erro mais comum.

| Camada | Assunto | Onde fica | Cuidado |
|---|---|---|---|
| **Global instructions** | **Voce.** Papel, siglas que usa, formato/tom preferido | Settings > Cowork > Global instructions | Carrega em **toda** sessao, inclusive tarefas agendadas. Mantenha enxuto — cada regra e contexto permanente |
| **Project instructions** | **O trabalho.** Proposito, workflow, definicao de pronto, permissao | Dentro do projeto | E aqui que mora quase tudo |
| **Folder instructions** | **Aquela pasta.** Convencao de nome, o que nao tocar | Ao selecionar a pasta | O **proprio Claude pode reescreve-las durante a sessao** — nao ponha ali nada que voce precise que fique |

Alem das tres, a **Description do projeto** nao e decorativa: o **Dispatch le a Description** pra escolher em qual projeto rodar uma tarefa. Description generica = tarefa caindo no projeto errado.

## 2. Mecanica

| Item | Fato |
|---|---|
| Onde roda | VM Linux isolada; monta **so as pastas autorizadas** |
| Arquivos | Le arquivos individuais ate **50 MB** |
| Persistencia | Memory store proprio por projeto, entre sessoes |
| Skills/plugins | Vem do **Customize** (sincroniza com a conta claude.ai). **Nao le `~/.claude`** do Claude Code |
| Connectors | Permissao em **Manual** (pergunta sempre), **Auto** (autonomo com checagem), **Skip** (sem aprovacao) |
| Compartilhamento | **Nenhum.** Projeto Cowork vive so na maquina, nao sincroniza |
| Arquivar | Apaga metadados (nome, instructions, links, memory); **nao apaga os arquivos em disco** |

O item de compartilhamento e o que mais morde time: nao existe "projeto do time" no Cowork. Cada pessoa monta o dela. Por isso a instrucao precisa de um arquivo-fonte versionado (ver `pacote.md`).

## 3. Estrutura recomendada

Seis blocos. Os quatro do meio sao obrigatorios em qualquer projeto que produz arquivo.

1. **Cabecalho** — dono, data de revisao, proposito.
2. **Entregavel** — o que sai daqui, em que formato.
3. **Definicao de pronto** — como voce sabe que a tarefa acabou. Sem isso ele para cedo ou tarde demais.
4. **Onde salvar** — pasta, convencao de nome, o que sobrescrever e o que versionar.
5. **Fronteira** — o que nunca fazer sem perguntar.
6. **Workflow** — a ordem dos passos, quando houver ordem que importa.

## 4. Template comentado

```
Dono: [nome] · Revisar em: [data]
Para que serve: [uma frase — vira a Description tambem]

ENTREGAVEL
[O que este projeto produz.] Formato: [xlsx/pptx/md/...].

PRONTO QUANDO
- [Condicao verificavel 1]
- [Condicao verificavel 2]
- [O que voce confere antes de me entregar]

ONDE SALVA
- [caminho da pasta]/[convencao de nome]
- Nunca sobrescreva [o que]. Versione como [padrao].

FRONTEIRA
- Pergunte antes de: [apagar / enviar / publicar / gastar / alterar fonte].
- Se [condicao de duvida], pare e me mostre o plano antes de executar.

WORKFLOW
1. [Passo]
2. [Passo]
3. [Passo de verificacao antes de entregar]
```

## 5. Exemplo — projeto operacional

Fechamento mensal de relatorio de marketing.

```
Dono: Fernando · Revisar em: 2027-02-01
Para que serve: fechar o relatorio mensal de midia paga por cliente.

ENTREGAVEL
Um .xlsx por cliente, com as formulas vivas (nao valores colados), mais um
resumo de 1 pagina em .md ao lado.

PRONTO QUANDO
- Toda metrica do mes fechado esta preenchida, sem celula vazia sem nota
- Os totais batem com a fonte; divergencia acima de 2% vira nota no resumo
- O resumo aponta as 3 maiores variacoes contra o mes anterior, com hipotese
- Voce releu o arquivo aberto antes de dizer que acabou

ONDE SALVA
- relatorios/[cliente]/[AAAA-MM]/ — um diretorio por mes
- Nunca sobrescreva mes ja fechado. Mes refeito vira [AAAA-MM]-v2

FRONTEIRA
- Pergunte antes de: enviar qualquer coisa pro cliente, apagar arquivo,
  alterar planilha fora de relatorios/.
- Se a fonte devolver periodo vazio, pare e me avise. Nao estime, nao
  preencha com zero.

WORKFLOW
1. Puxe os dados do periodo por cliente
2. Monte o xlsx a partir do modelo em modelos/relatorio-base.xlsx
3. Confira os totais contra a fonte
4. Escreva o resumo
5. Me liste o que ficou faltando, se ficou
```

O que faz esse exemplo funcionar: **toda linha de "PRONTO QUANDO" e verificavel**, e a fronteira nomeia acoes irreversiveis especificas em vez de dizer "tenha cuidado".

## 6. Global instructions — exemplo

Curto de proposito. E sobre voce, nao sobre trabalho.

```
Sou o Fernando — marketing e operacao de clinica odontologica e de
equipamento medico.
Siglas que uso: BS = Beauty Smile. TCO = custo total 5 anos.
Responda em portugues do Brasil. Direto, sem preambulo, sem elogio ao
meu pedido.
Quando terminar uma tarefa, diga o que ficou faltando antes de dizer o
que deu certo.
```

Se voce se pegar escrevendo sobre um projeto especifico aqui, mova pro projeto.

## 7. Erros especificos de Cowork

| Erro | Sintoma | Correcao |
|---|---|---|
| Instrucao conversacional | Ele explica o que faria em vez de fazer | Troque tom por entregavel + definicao de pronto |
| Sem definicao de pronto | Entrega pela metade, ou nunca para | Escreva condicoes verificaveis |
| Sem "onde salva" | Arquivo aparece em lugar aleatorio | Caminho + convencao de nome |
| Fronteira vaga | Ele faz algo irreversivel, ou pede permissao pra tudo | Nomeie as acoes; irreversivel em Manual |
| Description generica | Dispatch manda tarefa pro projeto errado | Description = o que produz, pra quem |
| Regra critica em folder instructions | Some sozinha | Mova pro projeto — o Claude reescreve as de pasta |
| Espera skill do `~/.claude` | "Nao conheco essa skill" | Adicione em Customize; Cowork nao le o diretorio do Claude Code |
| Instrucao so na maquina de um | Time diverge em semanas | Arquivo-fonte versionado (ver `pacote.md`) |

## 8. Orcamento

Nao ha limite publicado, mas global instructions carregam em toda sessao — trate como orcamento apertado (**mire 400–800 caracteres**). Project instructions podem ser maiores que as de Chat Project, porque carregam workflow e definicao de pronto; ainda assim, **fato e arquivo, nao instrucao**: o que e material de consulta vai pra pasta ou pra Links.
