# prompts/ — o que o n8n monta

Cada arquivo aqui **deriva de uma skill** deste plugin e diz de qual. O n8n faz GET destes arquivos
(tag fixa) e do `shared/` (repo privado, token), e monta:

```
system = shared/sistema-mkt.md + shared/contrato-de-escrita.md + shared/formato-de-saida.md
       + shared/formulas-espelho.md (só a seção usada) + prompts/<rito>.md
user   = JSON com os dados JÁ CONTADOS pelo Code node (o n8n conta; o Claude narra e julga)
```

Regras: modelo fixo (nunca "Auto"); temperature baixa; se um número não vier no JSON, o texto diz
"não consegui ler X" — nunca estima. O eval `evals/consistencia/` roda a mesma fixture pela skill e
por este prompt e exige os mesmos itens e números. **Se você mudar a skill, mude o prompt — e rode
o eval antes de subir a tag.**
