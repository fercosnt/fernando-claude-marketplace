# LGPD em Contratos — 7 Clausulas Obrigatorias

> Referencia para analise de conformidade LGPD em contratos empresariais.
> Base: Lei 13.709/2018, orientacoes ANPD, doutrina majoritaria.

---

## Quando a LGPD Incide

A LGPD incide sobre **todo contrato** em que haja tratamento de dados pessoais — independente do tipo (compras, servicos, locacao, engenharia, emprego). Se o contrato envolve coleta, armazenamento, compartilhamento ou processamento de dados de pessoas fisicas, as 7 clausulas abaixo sao obrigatorias.

---

## As 7 Clausulas Obrigatorias

### 1. Identificacao dos Agentes de Tratamento

| Item | Detalhe |
|------|---------|
| **O que** | Definir quem e Controlador e quem e Operador (LGPD art. 5, VI-VII) |
| **Por que** | Determina responsabilidades, obrigacoes de registro e regime de responsabilizacao (arts. 37-45) |
| **Red flag** | Contrato que trata dados pessoais sem identificar papeis → RED |
| **Texto-modelo** | "A CONTRATANTE atua como Controladora dos dados pessoais tratados no escopo deste contrato. A CONTRATADA atua como Operadora, tratando dados pessoais exclusivamente conforme instrucoes da Controladora." |

### 2. Finalidade e Base Legal

| Item | Detalhe |
|------|---------|
| **O que** | Especificar quais dados sao tratados, para qual finalidade, e com qual base legal (LGPD art. 7) |
| **Por que** | Principio da finalidade (art. 6, I) e adequacao (art. 6, II) — tratamento sem base legal e ilicito |
| **Red flag** | Base legal ausente ou inadequada ao contexto → RED |
| **As 10 bases legais (art. 7)** | I-Consentimento, II-Obrigacao legal, III-Administracao publica, IV-Pesquisa, V-Execucao de contrato, VI-Exercicio regular de direitos, VII-Protecao da vida, VIII-Tutela da saude, IX-Interesse legitimo, X-Protecao de credito |

#### Ponto Critico: Base Legal por Contexto

| Contexto | Base Legal Correta | Base Incorreta | Por que |
|----------|-------------------|----------------|---------|
| Relacao de emprego | Execucao de contrato (art. 7, V) ou Obrigacao legal (art. 7, II) | Consentimento (art. 7, I) | Desequilibrio de poder — empregado nao tem liberdade real para recusar (posicao ANPD) |
| Dados exigidos por lei (eSocial, RAIS, CAGED) | Obrigacao legal (art. 7, II) | Consentimento | Lei ja obriga o tratamento |
| Relacao comercial paritaria | Consentimento (art. 7, I) ou Execucao de contrato (art. 7, V) | — | Partes em equilibrio |
| Marketing direto | Consentimento (art. 7, I) ou Interesse legitimo (art. 7, IX) | Execucao de contrato | Nao e necessario para executar o contrato |

### 3. Seguranca e Sigilo

| Item | Detalhe |
|------|---------|
| **O que** | Medidas tecnicas e administrativas de seguranca (LGPD art. 46) |
| **Por que** | Obrigacao legal do agente de tratamento; ausencia gera responsabilidade objetiva |
| **Red flag** | Contrato sem mencao a seguranca de dados → YELLOW (se poucos dados) ou RED (dados sensiveis) |
| **Texto-modelo** | "A OPERADORA adotara medidas tecnicas e administrativas aptas a proteger os dados pessoais de acessos nao autorizados e de situacoes acidentais ou ilicitas de destruicao, perda, alteracao, comunicacao ou difusao." |
| **Exemplos de medidas** | Criptografia, controle de acesso, logs de auditoria, treinamento de pessoal, politica de seguranca da informacao |

### 4. Notificacao de Incidentes

| Item | Detalhe |
|------|---------|
| **O que** | Prazo e procedimento para comunicacao de incidentes de seguranca (LGPD art. 48) |
| **Por que** | Controlador deve comunicar ANPD e titulares em prazo razoavel — ANPD recomenda 72 horas |
| **Red flag** | Ausencia de clausula de incidentes → RED; prazo > 72h → YELLOW |
| **Texto-modelo** | "A OPERADORA devera comunicar a CONTROLADORA qualquer incidente de seguranca que envolva dados pessoais no prazo maximo de 72 (setenta e duas) horas apos tomar conhecimento, informando: natureza dos dados, titulares afetados, medidas adotadas e medidas para reverter ou mitigar os efeitos." |

### 5. Suboperadores

| Item | Detalhe |
|------|---------|
| **O que** | Regras para subcontratacao de terceiros que tratem dados pessoais |
| **Por que** | Operador nao pode subcontratar sem anuencia do Controlador — responsabilidade solidaria |
| **Red flag** | Permissao irrestrita de subcontratacao → RED; silencio sobre suboperadores → YELLOW |
| **Texto-modelo** | "A OPERADORA nao podera subcontratar terceiros para tratamento de dados pessoais sem previa e expressa autorizacao por escrito da CONTROLADORA. O suboperador estara sujeito as mesmas obrigacoes deste contrato." |

### 6. Direitos dos Titulares

| Item | Detalhe |
|------|---------|
| **O que** | Procedimento para atendimento dos direitos dos titulares (LGPD arts. 17-22) |
| **Por que** | Titulares podem exercer direitos a qualquer momento: acesso, correcao, eliminacao, portabilidade, informacao sobre compartilhamento |
| **Red flag** | Ausencia de procedimento → YELLOW; negacao de direitos → RED |
| **Texto-modelo** | "A OPERADORA cooperara com a CONTROLADORA para atendimento de requisicoes de titulares no prazo de 15 (quinze) dias uteis, conforme arts. 17-22 da LGPD." |

### 7. Destinacao ao Termino

| Item | Detalhe |
|------|---------|
| **O que** | O que acontece com os dados ao fim do contrato (LGPD art. 16) |
| **Por que** | Dados devem ser eliminados apos o termino do tratamento, salvo obrigacao legal de retencao |
| **Red flag** | Silencio sobre destino dos dados → YELLOW; retencao sem justificativa legal → RED |
| **Texto-modelo** | "Ao termino deste contrato, a OPERADORA devera, a criterio da CONTROLADORA: (a) devolver todos os dados pessoais em formato estruturado; ou (b) eliminar de forma segura e irrecuperavel todos os dados pessoais, emitindo declaracao de eliminacao no prazo de 30 (trinta) dias." |

---

## Sancoes por Descumprimento (arts. 52-54)

| Sancao | Gravidade |
|--------|-----------|
| Advertencia | Leve |
| Multa simples: ate 2% do faturamento, max R$ 50 milhoes por infracao | Grave |
| Multa diaria | Grave |
| Publicizacao da infracao | Grave (dano reputacional) |
| Bloqueio/eliminacao dos dados | Critica (paralisa operacao) |
| Suspensao parcial do banco de dados por 6 meses | Critica |
| Suspensao da atividade de tratamento por 6 meses | Critica |
| Proibicao parcial ou total da atividade de tratamento | Maxima |

---

## Controversia: Responsabilidade Solidaria vs. Subsidiaria

Arts. 42-45 criam regime de responsabilidade entre controlador e operador. Posicoes:
- **ANPD:** defende responsabilidade solidaria
- **Operadores:** argumentam subsidiaria
- **STJ:** ainda sem pacificacao (2026)

**Recomendacao:** incluir clausula de indenizacao cruzada e limitacao de responsabilidade entre as partes, independente da posicao adotada.
