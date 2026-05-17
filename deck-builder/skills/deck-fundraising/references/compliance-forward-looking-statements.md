# Compliance: Forward-Looking Statements + CVM + Rouanet

Disclaimers obrigatorios para deck de captacao quando contem projecoes futuras, valores estimados, timeline pra rodadas, ROI esperado, ou qualquer numero nao auditado. Aplica-se a investidor anjo/VC/family office (CVM) E patrocinador cultural (MinC/Rouanet).

## Quando disparar disclaimer (auto-trigger)

Esta skill **gera disclaimer automaticamente** se o STORYBOARD contem qualquer um destes elementos:

| Elemento | Razao |
|----------|-------|
| Projecao de MRR/receita futura | Sec. 27A Securities Act (US) + Res. CVM 160/22 |
| Multiplo de valuation projetado | Forward-looking statement classico |
| ROI patrocinador estimado | Promessa de retorno = oferta publica disfarcada |
| Timeline pra proxima rodada / Series A/B | "Sujeito a condicoes de mercado" |
| Numero de clientes/pacientes/eventos projetado | Performance future |
| Custos/CAC/LTV projetados em horizonte futuro | Unit economics futuro |
| Penetracao de mercado planejada | TAM/SAM/SOM com captura futura |

**Se NADA disso aparece** (deck so com historico auditado + ask), disclaimer e opcional mas recomendado.

## Disclaimer canonico (Brasil — CVM)

Vai como **slide separado** (tipo `disclaimer`) penultimo + **rodape resumido** em todos os slides com numero futuro.

### Slide disclaimer (texto completo)

> **Forward-Looking Statements & Confidencialidade**
>
> Este material contem declaracoes prospectivas (*forward-looking statements*) baseadas em premissas atuais da administracao da [NOME EMPRESA]. Resultados reais podem diferir materialmente das projecoes apresentadas devido a fatores incluindo, sem limitacao: condicoes economicas gerais, alteracoes regulatorias, dinamica competitiva, mudancas de comportamento do consumidor e disponibilidade de capital.
>
> Este documento NAO constitui oferta publica de valores mobiliarios nos termos da Lei 6.385/76, Resolucao CVM 160/22 (Ofertas Publicas de Distribuicao) ou Resolucao CVM 88/22 (Crowdfunding de Investimento). Distribuicao restrita a investidores qualificados conforme Resolucao CVM 30/21, sob NDA previamente assinado.
>
> As projecoes financeiras e operacionais nao constituem garantia de resultado futuro. Investidores devem consultar seus proprios assessores juridicos, contabeis e tributarios antes de qualquer decisao de investimento.
>
> Confidencial — distribuicao restrita.

### Rodape (todos os slides com numero futuro)

> Projecoes; ver disclaimer.

## Disclaimer canonico (US — SEC)

Quando deck e em ingles ou pitch a fundo US:

> **Forward-Looking Statements Disclaimer**
>
> This presentation contains forward-looking statements within the meaning of Section 27A of the Securities Act of 1933 and Section 21E of the Securities Exchange Act of 1934, qualifying for safe harbor under the Private Securities Litigation Reform Act of 1995 (PSLRA). Statements that are not historical facts — including projections, milestones, market opportunity, and expected outcomes — are forward-looking and subject to risks and uncertainties.
>
> Actual results may differ materially. This presentation does not constitute an offer to sell or solicitation of an offer to buy securities. Any offering will be made only to accredited investors pursuant to Regulation D, Rule 506(b)/506(c), and only through definitive offering documents.
>
> Confidential — for recipient use only.

## Anti-padroes especificos (BLOQUEAR — 🔴 no STORYBOARD)

### 1. Promessa de retorno garantido
Frases proibidas em qualquer slide:
- "Retorno garantido de X%"
- "Sem risco / risco zero"
- "Lucro certo"
- "Multiplica seu capital por X em Y anos" (sem "projetado")
- "Performance historica indica retorno futuro" (proibido CVM)

Se detectar qualquer uma → marcar 🔴 BLOQUEANTE no Compliance & Disclaimers do STORYBOARD + sugerir reescrita.

### 2. Oferta publica disfarcada (Res. CVM 160/22)
**NAO pode** pitch:
- Sem NDA assinado previamente
- A grupo >20 pessoas simultaneo (exceto demo day batch acelerador formal)
- Em midia ampla (LinkedIn post publico convocando investimento, anuncio pago, podcast aberto)
- Sem identificacao do investidor como "qualificado" (Res. CVM 30/21)

**Para crowdfunding ate R$15M:** Res. CVM 88/22 permite oferta publica via plataforma autorizada (Captable, Kria, Bloxs etc) — pitch publico OK se feito ATRAVES de plataforma registrada.

### 3. Confidencialidade implicita sem NDA
Slide nao pode dizer "confidencial" se NAO houver NDA. Ou poe NDA real, ou tira o claim de confidencialidade. Hibrido nao funciona em DD.

