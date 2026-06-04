# Advanced Workflow Builder — Guia Completo

Lancado no Level Up Summit (outubro 2025). Ativacao: Agency Settings > Labs > Sub Account > buscar "workflow" > habilitar "New Advanced Builder".

---

## Diferenciais vs Builder Padrao

| Feature | Builder Padrao | Advanced Builder |
|---------|---------------|-----------------|
| Layout | Arvore linear vertical | Canvas infinito com branches lado a lado |
| Navegacao | Scroll simples | Zoom, minimap, fit-to-screen |
| Visual | Monocromatico | Categorias com codigo de cores |
| Documentacao | Nenhuma | Sticky notes coloridos no canvas |
| Layout auto | Nenhum | Format Tree (auto-layout automatico) |
| Colaboracao | Nenhuma | Comments no canvas |
| Pause | So workflow inteiro | Pause por acao individual |
| Busca | Nenhuma | Find & Replace de custom values, tags, texto |

---

## Quando Usar o Advanced Builder

### Recomendado para:
- Workflows com **10+ steps** que precisam de visao panoramica
- **Consolidacao** de 2-4 workflows separados num unico canvas
- Workflows com **multiplos branches** paralelos
- Quando precisa **documentar** a logica com sticky notes
- Equipes que precisam **colaborar** no design do workflow

### NAO recomendado para:
- Workflows simples (3-5 steps lineares) — overhead desnecessario
- Workflows que precisam de **mais de 1 Goal Event** — limitacao mantida
- Historico de execucao critico que **nao pode ser perdido** na migracao

---

## Processo de Migracao

### ANTES de migrar (obrigatorio)

1. **DUPLICAR** o workflow original (Menu > Duplicate)
2. Renomear o duplicado como "[nome]-backup-[data]"
3. Anotar/exportar configuracoes criticas:
   - Triggers e filtros
   - Settings (re-entry, stop conditions, timezone)
   - Custom values usados
   - Tags criticas
4. Verificar que o backup esta funcional

### Migrar

1. Abrir o workflow original
2. Ativar Advanced Builder (se nao estiver ativo globalmente)
3. O GHL converte automaticamente

### DEPOIS de migrar

1. Verificar todos os steps e connections
2. Revisar triggers e filtros (podem precisar de re-configuracao)
3. Organizar visualmente com sticky notes
4. Usar Format Tree para auto-layout
5. Testar com contato real
6. Monitorar Execution Logs por 48h

### Limitacoes da migracao

- "Previously enrolled data may not fully migrate" — contatos ativos no workflow podem perder estado
- Historico de execucao pode ser perdido
- O canvas trata tudo como workflow unico — afeta scope de Goals e remove/add actions
- **NAO ha caminho de volta** (Advanced → Padrao nao e suportado)

---

## Features Exclusivas em Detalhe

### Sticky Notes

- Coloridos (multiplas cores disponiveis)
- Posicionaveis em qualquer lugar do canvas
- Usar para:
  - Documentar logica de negocio ("por que esse branch existe")
  - Separar visualmente processos diferentes no mesmo canvas
  - Anotar TODOs e melhorias futuras
  - Marcar areas que precisam de revisao

### Find & Replace (novo, abril 2026)

- Buscar custom values, tags, ou texto em qualquer parte do workflow
- Substituir em massa
- Ideal para:
  - Renomear tags em todo o workflow
  - Atualizar custom values quando campo muda de nome
  - Corrigir typos em mensagens

### Pause por Acao Individual

- No builder padrao, so da para pausar o workflow inteiro
- No Advanced, pausar acoes individuais enquanto o resto continua
- Util para debug isolado e manutencao sem parar todo o fluxo

### Format Tree (Auto-Layout)

- Reorganiza todo o workflow automaticamente
- Alinha branches, distribui espacamento
- Usar apos grandes editoracoes para limpar o visual

### Comments

- Adicionar comentarios em acoes especificas
- Util para revisao em equipe
- Diferente de sticky notes (que sao visuais no canvas)

---

## Estrategia de Consolidacao

O maior beneficio do Advanced Builder e consolidar workflows relacionados num unico canvas visual.

### Quando consolidar

- 2-4 workflows que compartilham o mesmo trigger ou contatos
- Workflows sequenciais (output de um e input de outro)
- Processos que a equipe precisa ver como um todo

### Como consolidar

1. Mapear todos os workflows envolvidos (triggers, actions, connections)
2. Identificar pontos de conexao (tags, fields, eventos)
3. Criar o workflow consolidado no Advanced Builder
4. Usar sticky notes coloridos para separar processos visualmente
5. Manter um unico Goal Event (limitacao do builder)
6. Testar cada "secao" individualmente
7. Testar o fluxo completo end-to-end

### Gotcha: Limitacao de 1 Goal

O Advanced Builder mantem a limitacao de 1 Goal Event por workflow. Ao consolidar:
- Escolher o Goal mais importante para o workflow como um todo
- Para outros pontos de "conclusao", usar If/Else + Remove from Workflow
- Planejar a estrategia de saida ANTES de consolidar

---

## Dicas de Produtividade

1. **Zoom out para visao macro** — use minimap para navegar rapidamente
2. **Sticky notes por cor** — convencionar cores (ex: amarelo=TODO, verde=OK, vermelho=bug)
3. **Format Tree regularmente** — canvas fica bagunçado com editoracoes frequentes
4. **Comments para code review** — antes de publicar, pedir revisao da equipe
5. **Pause individual para debug** — isolar o step problematico sem parar o workflow
