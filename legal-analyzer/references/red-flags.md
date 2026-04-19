# Red Flags — Clausulas Abusivas, Nulas e Riscos Criticos

> Catalogo de clausulas problematicas que devem ser flagadas como RED na analise de contratos.
> Jurisdicao: Brasil | Base legal: CC/2002, LGPD, Lei 8.245/1991, CDC, CLT, Lei 12.529/2011

---

## Erros Transversais (Todos os Tipos de Contrato)

| Red Flag | Consequencia | Artigo de Lei | Severidade |
|----------|-------------|---------------|------------|
| Clausula penal superior ao valor da obrigacao principal | Nula — juiz reduz equitativamente | CC arts. 412-413 | RED |
| Exclusao de responsabilidade por dolo ou culpa grave | Nula de pleno direito | CC + jurisprudencia STJ | RED |
| Multa cumulada com perdas e danos sem previsao expressa | Vedada como regra — so com clausula expressa | CC art. 416, par. unico | RED |
| Ausencia de clausula LGPD quando ha dados pessoais | Sancao ANPD ate 2% do faturamento (max R$ 50M); nulidade parcial | LGPD arts. 46-54 | RED |
| Qualificacao incompleta das partes (sem CNPJ/CPF, sem representante) | Invalidade do contrato | CC art. 104 | RED |
| Linguagem vaga no objeto ("prazo razoavel", "melhor esforco", "se possivel") | Litigio sobre interpretacao; impossibilidade de constituir mora | CC arts. 112-113 | YELLOW/RED |
| Exclusividade sem prazo definido | Risco anticoncorrencial; CADE pode impugnar | Lei 12.529/2011, art. 36 | RED |
| Renovacao automatica sem mecanismo de notificacao para nao renovar | Vinculacao involuntaria; dificuldade de sair do contrato | CC art. 473 | YELLOW |
| Objeto ilicito, impossivel ou indeterminavel | Nulidade absoluta | CC art. 166, II | RED |
| Contrato celebrado por agente absolutamente incapaz | Nulidade absoluta | CC art. 166, I | RED |
| Simulacao (aparencia de contrato diferente do real) | Nulidade do simulado | CC art. 167 | RED |
| Abuso de direito (exercicio que excede limites da boa-fe) | Ato ilicito | CC art. 187 | RED |
| Clausula que viola funcao social do contrato | Nula | CC art. 421 | RED |

---

## Red Flags por Tipo de Contrato

### Compras e Fornecimento

| Red Flag | Consequencia | Artigo |
|----------|-------------|--------|
| SLA sem metricas mensuraveis | Litigio sobre descumprimento | CC arts. 112-113 |
| Preco sem indice de reajuste em contrato > 12 meses | Desequilibrio economico previsivel | CC art. 317 |
| Transferencia de risco antes da entrega efetiva | Comprador assume risco sem posse | CC arts. 492-494 |
| Forca maior sem lista exemplificativa | Disputa sobre o que constitui forca maior | CC art. 393 |
| Renovacao automatica sem aviso previo proporcional a investimentos | Resilicao pode gerar dever de indenizar | CC art. 473, par. unico |

### Prestacao de Servicos

| Red Flag | Consequencia | Artigo |
|----------|-------------|--------|
| Prazo superior a 4 anos | Nulo — converte-se em 4 anos | CC art. 594 |
| Exclusividade + subordinacao + horario fixo + pessoalidade | Pejotizacao → vinculo empregaticio | CLT arts. 2-3 |
| Prestador sem habilitacao profissional exigida por lei | Contratante pode recusar pagamento | CC art. 606 |
| PI sem definicao de titularidade | Direitos ficam com o autor (prestador) | Lei 9.610/1998, art. 11 |
| Rescisao imediata sem aviso previo | Indenizacao devida ao prestador (vencido + metade do restante) | CC art. 602 |
| Pagamento antecipado integral sem garantia | Risco financeiro total | CC art. 476 |

### Locacao

| Red Flag | Consequencia | Artigo |
|----------|-------------|--------|
| Exigencia de duas garantias simultaneas | Contravencao penal (pena de prisao simples 5 dias a 6 meses) | Lei 8.245/1991, art. 43, II |
| Caucao superior a 3 alugueis | Excesso nulo | Lei 8.245/1991, art. 38, §2o |
| Multa por rescisao sem reducao proporcional ao tempo cumprido | Ilegal — juiz reduz proporcionalmente | Lei 8.245/1991, art. 4o, par. unico |
| Despesas extraordinarias de condominio atribuidas ao locatario | Nula | Lei 8.245/1991, art. 22, par. unico |
| Reajuste semestral (periodicidade < 12 meses) | Vedado | Lei 10.192/2001, art. 2o |
| Locacao comercial sem prazo determinado | Perde direito a acao renovatoria | Lei 8.245/1991, art. 51 |
| Clausula de renuncia a benfeitorias necessarias em locacao residencial | Abusiva | Lei 8.245/1991, art. 35 + CDC art. 51, I |
| Pagamento antecipado com garantia | Vedado exigir ambos | Lei 8.245/1991, art. 20 c/c art. 42 |

