# Compliance Anvisa — Equipamentos medicos e dentais

> Regras enforcement em 3 tiers (🔴 BLOCKER / 🟡 VERIFICAR / ✅ OK) para o STORYBOARD `deck-equipment`.
> Risco juridico real: badmouth pode gerar acao de concorrencia desleal (Lei 9.279/96 art. 195),
> denuncia CONAR + sancoes CFM (Resolucao 1.974/2011) e CFO (Resolucao 196/2019).

---

## 1. Classes Anvisa — referencia rapida

| Classe | Risco | Exemplos | Registro |
|--------|-------|----------|----------|
| I | Baixo | Espelho clinico, espatula, instrumentais simples | Notificacao |
| II | Medio | Scanners intraorais (Trios, iTero), unidades de raio-X, equipamentos eletromedicos basicos, implantes | Registro Anvisa |
| III | Alto | Laseres terapeuticos e cirurgicos (Fotona LightWalker, Lumenis), tomografos Cone Beam, equipamentos com radiacao ionizante | Registro Anvisa + requisitos adicionais (curso habilitacao operador, sala blindada se ionizante) |
| IV | Muito alto | Implantes ativos, equipamentos de suporte vital | Registro Anvisa + auditorias |

**Formato numero de registro:** `xxxxxxx-x` (10 digitos com hifen antes do ultimo) OU `MS xxxxxxx`.

**Onde verificar:** Consulta publica Anvisa em `consultas.anvisa.gov.br` (campo "Produtos para Saude").

---

## 2. Tier 🔴 BLOCKER — resolver ANTES de apresentar

### 🔴 B1. Equipamento sem registro Anvisa citado

**Por que bloqueia:** Apresentar/vender equipamento medico sem registro Anvisa vigente e infracao sanitaria (Lei 6.360/76). Acumula com publicidade enganosa (CDC art. 37).

**Fix:** Pedir ao usuario o numero de registro Anvisa do equipamento. Se nao tem ou e estrangeiro sem registro BR ainda, o equipamento nao pode ser vendido no Brasil — slide 14 deve declarar isso ou o pitch nao pode ocorrer.

### 🔴 B2. Claim fora de bula sem disclaimer "off-label"

**Por que bloqueia:** Indicacao terapeutica nao aprovada na bula/rotulagem e uso off-label. Apresentar como aprovado e propaganda enganosa.

**Fix:** Toda indicacao mencionada no deck deve constar na bula. Se for off-label cientificamente respaldado, marcar slide com texto "Uso off-label — evidencia cientifica em [referencias], indicacao nao constante em bula".

### 🔴 B3. Comparativo com badmouth

**Por que bloqueia:** Denegrir concorrente (mesmo verdadeiramente) configura concorrencia desleal (Lei 9.279/96 art. 195, III: "emprega meio fraudulento, para desviar... clientela de outrem"). Para profissionais de saude, soma-se infracao etica CFM 1.974/2011 art. 13 e CFO 196/2019 art. 8.

**Fix:** Seguir estrutura de comparativo responsavel da secao 5 deste documento.

---

## 3. Tier 🟡 VERIFICAR — sinalizar para humano confirmar

### 🟡 V1. Classe III declarada para laser

Laseres terapeuticos e cirurgicos sao Classe III. CFO Resolucao 35/2018 exige:
- Curso de habilitacao do operador (>=80h teorico + pratico)
- Registro CFO especifico para laser
- Sala adequada (sinalizacao, oculos)

Se o deck nao mostra explicitamente Classe III no slide 14 + nao menciona habilitacao do operador → 🟡.

### 🟡 V2. Conflito de interesse (COI) declarado

Apresentador e distribuidor, representante, recebe comissao ou tem participacao societaria na marca? Deve declarar em slide proprio OU rodape persistente. CFM 1.974/2011 art. 5 + CFO 196/2019.

Se o input nao revela natureza da relacao do apresentador com a marca → 🟡 (pedir ao usuario para esclarecer).

### 🟡 V3. Imagens de paciente real com TCLE

Caso clinico do slide 9 com imagem de paciente real exige Termo de Consentimento Livre e Esclarecido (TCLE) arquivado, conforme LGPD (Lei 13.709/18) + CFM/CFO. Marcar 🟡 sempre que slide 9 use imagem real, para confirmar arquivamento.

### 🟡 V4. Numero registro nao verificado

Se usuario forneceu numero mas nao confirmou consulta na base publica → 🟡.

---

## 4. Tier ✅ OK — pode prosseguir

