# Modelo de e-mail — credenciais de produção

Para `ecommerce@userede.com.br` (varejo ou segmento desconhecido) ou para o Box da Linha Direta
(clientes do atacado). Os 8 itens são exigência literal da documentação de Gestão de Acessos; manter
a numeração facilita o trabalho de quem recebe.

Pede as três APIs de uma vez: Gestão de Vendas, Gestão de Acessos e Link de Pagamento. Preencher o
que está entre colchetes antes de enviar.

---

**Assunto:** Solicitação de credenciais de produção — Gestão de Vendas, Gestão de Acessos e Link de Pagamento

Prezados,

Somos estabelecimento credenciado da Rede e gostaríamos de solicitar o cadastro de Organização,
Usuário e Aplicação para uso das APIs em ambiente de **produção**.

Já realizamos a integração e os testes no ambiente de Sandbox, com credenciais geradas pelo Portal
do Desenvolvedor. A integração autentica via OAuth 2.0 (`client_credentials`) e consome as rotas de
`merchant-statement` — vendas, vendas parceladas, pagamentos, ordens de crédito e débitos —
respeitando os limites de janela de cada rota e TLS 1.2. Também validamos a criação de links de
pagamento no simulador.

Segue o cadastro solicitado:

1. **Nome da Empresa/Organização parceira que usará as APIs da Rede:** [RAZÃO SOCIAL]
2. **CNPJ da Empresa/Organização:** [CNPJ]
3. **E-mail da Empresa/Organização:** [E-MAIL]
4. **Telefone da Empresa/Organização:** [TELEFONE]
5. **Segmento da Empresa/Organização:** Estabelecimento comercial — [RAMO, ex.: clínica
   odontológica]. Não atuamos como credenciadora ou subcredenciadora: o acesso é para conciliação
   do extrato e para cobrança dos nossos próprios pontos de venda.
6. **Nome do Cliente:** [SEU NOME COMPLETO]
7. **E-mail do Cliente:** [SEU E-MAIL]
8. **API(s) que deseja acessar:**
   - **Gestão de Vendas** (`merchant-statement`) — conciliação do extrato
   - **Gestão de Acessos** — para solicitar a liberação dos nossos pontos de venda
   - **Link de Pagamento** — geração de cobranças por API (cartão e PIX)

Nossos pontos de venda são: **[PV 1]**[, PV 2, …].

Sobre o **Link de Pagamento**: entendemos que ele exige projeto e credenciais distintos dos de
Gestão de Vendas, além da habilitação do produto e do aceite dos termos no portal userede. Favor
confirmar o procedimento e o que precisamos fazer do nosso lado. O uso previsto é gerar a cobrança
da consulta e enviá-la ao cliente, com acompanhamento do status pela própria API.

Como a Organização parceira e o Cliente são a mesma pessoa jurídica — somos o próprio
estabelecimento consultando o nosso extrato e cobrando os nossos clientes —, permanecemos à
disposição caso seja necessário algum ajuste no formato do cadastro.

Aproveito para perguntar se a liberação dos pontos de venda acima pode ser feita junto com este
cadastro, ou se devemos abrir a solicitação de acesso separadamente após receber as credenciais.

Atenciosamente,
[SEU NOME]
[CARGO] — [EMPRESA]
[TELEFONE]

---

## Por que cada parte está aí

- **O parágrafo do sandbox** não é enfeite: a Rede declara que *"para utilizar a API em Produção,
  primeiramente a Rede precisará certificar o parceiro em ambiente de Sandbox"*. Dizer que a etapa
  está cumprida, e ser específico sobre o que já roda, evita uma rodada de e-mail.
- **A ressalva do item 5** existe porque o formulário deles foi desenhado para parceiros
  (conciliadoras, software houses). Sem explicar que o acesso é ao próprio extrato, o pedido pode
  ser classificado errado.
- **O parágrafo do Link de Pagamento** antecipa três coisas que descobrimos testando: são
  credenciais de um **projeto separado** (a de Gestão de Vendas recebe 401 nas rotas de link e
  vice-versa), o produto precisa ser **habilitado comercialmente** e os termos aceitos no portal.
  Perguntar antes evita receber só metade do que se pediu.
- **A pergunta final sobre os PVs** antecipa o passo que mais trava: credencial de produção não dá
  acesso a estabelecimento nenhum, cada PV depende de solicitação e aprovação. Ver
  [producao.md](producao.md).

## Se preferir separar em dois e-mails

Faz sentido quando o Link de Pagamento ainda depende de decisão comercial interna: peça primeiro
Gestão de Vendas + Gestão de Acessos (que destravam a conciliação, já pronta) e deixe o Link de
Pagamento para um segundo pedido, quando o workflow do n8n estiver desenhado. O custo é uma rodada
a mais de e-mail; o ganho é não segurar o que já está pronto.
