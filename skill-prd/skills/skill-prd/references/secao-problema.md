# Guia: Secao Problema & Contexto

> Como escrever a secao mais importante do PRD — se o problema nao esta claro, nada mais importa.

---

## Por que esta secao e critica

O problema e a fundacao do PRD. Se a definicao estiver errada, todas as decisoes subsequentes serao enviesadas. A secao deve responder: **"Por que isso merece atencao agora?"**

Inspiracao: Amazon Working Backwards — comece pelo cliente, nao pela tecnologia.

---

## Enquadramento do Problema (MITRE Problem Framing)

Antes de redigir a secao Problema, use thinking cuidadoso para responder estas 3 perguntas. Se a HMW nao ficar clara, o problema precisa de refinamento com o usuario.

| # | Pergunta | O que revela |
|---|----------|-------------|
| 1 | **Look Inward** (Olhar para Dentro): Quais sao nossas suposicoes e vieses sobre este problema? O que estamos assumindo sem evidencia? | Vieses ocultos, suposicoes nao validadas |
| 2 | **Look Outward** (Olhar para Fora): Quem experimenta o problema? Quem NAO experimenta? O que os diferencia? | Segmentacao real do problema, edge cases |
| 3 | **Reframe** (Reenquadrar): Como podemos reformular o problema como uma pergunta "How Might We" (HMW)? | Direcao de solucao sem prescrever implementacao |

### Como aplicar

1. Responda as 3 perguntas via thinking cuidadoso ANTES de redigir
2. Se a HMW nao ficar clara → o problema precisa de refinamento
3. A HMW deve aparecer no PRD como subsecao opcional dentro de Problema & Contexto
4. Formato da HMW: "Como podemos [verbo] para [persona] de modo que [resultado]?"

### Exemplos de HMW

| Problema | HMW |
|----------|-----|
| Parceiros conferem extrato manualmente por 3h/semana | Como podemos automatizar a conciliacao para parceiros de modo que reduzam o tempo de 3h para <30min? |
| Gestores nao tem visibilidade do status financeiro | Como podemos dar visibilidade financeira para gestores de modo que tomem decisoes sem depender de relatorios manuais? |

> Para exploracao completa, ver MITRE Problem Framing Canvas (Dean Peters).

---

## Estrutura Recomendada

```markdown
## Problema & Contexto

[2-5 frases descrevendo o problema na voz do usuario]

### Evidencias

- [Dado quantitativo, quote de usuario, ticket de suporte, observacao]
- [Segundo ponto de evidencia]
- [Terceiro ponto de evidencia]

### Contexto (opcional)

[Background necessario para audiencia que nao conhece o dominio]
```

---

## Como Escrever na Voz do Usuario

O problema deve ser descrito da perspectiva de quem sofre com ele, nao de quem vai resolve-lo.

**Bom (voz do usuario):**
> "Parceiros da clinica precisam conferir manualmente cada linha do extrato bancario com os pagamentos registrados no sistema. O processo leva 2-3 horas por semana e erros passam despercebidos ate o fechamento mensal."

**Ruim (voz do desenvolvedor):**
> "O sistema nao tem um modulo de conciliacao bancaria automatizada."

**Bom (especifico, mensuravel):**
> "40% dos tickets de suporte sao sobre discrepancias entre valores pagos e valores registrados. O time financeiro gasta 12h/mes resolvendo esses casos."

**Ruim (vago, sem escala):**
> "Os usuarios reclamam que o financeiro e confuso."

---

## Tipos de Evidencia (do mais forte ao mais fraco)

| Tipo | Exemplo | Forca |
|------|---------|-------|
| Dados quantitativos | "35% de churn nos primeiros 30 dias" | Alta |
| Quotes diretas de usuarios | "Perco 2h/dia nessa planilha" — Maria, gestora | Alta |
| Tickets de suporte | "47 tickets/mes sobre erro de pagamento" | Alta |
| Observacao direta | "Em 5 sessoes de shadowing, todos hesitaram no passo 3" | Media |
| Feedback qualitativo | "Usuarios mencionam dificuldade no onboarding" | Media |
| Intuicao de dominio | "Acreditamos que isso causa atrito" | Baixa |

**Regra**: inclua pelo menos 2 evidencias, sendo pelo menos 1 de forca alta.

---

## Anti-Pattern: Solucao Disfarçada de Problema

Este e o erro mais comum. O autor descreve o que quer construir, nao o problema real.

| Solucao disfarçada | Problema real |
|-------------------|---------------|
| "Precisamos de um dropdown de filtros" | "Usuarios nao conseguem encontrar registros especificos entre centenas de itens" |
| "Precisamos de um dashboard" | "Gestores nao tem visibilidade do status financeiro sem pedir relatorios manuais" |
| "Precisamos integrar com a API X" | "Dados ficam desatualizados porque sao importados manualmente 1x/semana" |
| "Precisamos de notificacoes push" | "Parceiros perdem prazos porque nao sabem quando ha pendencias" |

**Teste**: remova qualquer mencao a tecnologia ou solucao. O problema ainda faz sentido? Se nao, reescreva.

---

## Quando Incluir Subsecao de Contexto

Inclua a subsecao "Contexto" quando:

- A audiencia inclui pessoas novas no dominio
- O problema depende de conhecimento de um processo de negocio especifico
- Ha historico relevante (tentativas anteriores, decisoes passadas)
- O problema envolve regulamentacao ou compliance

Nao inclua quando:

- O time ja conhece o dominio profundamente
- O problema e auto-explicativo com as evidencias
- O PRD e nivel Lean (mantenha enxuto)

---

## Checklist de Validacao

- [ ] O problema esta na voz do usuario, nao do desenvolvedor?
- [ ] Ha pelo menos 2 evidencias concretas?
- [ ] Nenhuma solucao especifica e mencionada na definicao do problema?
- [ ] Uma pessoa de fora do time entenderia o problema?
- [ ] O problema justifica investimento agora (urgencia/impacto)?
- [ ] Se ha subsecao de Contexto, ela e necessaria para a audiencia?
- [ ] MITRE Problem Framing aplicado (3 perguntas respondidas via thinking cuidadoso)?
- [ ] HMW (How Might We) formulada e coerente com o problema? (Standard+)
