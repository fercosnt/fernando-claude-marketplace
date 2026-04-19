# MEMO DE AVALIACAO DE RISCO JURIDICO

**Data**: 08/04/2026
**Elaborado por**: Claude (IA) — apoio a decisao
**Partes envolvidas**: Empresa contratante / Fornecedor de servicos de TI
**Tipo de contrato**: Prestacao de Servicos (TI)
**Valor estimado**: R$ 240.000,00/ano
**Referencia**: Renovacao de contrato de servicos de TI com alteracoes contratuais propostas pelo fornecedor

---

## 1. Descricao da Situacao

A empresa contratante esta em processo de renovacao de contrato de prestacao de servicos de TI com fornecedor atual. Nos ultimos 6 meses de vigencia do contrato, o fornecedor incorreu em 3 atrasos de entrega. O valor anual do contrato e de R$ 240.000,00. Na proposta de renovacao, o fornecedor solicita duas alteracoes substanciais: (i) inclusao de clausula de exclusividade sem prazo definido de vigencia; e (ii) remocao da clausula de SLA (Service Level Agreement) existente.

## 2. Background

O contrato em questao envolve servicos de TI, segmento no qual a dependencia operacional tende a ser elevada e a troca de fornecedor implica custos de transicao significativos (migracao de sistemas, curva de aprendizado, integracao de processos).

O historico de 3 atrasos em 6 meses indica um padrao recorrente de inadimplemento parcial, nao um incidente isolado. Esse historico e relevante porque demonstra tendencia de descumprimento de prazos pelo fornecedor.

Do ponto de vista juridico, as alteracoes propostas pelo fornecedor levantam questoes relevantes:

- **Exclusividade sem prazo**: No direito brasileiro, clausulas de exclusividade sem prazo determinado sao consideradas abusivas em contratos empresariais. O Codigo Civil (art. 473, paragrafo unico) estabelece que contratos por prazo indeterminado podem ser denunciados a qualquer tempo, mas a exclusividade sem prazo cria amarracao desproporcional. Adicionalmente, o CADE pode considerar clausulas de exclusividade sem prazo como pratica anticoncorrencial (Lei 12.529/2011).

- **Remocao de SLA**: A clausula de SLA e o principal instrumento de controle de qualidade e desempenho em contratos de TI. Sua remocao elimina metricas objetivas para aferir cumprimento contratual, dificulta a caracterizacao de inadimplemento (art. 475, CC/2002), e remove a base para aplicacao de penalidades ou rescisao motivada.

## 3. Avaliacao de Risco (Severidade x Probabilidade)

### Severidade: 4 — Alto

**Justificativa**: A combinacao das duas alteracoes propostas pelo fornecedor cria um cenario de exposicao significativa:

1. **Impacto financeiro**: A exclusividade sem prazo impede a contratacao de alternativas, gerando dependencia total de um fornecedor com historico de atrasos. Em cenario de inadimplemento grave, a empresa ficaria refem do fornecedor sem possibilidade de contratar substituto. O impacto financeiro potencial ultrapassa 15% do valor contratual, considerando custos de interrupcao operacional, eventuais custos de litigio para rescindir contrato com clausula de exclusividade, e perdas decorrentes de atrasos sem SLA para embasar penalidades.

2. **Impacto operacional**: Sem SLA, nao ha parametros objetivos para exigir nivel de servico. Interrupcoes ou degradacao de servico nao terao metrica contratual para responsabilizacao. Isso pode gerar interrupcao significativa de operacoes de TI.

3. **Impacto juridico**: A rescisao de contrato com clausula de exclusividade sem prazo pode gerar litigio. A ausencia de SLA dificulta a producao de prova de inadimplemento em eventual disputa judicial.

### Probabilidade: 4 — Provavel

**Justificativa**: Multiplos fatores convergem para uma probabilidade elevada de materializacao do risco:

1. **Historico concreto**: 3 atrasos em 6 meses constituem padrao, nao incidente isolado. A frequencia (um atraso a cada 2 meses em media) indica problema estrutural do fornecedor.

2. **Tendencia desfavoravel**: O fornecedor, ao inves de propor melhorias para os atrasos, busca remover justamente os mecanismos de controle (SLA) e criar amarracao contratual (exclusividade). Isso sugere que o fornecedor antecipa futuros descumprimentos e esta se protegendo preventivamente.

3. **Fatores de risco ativos**: A propria proposta de renovacao ja contem elementos que amplificam o risco. Se aceitas, as condicoes criam um cenario onde o risco de prejuizo e quase inevitavel.

### Score Final

| Severidade | Probabilidade | Score | Classificacao |
|------------|---------------|-------|---------------|
| 4 | 4 | 16 | RED |

**Matriz visual**:
```
              SEVERIDADE →
           1    2    3    4    5
P  1  |  1  |  2  |  3  |  4  |  5  |
R  2  |  2  |  4  |  6  |  8  | 10  |
O  3  |  3  |  6  |  9  | 12  | 15  |
B  4  |  4  |  8  | 12  |[16] | 20  |
.  5  |  5  | 10  | 15  | 20  | 25  |
```

