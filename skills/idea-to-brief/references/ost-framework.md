# Opportunity Solution Tree (Condensado)

Baseado em Teresa Torres, Continuous Discovery Habits (2021). Versao adaptada para gerar abordagens do brief com avaliacao comparativa.

## Quando usar

Na Fase 4.2 do idea-to-brief, apos preencher o MITRE canvas. O objetivo e divergir antes de convergir — gerar opcoes genuinas, nao apenas validar a primeira ideia.

## Estrutura

```
Outcome Desejado (1)
├── Oportunidade 1
│   ├── Solucao A
│   ├── Solucao B
│   └── Solucao C
├── Oportunidade 2
│   ├── Solucao D
│   ├── Solucao E
│   └── Solucao F
└── Oportunidade 3
    ├── Solucao G
    ├── Solucao H
    └── Solucao I
```

## Como preencher

### 1. Outcome Desejado

Definir UM resultado mensuravel que queremos alcancar. Deve ser:
- Especifico (nao "melhorar a experiencia")
- Mensuravel (metrica ou indicador)
- Conectado ao negocio (nao apenas tecnico)

Exemplo: "Reduzir de 3 horas para 30 minutos o tempo de preparacao de briefs de produto"

### 2. Oportunidades (3)

Cada oportunidade e um problema ou necessidade do usuario. Regras:

- **Oportunidades NAO sao solucoes**: "Usuarios mobile nao conseguem acessar" (oportunidade) vs "Precisamos de um app mobile" (solucao disfarçada)
- **Use evidencia**: Dados da pesquisa, workarounds observados, gaps identificados
- **Diversifique**: As 3 oportunidades devem abordar aspectos diferentes do problema

Para cada oportunidade, documentar:
- Problema/necessidade do usuario
- Evidencia (de onde veio: pesquisa, entrevista, dados)
- Impacto potencial (Alto/Medio/Baixo)

### 3. Solucoes (3 por oportunidade)

Para cada oportunidade, gerar 3 solucoes possiveis. As solucoes alimentam as abordagens do brief.

Diversificar em:
- **Ambicao**: MVP minimo vs versao robusta vs visao ambiciosa
- **Plataforma**: Skill vs app vs automacao vs prompt
- **Abordagem**: Build vs buy vs adapt

### 4. Avaliacao

Pontuar cada solucao em 3 dimensoes (1-5):

| Criterio | 1 (Baixo) | 3 (Medio) | 5 (Alto) |
|----------|-----------|-----------|----------|
| **Feasibility** | Requer tech nova + equipe grande + meses | Stack conhecida + esforco moderado | Stack atual + rapido de implementar |
| **Impact** | Melhoria marginal para poucos | Melhoria significativa para publico medio | Transformador para publico grande |
| **Market Fit** | Sem demanda observada | Demanda implicita (workarounds) | Demanda explicita (pedidos, pesquisas) |

### 5. Selecao

As 3 melhores solucoes (maior score total) se tornam as 3 abordagens do brief. Se todas vierem da mesma oportunidade, forcar diversidade selecionando pelo menos 1 de outra.

## Anti-patterns a evitar

- **Oportunidades disfarçadas de solucoes**: "Precisamos de X" nao e oportunidade, e solucao
- **Pular divergencia**: Gerar apenas 1 solucao por oportunidade
- **Outcome vago**: "Ser melhor" nao e mensuravel
- **Vieses de confirmacao**: Pontuar alto a solucao que voce ja queria
- **Sem evidencia**: Oportunidades inventadas sem base na pesquisa

## Formato de output para o brief

```markdown
## 5. Oportunidades Mapeadas (OST)

### Outcome desejado
**Resultado mensuravel**: [metrica + alvo]

### Oportunidade 1: [Nome]
- **Problema/necessidade**: [descricao]
- **Evidencia**: [fonte]
- **Impacto potencial**: [Alto/Medio/Baixo]

### Oportunidade 2: [Nome]
...

### Oportunidade 3: [Nome]
...
```
