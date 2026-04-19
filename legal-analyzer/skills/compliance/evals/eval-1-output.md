# Avaliacao de Conformidade — Contrato de Prestacao de Servicos de TI

## Resumo Executivo
- Classificacao geral: YELLOW
- Itens criticos: 0 RED
- Itens de atencao: 3 YELLOW
- Itens conformes: 8 GREEN
- Contexto da relacao: comercial paritaria (B2B, prestacao de servicos de TI)

## Eixo 1: Conformidade LGPD

| # | Item | Status | Fundamentacao |
|---|------|--------|---------------|
| 1 | Identificacao dos agentes | GREEN | LGPD art. 5, VI-VII — Clausula 5.1 identifica claramente CONTRATANTE como Controladora e CONTRATADA como Operadora. |
| 2 | Finalidade e base legal | GREEN | LGPD art. 7, V e art. 6, I-II — Clausula 5.2 especifica finalidade (integracao do sistema ERP), tipo de dados (dados pessoais de clientes) e base legal (execucao de contrato, art. 7, V). |
| 3 | Seguranca e sigilo | GREEN | LGPD art. 46 — Clausula 5.3 detalha medidas tecnicas e administrativas: criptografia em transito e repouso, controle de acesso por funcao e logs de auditoria. Atende ao padrao exigido. |
| 4 | Notificacao de incidentes | YELLOW | LGPD art. 48 — Clausula 5.4 estabelece prazo de 48 horas para comunicacao de incidentes. A ANPD recomenda 72 horas como prazo maximo. O prazo de 48h e mais restritivo que a recomendacao, portanto nao e problematico em si, porem a clausula nao detalha o procedimento de notificacao (natureza dos dados afetados, titulares afetados, medidas adotadas, medidas para mitigar efeitos), o que enfraquece a eficacia operacional. |
| 5 | Suboperadores | GREEN | Clausula 5.5 condiciona subcontratacao a autorizacao previa e escrita da Controladora. Conforme recomendacao doutrinaria e pratica de mercado. |
| 6 | Direitos dos titulares | GREEN | LGPD arts. 17-22 — Clausula 5.6 define cooperacao entre Operadora e Controladora para atender requisicoes de titulares com prazo de 15 dias uteis. Procedimento operacional presente. |
| 7 | Destinacao ao termino | GREEN | LGPD art. 16 — Clausula 5.7 preve devolucao ou eliminacao de dados em ate 30 dias, conforme instrucao da Controladora. Prazo e alternativas definidos. |

### Deteccao de Base Legal
- Contexto identificado: relacao comercial paritaria (B2B, prestacao de servicos de TI)
- Base legal utilizada no contrato: execucao de contrato (LGPD art. 7, V)
- Base legal recomendada: execucao de contrato (art. 7, V) ou consentimento (art. 7, I)
- Avaliacao: adequada — em relacao comercial paritaria entre empresas, a base de execucao de contrato e perfeitamente valida, pois o tratamento de dados de clientes e necessario para a integracao do sistema ERP, que e o objeto contratual.

## Eixo 2: Conformidade Codigo Civil

| Item | Status | Fundamentacao |
|------|--------|---------------|
| Clausula penal | GREEN | CC art. 412 — Multa de 10% sobre o valor remanescente do contrato. Em contrato de 24 meses a R$ 25.000/mes (total R$ 600.000), a multa maxima seria R$ 60.000 no inicio, decrescendo ao longo do tempo. Proporcional e dentro do limite legal (nao excede o valor da obrigacao principal). |
| Boa-fe e funcao social | YELLOW | CC arts. 421-422 — As clausulas sao razoavelmente equilibradas, porem o contrato carece de clausulas sobre obrigacoes reciprocas detalhadas (SLA, niveis de servico, criterios de qualidade, obrigacoes da CONTRATANTE quanto a fornecimento de informacoes e acessos). A ausencia de SLA em contrato de TI pode gerar ambiguidade interpretativa (CC arts. 112-113). |
| Vicios e garantias | YELLOW | CC arts. 441-443 — O contrato nao menciona garantia sobre o sistema ERP desenvolvido, prazos para reclamacao de defeitos, nem procedimento para correcao de vicios no software. Em contrato de desenvolvimento e manutencao de sistema, a ausencia de garantia explicita e uma lacuna relevante. |
| Onerosidade excessiva | GREEN | CC arts. 478-480 — Contrato de 24 meses com reajuste anual pelo IPCA/IBGE. O IPCA e o indice mais adequado para contratos de servicos, refletindo a inflacao ao consumidor. Contudo, o contrato nao possui clausula explicita de reequilibrio por eventos extraordinarios e imprevisiveis, o que seria recomendavel para contrato de longa duracao, mas a existencia de mecanismo de reajuste adequado e prazo definido mitiga o risco. |

