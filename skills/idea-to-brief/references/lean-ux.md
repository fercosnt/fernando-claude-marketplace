# Lean UX Canvas (Elementos Criticos)

Baseado em Jeff Gothelf, Lean UX Canvas v2. Versao focada nos elementos mais relevantes para pre-PRD: identificar suposicoes criticas e como valida-las.

## Quando usar

Na Fase 4.3 do idea-to-brief, apos MITRE e OST. O objetivo e expor as suposicoes que podem matar a ideia e definir o menor experimento para valida-las.

## Boxes Relevantes (4 de 8)

O canvas completo tem 8 boxes. Para idea-to-brief, focamos em 4:

### Box 1: Problema de Negocio

**Pergunta**: O que mudou no mundo que criou esse problema/oportunidade?

Como preencher:
- Use dados da pesquisa de mercado (sinais de timing)
- Conecte ao MITRE canvas (reformulacao do problema)
- Foque em mudancas recentes: nova tecnologia, regulacao, comportamento, concorrente

### Box 5: Solucoes

**Pergunta**: Quais solucoes possiveis atendem os outcomes de usuario e negocio?

Como preencher:
- Traga as top 3 solucoes do OST
- Cada solucao deve conectar um outcome de negocio a um outcome de usuario
- NAO escolha apenas 1 solucao nesta fase — diversidade importa

### Box 6: Hipoteses

**Pergunta**: Quais suposicoes estamos fazendo que, se estiverem erradas, matam a ideia?

Template de hipotese:
> "Acreditamos que [outcome de negocio] sera alcancado se [tipo de usuario] obter [beneficio] com [solucao/feature]."

Para cada hipotese, classificar o tipo de risco:
- **Valor**: Usuarios querem isso? (demanda)
- **Usabilidade**: Usuarios conseguem usar? (UX)
- **Viabilidade**: Conseguimos construir? (tech)
- **Feasibilidade**: O negocio suporta? (business model)

Gerar pelo menos 3 hipoteses, uma de cada tipo de risco se possivel.

### Box 7: O que aprender primeiro

**Pergunta**: Qual e a suposicao mais arriscada? A que, se errada, invalida tudo?

Como preencher:
1. Ranquear hipoteses por risco (impacto se estiver errada x incerteza)
2. A hipotese com maior risco e a que devemos testar primeiro
3. Definir o **menor trabalho para aprender**: o experimento mais barato e rapido

Tipos de experimento (do mais leve ao mais pesado):
1. **Desk research** — Ja feito na Fase 3 (verificar se responde a hipotese)
2. **Entrevista** — 5 conversas com usuarios potenciais (Mom Test)
3. **Landing page** — Pagina com CTA para medir interesse
4. **Concierge** — Executar o servico manualmente para 1-3 clientes
5. **Prototipo** — Mockup interativo para teste de usabilidade
6. **MVP** — Versao minima funcional para teste real

## Anti-patterns a evitar

- **Comecar com solucao**: "Queremos construir X" sem definir o problema
- **So 1 hipotese**: Se so tem 1, voce nao pensou o suficiente
- **Hipotese nao falsificavel**: "Usuarios vao gostar" nao e testavel
- **Pular experimentos**: Ir direto de hipotese para construcao
- **Confundir Box 2 com Box 4**: Outcomes de negocio (metricas) vs outcomes de usuario (motivacoes/empatia)

## Formato de output para o brief

```markdown
## 6. Suposicoes Criticas (Lean UX)

### Hipoteses

| # | Hipotese | Risco | Tipo |
|---|----------|-------|------|
| H1 | "Acreditamos que [outcome] sera alcancado se [usuario] obter [beneficio] com [solucao]" | [Alto/Medio/Baixo] | [Valor/Usabilidade/Viabilidade/Feasibilidade] |
| H2 | ... | | |
| H3 | ... | | |

### O que aprender primeiro

**Suposicao mais arriscada**: H[N] — [resumo]
**Justificativa**: [por que esta e a mais critica]

### Menor trabalho para aprender

| Experimento | Tipo | Esforco | O que valida |
|-------------|------|---------|-------------|
| [Experimento 1] | [tipo] | [tempo] | [qual hipotese] |
| [Experimento 2] | [tipo] | [tempo] | [qual hipotese] |
```
