# Clausulas para Contratos de Compras, Fornecimento e SLA

> Checklist de clausulas para analise de contratos de compra de materiais, fornecimento continuado, SLA e distribuicao.
> Jurisdicao: Brasil | Base legal: CC/2002, CDC, LGPD

---

## Clausulas Essenciais

| Clausula | Status | Artigo de Lei | Consequencia se Ausente |
|----------|--------|---------------|------------------------|
| Qualificacao completa das partes (CNPJ, representante legal, poderes) | Obrigatoria | CC art. 104 | Invalidade do contrato |
| Objeto: especificacao tecnica detalhada do produto/servico | Obrigatoria | CC art. 104 | Litigio sobre escopo; interpretacao contra quem redigiu |
| Padrao de qualidade e normas tecnicas aplicaveis | Obrigatoria | CC arts. 441-443 | Dificuldade de recusar produto fora de especificacao |
| Preco unitario, total e forma de calculo | Obrigatoria | CC art. 104 | Contrato sem preco = nulo ou sujeito a arbitramento |
| Condicoes de pagamento (prazo, forma, conta bancaria) | Obrigatoria | CC art. 104 | Mora do credor por nao indicar forma de pagamento |
| Indice de reajuste (IPCA ou IGP-M) e periodicidade | Recomendada | CC art. 317 | Desequilibrio economico; reajuste por arbitramento judicial |
| Prazo de entrega e cronograma | Obrigatoria | CC art. 389 | Impossibilidade de constituir mora; sem base para multa |
| Penalidades por atraso na entrega | Recomendada | CC arts. 408-412 | Necessidade de comprovar dano para cobrar indenizacao |
| Local de entrega e transferencia de risco | Recomendada | CC art. 492-494 | Risco permanece com vendedor ate entrega; litigio sobre transporte |
| Foro e lei aplicavel | Recomendada | CPC art. 63 | Foro do domicilio do reu (pode ser inconveniente) |

---

## Garantias e Vicios

| Clausula | Status | Artigo de Lei | Consequencia se Ausente |
|----------|--------|---------------|------------------------|
| Garantia contratual (prazo e abrangencia) | Recomendada | CC arts. 441-443 | Aplica-se apenas prazo legal: 30 dias (movel), 1 ano (imovel) |
| Procedimento de reclamacao por vicios (prazo, forma) | Recomendada | CC art. 445 | Prazo decadencial de 30 dias da entrega (bens moveis) |
| Substituicao ou abatimento por defeito | Recomendada | CC art. 442 | Comprador pode rejeitar OU pedir abatimento — sem controle do vendedor |
| Excecao de contrato nao cumprido | Obrigatoria (implicita) | CC art. 476 | Ja prevista em lei; clausula explicita da clareza ao procedimento |

---

## SLA (Service Level Agreement)

| Clausula | Status | Artigo de Lei | Consequencia se Ausente |
|----------|--------|---------------|------------------------|
| Metricas mensuraveis (uptime %, tempo de resposta, tempo de resolucao) | Obrigatoria | CC arts. 112-113 | Litigio sobre o que constitui descumprimento |
| Metodo de medicao das metricas | Recomendada | CC art. 113 | Disputa sobre como verificar cumprimento |
| Penalidades escalonadas por descumprimento | Recomendada | CC arts. 408-412 | Sem penalidade automatica; necessario provar dano |
| Limite da clausula penal (max valor da obrigacao) | Obrigatoria | CC art. 412 | **Clausula penal > valor do contrato = nula** |
| Exclusoes: janelas de manutencao, forca maior | Recomendada | CC art. 393 | Forca maior ja exclui responsabilidade por lei; manutencao vira litigio |
| Procedimento de escalonamento e gestao de incidentes | Recomendada | — | Comunicacao desorganizada; atraso na resolucao |
| Relatorios periodicos de performance | Recomendada | — | Dificuldade de comprovar descumprimento retroativamente |

---

## Distribuicao e Exclusividade

| Clausula | Status | Artigo de Lei | Consequencia se Ausente |
|----------|--------|---------------|------------------------|
| Territorio definido (exclusivo ou nao) | Obrigatoria | CC art. 112 | Ausencia de exclusividade = nao exclusivo (presuncao) |
| Metas minimas de compra como condicao de exclusividade | Recomendada | — | Exclusividade sem contraprestacao pode ser questionada |
| Prazo determinado ou indeterminado com aviso previo | Obrigatoria | CC art. 473, par. unico | Prazo indeterminado exige aviso previo razoavel |
| Indenizacao por rescisao imotivada | Recomendada | CC art. 473, par. unico | Se investimentos consideraveis, distribuidor pode reclamar judicialmente |
| **Exclusividade com prazo definido** | Obrigatoria | Lei 12.529/2011, art. 36 | Exclusividade sem prazo → risco anticoncorrencial (CADE) |

---

## Clausulas de Protecao

| Clausula | Status | Artigo de Lei | Consequencia se Ausente |
|----------|--------|---------------|------------------------|
| Clausula de confidencialidade | Recomendada | CC art. 422 (boa-fe) | Informacoes comerciais sem protecao contratual |
| LGPD: identificacao controlador/operador, finalidade, seguranca | Obrigatoria (se dados pessoais) | LGPD arts. 7, 46 | Sancao ANPD ate 2% do faturamento (max R$ 50M) |
| Forca maior e caso fortuito | Recomendada | CC art. 393 | Aplica-se regime legal; sem procedimento de notificacao definido |
| Seguro de transporte/carga | Recomendada | — | Risco de perda total sem cobertura |
| Anticorrupcao (Lei 12.846/2013) | Recomendada | Lei 12.846/2013 | Responsabilidade objetiva da empresa por atos de fornecedores |

---

## Rescisao

| Clausula | Status | Artigo de Lei | Consequencia se Ausente |
|----------|--------|---------------|------------------------|
| Hipoteses de rescisao por justa causa | Recomendada | CC art. 475 | Resolucao so por inadimplemento; sem procedimento claro |
| Aviso previo para rescisao sem justa causa | Obrigatoria | CC art. 473 | Rescisao imediata pode gerar dever de indenizar |
| Prazo de aviso previo (minimo 30-60 dias) | Recomendada | CC art. 473, par. unico | Juiz arbitra prazo razoavel |
| Renovacao automatica: condicoes e notificacao para nao renovar | Recomendada | CC art. 473 | Vinculacao involuntaria por renovacao tacita |
| Obrigacoes sobreviventes (confidencialidade, garantia) | Recomendada | — | Obrigacoes extinguem-se com o contrato |

---

## Red Flags Especificos de Compras

| Red Flag | Risco | Artigo |
|----------|-------|--------|
| Clausula penal superior ao valor total do contrato | Nula — juiz reduz equitativamente | CC arts. 412-413 |
| Exclusividade sem prazo definido | Anticoncorrencial — CADE pode impugnar | Lei 12.529/2011, art. 36 |
| Renovacao automatica sem mecanismo de notificacao | Vinculacao involuntaria | CC art. 473 |
| Preco sem indice de reajuste em contrato > 12 meses | Desequilibrio economico previsivel | CC art. 317 |
| SLA sem definicao de como medir descumprimento | Litigio sobre a metrica | CC arts. 112-113 |
| Forca maior sem lista exemplificativa | Disputa sobre o que constitui forca maior | CC art. 393 |
| Transferencia de risco antes da entrega efetiva | Comprador assume risco sem posse | CC arts. 492-494 |
