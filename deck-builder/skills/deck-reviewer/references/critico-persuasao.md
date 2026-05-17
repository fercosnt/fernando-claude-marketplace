# Critico 2 — Persuasao (invoca `/copy`)

Pergunta unica: **os hooks funcionam? a audiencia toma a acao?**

Foca em 3 pontos de alta-pressao do deck:

1. Slide 1 (capa ou primeira frase) — hook
2. Slide(s) CTA — chamada-a-acao
3. Mensagens-chave dos slides intermediarios (sample, nao exaustivo)

---

## 1. Hook do slide 1

**Regra:** a primeira frase precisa fazer a audiencia querer ouvir a segunda.

**Sinais de hook forte:**
- Numero contraintuitivo ("89% dos implantes premium falham por causa de X — nao por causa de Y")
- Status quo virado de cabeca pra baixo ("Voce nao precisa de mais leads. Precisa de menos.")
- Pergunta retorica forte ("E se a sua maior margem estiver no servico que voce mais reluta em vender?")
- Promessa especifica + numero ("Aumentamos ticket medio de 4 clinicas em 18 meses. Em media 47%.")

**Sinais de hook fraco:**
- Generico: "Hoje vou falar sobre..."
- Auto-referencial: "Somos a Beauty Smile, fundada em 2018..."
- Pergunta obvia: "Quem aqui quer crescer?"
- Estatistica sem ancora: "O mercado cresce muito."

### Invocar `/copy` para hook

Se `/copy` instalada (ver SKILL.md §integracao-copy), passa contexto e pede critica:

```
/copy duvida Hook do slide 1 desse deck — funciona?

Contexto:
- Objetivo do deck: {Meta.objetivo_unico}
- Audiencia: {Meta.audiencia}
- Big Idea: {Meta.big_idea}
- Vertical: {Meta.skill_geradora}

Hook atual (slide 1):
"{texto do slide 1 — action title + mensagem-chave + 1a frase das speaker notes}"

Devolva em ate 5 linhas:
1. Diagnostico (1 linha): hook forte / aceitavel / fraco — por que?
2. Se aceitavel/fraco: 2 variantes alternativas
3. Veredito: manter / ajustar / trocar
```

Captura a resposta e converte em issue:

- `/copy` diz "forte" → 🟢 (sem issue) ou nenhum issue
- `/copy` diz "aceitavel" → 🟢 com sugestao
- `/copy` diz "fraco" → 🟡 MAJOR com variantes do `/copy` como `Sugestao:`

### Fallback heuristico (SEM `/copy`)

Aplica checklist binario:

| Criterio | Tem? |
|----------|------|
| Numero especifico no hook | sim/nao |
| Verbo de acao forte (cresce, dobra, falha, perde) | sim/nao |
| Tensao ou paradoxo | sim/nao |
| Promessa concreta | sim/nao |

Score:
- 3-4 ✓ → hook OK, sem issue
- 2 ✓ → 🟢 com sugestao generica
- 0-1 ✓ → 🟡 MAJOR com sugestao "Hook fraco — instale skill `/copy` ou pense em hook tipo: '{template}'"

Templates de fallback (escolher conforme vertical):

| Vertical | Template |
|----------|----------|
| fundraising | "Numero contraintuitivo do mercado + ancora financeira + virada de status quo" |
| sales | "Custo do problema atual em R$ + numero especifico do ROI prometido" |
| clinical | "Caso clinico real com numero (recidiva, sucesso, tempo) + relevancia pra audiencia" |
| teaching | "Pergunta provocadora ligada ao dia-a-dia da audiencia + promessa do que vai dominar ao final" |
| scientific | "Lacuna especifica na literatura + contribuicao do trabalho em 1 frase quantificada" |

## 2. CTAs — clareza + especificidade

**Regra:** todo slide CTA precisa responder 3 perguntas:
1. **O que** a audiencia faz a seguir?
2. **Quando** (prazo, janela)?
3. **Como** (canal, contato, link)?

### Sinais de CTA fraco

| CTA fraco | Por que |
|-----------|---------|
| "Obrigado, alguma pergunta?" | Sem acao, sem prazo, sem canal |
| "Estamos a disposicao" | Generico — quem? quando? como? |
| "Vamos conversar" | Sem proxima etapa concreta |
| "Acesse nosso site" | Sem incentivo + sem janela |

