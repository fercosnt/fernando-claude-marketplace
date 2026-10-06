# 60 · Mapa dos bancos: o que cada skill lê e escreve

**L** = lê · **E** = escreve · **—** = não toca. `EO` = `rh-efetivar-onboarding` · `P1` = `rh-preparar-1a1` · `AV` = `rh-preparar-avaliacao` · `H` = `rh-historico`.

| Banco | EO | P1 | AV | H |
|---|---|---|---|---|
| 👤 Colaboradores | L: Nome, Cargo, Vínculo, Área, Unidade, Gestor direto / Contato contratante, Admissão, Status, Dia 30/60/90, Fortes/Lacunas da seleção, Aviso de privacidade entregue em. **Ignora** ficha cadastral (Data de nascimento, Idade, Estado civil, Endereço), CV (original), Parecer da seleção, E-mail, Telefone | L: Nome, Cargo, Vínculo, Status, Admissão, Dia 30/60/90. **Ignora** a ficha | L: como EO, mais `Decisão do dia 45 (CLT)`. **Ignora** a ficha | L: tudo **exceto** ficha, CV original, Parecer |
| 💼 Cargos | L: corpo (Parte I, Parte II, 🧭 Trilha padrão), Versão, Status, Status da trilha, Versão da trilha, Pendências [CONFIRMAR] | L: Parte I | L: Parte I, Critérios técnicos | L: Cargo, Versão |
| 🔒 Remuneração | — | — | — | L, só na visão de reajuste pedida |
| 🚀 Onboardings | **E** (cria; atualiza na revisão) | L: "Verificar na 1ª semana" | L: Status, Ajustes, "Verificar…" | L |
| 💬 1:1 | — | L: tudo exceto `Notas reservadas da Amanda`; **E** na página do 1:1 | L: notas, evidências, valores, planos, registro compartilhável, autoavaliação (comparação e pulso). Ignora `Notas reservadas` | L: tudo exceto `Notas reservadas` |
| 📊 Avaliações | L: existência e tipo | L: `Plano de ajuste` anterior | **L/E** | L (rascunho rotulado) |
| 🌱 PDI | — | L: Ação, Status, Prazo | **L/E** (modo D) | L |
| ⚠️ Ocorrências | — | — | — | L: só Data, Colaborador, Status, Documento formal (nunca `Fato observado`) |
| 🤖 Log do RH | **E** | **E** | **E** | **E** só se leu Remuneração |

Propriedades de 🚀 Onboardings: `Nome` (título) · `Colaborador` (relação, limite 1) · `Cargo` (relação, limite 1) · `Status` (Rascunho IA · Revisado · Em andamento · Concluído) · `Início` (data) · `Trilha usada` (Padrão · Inferida) · `Versão da trilha usada` (texto) · `Ajustes individuais` (texto, resumo) · `Buddy` (texto, **só a Amanda preenche**).
