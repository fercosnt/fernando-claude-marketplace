# Fases, prazos e donos — resumo operacional

A fonte é `shared/conteudo.md` do contexto (parâmetros editáveis pelo coordenador de criação). Este
arquivo é o resumo do que a skill precisa na hora de montar as fases. Se divergirem, o `conteudo.md`
manda.

## Fases por formato

| Formato | Fases, em ordem | `Prazo` da fase a partir da `Data planejada` (D0) |
|---|---|---|
| carrossel · story · foto · texto · artigo · newsletter · convite · impresso | Roteiro · Arte/Edição · Legenda · Aprovação · Postagem | D-7 · D-4 · D-2 · D-1 · D0 |
| **vídeo** (reels · vídeo curto · short · vídeo longo/YouTube · institucional · TikTok) | Roteiro · **Gravação** · Arte/Edição · Legenda · Aprovação · Postagem | D-10 · D-7 · D-4 · D-2 · D-1 · D0 |

- Prazo em sábado/domingo recua para a **sexta anterior**; prazo em **feriado** recua para o dia
  útil anterior. O script `scripts/escalonar_prazos.py --feriados 2026-10-12` faz isso; use-o em vez
  de contar de cabeça — dois prazos errados numa pauta de 12 peças é o
  bastante para o time parar de confiar.
- A **mãe** não tem `Prazo`; tem `Data planejada` e `Prazo interno` = D-1 (pronta e aprovada).
- Peça de arte = **6 páginas** (mãe + 5). Peça de vídeo = **7 páginas** (mãe + 6).

## Dono padrão por fase (proposta; a pessoa confirma)

| Fase | Área | Papel (o nome vem do banco 👥 Time / da fixture) |
|---|---|---|
| Roteiro | Social Media (ou Produto, quando o tema é lançamento) | social media / comunicação e produto |
| Gravação | Audiovisual | produtora de mídia |
| Arte/Edição | Design (arte) · Audiovisual (vídeo) | designer · produtora de mídia |
| Legenda | Social Media | social media |
| Aprovação | Criação · **clínica → LA&HA** | coordenador de criação · dono clínico |
| Postagem | Social Media | social media |

Propor por **área e formato**, nunca por carga. Se a pessoa disser "a designer está no CSBD esse
mês, põe a produtora nas artes", aceite — é ela quem sabe.

## `Aprovação clínica` — quando sugerir `Aguardando`

É um select (Não requer · Aguardando · Aprovada · Reprovada). Sugira `Aguardando` quando `Pilar =
Educativo/Clínico` · `Linha/Produto` é protocolo (GLP1TIGHT, Melasma, ATPReboost, qualquer protocolo
com indicação/resultado) · o tema fala de resultado, indicação, contraindicação ou paciente. `Não
requer` quando é claramente institucional, bastidores ou promocional sem claim. Em dúvida, perguntar.
Peça clínica: a fase Aprovação vai para o dono clínico; a aprovação acontece no grupo de WhatsApp e
quem aprova muda o select para `Aprovada` — a automação carimba `Aprovação clínica em`. A skill
nunca grava `Aprovada`: isso é ato de quem aprova.

## Exemplo — 1 carrossel + 1 reels, Data planejada 19/10/2026 (segunda)

| Peça | Fase | Prazo | Dono proposto (papel) |
|---|---|---|---|
| Carrossel · resultados 90 dias GLP1TIGHT (Instagram, Educativo/Clínico, aprovação clínica ✓) | Roteiro | 12/10 | social media |
| | Arte/Edição | 15/10 | designer |
| | Legenda | 16/10 (recuou do sáb 17) | social media |
| | Aprovação | 16/10 (recuou do dom 18) | dono clínico (LA&HA) |
| | Postagem | 19/10 | social media |
| Reels · bastidores do stand no CSBD (Instagram, Bastidores, aprovação clínica ✗) | Roteiro | 09/10 | social media |
| | Gravação | 12/10 | produtora de mídia |
| | Arte/Edição | 15/10 | produtora de mídia |
| | Legenda | 16/10 | social media |
| | Aprovação | 16/10 | coordenador de criação |
| | Postagem | 19/10 | social media |

Total: 2 mães + 11 fases = 13 páginas.
