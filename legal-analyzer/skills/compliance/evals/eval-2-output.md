# Avaliacao de Conformidade — Contrato Individual de Trabalho

## Resumo Executivo
- Classificacao geral: RED
- Itens criticos: 6 RED
- Itens de atencao: 1 YELLOW
- Itens conformes: 0 GREEN
- Contexto da relacao: emprego

## Eixo 1: Conformidade LGPD

| # | Item | Status | Fundamentacao |
|---|------|--------|---------------|
| 1 | Identificacao dos agentes | RED | LGPD art. 5, VI-VII — O contrato nao identifica quem e Controlador e quem e Operador dos dados pessoais. A Clinica Saude Total trata dados da empregada (CPF, biometria, dados trabalhistas) sem definir papeis de tratamento. |
| 2 | Finalidade e base legal | RED | LGPD art. 7, I vs. art. 7, II e V — O contrato usa consentimento ("consente expressamente") como base legal em relacao de emprego. Em relacao trabalhista, ha desequilibrio de poder que vicia o consentimento (posicao ANPD). A base legal correta seria execucao de contrato (art. 7, V) para dados operacionais e obrigacao legal (art. 7, II) para eSocial. Alem disso, a finalidade e excessivamente generica ("todas as finalidades relacionadas ao contrato"). |
| 3 | Seguranca e sigilo | RED | LGPD art. 46 — Ausencia total de clausula de seguranca de dados pessoais. O contrato coleta dados biometricos (ponto biometrico) que sao dados sensiveis (art. 11), exigindo nivel ainda maior de protecao. Nenhuma medida tecnica ou administrativa e mencionada. |
| 4 | Notificacao de incidentes | RED | LGPD art. 48 — Ausencia total de clausula de notificacao de incidentes de seguranca. Nao ha prazo nem procedimento definido para comunicacao em caso de vazamento de dados. |
| 5 | Suboperadores | RED | LGPD arts. 42-45 — Silencio total sobre subcontratacao de terceiros para tratamento de dados. Nao ha restricao nem procedimento para eventual compartilhamento com suboperadores. |
| 6 | Direitos dos titulares | RED | LGPD arts. 17-22 — Ausencia de clausula sobre direitos da titular (empregada) de acessar, corrigir, eliminar ou portar seus dados pessoais. Nao ha procedimento operacional definido. |
| 7 | Destinacao ao termino | RED | LGPD art. 16 — Silencio sobre o destino dos dados pessoais ao termino do contrato de trabalho. Nao define se dados serao eliminados ou retidos (e por qual base legal). |

### Deteccao de Base Legal
- Contexto identificado: emprego (contrato individual de trabalho CLT)
- Base legal utilizada no contrato: Consentimento (art. 7, I) — "consente expressamente"
- Base legal recomendada: Execucao de contrato (art. 7, V) para dados operacionais do vinculo empregaticio; Obrigacao legal (art. 7, II) para envio ao eSocial, RAIS e CAGED
- Avaliacao: INADEQUADA — Em relacao de emprego ha desequilibrio de poder entre empregador e empregado. O empregado nao tem liberdade real para recusar o consentimento, o que o torna viciado e invalido conforme orientacao da ANPD. O uso de consentimento em relacao trabalhista e considerado a base legal mais fragil e inadequada, pois o empregado pode revoga-lo a qualquer momento (art. 8, par. 5), criando inseguranca juridica para o empregador.

## Eixo 2: Conformidade Codigo Civil

| Item | Status | Fundamentacao |
|------|--------|---------------|
| Clausula penal | RED | CC art. 412 — A multa de R$ 50.000,00 e manifestamente desproporcional ao valor da obrigacao principal. O salario e de R$ 2.500,00 mensais; a multa equivale a 20 meses de salario. O art. 412 do Codigo Civil determina que a clausula penal nao pode exceder o valor da obrigacao principal. Alem disso, em contrato de trabalho, a CLT (art. 462) impoe limites ainda mais restritivos a descontos do empregado. |
| Boa-fe e funcao social | YELLOW | CC arts. 421-422 — A clausula de confidencialidade por prazo indeterminado apos o termino do contrato e desproporcional. Clausulas de confidencialidade pos-contrato devem ter prazo razoavel (tipicamente 1-2 anos) e escopo definido. Prazo indeterminado pode ser considerado abusivo por violar a funcao social do contrato e restringir excessivamente a liberdade profissional da empregada. A clausula "sigilo absoluto sobre todas as informacoes" tambem e excessivamente ampla — deveria especificar quais informacoes sao confidenciais. |
| Vicios e garantias | N/A | Nao aplicavel a contrato de trabalho — vicios redibitórios (CC arts. 441-443) referem-se a contratos de compra e venda e similares. |
| Onerosidade excessiva | N/A | Nao aplicavel — contrato de trabalho tem regramento proprio pela CLT. Reajustes salariais seguem convencao coletiva e legislacao trabalhista. |

## Classificacao Final

