---
name: rh-efetivar-onboarding
description: Depois que o formulário de Efetivação criou o colaborador no sistema de RH da Beauty Smile, confere o cadastro (cargo validado, vínculo, admissão, datas dos dias 30, 60 e 90, aviso de privacidade, marcos vencidos sem registro) e gera o rascunho do onboarding individual por lacuna — trilha padrão do cargo com datas absolutas, ajustes justificados linha a linha (fonte no cargo, fonte no CV ou "sem evidência", confiança) — e conduz a revisão da Amanda item por item até Revisado. Também propõe a trilha de um cargo que ainda não tem trilha. Use sempre que a Amanda ou o Fernando falarem de pessoa recém-contratada ou de onboarding, mesmo sem dizer "onboarding" — "efetivei a fulana", "confere o cadastro do fulano", "gera o onboarding da nova SDR", "monta os 30/60/90 do novo contratado", "passa o onboarding para revisado", "infere a trilha do editor de vídeo". Não cria pessoa (o formulário é a porta), não grava as datas 30/60/90, não avalia, não decide seguir ou não seguir, não cria PDI, não lê remuneração nem a ficha cadastral e não usa dado pessoal do CV.
---

# rh-efetivar-onboarding

Prepara o onboarding de quem acabou de entrar. O cadastro nasce no formulário de Efetivação; aqui "efetivar" é **conferir lendo**: nada é gravado em 👤 Colaboradores. O valor da skill é transformar a trilha padrão do cargo num plano datado e ajustado à pessoa, **sem** transformar silêncio do CV em defeito e **sem** tocar no que é dado pessoal. Quem decide cada ajuste é a Amanda.

## Antes de qualquer passo
Leia `../../CONTEXTO.md` e `../../references/00-nucleo.md` e faça o Passo 0. Esta skill lê **todos** os arquivos do núcleo, inclusive `20-redacao.md` (sem evidência ≠ lacuna e vocabulário PJ são o coração dela). Versão para o Log: `rh-efetivar-onboarding 0.1.0`.

## Modos
| Pedido | Modo |
|---|---|
| "gera o onboarding", "efetivei", "confere o cadastro" | **Gerar** (passos 1–10) |
| "passa para revisado", "aceito", "edito a 3", "recuso a 7" sobre um onboarding existente | **Revisar** (seção própria) |
| "infere a trilha", cargo com `Status da trilha` = Sem trilha | **Inferir trilha** dentro do Gerar (passo 4) |
| "cria o cadastro de X" | **R7** e nada criado. O resto do pedido segue |

## Gerar — passos
1. **Passo 0** (núcleo).
2. **Localizar o colaborador** em 👤 Colaboradores pelo nome (homônimo: pergunte a `Admissão`). Não existe → R7. `Status` ≠ Em experiência → avise e peça confirmação antes de seguir.
3. **Conferir o cadastro (só leitura)** e mostrar como lista ✔/⚠:
   - `Cargo`, `Vínculo` ou `Admissão` faltando → liste o que falta e pare.
   - Cargo com `Status` ≠ Validado → onboarding **bloqueado** (diga por quê).
   - Datas: calcule `Admissão + 29/59/89` e, se o cadastro trouxer `Dia 30/60/90`, confira. Divergiu → pare e avise. Mostre a conta.
   - `Aviso de privacidade entregue em` vazio → ⚠ "aviso de privacidade sem data: entregar e registrar antes de qualquer acesso".
   - **Marco já passado sem Avaliação** (cadastro retroativo) → "⚠ vencido sem registro" em destaque, um por marco, **sem sugerir decisão** nem o que "provavelmente" aconteceu. A decisão de um marco é da Amanda; a skill só aponta que o registro falta.
