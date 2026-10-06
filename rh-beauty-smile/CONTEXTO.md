# Contexto do sistema de RH

Este plugin não carrega IDs, URLs nem nomes de colaboradores: a lógica é pública, os dados ficam no Notion da clínica.

- **Onde está o sistema:** teamspace privado **"RH Beauty Smile"** no Notion. A página de entrada se chama **"Central do RH"**. Busque essa página pelo nome dentro do teamspace, abra e siga os links até os bancos. Se não achar um banco pela Central, busque pelo nome exato dentro do mesmo teamspace. Não achou a Central ou o teamspace → pare e diga que o conector do Notion não está enxergando o "RH Beauty Smile" (conta errada ou sem acesso); não invente ID.
- **Bancos (nomes exatos):** 💼 Cargos · 👤 Colaboradores · 🔒 Remuneração · 🚀 Onboardings · 💬 1:1 · 📊 Avaliações · 🌱 PDI · ⚠️ Ocorrências · 🤖 Log do RH.
- **Quem conversa:** só a Amanda (Coordenadora, decide) ou o Fernando (CEO, aprova) — papéis do sistema. Qualquer outra pessoa → R1.
- **Condição de uso:** dentro da organização Claude Team da clínica, com o conector do Notion logado como a própria pessoa.
- **Modo fixture (evals):** se o pedido indicar arquivos como "resultado das consultas", use `contexto-simulado.json` no lugar deste arquivo e não toque no Notion real (ver `references/40-gravacao-e-log.md`).
