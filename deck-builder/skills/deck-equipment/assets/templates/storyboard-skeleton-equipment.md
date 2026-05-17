# Deck: {nome-deck}

## Meta
- Skill geradora: deck-equipment
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Equipamento: {E1.nome}
- Classe Anvisa: {II / III / IV}
- Registro Anvisa: {numero ou "🟡 a confirmar"}
- Framework principal: FAB + TCO 5 anos + Payback + Sensitivity 3 cenarios
- Modo: {padrao | comparativo}
- max_ctas: 1
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

{2-3 paragrafos sobre o arco narrativo:}
- abre com o problema clinico que o equipamento resolve (slide 2)
- mostra a tecnologia + demo procedural (slides 3-4)
- ancora 3 features-chave com FAB (slides 5-7)
- contextualiza vs alternativas com comparativo respeitoso (slide 8 ou 8a-c)
- prova com caso clinico (slide 9)
- fecha argumento financeiro com TCO + Payback + Sensitivity (slides 10-12)
- amarra compliance + treinamento + financiamento (13-15)
- termina com 1 CTA claro (17-18)

---

## Slide 1 — Capa
Tipo: capa
Action title: {headline assertivo — vende o desfecho, nao o produto. Ex: "LightWalker paga em 18 meses sem dobrar equipamento" NAO "Apresentacao Fotona LightWalker"}
Mensagem-chave: {Big Idea condensada em 1 frase}
Speaker notes: {Quem somos, quem e o cliente, qual o ask especifico desta apresentacao}
Visual: {hero shot do equipamento em contexto clinico, NAO catalogo}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 30s
Objecao esperada: —

## Slide 2 — Problema
Tipo: problema
Action title: {dor concreta da clinica em 1 frase. Ex: "Periodontite cronica resiste a SRP isolado em 40% dos casos"}
Mensagem-chave: {Statement do problema clinico/economico que justifica o equipamento}
Speaker notes: {2-3 paragrafos contextualizando o problema com numeros do segmento}
Visual: {clinico frustrado, paciente recorrente, ou grafico de incidencia}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 45s
Objecao esperada: "ja resolvemos com X" → preparar resposta no slide 3

## Slide 3 — Tecnologia / Mecanismo
Tipo: conceitual
Action title: {Como o equipamento resolve. Ex: "Er:YAG ablaciona tecido duro sem dano termico colateral"}
Mensagem-chave: {Mecanismo de acao em 1 frase tecnica}
Speaker notes: {Explicar o mecanismo com 1 figura conceitual + 1 evidencia cientifica}
Visual: {esquema do mecanismo — onda + tecido + efeito}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 60s
Objecao esperada: "ja tem outras tecnologias que fazem isso" → preparar slide 8

## Slide 4 — Demo procedural
Tipo: demo
Action title: {Frase ancora do que sera mostrado. Ex: "Em 90 segundos, gengivectomia completa quadrante 1"}
Mensagem-chave: {O que sera demonstrado e por que importa}
Speaker notes: {Video curto, foto sequencial, ou caso simulado — se imagem de paciente real, requer TCLE arquivado}
Visual: {still do procedimento ou frame chave do video}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 90-120s
Objecao esperada: —

## Slide 5 — FAB Feature 1
Tipo: conceitual
Action title: {Beneficio condensado. Ex: "Dual wavelength elimina necessidade de segundo equipamento"}
Mensagem-chave: {Feature → Advantage → Benefit em 1 paragrafo}
Speaker notes:
- **Feature:** {caracteristica tecnica objetiva}
- **Advantage:** {por que diferenciado vs alternativas}
- **Benefit:** {resultado clinico + impacto economico quantificavel}
Visual: {diagrama da feature em uso}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 60s
Objecao esperada: {se aplicavel}

## Slide 6 — FAB Feature 2
Tipo: conceitual
{mesma estrutura do slide 5 para a 2a feature-chave}

## Slide 7 — FAB Feature 3
Tipo: conceitual
{mesma estrutura do slide 5 para a 3a feature-chave}

## Slide 8 — Comparativo responsavel (modo `padrao`)
Tipo: comparativo
Action title: {Frase que contextualiza criterio. Ex: "LightWalker vs LightSheer: depende do mix de procedimentos"}
Mensagem-chave: {Posicionamento neutro com criterio de escolha}
Speaker notes:
- Cita concorrente pelo nome com respeito
- Lista 2-3 forcas reconhecidas da alternativa (com fonte)
- Lista 2-3 limites com fonte explicita (bula, paper, benchmark — NUNCA achismo)
- Posiciona nosso equipamento como superior em criterio especifico
- Fecha com criterio neutro de escolha
- VERIFICAR: nenhuma frase proibida (ver compliance-anvisa-equipment.md secao 5)
Visual: {tabela lado-a-lado neutra OU 2 equipamentos em contexto clinico equivalente}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 90s
Objecao esperada: "por que nao a marca X?" → este slide responde

### [Modo `comparativo` substitui slide 8 por 8a/8b/8c]

