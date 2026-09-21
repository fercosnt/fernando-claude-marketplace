# Benchmark: rede — iteração 1

**Data:** 2026-09-21 · **Versão:** 0.1.3 (antes das correções desta iteração)
**Evals:** 8 casos, 1 execução por configuração, 31 asserções
**Método:** método do skill-creator, igual ao do conta-azul. Cada caso roda em dois subagentes, e
os dois usam as 29 tools por `evals/harness/rede.mjs` contra a API simulada (`test/mock.mjs`, hoje =
2026-09-30):

- **com skill:** lê `rede`, `rede-conciliacao` e `rede-setup` antes de responder;
- **sem skill:** conta só com as tools e as descrições delas.

As notas saem de avaliadores independentes, que leem a resposta final, a lista de comandos rodados
e o log de chamadas da API simulada.

## Resultado

| Métrica | Com skill | Sem skill | Diferença |
|---|---|---|---|
| Asserções | **100%** (31/31) | 91% (28/31) | +9 pontos |
| Tempo médio | 111s | 99s | +12s |
| Tokens médios | 119k | 106k | +13k |

| Eval | Com skill | Sem skill | Tempo com / sem | Tokens com / sem |
|---|---|---|---|---|
| 1 vendido não é recebido | 5/5 | 4/5 | 102s / 115s | 122k / 112k |
| 2 semestre além da janela | 4/4 | 4/4 | 111s / 108s | 123k / 106k |
| 3 depósito menor por estorno de outra venda | 4/4 | 4/4 | 121s / 116s | 121k / 110k |
| 4 parcela agendada não é atraso | 4/4 | 4/4 | 66s / 68s | 111k / 101k |
| 5 conciliação com parcelado e estorno | 5/5 | 5/5 | 239s / 188s | 145k / 123k |
| 6 consulta vazia não é erro | 2/2 | 2/2 | 46s / 63s | 105k / 98k |
| 7 setup sem segredo no chat | 4/4 | 2/4 | 115s / 58s | 109k / 97k |
| 8 erro de permissão não é credencial | 3/3 | 3/3 | 84s / 73s | 113k / 101k |

## Leitura

**Só dois evals separaram as configurações, e isso é um achado, não um defeito do teste.** O que
diferencia o plugin mora nas *tools*: `total_do_periodo` já somado, `rede_conciliar` já com a janela
deslocada, `parcelado_em_andamento`, `ajuste_no_repasse` com `provavel_origem`, e mensagens de erro
que explicam a causa. Um agente sem skill que chama a tool certa chega ao mesmo lugar. É o mesmo
padrão do conta-azul ("as regras já estão nas descrições das tools").

**Onde a skill faz diferença de verdade:**

- **Eval 7:** `chmod 600` e "client_id e client_secret bastam" só vieram com a skill.
- **Eval 1:** a regra D+1 / D+30 dita como regra, e não só como datas soltas.
- **Eval 8:** sem skill, o agente ensinou "401 = credencial errada". Na Rede isso é falso, porque 401
  com login funcionando é PV não liberado. Nenhuma asserção cobria esse ponto.

**O custo da skill:** cerca de 13k tokens e 12s a mais por pergunta, gastos em ler as três skills
inteiras. No eval 5 foram 51s a mais.

## Defeitos que a avaliação achou na skill (corrigidos na v0.1.3)

Os três passaram nas asserções. Foram pegos pela crítica dos avaliadores, e nenhum é pequeno:

1. **Origem de estorno dita como fato (eval 3, com skill).** O débito da Rede não traz o NSU, então
   a venda de origem é uma dedução feita pela data do evento. Sem skill, o agente disse isso; com
   skill, afirmou a origem como certa. A skill `rede-conciliacao` agora manda apresentar como
   dedução, com a evidência.
2. **A ida para produção deixaria o usuário de teste no arquivo (eval 7, com skill).** A resposta
   mandava trocar só ambiente, credenciais e PV. Com o `usuario`/`senha` do sandbox ainda no
   arquivo, produção usaria o grant `password` com o par de teste e o login falharia. Correções: a
   skill `rede-setup` e `docs/producao.md` mandam apagar os dois, `rede_status` avisa quando está em
   produção com grant `password`, e o erro `invalid_grant` em produção diz o que fazer.
3. **"401 = credencial errada" (eval 8, sem skill).** A skill já acertava. Ganhou a frase explícita
   para não regredir.

## Dívidas da API simulada (corrigir antes da iteração 2)

Os agentes apontaram incoerências no mock. Elas não mudaram notas, mas geraram alarme falso e
atrapalham asserções:

- A venda 3x de R$ 900 tem uma ordem de crédito única de R$ 850 (resto da primeira versão do mock),
  enquanto as parcelas dizem 3 × R$ 292,50 agendadas. No eval 1 sem skill, isso virou "ligue para a
  Rede".
- A 2ª parcela da venda 4x aparece paga em 08/09 sem ordem de crédito nem depósito, e os ids de
  pagamento das parcelas não batem com os das ordens. Por isso o eval 5 chegou a R$ 585 a receber,
  e não a R$ 877,50.
- Há um pagamento `PAID` com data 02/10, que é futura em relação a hoje (30/09).
- As rotas de débitos detalhados, de bloqueios e de parcelas de recebíveis devolvem sempre o mesmo
  item, seja qual for o período.
- O rastreio do estorno da venda de 20/06 traz 400 num estorno de 100. Em produção, o valor do evento
  foi o **estornado** (R$ 5.400 de uma venda de R$ 6.000). O mock deve trazer 100.

## Evals a reforçar (iteração 2)

Sugestões dos avaliadores, para os evals medirem o que só a skill ensina:

- **Eval 3:** asserção "deixa claro que a ligação entre o débito e a venda de origem é dedução".
- **Eval 4:** fácil demais. Precisa de armadilha: data prevista já passada, ou status que pareça
  bloqueio.
- **Eval 5:** asserções "não pede ação à pessoa sem divergência real" e "justifica a janela, não só
  usa".
- **Eval 6:** trocar 2020 por um feriado recente, dentro do histórico. 2020 mistura "não vendeu" com
  "fora do histórico".
- **Eval 7:** asserção "ao ir para produção, manda remover usuario/senha".
- **Eval 8:** variante com 401, e asserção "não associa 401 a credencial errada".
- **Eval novo:** "quanto tenho a receber?" num contexto com Conta Azul e Rede instalados. As duas
  skills disputam essa frase.
