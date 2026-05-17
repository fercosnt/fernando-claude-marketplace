# Compliance + Termos Juridicos BR — referencia operacional

Bloco de termos a injetar nos STORYBOARDs por modo. NAO substitui assessoria juridica do escritorio do cliente — gera a versao **comercial visual** com defaults seguros baseados em legislacao BR atualizada (2024-2026).

## 1. Reajuste — IPCA (default), NUNCA IGP-M

### Por que IPCA

- **IPCA (IBGE)** = inflacao oficial BR. Default pra contratos de servico em 2024-2026.
- **INPC (IBGE)** = aceitavel pra contratos menores ou setores que querem indice mais conservador.
- **IGP-M (FGV)** = caiu em desuso pos-pandemia (volatilidade extrema 2020-2022, picos de 35%+). Bancos e operadoras de telecom recuaram. **NAO usar como default**.

### Clausula-modelo (retainer)

```
O valor do investimento sera reajustado anualmente, na data de aniversario da
celebracao deste contrato, pela variacao positiva do Indice Nacional de Precos
ao Consumidor Amplo (IPCA), publicado pelo Instituto Brasileiro de Geografia
e Estatistica (IBGE), acumulada nos 12 meses anteriores. Caso o IPCA seja
extinto ou substituido, sera adotado o indice oficial que o substitua, ou,
na sua ausencia, o INPC/IBGE.
```

### Clausula adicional — Renegociacao por desequilibrio (art. 478 Codigo Civil)

```
As partes poderao renegociar o investimento na hipotese de variacao
extraordinaria e imprevisivel de custos diretos do servico superior a 15%
nos ultimos 12 meses, conforme art. 478 do Codigo Civil.
```

## 2. Foro de eleicao — Lei 14.879/2024 (jun/2024)

### Mudanca fundamental

Lei 14.879/2024 (jun/2024) **invalidou** clausulas de foro de eleicao que nao tenham **pertinencia** com:
- Domicilio de uma das partes, **OU**
- Local da obrigacao.

Foro aleatorio (ex: "Brasilia" pra contrato entre empresas de SP) **e nulo** desde junho/2024.

### Default seguro pra esta skill

- **Default:** Sao Paulo/SP, Comarca da Capital, Foro Central Civel.
- Justifica-se se:
  - Sede da contratada e SP-capital, OU
  - Local da obrigacao (execucao) e SP-capital.

### Clausula-modelo

```
Fica eleito o foro da Comarca de Sao Paulo, Capital, com renuncia expressa
de qualquer outro por mais privilegiado que seja, para dirimir quaisquer
duvidas ou litigios oriundos do presente contrato, sendo essa eleicao
pertinente ao domicilio de pelo menos uma das partes contratantes,
nos termos da Lei 14.879/2024.
```

### Quando NAO usar SP

- Se ambas as partes ficam fora de SP **E** a obrigacao nao acontece em SP → trocar pra cidade-sede de uma delas. Foro neutro NAO existe pos-lei 14.879/2024.

## 3. Multa moratoria + Multa compensatoria

### Multa moratoria (atraso de pagamento) — 2%/mes cap 20% STJ

```
O atraso no pagamento de qualquer parcela acarretara: (i) juros moratorios
de 1% ao mes, calculados pro rata die; (ii) multa moratoria de 2% sobre o
valor em atraso; (iii) correcao monetaria pelo IPCA/IBGE acumulado no
periodo. A multa moratoria total nao excedera 20% do valor original do debito,
conforme jurisprudencia consolidada do STJ.
```

**Atencao:** STJ invalida multa moratoria **acima de 20%** (REsp 1.061.530/RS, entre outros). Auditor desta skill bloqueia 🔴 multa moratoria >20%.

### Multa compensatoria — rescisao antecipada retainer

```
Em caso de rescisao antecipada por iniciativa do CONTRATANTE sem justa
causa, sera devida multa compensatoria equivalente a 3 (tres) meses do
valor mensal do investimento vigente na data da rescisao.

Em caso de rescisao por descumprimento contratual atribuivel a CONTRATADA,
nao sera devida multa, devendo a CONTRATADA restituir valores pagos
referentes a entregas nao realizadas.
```

**Defaults BR:** 1-3 meses de fee e padrao. **Esta skill usa 3 meses como default** — proporcional ao notice period de 60 dias e cobre custo de realocacao de time.

### Notice period

Default: **60 dias** (range 30-90). Notice <15 dias gera churn imprevisto pra contratada; >90 dias trava cliente.

## 4. LGPD — Bloco obrigatorio pos-2020

### Categoria do dado

- **Dados pessoais comuns:** nome, CPF, email, telefone. LGPD aplica integralmente.
- **Dados pessoais sensiveis** (art. 5, II LGPD): saude, biometria, orientacao sexual, origem racial, conviccao religiosa, dado genetico. **Tratamento restritivo** — base legal mais limitada. Beauty Smile (saude bucal) entra aqui se manipular prontuarios.

