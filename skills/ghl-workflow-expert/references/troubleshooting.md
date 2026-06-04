# Troubleshooting e Debug Avancado — GHL Workflows

## Indice
1. [Ferramentas de Debug](#ferramentas-de-debug)
2. [Arvore de Diagnostico](#arvore-de-diagnostico)
3. [Erros Comuns e Solucoes](#erros-comuns-e-solucoes)
4. [Race Conditions](#race-conditions)
5. [Problemas de Integracao](#problemas-de-integracao)
6. [Checklist de Debug](#checklist-de-debug)

---

## Ferramentas de Debug

### Execution Logs

O principal instrumento de debug. Acesso: Workflow → Execution History.

| Feature | Descricao |
|---------|-----------|
| Error highlighting | Erros destacados visualmente no campo Status |
| View Details | Link clicavel para detalhes de cada acao |
| Go To Action | Navega direto ao step no builder |
| Contact History | Historico completo do contato no workflow |
| Highlight Contact Path | Visualiza rota exata que o contato seguiu |
| Paginacao | 10/25/50 rows por pagina |
| Date range | Ate 30 dias, formato MMM-DD |

**Status types**:
- Workflow Completed — contato passou por todo o fluxo
- Removed by Workflow Action — removido por acao interna (Goal Event, Remove action)
- Removed by External Workflow Action — removido por outro workflow

### Trigger Stats (novo, abril 2026)

View embutida no trigger com metricas em tempo real:
- Contatos que tentaram entrar
- Matched vs unmatched por filtro
- Detalhes por contato individual
- Top razoes de nao-enrollment
- Busca por contato especifico

### Test com Contato Real

O teste interno do GHL nao e 100% confiavel. Sempre validar com contato real em ambiente de producao. Usar contatos diferentes para cada teste (mesmo contato pode ter cache/estado residual).

---

## Arvore de Diagnostico

### Workflow NAO dispara

```
1. Workflow esta publicado? (Draft nao executa)
   └─ NAO → Publicar

2. Trigger correto para o evento?
   └─ Ex: Form Submitted vs Contact Created sao triggers diferentes

3. Filtros do trigger bloqueando?
   └─ Verificar Trigger Stats → matched/unmatched
   └─ Filtro de tag/source/campo pode estar excluindo

4. Re-entry desabilitado + contato ja passou?
   └─ Verificar Execution Logs → contato ja aparece como Completed

5. Contact DND ativo?
   └─ DND bloqueia TODAS as comunicacoes

6. Time Window bloqueando?
   └─ Se fora do horario configurado, workflow aguarda proximo horario
   └─ NOTA: Time Window NAO afeta acoes administrativas (tags, fields)

7. Outro workflow removeu o contato?
   └─ Status "Removed by External Workflow Action" = outro workflow interferiu
```

### Workflow dispara mas ACAO falha

```
1. Race condition?
   └─ Verificar timestamps — se duas acoes no MESMO SEGUNDO = race condition
   └─ Solucao: Wait de 1 min entre acoes sequenciais criticas

2. Campo vazio no custom value?
   └─ {{contact.campo}} retorna vazio se campo nao preenchido
   └─ Solucao: Text Formatter com Default Value como fallback

3. Webhook falha?
   └─ Verificar: URL correta, auth valida, payload no formato esperado
   └─ Verificar: endpoint externo esta ativo e respondendo
   └─ Log mostra response code (200 = ok, 4xx = erro cliente, 5xx = erro servidor)

4. Email bounce?
   └─ Verificar sender reputation e configuracao de dominio (SPF/DKIM/DMARC)
   └─ Contato com email invalido → bounce

5. SMS nao entregue?
   └─ Verificar: numero valido, DND ativo, limite de envio atingido
   └─ Carrier filtering pode bloquear mensagens que parecem spam

6. Tag nao aplicou?
   └─ Race condition — log pode mostrar "sucesso" mas tag nao persistiu
   └─ Solucao: Wait de 1 min antes/depois de tag critica
```

### Workflow faz coisa ERRADA

```
1. If/Else avaliando errado?
   └─ Verificar: operador correto (is/is not/contains/starts with)
   └─ Verificar: case sensitivity (GHL e case-sensitive em comparacoes de texto)
   └─ Verificar: campo esta preenchido no momento da avaliacao

2. Contato no branch errado?
   └─ Timing: field update pode nao ter propagado quando If/Else executou
   └─ Solucao: Wait de 1 min antes do If/Else que depende de update recente

3. Mensagem duplicada?
   └─ Re-entry ON + sem Stop condition = contato recebe tudo de novo
   └─ Solucao: Configurar Stop on Response ou Goal Event

4. Timezone errado?
   └─ Contact Timezone vs Account Timezone
   └─ Contact sem timezone faz fallback para Account
   └─ Mudancas de timezone NAO afetam entradas ja ativas
```

---

## Erros Comuns e Solucoes

| # | Erro | Causa Raiz | Solucao |
|---|------|-----------|---------|
| 1 | Trigger nao dispara | Evento errado ou campos obrigatorios ausentes | Verificar tipo do trigger e todos os filtros |
| 2 | Race condition | Duas acoes executam no mesmo segundo | Wait de 1 min entre acoes sequenciais |
| 3 | Integracao falha | API key incorreta ou permissoes faltando | Verificar credentials em ambos os sistemas |
| 4 | Data mismatch | Field mapping errado entre sistemas | Auditoria de mapeamento + validacao na origem |
| 5 | Tag nao aplicou | Race condition mascarada | Verificar timestamps — mesmo segundo = race |
| 6 | Contato preso em Wait | Wait por evento que nunca acontece | Configurar timeout no Wait ou Goal Event |
| 7 | Loop infinito | Go To sem condicao de saida | Adicionar If/Else antes do Go To com limite |
| 8 | Premium overage | Excedeu execucoes do tier | Monitorar usage, otimizar premiums, upgrade tier |

---

## Race Conditions

Race conditions sao o problema mais insidioso em workflows GHL porque o log pode mostrar "sucesso" enquanto o resultado esta errado.

### Como identificar

- Duas acoes com **exatamente o mesmo timestamp** no Execution Log
- Tag/field que deveria estar atualizado mas nao esta
- If/Else que avalia valor "antigo" mesmo apos update

### Como prevenir

1. **Wait de 1 minuto** entre acoes que dependem uma da outra
2. **Nao confiar em updates instantaneos** de tags/fields
3. **Testar com timing real** (nao apenas preview)
4. **Se critico**: verificar campo com If/Else ANTES de usar

### Exemplo clasico

```
ERRADO:
  Update Field "status" = "qualificado"
  If/Else: status = "qualificado"?  ← Pode ler valor ANTIGO

CERTO:
  Update Field "status" = "qualificado"
  Wait: 1 minuto
  If/Else: status = "qualificado"?  ← Agora le valor atualizado
```

---

## Problemas de Integracao

### Webhook nao recebe dados

1. URL do webhook esta correta? (copiar novamente do GHL)
2. Metodo HTTP correto? (POST vs GET)
3. Auth headers corretos? (Bearer token, API key)
4. Payload no formato JSON valido?
5. Endpoint externo esta up? (testar com curl/Postman)
6. Firewall bloqueando? (whitelist IPs do GHL)

### Google Sheets nao atualiza

1. Conexao OAuth ativa? (pode expirar)
2. Sheet e tab corretos? (nome exato, case-sensitive)
3. Colunas mapeadas corretamente?
4. Sheet nao atingiu limite de linhas?

### Airtable com delay

Airtable triggers usam polling (~5 min), NAO webhook. Delay de ate 5 minutos e normal e esperado. Se precisa de tempo real, usar webhook do Airtable + Inbound Webhook do GHL.

---

## Checklist de Debug

Quando um workflow apresentar problema, seguir nesta ordem:

1. [ ] Verificar se workflow esta **publicado** (nao draft)
2. [ ] Verificar **Trigger Stats** — contato matched ou unmatched?
3. [ ] Verificar **Execution Logs** — contato entrou no workflow?
4. [ ] Verificar **timestamps** — ha acoes no mesmo segundo? (race condition)
5. [ ] Verificar **path do contato** — Highlight Contact Path no builder
6. [ ] Verificar **custom values** — campos vazios gerando erros?
7. [ ] Verificar **settings** — re-entry, stop on response, timezone, time window
8. [ ] Verificar **integracoes** — credentials validas, endpoints ativos
9. [ ] Testar com **contato diferente** (nao reusar mesmo contato de teste)
10. [ ] Se nada funcionar → consultar **NotebookLM** com descricao detalhada do problema
