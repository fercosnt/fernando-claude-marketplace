# Playbook Contratual da Empresa

> Preencha este arquivo com as posicoes negociais da sua empresa.
> Adicione-o ao Project Knowledge do Claude para que o Coordenador Legal use suas regras em vez dos defaults de mercado.
> 
> **Como preencher:** Substitua os textos entre [colchetes] pelas posicoes da sua empresa. Apague os exemplos quando nao forem mais necessarios.

---

## Dados da Empresa

- **Razao Social:** [Nome da empresa]
- **CNPJ:** [00.000.000/0000-00]
- **Sede (foro padrao):** [Cidade/UF]
- **Responsavel por contratos:** [Nome e cargo]
- **Email juridico:** [juridico@empresa.com.br]

---

## Compras (materiais, equipamentos, insumos)

### Posicoes Padrao

| Clausula | Posicao da Empresa | Range Aceitavel | Escalar se |
|----------|-------------------|-----------------|------------|
| Prazo de pagamento | [30 dias apos entrega] | [28-45 dias] | [Acima de 60 dias] |
| Garantia do produto | [12 meses] | [6-24 meses] | [Sem garantia] |
| Multa por atraso na entrega | [0,5% ao dia, max 10%] | [0,3%-1% ao dia] | [Sem multa] |
| Inspecao/aceite | [10 dias uteis apos entrega] | [5-15 dias] | [Aceite automatico] |
| Frete | [CIF — por conta do fornecedor] | [CIF ou FOB conforme valor] | [Frete por conta do comprador acima de R$ X] |

> **Exemplo preenchido:**
> - Prazo de pagamento: 30 dias apos aceite da NF, com boleto bancario
> - Garantia: minimo 12 meses a partir da entrega; para equipamentos criticos, exigir 24 meses
> - Multa por atraso: 0,5% por dia de atraso, limitada a 10% do valor do pedido

---

## Servicos (prestacao de servicos, consultoria, manutencao)

### Posicoes Padrao

| Clausula | Posicao da Empresa | Range Aceitavel | Escalar se |
|----------|-------------------|-----------------|------------|
| SLA / nivel de servico | [Definir metricas] | [Conforme criticidade] | [Sem SLA definido] |
| Limitacao de responsabilidade | [12 meses de fees] | [6-18 meses] | [Cap menor que 6 meses ou ilimitado] |
| Propriedade intelectual | [Cessao total ao contratante] | [Cessao ou licenca exclusiva] | [Retencao pelo prestador] |
| Reajuste anual | [IPCA] | [IPCA ou IGPM] | [Reajuste livre ou acima de IPCA+2%] |
| Rescisao sem justa causa | [Aviso previo 30 dias] | [30-60 dias] | [Aviso maior que 90 dias ou irrescindivel] |
| Confidencialidade | [Clausula no contrato ou NDA separado] | [Qualquer formato] | [Sem clausula de confidencialidade] |

> **Exemplo preenchido:**
> - SLA: 99,5% uptime para servicos de TI; resposta em 4h para severidade alta
> - Limitacao: cap mutuo de 12 meses do valor anual do contrato
> - Reajuste: IPCA acumulado dos ultimos 12 meses, aplicado na data-base

---

## Locacao (imoveis, equipamentos, espacos)

### Posicoes Padrao

| Clausula | Posicao da Empresa | Range Aceitavel | Escalar se |
|----------|-------------------|-----------------|------------|
| Reajuste anual | [IGP-M] | [IGP-M ou IPCA] | [Indice diferente sem justificativa] |
| Garantia locaticia | [Seguro fianca] | [Seguro fianca ou caucao 3 meses] | [Fiador PF ou caucao acima de 6 meses] |
| Prazo minimo | [12 meses] | [12-36 meses] | [Acima de 60 meses sem clausula de saida] |
| Multa por rescisao antecipada | [Proporcional ao prazo restante] | [Proporcional] | [Multa fixa integral independente do prazo] |
| Responsabilidade por manutencao | [Ordinaria: locatario / Extraordinaria: locador] | [Padrao Lei 8.245] | [Toda manutencao por conta do locatario] |
| Benfeitorias | [Necessarias: reembolsaveis / Uteis: negociar / Voluptuarias: sem reembolso] | [Conforme CC] | [Renuncia total a indenizacao por benfeitorias] |

> **Exemplo preenchido:**
> - Reajuste: IGP-M acumulado; se negativo, manter valor sem reducao
> - Garantia: seguro fianca com cobertura de 30 meses
> - Prazo: 36 meses com clausula de saida apos 12 meses mediante aviso de 60 dias

---

## Engenharia (obras, reformas, construcao, empreitada)

### Posicoes Padrao

