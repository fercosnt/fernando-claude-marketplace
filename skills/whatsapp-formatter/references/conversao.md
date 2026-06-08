# Conversao e sintaxe — referencia completa

Carregue quando precisar de casos de borda da sintaxe, do mapa completo de degradacao Markdown -> WhatsApp, ou dos limites do app.

## 1. Sintaxe nativa — detalhes finos

| Estilo | Sintaxe | Regra critica |
|--------|---------|---------------|
| Negrito | `*texto*` | UM asterisco. Colado ao texto. |
| Italico | `_texto_` | UM underscore. |
| Tachado | `~texto~` | UM til. |
| Mono inline | `` `texto` `` | UMA crase. Fundo cinza, fonte fixa. |
| Mono bloco | ` ```texto``` ` | TRES crases. Preserva quebras de linha internas. Nao combina com outros estilos. |
| Lista marcador | `- texto` | Hifen + espaco, inicio de linha. Renderiza bullet. |
| Lista numerada | `1. texto` | Digito + ponto + espaco, inicio de linha. |
| Citacao | `> texto` | `>` + espaco, inicio de linha. Barra vertical a esquerda. |

**Listas, citacao e codigo inline/bloco** sao recursos nativos do WhatsApp desde 2024 e funcionam igual em Android, iOS, WhatsApp Web e desktop.

### Combinacoes
- Negrito + italico: `*_texto_*`
- Negrito + italico + tachado: `*~_texto_~*`
- O simbolo mais externo e o mais interno tem que fechar na ordem certa.
- **Monoespacado (crases) cancela tudo:** ao trocar a fonte, perde negrito/italico/tachado daquele trecho. Nunca combine crase com outro estilo.

### Pegadinhas de espaco e linha
- `* texto *` (com espaco interno) **nao formata**. Tem que colar: `*texto*`. Vale pra todos os estilos inline.
- `-`, `>`, `1.` so disparam no **inicio da linha** e **com espaco** depois. Sem espaco, viram texto literal.
- Quebra de linha: no WhatsApp Web/desktop e `Shift+Enter`; no mobile, o botao de nova linha do teclado. Texto colado com quebras preserva as quebras. Linhas em branco entre blocos sao mantidas.

### Sem caractere de escape
WhatsApp nao tem escape oficial. Pra mostrar um `*`, `_` ou `~` literal, evite cercar texto com eles em par — um simbolo isolado ou com espaco adjacente nao dispara formatacao.

## 2. Mapa completo de degradacao Markdown -> WhatsApp

| Markdown (entrada) | WhatsApp (saida) | Notas |
|--------------------|------------------|-------|
| `**bold**` / `__bold__` | `*bold*` | 2 asteriscos -> 1. Erro mais comum dos LLMs. |
| `*italic*` / `_italic_` | `_italic_` | Italico = underscore. Asterisco simples e negrito no WhatsApp. |
| `~~strike~~` | `~strike~` | Til duplo -> simples. |
| `` `code` `` | `` `code` `` | Inline = 1 crase. Passa direto. |
| ` ```code``` ` | ` ```code``` ` | Bloco = 3 crases. Passa direto. |
| `# H1` ... `###### H6` | `*TITULO*` (negrito, idealmente caixa alta) + linha em branco | Sem heading real. Pode prefixar emoji (📌). Nunca deixar `#`. |
| `- item` / `* item` | `- item` | Preferir hifen; asterisco como bullet colide com negrito. |
| `1. item` | `1. item` | Passa direto. |
| `> quote` | `> quote` | Passa direto. Quote multi-paragrafo nao e robusto — repita `>` por linha. |
| `[texto](url)` | `texto: url` (ou `texto (url)`) | Sem link ancora. So URL crua vira clicavel. Nunca deixar `[..](..)`. |
| `![alt](img.png)` | remover, ou `alt: url` | Imagem markdown nao renderiza no texto. |
| Tabela `\| a \| b \|` | lista `*Campo:* valor` por linha; ou, se forem dados curtos alinhados, bloco de 3 crases (monospace preserva alinhamento) | Sem tabela. Pipes viram lixo visual. |
| `---` / `***` (hr) | linha em branco, ou `------` / `━━━` | Sem regua horizontal. |
| `[^1]` footnote | inline no texto ou remover | Sem suporte. |

### Ordem de substituicao importa
Trate negrito `**`/`__` **antes** de italico `*`/`_`. Como o asterisco simples e ambiguo (markdown usa pra italico, WhatsApp usa pra negrito), se voce processar italico primeiro pode estragar o negrito. Sempre: bold duplo -> bold simples, depois italico -> underscore.

## 3. Por que o LLM erra (lembrete)

O modelo emite Markdown por reflexo de treino, assumindo um renderizador no destino. WhatsApp nao tem. Markdown e "instrucao pra um renderizador", nao texto ja formatado. Os erros recorrentes, em ordem:

1. Negrito com `**` (asterisco duplo).
2. Heading com `#`.
3. Link `[texto](url)` cru.
4. Tabela com pipes.
5. Italico com asterisco simples (sai negrito).
6. Tachado `~~` duplo.
7. Confundir crase inline (1) com bloco (3).
8. Bullet com `*` colidindo com negrito.

Por isso o passo de lint no SKILL.md varre esses padroes especificos.

## 4. Limites de caracteres

- Mensagem pessoal / grupo: ate **65.536 caracteres** (na pratica, ilimitado).
- Status de texto: ate **700 caracteres**.
- WhatsApp Business API (templates): body ate **1.024 caracteres**, sem tabs/newlines/4+ espacos seguidos. So relevante se o usuario disser que e template de API — nao se aplica a mensagem normal.

Legibilidade pede mensagens bem mais curtas que o limite tecnico. Se passar de ~10-12 linhas, considere quebrar.

## Fontes
- WhatsApp FAQ — How to format your messages: https://faq.whatsapp.com/539178204879377/
- TechCrunch — listas, block quotes e inline code (fev/2024): https://techcrunch.com/2024/02/21/whatsapp-adds-formatting-support-for-lists-block-quotes-and-inline-code/
- Periskope — bold/italic/strike/code e combinacoes: https://periskope.app/blog/bold-text-in-whatsapp
- lib `tupe12334/md-to-whatsapp` (modos de degradacao): https://github.com/tupe12334/md-to-whatsapp
- TypeCount — limites de caracteres: https://typecount.com/blog/whatsapp-character-limit
