# Levantamento na Ótica Kadosh

Resumo do que o grupo viu e ouviu na ótica. As regras de negócio (RN) citadas estão completas na Seção 4 do [README](../README.md).

## 1. Identificação

| Item | Registro |
| --- | --- |
| Organização | Ótica Kadosh, comércio com fins lucrativos que vende armações e lentes |
| Endereço | Av. Diogo da Costa Tavares, 125, Jardim Romano, São Paulo/SP, CEP 08191-000 |
| Telefone da loja | (11) 99349-4371 |
| Responsável que atendeu o grupo | Marcos Vinícius Silva Menezes, gerente (contato pelo telefone da loja) |
| Outros funcionários | Guilherme de Souza Silva (optometrista) e Kaique Batista dos Santos (consultor óptico) |

## 2. Visita e entrevista

| Item | Registro |
| --- | --- |
| Data | 05/09/2026 |
| Local | Dentro da ótica, presencial |
| Entrevistado | Marcos Vinícius Silva Menezes, gerente |
| Integrantes presentes | Cauã Batista Freire, João Felipe de Sousa Pires e Victor Augusto Silva Marcilio |
| Depois da visita | O gerente continuou respondendo dúvidas do grupo por mensagem (relatos de 14/10/2026 e 15/10/2026) |

## 3. O que o grupo observou na loja

Observação feita pelo grupo, separada do que o gerente disse:

- O **formulário de pedido** preenchido na venda.
- O **comprovante** entregue ao cliente (o canhoto de compra e venda).
- O **laudo** produzido na ótica pelo optometrista.
- Os registros de pedidos, estoque e parcelas ficam **em papel e em planilhas separadas**.

As fotos do formulário e do laudo mostram dados pessoais e de saúde de clientes reais. Por isso **não foram publicadas** no repositório.

## 4. O que o gerente informou

### Porte e rotina

- A loja tem três funcionários: optometrista, gerente e consultor óptico.
- São cerca de **100 atendimentos e 80 vendas por semana**. Nem todo atendimento termina em venda.
- Um banco de dados usado antes na loja apresentava falhas frequentes.
- Os clientes pagam à vista, parcelado ou em partes. A loja compra de fornecedores quando falta produto e trata trocas e devoluções.

### Regras relatadas

| Tema | O que foi relatado | Regra no README |
| --- | --- | --- |
| Receita trazida pelo cliente | Aceita se tiver até um ano da emissão; senão, a loja faz novo teste | RN-03 |
| Venda sem receita | Óculos de sol sem grau podem ser vendidos sem receita; lente de grau exige receita | RN-09 e RN-16 |
| Quem faz o quê | O optometrista emite o laudo; o consultor conduz o atendimento comercial que fecha a venda | RN-15 |
| Medidas por olho | DNP e altura são registradas por olho | RN-13 |
| Encomenda | Só é liberada com sinal de pelo menos 30% do total e previsão de conclusão | RN-18 |
| Garantia | A garantia é contada a partir da montagem: um ano para armações e seis meses para lentes. Para armações, cobre defeitos de fabricação, mola e parafuso. Para lentes, cobre adaptação, erro de grau, eficácia do tratamento e riscos, conforme o regulamento da ótica | RN-07 e RN-19 |
| Suporte após a entrega | Ajustes, plaquetas e parafusos, de graça e sem prazo | RN-20 |
| Retirada | O cliente retira o óculos com o canhoto de compra e venda | RN-21 |
| Nota fiscal | A loja emite quando solicitada. O grupo registra tipo, número e data do documento emitido | RN-22 |
| Desistência | Relatada a política de considerar o pedido ainda não enviado ao fornecedor e o limite de 24 horas da compra | RN-24 |
| Troca e Devolução |  Depende de avaliação do produto e da causa do dano, e pode ser aprovada ou recusada. Peças intactas podem ser reaproveitadas e as demais são descartadas | RN-08 e RN-25 |
| Formulário | O campo “Retirada a partir das” indica o horário previsto para a retirada do produto. | RN-27 |

## 5. O que não foi confirmado

- O regulamento de garantia da ótica não foi apresentado ao grupo.
- As regras de nota fiscal e de reembolso são relatos do gerente. Não são parecer jurídico.
- Tipos de dados, tamanhos e prazos de retenção usados no dicionário são propostas do grupo, e não práticas confirmadas da loja.

## 6. Comprovação

- Foto do grupo dentro da ótica, com o letreiro "Ótica Kadosh" na parede: [Otica kadoshi.jpeg](../Otica%20kadoshi.jpeg).

## 7. O que mudou desde a primeira versão da Entrega 1

Comparação com a versão que recebeu a correção do professor.

### Na organização e no levantamento

- A primeira versão não trazia nome, endereço nem contato da loja. Agora estão registrados a organização, o endereço, o telefone, o responsável (Marcos Vinícius) e a visita de 05/09/2026.
- Depois da visita, o gerente respondeu por mensagem a novas dúvidas (14 e 15/10/2026): o que a garantia cobre, a política de desistência, a venda de óculos sem grau sem receita e as medidas de DNP e altura por olho.
- Confirmações de 15/10/2026 registradas no README: parcelamento do saldo no cartão em até dez parcelas de no mínimo R$ 50,00 (RN-17); toda venda precedida de orçamento, com validade usual de 24 horas (RN-23); lentes contadas por par e armações por unidade (RN-26).

### No modelo e nos documentos

- Os processos deixaram de ser listas de atributos e viraram 12 processos, cada um com entrada, responsável, sequência e saída.
- Os requisitos passaram de 9 funcionais e 6 não funcionais para 18 funcionais e 7 não funcionais. As regras de negócio chegaram a 33 (RN-01 a RN-33).
- Por orientação do professor, foram retiradas as ligações diretas VENDA–PARCELA e VENDA–RECEITA. A parcela agora vem do pagamento de sinal, e a receita vem do atendimento.
- Venda e compra passaram a ligar direto ao PRODUTO (CONTÉM e ADQUIRE), sem entidades de item. TROCA_DEVOLUCAO liga à venda e ao produto.
- PRODUTO ganhou especialização total e disjunta em LENTE e ARMACAO.
- O DER agora está dentro do repositório, e o dicionário em HTML tem relacionamentos, fluxo de dados, convenções, log de acesso e LGPD.