## Classificacao Final

O contrato apresenta boa conformidade geral, especialmente no eixo LGPD, onde as 7 clausulas obrigatorias estao presentes com fundamentacao legal adequada. A base legal escolhida (execucao de contrato) e correta para o contexto comercial B2B. Os pontos de atencao concentram-se em detalhes operacionais: a clausula de notificacao de incidentes poderia detalhar melhor o procedimento, e o contrato carece de clausulas tipicas de TI como SLA, garantia de software e procedimento para correcao de defeitos. Nenhum item foi classificado como RED, indicando que nao ha risco critico de nulidade ou ilicitude.

## Perguntas para o Juridico

1. A clausula 5.4 (notificacao de incidentes em 48h) deveria incluir detalhamento do procedimento — quais informacoes a Operadora deve fornecer ao comunicar o incidente (natureza dos dados, titulares afetados, medidas adotadas)?
2. Ha necessidade de incluir clausula de SLA com niveis de servico, tempo de resposta e penalidades por descumprimento, considerando que o objeto e desenvolvimento e manutencao de sistema ERP?
3. Deveria haver clausula especifica de garantia sobre o software desenvolvido, com prazo para reclamacao de vicios e procedimento de correcao?
4. E recomendavel incluir clausula de reequilibrio contratual por onerosidade excessiva (CC arts. 478-480) alem do reajuste pelo IPCA, considerando que o prazo e de 24 meses renovaveis?
5. A clausula 5.7 (destinacao ao termino) deveria exigir declaracao formal de eliminacao por parte da CONTRATADA, como comprovacao de compliance?

## Recomendacoes de Redacao

### Clausula 5.4 — Notificacao de Incidentes (YELLOW)
Texto atual: "Incidentes de seguranca serao comunicados a CONTRATANTE em ate 48 horas apos ciencia."

Texto sugerido:
> "A CONTRATADA devera comunicar a CONTRATANTE qualquer incidente de seguranca que envolva dados pessoais no prazo maximo de 48 (quarenta e oito) horas apos tomar conhecimento, informando: (a) natureza dos dados pessoais afetados; (b) informacoes sobre os titulares envolvidos; (c) indicacao das medidas tecnicas e de seguranca utilizadas para protecao dos dados; (d) riscos relacionados ao incidente; (e) medidas adotadas e a adotar para reverter ou mitigar os efeitos do incidente."

### Boa-Fe e Funcao Social — SLA (YELLOW)
Incluir clausula de nivel de servico:
> "A CONTRATADA devera manter disponibilidade do sistema ERP de no minimo 99,5% ao mes, excluindo janelas de manutencao programada. Falhas criticas deverao ser atendidas em ate 4 (quatro) horas uteis. A CONTRATANTE devera fornecer acessos, informacoes e infraestrutura necessarios para a execucao dos servicos em tempo habil."

### Vicios e Garantias (YELLOW)
Incluir clausula de garantia de software:
> "A CONTRATADA garante o funcionamento do sistema ERP conforme especificacoes tecnicas acordadas pelo periodo de 90 (noventa) dias apos cada entrega ou atualizacao. Vicios de software identificados neste periodo serao corrigidos sem custo adicional, no prazo de 15 (quinze) dias uteis apos a notificacao."

---

> **Aviso:** Esta avaliacao de conformidade e uma ferramenta auxiliar de triagem e NAO constitui parecer juridico. Recomenda-se consultar advogado para validacao das conclusoes e tomada de decisoes. Jurisdicao: Brasil. Legislacao de referencia: LGPD (Lei 13.709/2018), Codigo Civil (Lei 10.406/2002).