## Disclaimer Rouanet (sponsorship cultural)

Substitui o disclaimer CVM quando deck e sponsorship cultural com Lei 8.313/91 (Rouanet) ou leis estaduais/municipais equivalentes.

### Slide disclaimer (Rouanet)

> **Lei de Incentivo a Cultura — PRONAC nº [NUMERO]**
>
> O projeto [NOME PROJETO] foi aprovado pelo Ministerio da Cultura (MinC) sob o numero PRONAC nº [XXXXXX] em [DATA], permitindo captacao via Lei Federal 8.313/91 (Lei Rouanet). Valores indicados como meta de captacao estao sujeitos a homologacao do Ministerio da Cultura e a regras de utilizacao publicadas no DOU.
>
> Patrocinadores pessoa juridica tributados pelo lucro real podem deduzir ate 4% do IRPJ devido conforme art. 26 da Lei 8.313/91. Pessoa fisica pode deduzir ate 6% do IR devido (Art. 26 inc. II). Contrapartidas de visibilidade descritas neste material sao garantidas mediante assinatura de Termo de Patrocinio especifico.
>
> Este material nao constitui oferta publica de valores mobiliarios. Projecoes de alcance, audiencia e ROI patrocinador sao estimativas baseadas em edicoes anteriores e tendencias de mercado — resultados podem variar.
>
> Confidencial — distribuicao restrita a patrocinadores potenciais.

### Variantes regionais
- **Lei do Audiovisual (Lei 8.685/93)** — para projetos audiovisuais (cinema, serie, doc)
- **Lei estadual de incentivo (Lei Aldir Blanc / ProAC SP / FAR-J etc)** — citacao especifica do mecanismo
- **Lei municipal (Lei do Mendonca SP, Lei de Incentivo RJ etc)** — quando municipal

**Regra:** sempre citar o mecanismo legal exato pelo qual a deducao acontece. Sem isso = patrocinador tem risco fiscal.

## Tier de issues no STORYBOARD

Skill marca no campo `## Compliance & Disclaimers` do STORYBOARD:

### 🔴 BLOQUEANTE (resolver antes de apresentar)
- Promessa de retorno garantido (qualquer slide)
- Confidencialidade reclamada sem NDA mencionado
- Oferta publica sem qualificacao do investidor (>20 pessoas + sem plataforma Res. 88/22)
- Slide de tracao com dado inventado/sem fonte
- Claim regulatorio (Anvisa, CFO, MinC) sem numero/citacao

### 🟡 VERIFICAR (revisar antes de apresentar)
- Projecao sem premissa explicita ("vamos faturar R$10M em 2027" sem mecanismo)
- TAM top-down sem fundamentacao bottom-up
- Logo wall sem permissao escrita (cliente pode pedir retirada)
- Time slide com pessoa nao confirmada/em negociacao
- ROI patrocinador sem metodologia de calculo

### ✅ OK (confirmacoes positivas)
- Disclaimer canonico presente como slide separado
- Ask especifico (valor + uso + timeline)
- TAM bottom-up com fontes citadas
- Numeros de tracao auditados/com fonte
- NDA mencionado (se confidencialidade reclamada)

## Casos especiais

### Family office BR
Disclaimer canonico CVM **+ aviso adicional** sobre fluxo de caixa vs equity:

> Family office considerando este investimento deve avaliar perfil de risco vs preservacao de capital. Equity em startup early-stage tem alta correlacao com mercado de risco e baixa liquidez — typical lock-up de 3-7 anos ate evento de liquidez.

### Fundo international (US/Europa em deal BR)
**Adicionar:**
- FATCA compliance mention
- Cross-border tax structure caveat
- IOF (BR) + withholding tax disclosure
- "Deal subject to Brazilian Central Bank capital flow registration"

### Captacao via SAFE/CCB/Mutuo Conversivel
**Adicionar slide adicional** ("Estrutura da rodada") com:
- Instrumento (SAFE / CCB / Mutuo / Equity direto)
- Valuation cap (se SAFE com cap)
- Discount rate (se SAFE com discount)
- Maturity/conversion trigger (se CCB ou mutuo)
- Drag-along / tag-along / liquidation preference (se equity direto)

NAO substitui assessoria juridica — disclaimer:

> Estrutura sujeita a confirmacao via term sheet definitivo + DD legal. Termos finais podem diferir.

## Checklist final (skill aplica antes de finalizar STORYBOARD)

- [ ] Disclaimer slide separado adicionado (penultimo, antes de agradecimento)
- [ ] Rodape resumido em slides com numeros futuros
- [ ] Anti-padroes 1-3 escaneados — nenhum 🔴 bloqueante encontrado
- [ ] Se sponsorship cultural → numero PRONAC + lei especifica citados
- [ ] Se Anvisa/CFO/CFM relevante → footnote com numero/responsavel tecnico
- [ ] Se US deal → SEC disclaimer adicionado
- [ ] Tier de issues preenchido (🔴/🟡/✅)