### Clausula-modelo (retainer — adaptar por contexto)

```
As partes obrigam-se a observar a Lei Geral de Protecao de Dados Pessoais
(Lei 13.709/2018 - LGPD) e atos normativos correlatos da ANPD.

I. A CONTRATADA atuara como OPERADORA dos dados pessoais que vier a tratar
   por conta da CONTRATANTE, na qualidade de CONTROLADORA.
II. O tratamento sera limitado a finalidade estritamente necessaria a execucao
    deste contrato (principios da finalidade, adequacao e necessidade — art. 6).
III. A CONTRATADA implementara medidas tecnicas e administrativas aptas a
     proteger os dados (art. 46): controle de acesso, criptografia em transito
     e em repouso, registro de operacoes, treinamento de equipe.
IV. Eventual incidente de seguranca sera comunicado a CONTRATANTE em ate 48h.
V. Ao termino do contrato, os dados serao devolvidos ou eliminados, mediante
   termo formal, ressalvada a guarda obrigatoria por lei.
```

### Disclaimer Beauty Smile / Fotona / saude

Quando categoria sensivel → adicionar:

```
Os dados de saude sao categoria sensivel (art. 5, II LGPD). Seu tratamento
exige base legal especifica (art. 11) e medidas reforcadas de seguranca.
A CONTRATADA mantera registro detalhado de operacoes (art. 37) e indicara
encarregado de dados (DPO) acessivel a CONTRATANTE.
```

### Penalidades LGPD

- Advertencia, multa simples ate 2% do faturamento (cap R$ 50 milhoes por infracao).
- Precedente RJ: R$ 300k em danos coletivos por vazamento.

## 5. CADE — Modo `strategic-partnership` (Lei 12.529/2011)

### Criterios de notificacao obrigatoria

Notificacao **simultanea** ao CADE se:
- **Grupo 1:** faturamento bruto BR no ultimo exercicio ≥ **R$ 750 milhoes**, **E**
- **Grupo 2:** faturamento bruto BR no ultimo exercicio ≥ **R$ 75 milhoes**.

Valores atualizados pela Portaria Interministerial MF/MJ 994/2012 (vigente).

### Tipos de ato submetidos

Concentracoes economicas:
- Fusao
- Aquisicao de controle ou parte (≥20% pra concorrentes, ≥5% pra mesma cadeia)
- Joint venture com efeitos no BR
- Contrato associativo, consorcio (com restricao concorrencial)

### Prazo

- **Standard:** ate **240 dias** apos protocolo, prorrogavel por **90 dias**.
- **Sumario** (operacoes sem preocupacao concorrencial — overlap baixo): ate 30 dias.

### Disclaimer obrigatorio no slide (literal)

```
Esta proposta esta sujeita a aprovacao do Conselho Administrativo de Defesa
Economica (CADE) caso atinja os criterios da Lei 12.529/2011 (faturamento
bruto BR de R$ 750 milhoes para um grupo e R$ 75 milhoes para o outro).

Prazo estimado de aprovacao: 240 a 330 dias corridos apos protocolo.
O closing fica condicionado a obtencao desta aprovacao.
```

### Quando NAO precisa CADE

Se nenhum dos grupos atinge o gatilho, **mencionar no slide**:

```
Os criterios da Lei 12.529/2011 nao se aplicam a este caso
(faturamentos abaixo dos thresholds). Notificacao ao CADE dispensada.
```

Transparencia ja antecipa pergunta de comite juridico.

## 6. Mediacao previa — clausula recomendada

CNJ: mediacao previa reduz custos de litigio ~40%.

```
Antes de qualquer medida judicial, as partes submeterao a controversia a
mediacao previa, pelo prazo de 60 (sessenta) dias, em camara de mediacao
de comum acordo (sugerimos: CAM-CCBC, Camara FGV-DIR, ou CAMARB).
Esgotado o prazo sem acordo, fica autorizada a propositura de medida judicial.
```

## 7. NDA / Confidencialidade — modo `strategic-partnership` + retainer sensivel

Bloco padrao:

```
As partes obrigam-se a guardar sigilo sobre toda informacao confidencial
trocada em razao deste contrato, durante sua vigencia e por 5 (cinco) anos
apos seu termino.

"Informacao confidencial" abrange dados financeiros, listas de clientes,
estrategia, propriedade intelectual, prontuarios, planos de produto, e
qualquer informacao marcada como confidencial ou que assim deva ser
considerada por sua natureza.

Ao termino do contrato, cada parte devolvera ou destruira, mediante termo
formal, toda informacao confidencial recebida, retendo apenas as copias
legalmente exigidas, em arquivo segregado.
```