| Clausula | Posicao da Empresa | Range Aceitavel | Escalar se |
|----------|-------------------|-----------------|------------|
| Reajuste | [INCC] | [INCC ou CUB] | [Indice diferente sem justificativa] |
| Retencao tecnica | [5% sobre cada medicao] | [3%-10%] | [Sem retencao ou acima de 15%] |
| Garantia da obra | [5 anos] | [5 anos (CC art. 618)] | [Menos de 5 anos] |
| Seguro de obra | [Obrigatorio, all risks] | [All risks ou riscos nomeados] | [Sem seguro] |
| Cronograma fisico-financeiro | [Obrigatorio, vinculante] | [Obrigatorio] | [Sem cronograma ou indicativo] |
| Multa por atraso | [0,1% por dia, max 10%] | [0,05%-0,2% por dia] | [Sem multa por atraso em obra] |
| Subcontratacao | [Permitida com aprovacao previa] | [Com ou sem aprovacao] | [Livre sem notificacao] |

> **Exemplo preenchido:**
> - Retencao: 5% sobre cada medicao, liberada 30 dias apos aceite final
> - Cronograma: fisico-financeiro mensal, com tolerancia de 10% no prazo de cada etapa
> - Seguro: all risks no valor total da obra + RC para terceiros

---

## NDA / Acordo de Confidencialidade

### Posicoes Padrao

| Clausula | Posicao da Empresa | Range Aceitavel | Escalar se |
|----------|-------------------|-----------------|------------|
| Tipo | [Mutuo (bilateral)] | [Mutuo] | [Unilateral desfavoravel] |
| Prazo de vigencia | [3 anos apos termino da relacao] | [2-5 anos] | [Acima de 7 anos ou perpetuo] |
| Definicao de info confidencial | [Ampla, com lista exemplificativa] | [Clara e abrangente] | [Vaga ou excessivamente restritiva] |
| Carveouts (excecoes) | [Info publica, ordem judicial, desenvolvimento independente, posse anterior] | [Minimo 3 carveouts padrao] | [Sem carveouts] |
| Penalidade por violacao | [Perdas e danos apuraveis] | [Perdas e danos ou multa definida] | [Clausula penal desproporcional] |
| Devolucao/destruicao | [Obrigatoria ao termino, com certificado] | [Com prazo definido] | [Sem obrigacao de devolucao] |

> **Exemplo preenchido:**
> - Tipo: mutuo, ambas as partes com mesmas obrigacoes
> - Prazo: 3 anos apos o termino da relacao comercial
> - Carveouts: informacao publica, previamente em posse, desenvolvida independentemente, exigida por lei/ordem judicial

---

## Regras Gerais (aplicaveis a todos os tipos)

### LGPD / Dados Pessoais

| Item | Posicao da Empresa |
|------|-------------------|
| DPA obrigatorio? | [Sim, sempre que houver tratamento de dados pessoais] |
| Notificacao de incidente | [72 horas] |
| Subprocessadores | [Permitidos com aprovacao previa e mesmo nivel de protecao] |
| Transferencia internacional | [Apenas com clausulas padrao ou adequacao ANPD] |
| Retencao de dados | [Apenas durante vigencia + [X] meses para obrigacoes legais] |
| Direitos dos titulares | [Contratado deve cooperar no atendimento] |

### Clausula Penal / Multas

| Item | Posicao da Empresa |
|------|-------------------|
| Limite maximo | [Valor da obrigacao principal (CC art. 412)] |
| Multa por inadimplemento | [10% do valor do contrato] |
| Juros de mora | [1% ao mes] |
| Correcao monetaria | [IPCA ou IGP-M conforme tipo] |

### Foro e Resolucao de Disputas

| Item | Posicao da Empresa |
|------|-------------------|
| Foro | [Comarca de [cidade/UF]] |
| Arbitragem | [Apenas para contratos acima de R$ [valor]] |
| Mediacao previa | [Obrigatoria antes de litigio, prazo de [30] dias] |

### Rescisao

| Item | Posicao da Empresa |
|------|-------------------|
| Sem justa causa | [Aviso previo de [30] dias] |
| Com justa causa | [Notificacao + prazo de cura de [15] dias] |
| Efeitos da rescisao | [Pagamento proporcional ao executado + devolucao de materiais] |

---

## Limites de Alcada (quando escalar internamente)

| Valor do Contrato | Quem Aprova | Observacao |
|-------------------|-------------|------------|
| Ate R$ [50.000] | [Gerente de compras] | [Aprovacao direta] |
| R$ [50.001] a R$ [500.000] | [Diretor da area] | [Parecer juridico recomendado] |
| Acima de R$ [500.000] | [Diretoria + Juridico] | [Parecer juridico obrigatorio] |

---

## Notas e Observacoes da Empresa

> Use este espaco para adicionar regras especificas, fornecedores com tratamento diferenciado, ou instrucoes que nao se encaixam nas secoes acima.

[Suas notas aqui]

---

> **Como usar este playbook:** Salve este arquivo como `legal.local.md` e adicione ao Project Knowledge do seu projeto no Claude. O Coordenador Legal vai consultar automaticamente suas posicoes em vez de usar os defaults de mercado.