- Registro Anvisa citado com numero verificavel
- COI declarado (slide proprio ou rodape persistente)
- Comparativo responsavel (segue secao 5 deste documento)
- TCLE arquivado para caso clinico com imagem real
- Habilitacao do operador citada (se Classe III)
- Indicacoes todas dentro da bula OU marcadas como off-label com referencias

---

## 5. Comparativo responsavel — anti-badmouth

### Estrutura obrigatoria

1. **Cite o concorrente pelo nome com respeito.**
   - "Lumenis LightSheer e referencia consolidada em fotodepilacao desde 2003..."
   - "Straumann SLActive e padrao-ouro em superficie de implante..."

2. **Liste 2-3 forcas reconhecidas da alternativa.**
   - Forcas reais, baseadas em literatura, bula, ou benchmark independente.
   - NUNCA inventar fraqueza para parecer balanceado.

3. **Liste 2-3 limites com fonte explicita.**
   - Citar bula, paper, ou benchmark publico. NUNCA achismo ou "experiencia do apresentador" como unica fonte.
   - Limite e diferente de defeito — "nao integra Nd:YAG" e limite; "nao funciona" e badmouth.

4. **Posicione nosso equipamento como superior em criterio especifico.**
   - "O LightWalker se diferencia por integrar Er:YAG + Nd:YAG no mesmo chassi."
   - NUNCA "e melhor em tudo" — superioridade geral e implausivel e gera ceticismo.

5. **Feche com criterio neutro de escolha.**
   - "O melhor equipamento depende do mix de procedimentos da clinica, volume e orcamento."
   - Devolve poder de decisao ao cliente — alinha com venda consultiva.

### Frases proibidas (lista nao exaustiva)

| Categoria | Exemplos |
|-----------|----------|
| Adjetivos pejorativos | "inferior", "ultrapassado", "limitado", "fraco", "obsoleto" |
| Negacoes generalistas | "nao funciona", "nao serve para nada", "ninguem usa mais" |
| Insinuacoes | "tem fama de quebrar", "ouvi varios reclamando", "sabe-se que..." |
| Comparativos absolutos | "muito melhor", "incomparavel", "destrua a concorrencia" |
| Especulacao sobre concorrente | "X esta perdendo mercado porque...", "Y vai descontinuar..." |

### Frase modelo canonica

> "Tanto o LightWalker quanto o LightSheer atendem fotodepilacao com seguranca. O LightWalker se diferencia por integrar Er:YAG (2940nm) e Nd:YAG (1064nm) no mesmo chassi, o que elimina a necessidade de um segundo equipamento para protocolos periodontais e cirurgicos. O LightSheer e mais especializado em fotodepilacao isolada e tem custo de aquisicao inicial menor. A escolha depende do mix de procedimentos da clinica: se >40% sao laseres nao-fotodepilatorios, o LightWalker tende a pagar mais rapido pela integracao; se a clinica e majoritariamente fotodepilacao, o LightSheer pode ser suficiente."

### Modo `comparativo` (slides 8a-8c)

Quando cliente avalia 2-3 marcas simultaneamente, expandir slide 8 em 3:

- **8a Tabela de forcas**: cada marca em coluna, 3-4 forcas reconhecidas listadas com fonte
- **8b Tabela de limites**: cada marca em coluna, 2-3 limites com fonte (bula, paper, benchmark)
- **8c Criterio neutro de escolha**: 1 frase de fechamento que ancora a decisao em criterio mensuravel (volume, mix, orcamento, integracao com fluxo existente)

NUNCA criar tabela "vencedor por categoria" — implica badmouth implicito.

---

## 6. Compliance especifico por categoria

### Laser (Classe III)
- Slide 14 deve declarar: numero Anvisa + Classe III + habilitacao CFO/CFM exigida
- Modo de operacao com classe de seguranca laser (1-4) se aplicavel

### Implantes
- Material (titanio grau 4 vs 5, zirconia) deve constar com norma ISO
- Indicacao de carga (imediata, precoce, tardia) deve estar dentro do protocolo aprovado

### Scanners intraorais (Classe II)
- LGPD: arquivos STL/PLY do paciente sao dados de saude
- Integracao com software deve mencionar conformidade DICOM/HL7

### Equipamentos com radiacao ionizante (Cone Beam, raio-X)
- Adicional: licenciamento CNEN, sala blindada com laudo, dosimetro operador
- Sliding Programa de Garantia da Qualidade (PGQ) obrigatorio