Este contrato de trabalho apresenta graves deficiencias de conformidade regulatoria. O problema mais critico e o uso de consentimento como base legal para tratamento de dados em relacao de emprego — base inadequada conforme orientacao da ANPD, que reconhece o desequilibrio de poder entre empregador e empregado. A clausula de protecao de dados (clausula 4) e a unica que menciona LGPD, mas o faz de forma incorreta e insuficiente: usa base legal errada, nao identifica agentes de tratamento, nao estabelece medidas de seguranca, nao preve notificacao de incidentes, ignora direitos dos titulares e silencia sobre destinacao ao termino. A coleta de dados biometricos (ponto biometrico) agrava a situacao por tratar-se de dado sensivel (LGPD art. 11). No eixo do Codigo Civil, a clausula penal de R$ 50.000,00 e desproporcional ao salario e a confidencialidade por prazo indeterminado e abusiva.

## Perguntas para o Juridico

1. A clausula penal de R$ 50.000,00 e executavel considerando que o salario e R$ 2.500,00? Qual valor seria proporcional e defensavel? (CC art. 412)
2. O consentimento na clausula 4 deve ser substituido por qual base legal especifica para cada tipo de tratamento (operacional, eSocial, biometria)? (LGPD art. 7)
3. O tratamento de dados biometricos (ponto) exige consentimento especifico e destacado por ser dado sensivel (LGPD art. 11) — como estruturar isso sem conflitar com a inadequacao do consentimento em relacao de emprego?
4. A confidencialidade por prazo indeterminado e defensavel judicialmente? Qual prazo a jurisprudencia trabalhista tem aceito?
5. E necessario elaborar clausula separada de protecao de dados ou um addendum/aditivo contratual especifico de LGPD?
6. A empresa possui Relatorio de Impacto a Protecao de Dados (RIPD) para o tratamento de biometria dos empregados? (LGPD art. 38)

## Recomendacoes de Redacao

### Clausula 4 — Protecao de Dados (substituir integralmente)

Texto atual: "A empregada consente expressamente com o tratamento de seus dados pessoais para todas as finalidades relacionadas ao contrato de trabalho, incluindo envio de informacoes ao eSocial, controle de ponto biometrico e comunicacoes internas."

**Texto recomendado:**

> **4. PROTECAO DE DADOS PESSOAIS**
>
> 4.1. A EMPREGADORA, na qualidade de Controladora de dados pessoais nos termos da LGPD (Lei 13.709/2018), tratara os dados pessoais da EMPREGADA para as seguintes finalidades e bases legais:
>
> a) Execucao do contrato de trabalho (art. 7, V da LGPD): dados cadastrais, bancarios e funcionais necessarios a gestao do vinculo empregaticio;
>
> b) Cumprimento de obrigacao legal (art. 7, II da LGPD): envio de informacoes ao eSocial, RAIS, CAGED e demais obrigacoes trabalhistas e previdenciarias;
>
> c) Controle de ponto biometrico: por tratar-se de dado pessoal sensivel (art. 5, II e art. 11 da LGPD), o tratamento sera realizado com base em [definir base legal adequada com orientacao juridica — obrigacao legal ou consentimento especifico e destacado].
>
> 4.2. A EMPREGADORA adotara medidas tecnicas e administrativas aptas a proteger os dados pessoais de acessos nao autorizados e de situacoes acidentais ou ilicitas de destruicao, perda, alteracao, comunicacao ou difusao (art. 46 da LGPD).
>
> 4.3. Em caso de incidente de seguranca envolvendo dados pessoais da EMPREGADA, a EMPREGADORA comunicara a titular e a ANPD no prazo de 72 (setenta e duas) horas (art. 48 da LGPD).
>
> 4.4. A EMPREGADA podera exercer seus direitos de titular previstos nos arts. 17-22 da LGPD mediante solicitacao ao setor de Recursos Humanos.
>
> 4.5. Ao termino do contrato de trabalho, os dados pessoais serao retidos apenas pelo prazo necessario ao cumprimento de obrigacoes legais trabalhistas e previdenciarias (art. 16, I da LGPD), sendo eliminados de forma segura apos o decurso dos prazos legais.

### Clausula 5 — Clausula Penal (substituir)

Texto atual: "Em caso de descumprimento de qualquer obrigacao contratual, a parte infratora pagara multa de R$ 50.000,00."

**Texto recomendado:**

> **5. CLAUSULA PENAL:** Em caso de descumprimento de qualquer obrigacao contratual, a parte infratora pagara multa equivalente a 1 (um) salario contratual vigente, sem prejuizo de eventual apuracao de perdas e danos quando expressamente previsto neste contrato (CC art. 416, paragrafo unico).

### Clausula 6 — Confidencialidade (substituir)

Texto atual: "A empregada obriga-se a manter sigilo absoluto sobre todas as informacoes da clinica por prazo indeterminado apos o termino do contrato."

**Texto recomendado:**

> **6. CONFIDENCIALIDADE:** A EMPREGADA obriga-se a manter sigilo sobre informacoes confidenciais da EMPREGADORA, assim entendidas: dados de pacientes, protocolos clinicos, informacoes financeiras e estrategias comerciais. Esta obrigacao perdurara por 2 (dois) anos apos o termino do contrato de trabalho, ressalvadas as informacoes que se tornarem publicas por meios licitos ou que a EMPREGADA comprove ter obtido de forma independente.

---

> **Aviso:** Esta avaliacao de conformidade e uma ferramenta auxiliar de triagem e NAO constitui parecer juridico. Recomenda-se consultar advogado para validacao das conclusoes e tomada de decisoes. Jurisdicao: Brasil. Legislacao de referencia: LGPD (Lei 13.709/2018), Codigo Civil (Lei 10.406/2002).