### Engenharia e Empreitada

| Red Flag | Consequencia | Artigo |
|----------|-------------|--------|
| Obra sem ART/RRT registrada | Exercicio ilegal da profissao; interdicao; multa | Lei 5.194/1966, art. 14 |
| Empreitada global sem clausula de imprevistos | Empreiteiro absorve todos os aumentos — risco de abandono | CC art. 619 |
| Garantia de solidez e seguranca inferior a 5 anos | Clausula nula — prazo legal irrenunciavel | CC art. 618 |
| Aceitacao tacita (uso da obra sem ressalva formal) | Extingue reclamacao por vicios aparentes | CC art. 615 |
| Subcontratacao em empreitada de lavor sem anuencia | Vedada por lei | CC art. 626 |
| Cronograma fisico nao soma 100% | Inconsistencia numerica → dados nao confiaveis | — |
| Medicoes parciais nao somam total global | Inconsistencia numerica | — |
| Ausencia de retencao de pagamento | Sem garantia financeira de conclusao | — |
| Responsabilidade trabalhista nao endereçada | Contratante pode responder subsidiariamente | TST Sumula 331 |

### Contratos de Trabalho (CLT)

| Red Flag | Consequencia | Artigo |
|----------|-------------|--------|
| Experiencia prorrogada mais de uma vez | Converte-se em prazo indeterminado | CLT art. 451 |
| Experiencia superior a 90 dias | Excesso nulo | CLT art. 445, par. unico |
| Remuneracao variavel mal definida | Pode ser incorporada como fixa | CLT + TST |
| Non-compete sem compensacao financeira | Nula — priva subsistencia | CF art. 6o; TST |
| Non-compete sem limitacao temporal (> 2 anos) | Nula ou reduzivel judicialmente | TST |
| Non-compete sem limitacao territorial/material | Nula por generalidade | TST |
| Consentimento como base LGPD em relacao de emprego | Base inadequada — usar execucao de contrato ou obrigacao legal | LGPD art. 7; posicao ANPD |
| Alteracao contratual unilateral prejudicial | Nula | CLT art. 468 |

### NDA / Confidencialidade

| Red Flag | Consequencia | Artigo |
|----------|-------------|--------|
| Definicao de "informacao confidencial" = "toda informacao da empresa" | Vagueza excessiva — pode ser anulada | CC arts. 112-113 |
| NDA sem prazo pos-contratual definido | Risco de arguicao de perpetuidade abusiva | CC art. 421 |
| Ausencia de carveouts padrao (dominio publico, posse previa) | Escopo excessivo; impraticavel | — |
| Non-compete embutido em NDA sem requisitos de validade | Nulo se sem compensacao, limite temporal e territorial | TST |
| Penalidade desproporcional por violacao | Nula na parte excessiva | CC arts. 412-413 |
| Obrigacao unilateral (so receptor obrigado, sem reciprocidade) | Pode ser questionada se desequilibrada | CC art. 422 |

---

## Verificacao Numerica — Red Flags

| Verificacao | Red Flag | Tolerancia |
|-------------|----------|------------|
| Soma de itens ≠ total declarado | Inconsistencia matematica | Zero |
| Base × percentual/100 ≠ valor calculado | Percentual incorreto | Zero |
| Cronograma fisico (%) nao soma 100% | Cronograma inconsistente | Zero |
| Parcelas × valor ≠ total | Pagamento inconsistente | Zero |
| Indice de reajuste inadequado ao tipo (ex: IGP-M em obra, deveria ser INCC) | Reajuste potencialmente prejudicial | YELLOW |
| Clausula penal > valor da obrigacao | Nula | CC art. 412 |
| Retencao sobre base incorreta | Valor retido maior ou menor que devido | Zero |

---

## Relacao de Consumo (CDC) — Red Flags Adicionais

Quando uma das partes e consumidora (pessoa fisica ou juridica destinataria final):

| Red Flag | Consequencia | Artigo |
|----------|-------------|--------|
| Renuncia a direitos do consumidor | Nula de pleno direito | CDC art. 51, I |
| Transferencia de responsabilidade a terceiros | Nula | CDC art. 51, III |
| Obrigacao considerada iniqua ou que coloque consumidor em desvantagem exagerada | Nula | CDC art. 51, IV |
| Venda casada (condicionar fornecimento a outro produto/servico) | Pratica abusiva | CDC art. 39, I |
| Limite quantitativo de produto sem justa causa | Pratica abusiva | CDC art. 39, I |
| Vantagem manifestamente excessiva | Pratica abusiva | CDC art. 39, V |
| Contrato nao dado a conhecer previamente ao consumidor | Nao obriga o consumidor | CDC art. 46 |

---

## Como Usar Este Catalogo

1. **Na analise**: comparar cada clausula do contrato contra os red flags do tipo correspondente
2. **Classificacao**: RED flags sao bloqueadores — requerem correcao antes de assinatura
3. **Redline**: para cada RED, sugerir redacao alternativa conforme legislacao
4. **Escalacao**: RED flags com consequencia "nula" ou "contravencao" → levar ao juridico obrigatoriamente