4. **Trilha.** Leia o corpo do cargo (Parte I, Parte II e 🧭 Trilha padrão). `Status da trilha` = Sem trilha (ou a seção 🧭 não existe) → **modo Inferir**: monte a trilha a partir da Parte II (rotina) e dos entregáveis/marcos da Parte I; `Trilha usada` = Inferida; confiança **no máximo média** em toda linha; avise "trilha inferida: revisão reforçada, linha a linha". Cultura, acessos e conformidade que o cargo não descreve ficam "a definir na trilha validada" — **não invente** itens (sobretudo de conformidade clínica).
5. **Fontes da pessoa.** Use `Fortes da seleção`, `Lacunas da seleção` e o CV anexado à conversa (ou colado). Aplique `10-dados.md` §C: do CV só experiência, formação, ferramentas, idiomas, resultados e datas de trabalho.
   **Sem CV:** o cruzamento não tem base, então não há ajuste individual nem linha "verificar" — só a trilha padrão datada, com "sem ajustes individuais — CV ausente". Mostre `Fortes da seleção` e `Lacunas da seleção` como estão, num bloco "Para a Amanda considerar", sem transformá-los em linha de ajuste, e ofereça: "se anexar o CV, gero os ajustes". Assim a Amanda vê a lacuna escrita sem que a skill decida por ela com evidência pela metade.
6. **Datas absolutas.** Marcos vêm do passo 3. Fases anteriores contam da `Admissão` em dias úteis, como a trilha define (D0, D1–D5, semanas 2–3, semana 4+). Marco (ou dia 40/85) que cai em sábado, domingo ou feriado nacional: mantenha a data da fórmula e sinalize "cai num sábado — a conversa precisa acontecer antes". Um marco "dia 45" na trilha vira "check-in do dia 30 (CLT: carrega a decisão do dia 45)", com aviso de que a trilha precisa de atualização.
7. **Itens fixos** (apresentações, buddy, rituais, acessos, treinamentos, termos, conformidade): copie **sem alteração**, só com a data. O buddy entra como função ("apoio do dia a dia, fora da decisão"), com nome "a definir pela Amanda" — nunca a Amanda/Coordenação, que avalia.
8. **Cruzamento** de cada competência técnica, responsabilidade e ferramenta da Parte I (e dos requisitos desejáveis que a trilha usa) com as fontes, pela tabela de `20-redacao.md`: coberta · lacuna (escrita em Lacunas da seleção) · lacuna provável (CV mostra claramente menos) · **sem evidência** → "Verificar na 1ª semana: <competência>. Como: <observação ou tarefa curta>". Competências comportamentais (proatividade, resiliência…) não viram linha "verificar": elas se observam no 1:1 e nos marcos. No máximo **5** linhas "verificar", as mais ligadas ao trabalho da 1ª semana. Liste numa linha só o que ficou coberto e com qual fonte.
9. **Ajustes:** no máximo **10** (mais que isso vira ruído e a revisão vira carimbo). Tipos: acelerar · reforçar · aprofundar. Nunca em item fixo. Cada linha: fonte no cargo · fonte no CV/seleção (ou "sem evidência") · confiança · decisão da Amanda (vazia). As linhas "verificar na 1ª semana" entram na mesma tabela com confiança baixa (ou "—"), mas não contam no teto de 10.
10. **Mostrar, confirmar, gravar, logar.** Mostre a saída (modelo abaixo), pergunte "Gravo como Rascunho IA em Onboardings?" e só grave com "sim". Depois, uma linha no Log.

## PJ (`Vínculo` = PJ)
O onboarding é **início de contrato de fornecedor**. Escreva em termos de entregável, prazo combinado, critério de aceite, contato do contratante, reunião de acompanhamento do contrato e marco 30/60/90 do contrato (no 90: seguir com o contrato · encerrar o contrato — decisão humana). Item da trilha com vocabulário de vínculo (ex.: horário, ponto, jornada, chefe): **copie como está**, com ⚠ "vocabulário de vínculo (PJ) — a Amanda decide", e **siga** — não reescreva, não esconda, não trave, não diga que foi aprovado. No seu próprio texto, não use essas palavras nem para comentar a regra.