## 8. Compliance setorial — heredado do bundle do cliente

### Beauty Smile (odontologia BR)

- **CFO Resolucao 196/2019** — publicidade odontologica: vedado promessa de cura, antes/depois sem TCLE, sensacionalismo, garantia de resultado.
- **CFO Resolucao 217/2020** — telesservicos odontologicos: limites de telerregulacao.
- **CFM Resolucao 2.336/2023** — telessaude/telemedicina (quando ha medico envolvido).
- **LGPD dados saude** — categoria sensivel (vide §4 acima).
- **Anvisa RDC** — quando ha procedimento com material biologico.

### Fotona (equipamento laser, Anvisa Classe III)

- **Anvisa Classe III** — equipamento laser de alta energia. Material promocional **nao pode** ter comparativo direto com concorrente sem evidencia controlada.
- **CFO 196/2019** aplicada a midia clinica.
- **Disclaimer literal pra deck:**

```
Equipamento Anvisa Classe III. Indicacoes, contraindicacoes e parametros
operacionais conforme bula. Resultados clinicos individuais podem variar.
Evidencia cientifica em {referencias}. Comparacoes com outras tecnologias
baseiam-se em literatura citada, nao em testes head-to-head proprios.
```

### Carnaval 360 (eventos)

- **ECAD** — direitos autorais musicais (obrigatorio).
- **Lei Geral do Esporte 14.597/2023** — quando evento esportivo.
- **Anvisa eventos com alimentos** — quando ha praca de alimentacao.
- **Lei Pele / ECA** — eventos com publico infantojuvenil.

## 9. Assinatura eletronica — Clicksign vs DocuSign vs ICP-Brasil

- **STJ nov/2024** reafirmou validade de assinatura eletronica **sem ICP-Brasil** (MP 2.200-2/2001 + Lei 14.063/2020). REsp + acordaos recentes consolidam.
- **Clicksign** lider local BR (115M+ signatarios, ISO 27001+27701).
- **DocuSign** quando contraparte e multinacional.
- **ICP-Brasil** preferida em escritorios de advocacia, governo, setores regulados (saude tem usado mais).

**Default desta skill:** sugerir Clicksign no CTA do slide final.

## 10. Stack de duplicata eletronica + boleto

- **Duplicata eletronica:** adocao voluntaria Q1 2026, obrigatoria fim de 2026 para grandes empresas.
- **Boleto:** ainda padrao 74% volume B2B BR (Carta Capital 2025).
- **PIX:** crescendo como B2B em valores menores; ainda <30% volume B2B ticket medio-alto.

Slide de termos de pagamento deve oferecer: a vista (PIX/TED) com desconto / parcelado boleto / duplicata por fase.

## 11. M&A — campos canonicos do term sheet BR (refresh)

Range BR 2024-2026:

| Campo | Range BR |
|-------|----------|
| Escrow & Indemnification | **10-12% por 18 meses** (vs 8-10% mercados maduros — risco contingencias trabalhistas/fiscais) |
| Cap indenizacao | **15-25% do deal value** (vs 10-20% mercados maduros) |
| Basket | 0,5-1,5% |
| Break-up fee | 1-5% do deal value |
| Lock-up | 6-24 meses (em deals com stock + earn-out) |
| Survival reps & warranties | 18-36 meses; trabalhista/tributario "material" |
| Earn-out | 1-5 anos; precedente STJ REsp 2.117.094/SP (cumprimento ficto se buyer obstruir) |
| Non-compete key people | 2-5 anos |
| MAC clause | trigger revenue queda >X%, regulatorio, forca maior |
| Working Capital Adjustment | "locked box" ou "completion accounts"; media 12 meses |

## 12. Fontes

- Lei 12.529/2011 — Sistema Brasileiro de Defesa da Concorrencia
- Lei 13.709/2018 — LGPD
- Lei 14.063/2020 — assinatura eletronica
- Lei 14.879/2024 (jun/2024) — foro de eleicao
- Codigo Civil arts. 478, 421-A
- STJ REsp 1.061.530/RS — limite multa moratoria 20%
- STJ REsp 2.117.094/SP — earn-out cumprimento ficto
- Portaria Interministerial MF/MJ 994/2012 — thresholds CADE
- CFO Resolucoes 196/2019 e 217/2020 — odontologia
- CFM Resolucao 2.336/2023 — telessaude
- ANPD — Resolucao 15/2024 (sancoes LGPD)
- CNJ — relatorio mediacao 2024
- Carta Capital 2025 — 77% B2B BR a prazo
- Clicksign — STJ valida assinatura eletronica nov/2024
- Migalhas — Contratos B2B Clausulas Essenciais
- Migalhas — Earn-out M&A Riscos e Boas Praticas