### CTAs fortes (exemplos por vertical)

| Vertical | CTA forte |
|----------|-----------|
| fundraising | "R$500k @ 8% equity / 6 meses. Term sheet pronto em 7 dias. Fernando@beautysmile.com.br" |
| sales | "Demo de 45min na sua clinica nas proximas 2 semanas. Reserva agora: {link} (so 4 vagas/mes)" |
| proposal | "Aceite ate {DATA+14d}. Inicio em {DATA+21d}. Valido se assinado ate {DATA+14d}." |
| clinical | "Marcar avaliacao gratuita {clinica} ate {DATA+30d}. Whatsapp: {numero}" |
| teaching | "Hands-on agora (worksheet anexo) + leitura {ref} ate proxima aula + quiz online ate domingo" |
| scientific | "Read full paper: {DOI}. Replicate code: {repo}. Contact: {email}" |

### Invocar `/copy` para CTA

Quando `/copy` disponivel:

```
/copy duvida CTA do slide {N} desse deck — vai converter?

Contexto:
- Vertical: {vertical}
- Objetivo do deck: {objetivo}
- Audiencia: {audiencia}

CTA atual:
"{texto do slide CTA — action title + mensagem-chave + speaker notes relevantes}"

Devolva:
1. CTA responde O QUE / QUANDO / COMO? (sim/parcial/nao)
2. Se faltar: variante reescrita
3. Veredito: aprova / ajusta / reescreve
```

### Severidade CTAs

- CTA com 0 das 3 dimensoes (O que/Quando/Como): 🟡 MAJOR
- CTA com 1 das 3: 🟡 MAJOR
- CTA com 2 das 3: 🟢 MINOR
- CTA com 3 das 3: sem issue
- CTA inexistente em vertical que exige: 🔴 BLOCKER (ja capturado pelo Critico Clareza — NAO duplicar; reviewer faz dedupe)

## 3. Mensagens-chave dos slides intermediarios (sample)

**Regra:** o reviewer NAO checa slide por slide (custaria muito). Sampling:

- Slide 2 (geralmente problema)
- Slide do meio (geralmente solucao/dados)
- Slide N-1 (geralmente prova social ou ROI)

Para cada um, aplica:

- Mensagem-chave parafraseavel em 1 frase? OK
- Mensagem-chave generica ("queremos crescer")? 🟢
- Mensagem-chave contradiz outra anterior? 🟡

NUNCA 🔴 por mensagem-chave isolada — sempre escalavel ao Critico Clareza ou SUCCESs se for sistemico.

---

## Fallback graceful — quando `/copy` NAO esta instalada

No header do review, registra:

```markdown
## Meta
- ...
- Criticos aplicados: clareza + persuasao (heuristico — `/copy` indisponivel) + SUCCESs
```

E no Critico Persuasao, em vez de citar `/copy`, cita as heuristicas embutidas:

> Sugestao: hook nao tem numero nem virada de status quo. Considerar template "Numero contraintuitivo + tensao narrativa". Instalar skill `/copy` para refinar com criticos de copywriting profissional.

## Fonte canonica (NB1)

- Pitch Anything (Klaff) — frame control + intriga
- Made to Stick (Heath) — Concrete + Credible
- /copy skill local (Fernando) — frameworks AIDA / PAS / PULSE / BAB

## Output do Critico Persuasao

```python
[
  {"slide_n": 1, "tipo_slide": "capa", "critico": "persuasao",
   "severidade": "🟡",
   "problema": "Hook generico: 'Hoje vou falar sobre Beauty Smile' — sem numero, sem tensao",
   "sugestao": "Reescrever: 'Premium ja paga R$48k/ano em odontologia. Beauty Smile capturou 4 dessas pessoas. Aqui esta como.'"},
  {"slide_n": 13, "tipo_slide": "CTA", "critico": "persuasao",
   "severidade": "🔴",
   "problema": "CTA inexistente — slide 13 (final) e 'Obrigado'",
   "sugestao": "Adicionar slide 14 'Ask' com R$500k @ 8% / 6 meses, term sheet em 7 dias, fernando@beautysmile.com.br"}
]
```