#### Slide 8a — Forcas das alternativas
Tipo: comparativo
Action title: {Frase neutra. Ex: "Cada marca tem forcas reconhecidas"}
Speaker notes:
- Tabela 3 colunas (1 por marca)
- 3 forcas reais por marca, com fonte explicita
- NUNCA inventar fraqueza para parecer balanceado

#### Slide 8b — Limites das alternativas
Tipo: comparativo
Action title: {Frase neutra. Ex: "E cada uma tem limites a considerar"}
Speaker notes:
- Tabela 3 colunas (1 por marca)
- 2 limites reais por marca, com fonte explicita
- "limite" e diferente de "defeito" — preferir contexto

#### Slide 8c — Criterio neutro de escolha
Tipo: comparativo
Action title: {Frase ancorada em criterio mensuravel. Ex: "A escolha depende do mix de casos da clinica"}
Speaker notes:
- 1 paragrafo articulando criterio de escolha
- NUNCA "vencedor por categoria" — devolve poder ao cliente
- Recomendacao implicita: "para o seu perfil, X tende a fazer mais sentido"

## Slide 9 — Caso clinico
Tipo: prova-social
Action title: {Resultado clinico concreto. Ex: "Caso real: periodontite cronica grau III resolvida em 3 sessoes"}
Mensagem-chave: {Resultado mensuravel + paciente real ou estudo de caso da literatura}
Speaker notes:
- Apresentar caso com antes/depois
- Se imagem de paciente real: TCLE arquivado (LGPD + CFM/CFO) — marcar 🟡 se nao confirmado
- Citar paper ou estudo se caso e da literatura
Visual: {antes/depois com bracket — se TCLE; OU figura de paper citado}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 90s
Objecao esperada: "isso e caso isolado?" → citar N de casos similares

## Slide 10 — TCO 5 anos
Tipo: financeiro
Action title: {Frase com numero condensado. Ex: "Custo total 5 anos: R$420k — 50% e consumo + manutencao"}
Mensagem-chave: {Tabela TCO 5 anos × 5 componentes}
Speaker notes:
- Aquisicao (Ano 1 ou distribuido se financiado)
- Consumiveis (custo por procedimento × volume anual)
- Manutencao (preventiva contratual + corretiva ~3-5% valor/ano)
- Treinamento (inicial Ano 1 + reciclagem Ano 3 e Ano 5)
- Software/atualizacao (licencas anuais)
- Total por ano + acumulado
Visual: tabela com header + 5 linhas + total + acumulado
Prompt de imagem: skip (slide financeiro, fora da whitelist D5)
Tempo estimado: 90s
Objecao esperada: "esta calculado de forma realista?" → mostrar premissas no apendice

## Slide 11 — Payback
Tipo: financeiro
Action title: {Frase com payback em meses. Ex: "Payback em 18 meses no cenario realista"}
Mensagem-chave: {Formula + payback no cenario realista}
Speaker notes:
- Formula: Margem por procedimento = Preco cobrado − Custo variavel − (Depreciacao + manutencao alocada)
- Procedimentos para payback = Investimento total / Margem por procedimento
- Tempo de payback = Procedimentos / (Procedimentos por mes × 12)
- Volume realista assumido (= E4 do usuario)
- Margem por procedimento detalhada
Visual: diagrama de fluxo da formula OU grafico de fluxo de caixa acumulado
Prompt de imagem: skip (slide financeiro)
Tempo estimado: 60s
Objecao esperada: "e se eu nao atingir o volume?" → o slide 12 responde

## Slide 12 — Sensitivity 3 cenarios
Tipo: financeiro
Action title: {Frase de defesa pessimista. Ex: "Mesmo no pessimista (10/mes), paga em 30 meses"}
Mensagem-chave: {Tabela 3 cenarios com defesa do pessimista}
Speaker notes:
- Tabela: Otimista / Realista / Pessimista
- Linhas: Volume/mes, Preco medio, Margem, Payback (meses), ROI 5 anos
- Otimista = realista × 1.5-2.0 em volume + preco no terco superior
- Realista = E4 do usuario
- Pessimista = realista × 0.5-0.7 + preco minimo defensivel
- **Pessimista DEVE pagar.** Senao, recomendar revisitar E2/E4.
- Frase de fechamento: "mesmo no pessimista, paga em N meses"
Visual: tabela 3 colunas × 5 linhas
Prompt de imagem: skip (financeiro)
Tempo estimado: 90s
Objecao esperada: "como sabemos se realista nao e otimista demais?" → mostrar bench regional no apendice

## Slide 13 — Treinamento + suporte tecnico
Tipo: conceitual
Action title: {Frase reduzindo friccao. Ex: "Treinamento incluso + suporte tecnico Brasil em 24h"}
Mensagem-chave: {Onboarding + suporte continuo}
Speaker notes:
- Curso inicial (carga horaria, lugar, instrutores)
- Habilitacao CFO/CFM se laser
- Reciclagens periodicas
- Suporte tecnico local (BR) + remoto
- SLA de atendimento
Visual: {time de treinamento ou foto curso}
Prompt de imagem: skip (conceitual mas operacional — opcional)
Tempo estimado: 45s
Objecao esperada: "e se quebrar?" → ja respondido

