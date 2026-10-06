# 40 · Gravação e Log: confirmar, gravar como rascunho, uma linha no Log

| Regra | Como |
|---|---|
| Confirmação | Toda gravação é precedida da **saída** da skill (o que vai para qual banco e propriedade) e de uma pergunta explícita. Sem "sim" da Amanda ou do Fernando, não grava. Na revisão linha a linha, "ok" solto não vale para linhas não vistas |
| Rascunho | Onboardings e Avaliações: `Status = Rascunho IA`. 1:1 e PDI: o rascunho fica no chat; a Amanda confirma na conversa **antes** de gravar (1:1: `Situação` = Válido; PDI: `Status` = Planejada, só das ações confirmadas), porque esses bancos não têm estado de rascunho |
| Transições da skill | Só Onboardings `Rascunho IA → Revisado` (todas as linhas decididas). O resto (`Em andamento`, `Concluído`, decisão, aprovação, liberação) é ato humano na interface |
| Falha | Pré-voo falhou → nada parcial: rascunho em texto e "não gravei; sem Log" (R9). Registro gravado e Log falhou: diga, tente uma vez e entregue o texto da linha para a Amanda colar |
| Escrita em Colaboradores | Nenhuma skill escreve em 👤 Colaboradores. Cadastro nasce do formulário de Efetivação |

## Modo fixture (evals e treino)
Quando o pedido diz "use os arquivos X como resultado das consultas; não consulte o Notion; não grave":
- Trate os arquivos como o retorno do Notion e `contexto-simulado.json` como o `CONTEXTO.md`.
- Não chame nenhuma ferramenta do Notion, de e-mail ou de mensagem.
- No fim, descreva **campo a campo** o que gravaria (banco, propriedade = valor; corpo da página em blocos), **inclusive a linha do Log** com os 7 campos.
- Se um dado de fixture traz data de fórmula preenchida (ex.: `Dia 30`), use-a e confira contra `Admissão + 29`.

## Linha do Log do RH
Uma por gravação. Só cria; nunca edita nem apaga.

| Propriedade | Preenchimento |
|---|---|
| `Entrada` (título) | `AAAA-MM-DD · <skill> · <operação> · <colaborador ou cargo, ou "—">` |
| `Data` | data e hora da gravação |
| `Origem` | sempre `Skill` |
| `Skill` | nome e versão (ex.: `rh-efetivar-onboarding 0.1.0`) |
| `Registro afetado` | URL da página criada ou alterada (no modo fixture: "URL da página criada") |
| `O que foi feito` | texto curto (≤ 200 caracteres), **sem conteúdo**: contagens e tipo de operação, ex.: "rascunho de onboarding: 8 ajustes, 2 para verificar; trilha padrão; CV anexado" |
| `Revisado por` | quem confirmou na conversa (Amanda ou Fernando; nos evals, o nome fictício que respondeu) |

O Log **não contém** dado proibido, trecho de transcrição, CV ou autoavaliação, nota nem valor, nem nome de competência pessoal. Consulta sem gravação não gera linha, exceto a leitura de Remuneração pelo `rh-historico`.
