# MITRE Problem Framing Canvas (Condensado)

Baseado no MITRE Innovation Toolkit v3. Versao adaptada para preenchimento automatico com validacao do usuario.

## Quando usar

Na Fase 4.1 do idea-to-brief, apos receber resultados da pesquisa paralela. O objetivo e garantir que estamos resolvendo o problema certo antes de pensar em solucoes.

## As 3 Fases

### Fase 1: Look Inward

Examinar nossas proprias suposicoes e vieses antes de olhar para fora.

| Pergunta | Como preencher |
|----------|---------------|
| **Qual e o problema?** | Descrever sintomas observados, nao solucoes. Use dados da pesquisa de mercado. |
| **Por que nao foi resolvido?** | Categorizar: (1) Novo — ninguem tentou, (2) Dificil — tentaram e falharam, (3) Baixa prioridade — nao vale o esforco percebido, (4) Falta de recurso — vale mas nao ha capacidade, (5) Inequidade sistemica — afeta quem nao tem voz. |
| **Como somos parte do problema?** | Listar suposicoes que estamos fazendo. Que vieses temos? Que informacao nos falta? Estamos confundindo "eu quero isso" com "o mercado precisa disso"? |

### Fase 2: Look Outward

Entender quem sofre, quando, onde e as consequencias.

| Pergunta | Como preencher |
|----------|---------------|
| **Quem sofre com o problema? Quando e onde?** | Persona primaria + contexto. Use dados da pesquisa de concorrentes (workarounds = dor real). |
| **Quem mais tem? Quem NAO tem?** | Expandir alem da persona primaria. Quem nao sofre? Por que? Isso revela algo sobre a causa raiz? |
| **Quem foi excluido da conversa?** | Stakeholders marginalizados, edge cases, usuarios que nao conseguem articular a dor. Principio equity-driven. |
| **Quem se beneficia quando o problema existe?** | Status quo beneficia alguem? Concorrentes? Intermediarios? Resistencia a mudanca? |
| **Quem se beneficia quando o problema NAO existe?** | Quem ganha com a solucao? Sao os mesmos que sofrem? |

### Fase 3: Reframe

Reformular o problema incorporando insights das fases anteriores.

1. **Reformulacao do problema**: Escrever uma frase que capture a essencia do problema real (nao a solucao desejada). Deve ser diferente da descricao original se Look Inward/Outward revelaram algo novo.

2. **How Might We (HMW)**: Converter o problema em pergunta acionavel:
   > "Como podemos [acao que aborda o problema] para [objetivo/condicao desejada]?"

   Regras para bom HMW:
   - Nao muito amplo ("Como podemos melhorar a saude?")
   - Nao muito estreito ("Como podemos adicionar um botao de exportar?")
   - Nao contem solucao embutida ("Como podemos criar um app?")
   - Foca no problema, nao na tecnologia

## Anti-patterns a evitar

- **Pular Look Inward**: Ir direto para "quem sofre" sem examinar proprias suposicoes
- **Ignorar "quem se beneficia"**: Status quo sempre beneficia alguem — entender resistencia
- **Problem statement generico**: "Melhorar a experiencia" nao e um problema, e um desejo
- **HMW muito estreito**: Se o HMW ja contem a solucao, nao e um bom HMW
- **Confundir sintoma com causa**: "Usuarios reclamam do tempo de carregamento" (sintoma) vs "Arquitetura nao escala para volume atual" (causa)

## Formato de output para o brief

```markdown
## 4. Enquadramento do Problema (MITRE Problem Framing)

### Look Inward

| Pergunta | Resposta |
|----------|----------|
| **Qual e o problema?** | [sintomas observados com dados] |
| **Por que nao foi resolvido?** | [categoria + explicacao] |
| **Como somos parte do problema?** | [suposicoes e vieses identificados] |

### Look Outward

| Pergunta | Resposta |
|----------|----------|
| **Quem sofre com o problema?** | [persona + contexto + consequencias] |
| **Quem mais tem? Quem NAO tem?** | [expansao + insight] |
| **Quem foi excluido da conversa?** | [vozes marginalizadas] |
| **Quem se beneficia quando o problema existe?** | [beneficiarios do status quo] |

### Reframe

**Reformulacao do problema:**
> [frase que captura o problema real]

**How Might We:**
> Como podemos [acao] para [objetivo]?
```
