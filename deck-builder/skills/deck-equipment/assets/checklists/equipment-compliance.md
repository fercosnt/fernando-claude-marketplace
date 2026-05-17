# Checklist Compliance — deck-equipment

Aplicar este checklist em todo STORYBOARD `deck-equipment` ANTES de finalizar v1.
Classifica cada item em 🔴 BLOCKER / 🟡 VERIFICAR / ✅ OK.

> Detalhamento de cada regra em [../references/compliance-anvisa-equipment.md](../../references/compliance-anvisa-equipment.md).

---

## 🔴 BLOCKER — resolver ANTES de apresentar

- [ ] Numero de registro Anvisa do equipamento citado no slide 14? (formato `xxxxxxx-x` ou `MS xxxxxxx`)
- [ ] TODAS as indicacoes mencionadas estao dentro da bula/rotulagem aprovada? (off-label requer disclaimer explicito + referencia)
- [ ] Bloco comparativo (slide 8 ou 8a-c) esta SEM frases proibidas do anti-badmouth? Verificar:
  - "inferior", "ultrapassado", "limitado", "obsoleto", "fraco"
  - "nao funciona", "nao serve", "ninguem usa mais"
  - "tem fama de quebrar", "ouvi reclamar"
  - "muito melhor", "incomparavel", "destrua a concorrencia"
  - "X esta perdendo mercado", "Y vai descontinuar"

## 🟡 VERIFICAR — sinalizar para humano confirmar antes da apresentacao

- [ ] Se laser → Classe III declarada explicitamente no slide 14?
- [ ] Se laser → habilitacao do operador CFO 35/2018 declarada ou contemplada?
- [ ] Conflito de interesse (COI) do apresentador declarado em slide proprio OU rodape persistente?
- [ ] Caso clinico do slide 9 com imagem de paciente real → TCLE arquivado e conforme LGPD?
- [ ] Numero de registro Anvisa verificado em base publica (`consultas.anvisa.gov.br`)?
- [ ] Se equipamento com radiacao ionizante → licenciamento CNEN + sala blindada + dosimetro operador citados?
- [ ] Se scanner intraoral → LGPD aplicada aos arquivos STL/PLY/dados do paciente?

## ✅ OK — pode prosseguir

- [ ] Registro Anvisa citado com numero verificavel
- [ ] COI declarado (slide proprio ou rodape)
- [ ] Comparativo responsavel — segue estrutura obrigatoria:
  - cita concorrente pelo nome com respeito
  - lista 2-3 forcas reconhecidas
  - lista 2-3 limites com fonte explicita
  - posiciona equipamento como superior em criterio especifico
  - fecha com criterio neutro de escolha
- [ ] TCLE arquivado para caso clinico com imagem real
- [ ] Habilitacao do operador citada se Classe III
- [ ] Indicacoes dentro da bula OU off-label explicitamente marcado

---

## Algoritmo de classificacao

1. Rodar regex anti-badmouth contra TEXTO TODO do slide 8 / 8a / 8b / 8c
2. Se HIT → 🔴 BLOCKER (listar frase encontrada + slide + linha)
3. Procurar string Anvisa + numero registro no slide 14 → se ausente, 🔴
4. Procurar indicacoes mencionadas vs bula conhecida → se divergencia sem disclaimer "off-label", 🔴
5. Procurar `Classe III` + `CFO` no slide 14 SE auto-detection Fotona/laser ativada → se ausente, 🟡
6. Procurar COI no deck → se ausente E apresentador tem relacao comercial declarada em E1/E5, 🟡
7. Procurar TCLE no slide 9 SE imagem real → se ausente, 🟡

## Output

Preencher bloco `## Compliance & Disclaimers` do STORYBOARD com cada item classificado:

```markdown
## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes:
- Slide 14: numero de registro Anvisa nao citado
- Slide 8: frase "Lumenis e ultrapassado" detectada — anti-badmouth violado

🟡 Verificar:
- Slide 14: Classe III nao declarada explicitamente (auto-detection Fotona ativa)
- Slide 9: imagem de paciente — confirmar TCLE arquivado

✅ OK:
- Comparativo cita concorrente com respeito (resto do slide 8)
- COI nao aplicavel (apresentador nao tem relacao comercial)
```