## 4. Fatores Contribuintes

### Fatores que aumentam o risco
- **Historico de inadimplemento reiterado**: 3 atrasos em 6 meses demonstram padrao sistematico, nao falha pontual
- **Exclusividade sem prazo**: Cria lock-in contratual desproporcional, eliminando poder de barganha da contratante e potencialmente configurando clausula abusiva
- **Remocao de SLA**: Elimina o unico instrumento objetivo de controle de qualidade e base para penalidades contratuais
- **Assimetria na proposta**: O fornecedor busca mais protecao (exclusividade) e menos responsabilidade (sem SLA) simultaneamente, indicando postura negocial desequilibrada
- **Dependencia operacional de TI**: Servicos de TI tipicamente geram alta dependencia, tornando a troca de fornecedor custosa e demorada

### Fatores que diminuem o risco
- **Contrato ainda nao renovado**: A empresa esta em fase de negociacao e pode rejeitar as alteracoes propostas ou negociar termos intermediarios
- **Valor relativamente contido**: R$ 240.000/ano, embora significativo, nao representa exposicao catastrofica para a maioria das empresas de medio porte
- **Existencia de contrato anterior com SLA**: O fato de haver SLA no contrato vigente indica que a empresa ja possui parametros definidos que podem ser mantidos ou aprimorados

## 5. Plano de Mitigacao

| # | Acao | Responsavel sugerido | Prazo | Prioridade |
|---|------|---------------------|-------|------------|
| 1 | Rejeitar a remocao da clausula de SLA. Manter os niveis de servico existentes e, se possivel, incluir penalidades progressivas por atraso (multa diaria ou por ocorrencia) | Gestor de contratos / Juridico | Imediato — antes da assinatura | Alta |
| 2 | Rejeitar a clausula de exclusividade sem prazo. Se a exclusividade for estrategicamente necessaria, limitar a 12 meses com revisao periodica e clausula de saida por descumprimento | Gestor de contratos / Juridico | Imediato — antes da assinatura | Alta |
| 3 | Incluir clausula de rescisao motivada vinculada ao descumprimento de SLA, com prazo de cura (ex: 15 dias para corrigir) e direito de rescisao sem onus apos reincidencia | Juridico | Antes da assinatura | Alta |
| 4 | Documentar formalmente os 3 atrasos ocorridos nos ultimos 6 meses (datas, impactos, comunicacoes) para criar historico probatorio | Gestor de TI | 7 dias | Media |
| 5 | Realizar pesquisa de mercado com ao menos 2 fornecedores alternativos para ter opcao de troca caso a negociacao nao evolua satisfatoriamente | Compras / TI | 15 dias | Media |
| 6 | Incluir clausula de benchmark periodico (a cada 12 meses) permitindo comparacao de precos e qualidade com mercado, com direito de renegociacao | Juridico / Compras | Antes da assinatura | Media |
| 7 | Definir prazo maximo de contrato de 12 a 24 meses com renovacao condicionada a avaliacao de desempenho | Gestor de contratos | Antes da assinatura | Alta |

## 6. Monitoramento

| Indicador | Frequencia | Gatilho de alerta |
|-----------|-----------|-------------------|
| Cumprimento de prazos de entrega (SLA) | Mensal | Qualquer atraso superior a 5 dias uteis ou 2+ atrasos no trimestre |
| Qualidade das entregas (bugs criticos, retrabalho) | Mensal | Taxa de retrabalho acima de 15% das entregas |
| Andamento da negociacao contratual | Semanal (ate assinatura) | Fornecedor insistir na remocao de SLA ou exclusividade sem prazo |
| Disponibilidade de fornecedores alternativos | Trimestral | Reducao de opcoes no mercado ou aumento significativo de custos |
| Nivel de dependencia operacional do fornecedor | Semestral | Aumento de sistemas ou processos criticos sob gestao do fornecedor |

## 7. Proximos Passos

- [ ] Comunicar formalmente ao fornecedor a rejeicao da remocao de SLA e da exclusividade sem prazo definido
- [ ] Solicitar ao juridico revisao da minuta de renovacao com inclusao de clausulas protetivas (penalidades progressivas, rescisao motivada, prazo de cura)
- [ ] Documentar os 3 atrasos dos ultimos 6 meses com evidencias (e-mails, tickets, relatorios)
- [ ] Iniciar cotacao com pelo menos 2 fornecedores alternativos de servicos de TI
- [ ] Definir internamente o prazo-limite para conclusao da negociacao antes de considerar troca de fornecedor

---

**AVISO**: Esta avaliacao de risco e um instrumento de apoio a decisao e NAO constitui parecer juridico. Foi gerada por inteligencia artificial com base nas informacoes fornecidas. Para decisoes juridicas vinculantes, consulte um advogado habilitado pela OAB.