## Slide 14 — Compliance Anvisa
Tipo: disclaimer
Action title: {Statement de compliance. Ex: "Registro Anvisa Classe III XX-XX vigente; operador habilitado CFO/CFM"}
Mensagem-chave: {Compliance objetivo}
Speaker notes:
- Numero de registro Anvisa
- Classe declarada (II / III / IV)
- Se laser: Classe III + habilitacao CFO 35/2018
- Indicacoes dentro da bula (off-label marcado explicitamente se houver)
- COI declarado (se apresentador tem relacao comercial com marca)
- LGPD para dados de paciente se aplicavel
Visual: logo Anvisa + texto compliance
Prompt de imagem: skip (disclaimer)
Tempo estimado: 30s
Objecao esperada: —

## Slide 15 — Condicoes comerciais + financiamento
Tipo: financeiro
Action title: {Frase com condicao. Ex: "R$280k a vista ou R$320k em 36x; entrega em 60 dias"}
Mensagem-chave: {Condicoes objetivas}
Speaker notes:
- Preco a vista + parcelado
- Prazo de entrega
- Garantia + extensoes disponiveis
- Trade-in se aplicavel
Visual: tabela condicoes
Prompt de imagem: skip
Tempo estimado: 45s
Objecao esperada: "tem desconto?" → flexivel mas com piso

## Slide 16 — Apendice tecnico (opcional)
Tipo: apendice
Action title: Especificacoes tecnicas detalhadas
Mensagem-chave: detalhes para engenheiro/tecnico do hospital
Speaker notes: spec sheet completo
Prompt de imagem: skip

## Slide 17 — CTA
Tipo: CTA
Action title: {Ask especifico. Ex: "Proximo passo: visita demonstrativa em 7 dias com 3 pacientes selecionados"}
Mensagem-chave: {1 unico CTA}
Speaker notes:
- O que pedimos especificamente
- Quando (data/janela)
- Quem (decisores envolvidos)
Visual: minimalista, foco na frase
Prompt de imagem: skip (CTA)
Tempo estimado: 30s
Objecao esperada: "preciso pensar" → preparar follow-up

## Slide 18 — Proximos passos (agradecimento)
Tipo: agradecimento
Action title: Obrigado + canais de contato
Mensagem-chave: agradecimento + dados de contato
Speaker notes: dados objetivos
Visual: minimalista
Prompt de imagem: skip

---

## Storyboard de Imagens (handoff pra deck-image-prompts)

Lista para `deck-image-prompts` preencher (whitelist D5):
- Slide 1 (capa): {brief}
- Slide 2 (problema): {brief}
- Slide 3 (conceitual): {brief}
- Slide 4 (demo): {brief}
- Slide 5/6/7 (FAB conceitual): {opcional — apenas se diagrama tecnico claro}
- Slide 8 ou 8a/8b/8c (comparativo): {brief}
- Slide 9 (prova-social): {brief — se TCLE, foto real; senao stock/ilustracao}

Skip por default: 10, 11, 12 (financeiro), 14 (disclaimer), 15 (financeiro), 17 (CTA), 18 (agradecimento).
Override `--include-dados` se o grafico de payback ou sensitivity for chave visual.

---

## Checklist de Revisao (handoff pra deck-reviewer)

- [ ] Action titles em TODOS os slides (nao titulos descritivos)
- [ ] 1 ideia por slide
- [ ] Horizontal logic test: ler so action titles em sequencia conta a historia?
- [ ] Hook do slide 1 testado contra /copy
- [ ] CTA unico (max_ctas: 1)
- [ ] FAB completo (3 features × F-A-B)
- [ ] TCO 5 anos com 5 componentes minimos
- [ ] Payback formula + numero realista
- [ ] Sensitivity 3 cenarios com pessimista pagando
- [ ] Comparativo respeitoso (sem frase proibida do anti-badmouth)
- [ ] Compliance Anvisa Classe + registro
- [ ] Habilitacao CFO/CFM se laser
- [ ] COI declarado
- [ ] TCLE arquivado se imagem de paciente real

---

## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes (resolver antes de apresentar):
- {Equipamento mencionado SEM numero de registro Anvisa correspondente?}
- {Claim fora de bula sem disclaimer "off-label"?}
- {Comparativo com badmouth — frases proibidas detectadas?}

🟡 Verificar antes:
- {Classe III declarada explicitamente para laser?}
- {Conflito de interesse (distribuidor/representante/comissao) declarado?}
- {Imagens de paciente real com TCLE arquivado?}
- {Numero registro Anvisa verificado em base publica?}

✅ OK:
- {Registro Anvisa citado com numero verificavel}
- {COI declarado}
- {Comparativo responsavel}
- {TCLE arquivado}
- {Habilitacao do operador citada se Classe III}