## Saída antes de gravar (modelo)
```
**Conferência do cadastro — <Nome>**
✔/⚠ Cargo (<cargo>, Validado v<n>) · Vínculo · Admissão <data> · Dia 30 <data> · Dia 60 <data> · Dia 90 <data> (Admissão + 29/59/89)
⚠ <avisos: aviso de privacidade, marcos vencidos sem registro, [CONFIRMAR] do cargo>

**O que li:** cadastro (campos de trabalho), cargo <nome> v<n> (Partes I, II, 🧭 t<n>), Fortes/Lacunas da seleção, CV anexado (só experiência, formação, ferramentas e idiomas) | CV ausente.

**Trilha datada** (Data · Fase · Item · Origem: fixo/ajuste/marco)
...
**Ajustes** (# · Ajuste · Fonte no cargo · Fonte no CV/seleção · Confiança · Decisão da Amanda)
...
**Verificar na 1ª semana:** <competência — como verificar>
**Avisos:** trilha inferida | CV ausente | ⚠ PJ | [CONFIRMAR]
Lembrete: acrescente o nome à lista `Colaborador (nome informado)` do 1:1, se ainda não estiver.
**Gravo como Rascunho IA em Onboardings?**
```
Escreva datas como AAAA-MM-DD. Mantenha a saída enxuta (uma tabela de trilha, uma de ajustes, poucos avisos): a Amanda revisa isso linha a linha, e cada linha a mais é tempo dela. Sem CV, troque a tabela de ajustes pelo bloco "Para a Amanda considerar".

## O que grava (só depois do "sim")
🚀 Onboardings (cria): `Nome` = "Onboarding — <Nome>" · `Colaborador` · `Cargo` · `Status` = Rascunho IA · `Início` = `Admissão` · `Trilha usada` = Padrão | Inferida · `Versão da trilha usada` (ex.: "t1 · descritivo v3") · `Ajustes individuais` = "N ajustes: A alta, M média, B baixa; V para verificar; P sem decisão da Amanda".
**Corpo:** callout de Rascunho IA → (a) trilha datada → (b) tabela de ajustes → (c) "Verificar na 1ª semana" → marcos.
**Nunca:** `Buddy` (é da Amanda), escrita em Colaboradores, campo de pulso, datas 30/60/90 como propriedade.

Log (7 campos de `40-gravacao-e-log.md`): `Entrada` = "AAAA-MM-DD · rh-efetivar-onboarding · rascunho de onboarding · <Nome>" · `O que foi feito` = "rascunho de onboarding: N ajustes, V para verificar; trilha padrão|inferida; CV anexado|ausente".

## Revisar — linha a linha
O rascunho só vale depois que a Amanda decide **cada** linha. "Aceito tudo" é atalho seguro apenas para o que a skill tem confiança alta; linha baixa, "sem evidência" ou de trilha inferida precisa do olho dela.
1. Leia o onboarding (corpo e `Ajustes individuais`). Pedido de `Revisado` com linhas sem decisão → **não mude o status**: "faltam N linhas sem decisão: <números>". A contagem vem da tabela do corpo.
2. Registre uma decisão por linha: aceito · editado (com o novo texto; se ela não disser o texto, pergunte) · recusado.
3. "Aceito tudo" / "ok" → aplique só às linhas de confiança **alta**; liste as de confiança baixa, "sem evidência" ou trilha inferida e peça decisão individual.
4. Pedidos fora do onboarding individual:
   - Remover/alterar **item fixo** → recuse: "item fixo vem da trilha do cargo; quem muda é a trilha (no Cargo), não este onboarding."
   - Buddy = Amanda/Coordenação (nos evals, Bianca) → recuse: buddy não pode ser quem avalia; fica "a definir pela Amanda", e o campo `Buddy` ela preenche na interface com outra pessoa.
5. Todas as linhas decididas → mostre o resumo, pergunte e, com "sim": grave as decisões na coluna do corpo, atualize `Ajustes individuais` (P = 0), `Status` = Revisado e uma nova linha no Log: `O que foi feito` = "revisão: 12 linhas: 9 aceitas, 2 editadas (3, 7), 1 recusada (11)" (com os números reais), `Revisado por` = quem decidiu.
`Em andamento` e `Concluído` são da Amanda na interface; a skill nunca vai além de `Revisado`.

## Travas (resumo)
Sem dado pessoal do CV nem da ficha · sem evidência ≠ lacuna · item fixo intocável · buddy ≠ avaliadora · PJ pelo `20-redacao.md` · `[CONFIRMAR]` no cargo → "aguarda confirmação do cargo" no item afetado · nunca decide nem sugere seguir/não seguir · não lê Remuneração. Recusas usadas: R1, R3, R4, R7, R9.
