
# Entrega 1 — Modelo Conceitual (DER)
### Modelagem de um sistema de gestão de informações para uma organização de pequeno porte

**Organização estudada: Ótica Kadosh** · Projeto acadêmico de Modelagem de Dados

---

## Metadados

- **Nomes dos alunos e RGM**

| Integrante | RGM |
| --- | --- |
| Victor Augusto Silva Marcilio | 47190175 |
| João Felipe de Sousa Pires | 48165379 |
| Cauã Batista Freire | 48355127 |
| João Victor Gobi Romero | 48114642 |
| Guilherme Araujo de Oliveira | 47116862 |

---

## 1. Caracterização da Organização

- **Nome e natureza da organização:** **Ótica Kadosh**, estabelecimento comercial **com fins lucrativos** que vende produtos ópticos (armações e lentes). Fica na Av. Diogo da Costa Tavares, 125, Jardim Romano, São Paulo/SP, CEP 08191-000.
- **Contexto e porte:** pequeno comércio com **três funcionários**: um optometrista (**Guilherme de Souza Silva**), um gerente (**Marcos Vinícius Silva Menezes**) e um consultor óptico (**Kaique Batista dos Santos**). O gerente informou cerca de **100 atendimentos e 80 vendas por semana**, o que indica que parte dos atendimentos não termina em venda. A ótica atende clientes presencialmente, vende armações e lentes, recebe pagamentos à vista, parcelados ou em partes, mantém estoque, compra de fornecedores quando falta produto e trata trocas e devoluções.
- **Problemas e necessidades identificados:** pedidos, estoque e parcelas são controlados em **papel e planilhas separadas**, e um banco de dados usado antes apresentava falhas frequentes. Hoje não há vínculo seguro entre atendimento, receita, pedido, pagamentos, compras ao fornecedor, estoque e trocas, e cada consulta exige abrir vários registros. O sistema precisa relacionar tudo isso, saber o saldo de estoque e o saldo a pagar de cada pedido e proteger os dados de saúde dos clientes.
- **Justificativa da escolha:** o grupo tem acesso presencial à ótica e ao gerente. O negócio é pequeno o bastante para o primeiro DER, mas tem processos encadeados e observáveis (atendimento, receita, venda, pagamento, compra, montagem, retirada, garantia e troca) que exigem relacionamentos variados: 1:1, 1:N, entidades fracas e generalização.
- **Evidências da organização:**
  - Endereço: Av. Diogo da Costa Tavares, 125, Jardim Romano, São Paulo/SP.
  - Contato da loja: (11) 99349-4371. Entrevistado: **Marcos Vinícius Silva Menezes**, gerente.
  - **Data da visita e entrevista:** 05/09/2026, presencial, com observação do formulário de pedido, do comprovante entregue ao cliente e do laudo produzido na ótica. Depois da visita, o gerente respondeu por mensagem a dúvidas pontuais (venda sem receita e medidas por olho).
  -Fotografia feita no interior da ótica durante a visita: [Otica kadoshi.jpeg](./Otica%20kadoshi.jpeg).
  - As fotos do formulário e do laudo contêm dados pessoais e de saúde reais; por isso **não foram publicadas**.

---

## 2. Processos de Negócio

- **Principais processos mapeados:**
  1. **Atendimento e prescrição:** o cliente é atendido por um funcionário. A receita trazida é aceita se tiver até 1 ano; caso contrário, a ótica faz o teste e produz um **laudo**. A data da receita é anotada. As medidas são por olho (direito e esquerdo) e por distância (longe e perto); DNP e altura são registradas por olho.
  2. **Pedido e venda:** o consultor registra no formulário o cliente, as datas, as medidas, a armação e as lentes, com quantidade e preço (por armação e por par de lentes), o total, o sinal pago e o saldo. Há uma via da ótica e um comprovante resumido para o cliente. Pode haver venda sem receita (por exemplo, óculos de sol sem grau).
  3. **Pagamento e parcelas:** aceita Pix, dinheiro, débito e crédito, inclusive pagamento parcial ou parcelado. As parcelas futuras são acompanhadas em planilha separada.
  4. **Estoque e fornecedores:** se o pedido não pode ser atendido com o estoque, o gerente solicita armações ou lentes a um fornecedor (por ligação ou mensagem), anotando fornecedor, contato, produto, quantidade, custo, data do pedido e data de chegada. Entradas e saídas ficam em planilha de estoque. Cada compra atende um único pedido.
  5. **Montagem, retirada e garantia:** com os produtos em mãos, a ótica monta e finaliza os óculos, avisa o cliente e registra a **retirada efetiva**. A **garantia é de 1 ano**, contada da montagem/finalização.
  6. **Trocas e devoluções:** o pedido em papel registra a data do ocorrido, a possível cobrança e a descrição do dano. A substituição sai do estoque ou de novo pedido ao fornecedor. Peças intactas são reaproveitadas e as demais, descartadas.

## 3. Requisitos do Sistema


### 3.1 Requisitos Funcionais

| ID | O sistema deve permitir... | Origem |
| --- | --- | --- |
| RF-01 | Cadastrar e consultar os dados do cliente usados no pedido. | Formulário de pedido |
| RF-02 | Registrar o atendimento, associando cliente e funcionário responsável. | Atendimento presencial e campo "Consultor" |
| RF-03 | Registrar receita trazida ou laudo da ótica, com data e medidas por olho (OD/OE) e distância (longe/perto), incluindo DNP e altura por olho. | Laudo, pedido e entrevista |
| RF-04 | Conferir a data da receita trazida pela regra de 1 ano praticada pela ótica. | Entrevista |
| RF-05 | Registrar o pedido com itens de armação e lentes, quantidades, preços, total, sinal e saldo, com ou sem receita. | Formulário e comprovante |
| RF-06 | Registrar pagamentos parciais e parcelas, sem perder o vínculo com o pedido, e consultar parcelas vencidas ou em aberto. | Entrevista e planilha de parcelas |
| RF-07 | Registrar compra ao fornecedor, vinculada ao pedido, com itens, quantidades, custos, data de solicitação e de chegada. | Entrevista |
| RF-08 | Registrar entradas e saídas de estoque e consultar o saldo de cada produto. | Planilha de estoque |
| RF-09 | Registrar montagem/finalização, retirada efetiva e calcular o fim da garantia (1 ano). | Entrevista e formulário |
| RF-10 | Registrar troca ou devolução, dano, eventual cobrança e destino das peças (reaproveitada ou descartada), gerando o movimento de estoque. | Entrevista e anotação no pedido |
| RF-11 | Emitir o comprovante resumido do pedido para o cliente. | Comprovante em papel |
| RF-12 | Consultar o histórico de atendimentos, receitas e pedidos de um cliente. | Necessidade apontada pela entrevista |
| RF-13 | Controlar o acesso por perfil (gerente, optometrista e consultor óptico). | Estrutura da equipe |
| RF-14 | Consultar vendas, compras e estoque por período. | Gestão da ótica † |

### 3.2 Requisitos Não Funcionais

| ID | Qualidade proposta | Justificativa |
| --- | --- | --- |
| RNF-01 | **Segurança e privacidade:** restringir o acesso a dados pessoais e a receitas e medidas conforme o perfil, em conformidade com a LGPD (dado de saúde é dado pessoal sensível, art. 5º, II). | Documentos contêm CPF, contatos e dados de saúde. |
| RNF-02 | **Disponibilidade e recuperação:** manter cópia de segurança diária e permitir recuperação em até 4 horas após uma falha †. | O banco anterior falhava com frequência. |
| RNF-03 | **Integridade:** garantir integridade referencial entre pedido, itens, pagamentos, compras e movimentos de estoque. | Evita registros órfãos e saldos sem origem. |
| RNF-04 | **Usabilidade:** em teste com um funcionário, consultar o histórico e o estado de um pedido pela interface, sem recorrer a papel ou planilhas. | Hoje as informações estão em vários registros. |
| RNF-05 | **Rastreabilidade:** manter trilha de auditoria com autor, data, valor anterior e valor novo para alterações de valores, medidas e trocas. | Permite conferência posterior. |
| RNF-06 | **Desempenho:** abrir o histórico de um cliente em até 3 segundos, com 10 mil pedidos cadastrados †. | Atendimento no balcão não pode esperar. |
| RNF-07 | **Disponibilidade no horário de atendimento:** o sistema deve estar disponível durante o funcionamento da loja †. | Vendas e atendimentos dependem dele. |

† Valor proposto pelo grupo, ainda não validado com a ótica.

---

## 4. Regras de Negócio
 
- **Regras operacionais:**

| ID | Regra | Fundamento |
| --- | --- | --- |
| RN-01 | Não há venda sem atendimento. Um atendimento resulta em no máximo uma venda. | Entrevista |
| RN-02 | Cada pedido usa sua própria receita; a mesma receita não é reutilizada em outro pedido. | Entrevista |
| RN-03 | A receita trazida é aceita se tiver até 1 ano de emitida; caso contrário, a ótica faz novo teste. | Entrevista; prática da ótica, não prazo legal geral |
| RN-04 | O pedido registra armação e lentes; os preços são por armação e por par de lentes. | Formulário e entrevista |
| RN-05 | O pedido pode ser pago em partes e ter parcelas acompanhadas em planilha. | Entrevista |
| RN-06 | Um pedido pode não gerar compra (usa estoque); se gerar, cada compra atende um único pedido e um único fornecedor. | Entrevista |
| RN-07 | A garantia começa na montagem/finalização, não na retirada: 1 ano para a armação e 6 meses para a lente (cobertura na RN-19). | Entrevista; resposta do gerente (14/10/2026) |
| RN-08 | Em troca ou devolução, peças intactas podem ser reaproveitadas e as demais são descartadas. | Entrevista |
| RN-09 | Uma venda pode não ter receita (por exemplo, óculos de sol sem grau). | Resposta do gerente |
| RN-10 | Cada receita tem no máximo 4 linhas de medida (OD/OE × longe/perto), garantido pela chave composta. | Laudo e pedido |
| RN-11 | A soma dos pagamentos de uma venda não pode ultrapassar o valor total. | Modelagem |
| RN-12 | O motivo do movimento de estoque define a origem obrigatória (item de venda, item de compra ou troca). | Modelagem |
| RN-13 | DNP e altura são registradas por olho. | Resposta do gerente |
| RN-14 | Todo produto é exatamente uma armação ou exatamente uma lente. | Modelagem (generalização disjunta e total) |
| RN-15 | O teste de vista e o laudo são realizados somente pelo optometrista; toda receita com origem LAUDO_OTICA pertence a um atendimento conduzido por funcionário com função OPTOMETRISTA. | Resposta do gerente (14/10/2026) |
| RN-16 | Lentes de grau só são vendidas com prescrição: receita de oftalmologista trazida pelo cliente ou laudo feito na própria ótica. Venda sem receita só é possível sem lente de grau (RN-09). | Resposta do gerente (14/10/2026) |
| RN-17 | O pagamento pode ser parcelado em até 10 parcelas, e cada parcela tem valor mínimo de R$ 50,00. | Resposta do gerente (14/10/2026) |
| RN-18 | Para encomendar a fabricação dos óculos, o pedido exige entrada (sinal) de no mínimo 30% do valor total, e o cliente recebe a data prevista em que os óculos estarão prontos. | Resposta do gerente (14/10/2026) |
| RN-19 | A garantia da armação (1 ano) cobre defeito de fabricação, mola da armação e parafuso. A garantia da lente (6 meses) cobre adaptação, erro de grau, tratamento sem a eficácia esperada e arranhões, conforme o regulamento da ótica. | Resposta do gerente (14/10/2026); regulamento não consultado pelo grupo † |
| RN-20 | Após a entrega, o cliente tem suporte técnico vitalício e gratuito: troca de plaquetas, ajustes e parafusos não são cobrados. | Resposta do gerente (14/10/2026) |
| RN-21 | Os óculos são entregues a qualquer pessoa que apresente o canhoto de compra e venda (comprovante) dado ao cliente no dia da aquisição. | Resposta do gerente (14/10/2026) |
| RN-22 | A nota fiscal é emitida somente quando o cliente solicita. | Resposta do gerente (14/10/2026) |
| RN-23 | Todo orçamento é anotado e entregue ao cliente antes do fechamento do pedido. | Resposta do gerente (14/10/2026) |
 
- **Restrições organizacionais:**
  - **Prazo de 1 ano da receita trazida e garantia de 1 ano** contada da montagem: definem os atributos de data e o cálculo do fim da garantia.
  - **Dados de saúde (receitas e medidas):** exigem controle de acesso e trilha de auditoria por força da LGPD.
  - **Cobrança por dano:** a ótica cobra em alguns casos, inclusive por imprudência do cliente; por isso a troca guarda um valor cobrado opcional.
  - **Retirada efetiva** diferente de montagem: o sistema precisa guardar as duas datas.
- **Cuidados de publicação:** exemplos de valores usados neste projeto são fictícios; fotos de documentos com dados reais não foram publicadas.


---

## 5. Dicionário de Dados Conceitual

O dicionário completo, com notação formal, índices, log, matriz de acesso e LGPD, está no arquivo [`Dicionario_de_Dados_Otica_Kadosh.html`](Dicionario_de_Dados_Otica_Kadosh.html) (visualização: [GitHub Pages](https://jfpiresoficial.github.io/otica-kadosh-modelagem-dados/Dicionario_de_Dados_Otica_Kadosh.html)). Abaixo estão as **17 entidades e 105 colunas** (atributos do DER mais chaves estrangeiras). Nomes físicos usam prefixos (`ID_` identificador, `NM_` nome, `DT_` data, `DH_` data e hora, `HR_` horário, `QT_` quantidade, `VL_` valor, `TP_`/`CD_` tipo e código de domínio, `DS_` descrição, `NR_` número). **PK** é chave primária e **FK** chave estrangeira. Os exemplos de valores no HTML são fictícios. Marca **†**: decisão do grupo ainda não validada com a ótica.

**Glossário óptico:** **OD/OE** olho direito/esquerdo · **DE/DC** dioptria esférica/cilíndrica (no laudo) · **AV** acuidade visual · **DNP** distância nasopupilar (usada na montagem das lentes).


### CLIENTE

Pessoa física que procura a ótica e cujos dados são anotados no pedido (nome, CPF, contatos e endereço). É quem solicita os atendimentos. **Identificação:** `@ID_CLIENTE`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_CLIENTE` (`id_cliente`) | Código interno do cadastro; não sofre operação matemática. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema; nunca reutilizado. |
| `NM_CLIENTE` (`nome`) | Nome completo do cliente, como escrito no pedido. Identifica o cliente nos atendimentos e no comprovante. Tipo: `varchar(120)`; obrigatório: Sim. | É o nome do cliente, nunca o do funcionário do campo “Consultor”. |
| `DT_NASCIMENTO` (`data_nasc`) | Data de nascimento (campo “Data Nasc.” do pedido). Ajuda a confirmar identidade e faixa etária. Tipo: `date`; obrigatório: Não. | † Preenchimento obrigatório não confirmado com a ótica. |
| `NR_CPF` (`cpf`) | CPF, somente dígitos. Dado pessoal protegido pela LGPD. Tipo: `char(11)`; obrigatório: Não. | Se informado: 11 dígitos válidos e único no cadastro. |
| `DS_EMAIL` (`email`) | Endereço de e-mail para contato. Tipo: `varchar(120)`; obrigatório: Não. | Se informado, deve ter formato válido. |
| `NR_TELEFONE_FIXO` (`telefone_fixo`) | Telefone fixo com DDD, somente dígitos (campo “Tel. Fixo”). Tipo: `varchar(11)`; obrigatório: Não. | Sem regra específica. |
| `NR_TELEFONE_CELULAR` (`telefone_celular`) | Celular com DDD (campo “Tel. Celular”). Canal usado para avisar que os óculos ficaram prontos. Tipo: `varchar(11)`; obrigatório: Não. | † Ao menos um meio de contato (celular, fixo ou e-mail) deve existir no cadastro. |
| `DS_LOGRADOURO` (`logradouro`) | Rua, avenida ou similar do endereço. Tipo: `varchar(120)`; obrigatório: Não. | Sem regra específica. |
| `NR_ENDERECO` (`numero_endereco`) | Número do imóvel (campo “Nº” ao lado do CEP). Texto, pois pode ter complemento como “12-A”. Tipo: `varchar(10)`; obrigatório: Não. | Sem regra específica. |
| `NM_BAIRRO` (`bairro`) | Bairro do endereço. Tipo: `varchar(60)`; obrigatório: Não. | Sem regra específica. |
| `NM_CIDADE` (`cidade`) | Cidade do endereço. Tipo: `varchar(60)`; obrigatório: Não. | Sem regra específica. |
| `NR_CEP` (`cep`) | CEP, somente dígitos. Tipo: `char(8)`; obrigatório: Não. | Se informado: 8 dígitos. |

### FUNCIONARIO

Integrante da equipe da ótica que atende clientes: optometrista, gerente ou consultor óptico. **Identificação:** `@ID_FUNCIONARIO`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_FUNCIONARIO` (`id_funcionario`) | Código interno do funcionário. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `NM_FUNCIONARIO` (`nome`) | Nome do integrante da equipe; aparece como “Consultor” no pedido. Tipo: `varchar(120)`; obrigatório: Sim. | Sem regra específica. |
| `TP_FUNCAO` (`funcao`) | Papel exercido na ótica. Define o que a pessoa pode fazer no sistema (Seção 6). Tipo: `varchar(20)`; obrigatório: Sim. | Domínio: OPTOMETRISTA, GERENTE, CONSULTOR_OPTICO (relatado na entrevista de 05/09/2026). |
| `NR_TELEFONE` (`telefone`) | Telefone de contato do funcionário. Tipo: `varchar(11)`; obrigatório: Não. | † Guarda de telefone individual não confirmada. |

### ATENDIMENTO

Evento em que um funcionário atende um cliente na loja. É a origem de qualquer receita e de qualquer venda. **Identificação:** `@ID_ATENDIMENTO`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_ATENDIMENTO` (`id_atendimento`) | Código interno do atendimento. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `ID_CLIENTE` — vínculo SOLICITA | Cliente atendido. Tipo: `integer`; obrigatório: Sim (FK). | FK para CLIENTE. Todo atendimento tem exatamente um cliente. |
| `ID_FUNCIONARIO` — vínculo CONDUZ | Funcionário responsável pelo atendimento. Tipo: `integer`; obrigatório: Sim (FK). | FK para FUNCIONARIO. Exatamente um por atendimento. |
| `DH_ATENDIMENTO` (`data_hora`) | Data e hora em que o atendimento ocorreu. É diferente da “Data da Compra” da venda. Tipo: `datetime`; obrigatório: Sim. | Sem regra específica. |
| `TP_MEIO_CONTATO` (`meio_contato`) | Como o cliente chegou à ótica (campo “Meio de contato” do pedido). Tipo: `varchar(30)`; obrigatório: Não. | † Lista de valores não confirmada; texto livre por enquanto. |

> RN-01: não há venda sem atendimento. Um atendimento resulta em no máximo uma venda e origina no máximo uma receita.

### RECEITA

Prescrição oftalmológica usada no pedido: trazida pelo cliente ou produzida pela ótica em laudo optométrico. **Identificação:** `@ID_RECEITA`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_RECEITA` (`id_receita`) | Código interno da receita. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `ID_ATENDIMENTO` — vínculo ORIGINA | Atendimento em que a receita foi obtida ou apresentada. Tipo: `integer`; obrigatório: Sim (FK, único). | FK para ATENDIMENTO; único: um atendimento origina no máximo uma receita. |
| `TP_ORIGEM` (`origem`) | De onde veio a prescrição. Tipo: `varchar(11)`; obrigatório: Sim. | Domínio: TRAZIDA (apresentada pelo cliente) ou LAUDO_OTICA (teste feito na ótica). |
| `DT_RECEITA` (`data_receita`) | Data anotada na receita ou no laudo. Tipo: `date`; obrigatório: Sim. | RN-03: receita trazida é aceita se tiver até 1 ano; senão a ótica faz novo teste. É prática da ótica, não prazo legal geral. |
| `DS_OBSERVACAO` (`observacao`) | Anotação complementar do laudo (espaço “Obs.”). Tipo: `varchar(255)`; obrigatório: Não. | Só quando houver anotação. |

> RN-02: cada pedido usa sua própria receita; a mesma receita não é reutilizada em outra venda.

### RECEITA_MEDIDA

Conjunto de medidas ópticas de um olho para uma distância (longe ou perto) dentro de uma receita. É entidade fraca de RECEITA. **Identificação:** `@ID_RECEITA + @CD_OLHO + @CD_DISTANCIA`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_RECEITA` — vínculo POSSUI | Receita a que a medida pertence. Tipo: `integer`; obrigatório: Sim (PK, FK). | FK para RECEITA; parte da chave. |
| `CD_OLHO` (`olho`) | Olho a que a linha se refere. Tipo: `char(2)`; obrigatório: Sim (PK). | Domínio: OD (direito) ou OE (esquerdo). Medida de um olho nunca é atribuída ao outro. |
| `CD_DISTANCIA` (`distancia`) | Finalidade visual da linha. Tipo: `varchar(5)`; obrigatório: Sim (PK). | Domínio: LONGE ou PERTO. Nem sempre as duas são preenchidas. |
| `VL_ESFERICO` (`esferico`) | Grau esférico em dioptrias (DE no laudo; coluna “Esférico” no pedido). Tipo: `decimal(4,2)`; obrigatório: Não. | Faixa usual de −20,00 a +20,00; passo de 0,25. |
| `VL_CILINDRICO` (`cilindro`) | Grau cilíndrico em dioptrias (DC no laudo; coluna “Cilíndrico” no pedido). Tipo: `decimal(4,2)`; obrigatório: Não. | Faixa usual de −8,00 a 0,00; se houver cilindro, o eixo é informado. |
| `VL_EIXO` (`eixo`) | Eixo do cilindro em graus. Tipo: `smallint`; obrigatório: Não. | Entre 0 e 180. |
| `VL_ACUIDADE_VISUAL` (`acuidade_visual`) | Acuidade visual (AV) registrada no laudo. Tipo: `varchar(10)`; obrigatório: Não. | Texto, pois pode ser fração (20/20) ou decimal (0,8). |
| `VL_DNP` (`dnp`) | Distância nasopupilar, em mm, usada na montagem das lentes. Tipo: `decimal(4,1)`; obrigatório: Não. | Registrada por olho (confirmado pelo gerente). |
| `VL_ALTURA` (`altura`) | Altura da lente na armação, em mm. Tipo: `decimal(4,1)`; obrigatório: Não. | Registrada por olho (confirmado pelo gerente). |

> RN-10: no máximo 4 linhas por receita, garantido pela chave composta. RN-13: DNP e altura são por olho.

### VENDA

Pedido de óculos registrado após o atendimento: valores, montagem, retirada e garantia. Corresponde ao formulário de pedido em papel. **Identificação:** `@ID_VENDA`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_VENDA` (`id_venda`) | Número do pedido. Chave técnica única, pois a unicidade do número impresso no bloco não foi confirmada. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `ID_ATENDIMENTO` — vínculo RESULTA EM | Atendimento que originou o pedido. Tipo: `integer`; obrigatório: Sim (FK, único). | RN-01. Um atendimento resulta em no máximo uma venda. |
| `ID_RECEITA` — vínculo É USADA EM | Receita usada no pedido. Tipo: `integer`; obrigatório: Não (FK, único). | RN-02 e RN-09: opcional (óculos de sol sem grau); quando existe, não pode repetir em outra venda. |
| `DT_COMPRA` (`data_compra`) | Data do pedido (campo “Data da Compra”). Não é a data de montagem, retirada nem pagamento. Tipo: `date`; obrigatório: Sim. | Sem regra específica. |
| `VL_TOTAL` (`valor_total`) | Total cobrado pelo pedido (campo “Total: R$”), antes de considerar o que já foi pago. Tipo: `decimal(10,2)`; obrigatório: Sim. | Igual à soma de quantidade × preço unitário dos itens. |
| `CD_STATUS` (`status`) | Etapa do pedido no acompanhamento. Tipo: `varchar(20)`; obrigatório: Sim. | † Proposta: ABERTO, AGUARDANDO_PRODUTO, EM_MONTAGEM, PRONTO, RETIRADO, CANCELADO. Estados a validar com a ótica. |
| `DT_MONTAGEM_FINALIZACAO` (`data_montagem_finalizacao`) | Data em que lente e armação foram montadas e os óculos finalizados. Tipo: `date`; obrigatório: Não. | RN-07: inicia a garantia de 1 ano, independentemente da retirada. |
| `DT_RETIRADA` (`data_retirada`) | Data em que o cliente retirou os óculos. Tipo: `date`; obrigatório: Não. | Retirada efetiva (confirmado). Nula até a retirada. Não é anterior à montagem. |
| `HR_RETIRADA` (`horario_retirada`) | Horário anotado em “A partir das” no pedido. Tipo: `time`; obrigatório: Não. | † Não confirmado se é horário previsto ou efetivo. |
| `DS_OBSERVACAO` (`observacao`) | Anotação livre do pedido (“Obs.”). Tipo: `varchar(255)`; obrigatório: Não. | Sem regra específica. |

> Dados derivados, não armazenados: valor pago = soma dos pagamentos; saldo a pagar = VL_TOTAL − valor pago; fim da garantia = DT_MONTAGEM_FINALIZACAO + 1 ano.

> RN-11: a soma dos pagamentos não pode ultrapassar VL_TOTAL.

### ITEM_VENDA

Linha de um pedido: uma armação ou um par de lentes, com quantidade e preço. Entidade fraca de VENDA. **Identificação:** `@ID_VENDA + @NR_ITEM`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_VENDA` — vínculo É COMPOSTA POR | Pedido ao qual a linha pertence. Tipo: `integer`; obrigatório: Sim (PK, FK). | FK para VENDA; parte da chave. |
| `NR_ITEM` (`numero_item`) | Número de ordem da linha dentro do pedido. Tipo: `smallint`; obrigatório: Sim (PK). | Sequencial a partir de 1, por venda. |
| `ID_PRODUTO` — vínculo REFERE-SE A | Produto vendido nesta linha. Tipo: `integer`; obrigatório: Sim (FK). | FK para PRODUTO. Exatamente um por linha. |
| `QT_ITEM` (`quantidade`) | Unidades: armações (“Qnt. Armação”) ou pares de lentes (“Qnt. de Lentes em Pares”). Tipo: `integer`; obrigatório: Sim. | Maior que zero. |
| `VL_PRECO_UNITARIO` (`preco_unitario`) | Preço de uma armação ou de um par de lentes. Tipo: `decimal(10,2)`; obrigatório: Sim. | RN-04: preço por armação e por par de lentes, não por lente individual. |
| `DS_OBSERVACAO` (`observacao`) | Comentário do item (“Obs. da Lente”, por exemplo). Tipo: `varchar(255)`; obrigatório: Não. | Não substitui as medidas da receita. |

### PARCELA

Valor futuro combinado para pagamento a prazo de uma venda. Hoje é acompanhada em planilha separada. Entidade fraca de VENDA. **Identificação:** `@ID_VENDA + @NR_PARCELA`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_VENDA` — vínculo É PARCELADA EM | Venda a que a parcela pertence. Tipo: `integer`; obrigatório: Sim (PK, FK). | FK para VENDA; parte da chave. |
| `NR_PARCELA` (`numero_parcela`) | Número da parcela dentro da venda. Tipo: `smallint`; obrigatório: Sim (PK). | Sequencial a partir de 1. |
| `VL_PARCELA` (`valor`) | Valor combinado da parcela. Tipo: `decimal(10,2)`; obrigatório: Sim. | A soma das parcelas não ultrapassa VL_TOTAL. |
| `DT_VENCIMENTO` (`data_vencimento`) | Data em que a parcela vence. Tipo: `date`; obrigatório: Sim. | Sem regra específica. |
| `CD_STATUS` (`status`) | Situação da parcela. Tipo: `varchar(15)`; obrigatório: Sim. | † Proposta: ABERTA, PAGA, ATRASADA. Cabeçalhos da planilha atual não foram fornecidos. |

> RN-05: o pedido pode ser pago em partes e ter parcelas acompanhadas em planilha.

### PAGAMENTO

Valor efetivamente recebido do cliente em uma venda, inclusive o sinal. Pode quitar uma parcela. **Identificação:** `@ID_PAGAMENTO`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_PAGAMENTO` (`id_pagamento`) | Código interno do recebimento. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `ID_VENDA` — vínculo RECEBE | Venda que recebeu o valor. Tipo: `integer`; obrigatório: Sim (FK). | FK para VENDA. Exatamente uma. |
| `NR_PARCELA` — vínculo QUITA | Parcela quitada, quando houver. Tipo: `smallint`; obrigatório: Não (FK composta). | FK composta (ID_VENDA, NR_PARCELA) para PARCELA; nula quando não quita parcela específica. |
| `VL_PAGAMENTO` (`valor`) | Quantia recebida nesta operação (campo “Sinal/Pago” é o primeiro pagamento). Tipo: `decimal(10,2)`; obrigatório: Sim. | Maior que zero. Pagamento parcial é aceito. |
| `TP_FORMA` (`forma`) | Meio pelo qual o cliente pagou. Tipo: `varchar(10)`; obrigatório: Sim. | Domínio: PIX, DINHEIRO, DEBITO, CREDITO (relatado na entrevista). O parcelamento é tratado em PARCELA. |
| `DT_PAGAMENTO` (`data_pagamento`) | Data em que o recebimento ocorreu. Tipo: `date`; obrigatório: Sim. | Registro proposto para acompanhar pagamentos parciais. |

> RN-11: soma dos pagamentos de uma venda ≤ VL_TOTAL.

### FORNECEDOR

Empresa da qual a ótica solicita armações e lentes. O gerente faz as solicitações por ligação ou mensagem. **Identificação:** `@ID_FORNECEDOR`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_FORNECEDOR` (`id_fornecedor`) | Código interno do fornecedor. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `NM_FORNECEDOR` (`nome`) | Nome pelo qual a ótica identifica o fornecedor. Tipo: `varchar(120)`; obrigatório: Sim. | Confirmado na entrevista. |
| `NR_CNPJ` (`cnpj`) | CNPJ somente dígitos. Tipo: `char(14)`; obrigatório: Não. | † Registro pela ótica não confirmado. Se informado, 14 dígitos válidos e único. |
| `DS_ENDERECO` (`endereco`) | Endereço do fornecedor em texto. Tipo: `varchar(200)`; obrigatório: Não. | † Registro pela ótica não confirmado. |
| `DS_CONTATO` (`contato`) | Telefone ou canal de mensagem usado para pedir produtos. Tipo: `varchar(120)`; obrigatório: Não. | Confirmado: o contato é registrado e usado nas solicitações. |

### COMPRA

Solicitação de produtos a um fornecedor para atender um pedido de cliente que não pode ser feito só com estoque. **Identificação:** `@ID_COMPRA`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_COMPRA` (`id_compra`) | Código interno da solicitação. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `ID_FORNECEDOR` vínculo FORNECE | Fornecedor para o qual a compra foi feita. Tipo: `integer`; obrigatório: Sim (FK). | FK para FORNECEDOR. Exatamente um. |
| `ID_VENDA` — vínculo DEMANDA | Pedido de cliente que motivou a compra. Tipo: `integer`; obrigatório: Sim (FK). | RN-06: cada compra atende um único pedido. Um pedido pode ter zero ou várias compras. |
| `DT_PEDIDO` (`data_pedido`) | Data em que a ótica pediu os produtos ao fornecedor. Tipo: `date`; obrigatório: Sim. | Diferente da “Data da Compra” da venda. |
| `DT_CHEGADA` (`data_chegada`) | Data em que os produtos chegaram à ótica. Tipo: `date`; obrigatório: Não. | Nula até a chegada. Não é anterior a DT_PEDIDO. |
| `CD_STATUS` (`status`) | Situação da solicitação. Tipo: `varchar(15)`; obrigatório: Sim. | † Proposta: SOLICITADA, RECEBIDA, CANCELADA. |

> Dado derivado, não armazenado: valor total da compra = soma de quantidade × custo dos itens.

### ITEM_COMPRA

Linha de uma compra: produto, quantidade e custo. Entidade fraca de COMPRA. **Identificação:** `@ID_COMPRA + @NR_ITEM`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_COMPRA` — vínculo É COMPOSTA POR | Compra a que a linha pertence. Tipo: `integer`; obrigatório: Sim (PK, FK). | FK para COMPRA; parte da chave. |
| `NR_ITEM` (`numero_item`) | Número de ordem da linha na compra. Tipo: `smallint`; obrigatório: Sim (PK). | Sequencial a partir de 1. |
| `ID_PRODUTO` — vínculo REFERE-SE A | Produto solicitado. Tipo: `integer`; obrigatório: Sim (FK). | FK para PRODUTO. Exatamente um por linha. |
| `QT_ITEM` (`quantidade`) | Unidades solicitadas. Tipo: `integer`; obrigatório: Sim. | Maior que zero. |
| `VL_CUSTO_UNITARIO` (`custo_unitario`) | Custo de uma unidade, pago ao fornecedor. Tipo: `decimal(10,2)`; obrigatório: Sim. | † Confirmar com o gerente se o valor anotado é por unidade ou o total da linha. |

### PRODUTO

Armação ou lente que a ótica vende, compra e estoca. Generalização de LENTE e ARMACAO. **Identificação:** `@ID_PRODUTO`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_PRODUTO` (`id_produto`) | Código interno do produto. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `CD_TIPO` (`tipo`) | Categoria do produto. Tipo: `varchar(10)`; obrigatório: Sim. | Domínio: ARMACAO ou LENTE. Define em qual tabela de especialização o produto tem registro (RN-14). |
| `DS_REFERENCIA` (`referencia`) | Código ou modelo comercial (“Ref. Armação” no pedido). Tipo: `varchar(60)`; obrigatório: Sim. | † Formato e unicidade não confirmados. |
| `NM_MARCA` (`marca`) | Marca do produto. Tipo: `varchar(60)`; obrigatório: Não. | Existência de cadastro geral de marcas não confirmada. |

> Dado derivado, não armazenado: saldo disponível = soma das entradas − soma das saídas em MOVIMENTO_ESTOQUE.

### LENTE

Especialização de PRODUTO com os dados próprios de uma lente. **Identificação:** `@ID_PRODUTO (também FK para PRODUTO)`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_PRODUTO` — vínculo ESPECIALIZA-SE EM | Produto que é uma lente. Tipo: `integer`; obrigatório: Sim (PK, FK). | FK para PRODUTO com CD_TIPO = LENTE. |
| `VL_INDICE` (`indice`) | Índice de refração da lente (opções do formulário). Tipo: `decimal(3,2)`; obrigatório: Não. | Sem regra específica. |
| `DS_TRATAMENTO` (`tratamento`) | Tratamento aplicado (antirreflexo, filtro etc.). Tipo: `varchar(60)`; obrigatório: Não. | O formulário oferece opções; forma de registro no estoque a validar. |
| `DS_BLOCO` (`bloco`) | Característica de lente denominada bloco. Tipo: `varchar(30)`; obrigatório: Não. | † Significado e domínio a validar com a ótica. |

### ARMACAO

Especialização de PRODUTO com os dados próprios de uma armação. **Identificação:** `@ID_PRODUTO (também FK para PRODUTO)`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_PRODUTO` — vínculo ESPECIALIZA-SE EM | Produto que é uma armação. Tipo: `integer`; obrigatório: Sim (PK, FK). | FK para PRODUTO com CD_TIPO = ARMACAO. |
| `TP_ARMACAO` (`tipo_armacao`) | Tipo da armação escolhido pelo cliente (“Tipo de Armação”). Tipo: `varchar(40)`; obrigatório: Não. | Aplica-se só à armação. |
| `DS_MATERIAL` (`material`) | Material da armação. Tipo: `varchar(40)`; obrigatório: Não. | † Uso pela ótica não confirmado. |

### TROCA_DEVOLUCAO

Ocorrência em que o cliente pede troca ou devolução de um item vendido, por dano ou outro motivo. **Identificação:** `@ID_OCORRENCIA`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_OCORRENCIA` (`id_ocorrencia`) | Código interno da ocorrência. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `ID_VENDA, NR_ITEM` — vínculo É OBJETO DE | Item vendido que motivou a ocorrência. Tipo: `integer + smallint`; obrigatório: Sim (FK composta). | FK composta para ITEM_VENDA. Um item pode ter zero ou várias ocorrências. |
| `DT_OCORRIDO` (`data_ocorrido`) | Data do fato que levou à troca ou devolução, anotada no pedido. Tipo: `date`; obrigatório: Sim. | Diferente da data do registro no sistema. |
| `TP_OCORRENCIA` (`tipo`) | Classificação da ocorrência. Tipo: `varchar(10)`; obrigatório: Sim. | Domínio: TROCA ou DEVOLUCAO. |
| `DS_DANO` (`descricao_dano`) | Descrição do que quebrou ou foi danificado. Tipo: `varchar(255)`; obrigatório: Não. | Obrigatória quando houver dano; ajuda a decidir se a peça é reaproveitável. |
| `VL_COBRADO` (`valor_cobrado`) | Quantia cobrada do cliente, quando houver. Tipo: `decimal(10,2)`; obrigatório: Não. | † A ótica cobra em alguns danos, inclusive por imprudência; valor e critério não detalhados. Padrão 0,00. |
| `CD_STATUS` (`status`) | Situação da ocorrência. Tipo: `varchar(15)`; obrigatório: Sim. | † Proposta: ABERTA, CONCLUIDA. |

> RN-08: na troca/devolução, peças intactas podem ser reaproveitadas e as demais são descartadas; ambos geram movimento de estoque.

### MOVIMENTO_ESTOQUE

Lançamento de entrada ou saída de um produto no estoque. O saldo é sempre calculado a partir dele. **Identificação:** `@ID_MOVIMENTO`.

| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_MOVIMENTO` (`id_movimento`) | Código interno do lançamento. Tipo: `integer`; obrigatório: Sim (PK). | Gerado pelo sistema. |
| `ID_PRODUTO` — vínculo É MOVIMENTADO EM | Produto movimentado. Tipo: `integer`; obrigatório: Sim (FK). | FK para PRODUTO. Exatamente um. |
| `DT_MOVIMENTO` (`data`) | Data do lançamento no controle de estoque. Tipo: `date`; obrigatório: Sim. | Sem regra específica. |
| `QT_MOVIMENTO` (`quantidade`) | Unidades movimentadas. Tipo: `integer`; obrigatório: Sim. | Sempre positiva; o sinal vem da direção. |
| `CD_DIRECAO` (`direcao`) | Efeito no saldo. Tipo: `varchar(7)`; obrigatório: Sim. | Domínio: ENTRADA ou SAIDA. |
| `CD_MOTIVO` (`motivo`) | Por que o movimento aconteceu. Tipo: `varchar(20)`; obrigatório: Sim. | Domínio: COMPRA, VENDA, REAPROVEITAMENTO, DESCARTE, AJUSTE (†). Define a origem obrigatória (RN-12). |
| `ID_VENDA, NR_ITEM_VENDA` — vínculo GERA SAÍDA | Item de venda que gerou a saída. Tipo: `integer + smallint`; obrigatório: Não (FK composta). | Obrigatória quando CD_MOTIVO = VENDA. |
| `ID_COMPRA, NR_ITEM_COMPRA` — vínculo GERA ENTRADA | Item de compra que gerou a entrada. Tipo: `integer + smallint`; obrigatório: Não (FK composta). | Obrigatória quando CD_MOTIVO = COMPRA. |
| `ID_OCORRENCIA` — vínculo ORIGINA | Troca ou devolução que originou o movimento. Tipo: `integer`; obrigatório: Não (FK). | Obrigatória quando CD_MOTIVO = REAPROVEITAMENTO ou DESCARTE. |

> RN-12: COMPRA → entrada com item de compra; VENDA → saída com item de venda; REAPROVEITAMENTO → entrada com troca; DESCARTE → saída com troca; AJUSTE → sem origem. Exatamente uma origem, exceto AJUSTE.


---

## 6. Modelagem Conceitual (Entidades, Atributos, Relacionamentos)

- **Entidades reconhecidas (17):**

| Entidade | Por que existe |
| --- | --- |
| CLIENTE | Quem solicita atendimento; seus dados aparecem no pedido. |
| FUNCIONARIO | Quem conduz o atendimento (optometrista, gerente, consultor). |
| ATENDIMENTO | Evento que antecede qualquer receita ou venda; guarda o histórico mesmo quando não há venda. Associativa entre CLIENTE e FUNCIONARIO. |
| RECEITA | Prescrição trazida ou laudo produzido na ótica; tem data para a regra de 1 ano. |
| RECEITA_MEDIDA | Medidas por olho e por distância; entidade fraca de RECEITA. |
| VENDA | Pedido: valores, montagem, retirada e garantia. |
| ITEM_VENDA | Linha do pedido (armação ou par de lentes); entidade fraca de VENDA. |
| PARCELA | Valor futuro combinado; entidade fraca de VENDA. |
| PAGAMENTO | Valor efetivamente recebido, inclusive o sinal. |
| FORNECEDOR | Quem fornece armações e lentes. |
| COMPRA | Solicitação ao fornecedor para atender um pedido. |
| ITEM_COMPRA | Linha da compra; entidade fraca de COMPRA. |
| PRODUTO | Armação ou lente; generalização de LENTE e ARMACAO. |
| LENTE e ARMACAO | Dados próprios de cada tipo de produto. |
| TROCA_DEVOLUCAO | Ocorrência sobre um item vendido. |
| MOVIMENTO_ESTOQUE | Entradas e saídas, origem do saldo de estoque. |

- **Atributos e classificações:** os atributos de cada entidade estão na Seção 5. Classificam-se em **identificadores** (inclusive compostos em `RECEITA_MEDIDA`, `ITEM_VENDA`, `ITEM_COMPRA` e `PARCELA`), **obrigatórios**, **opcionais** (datas de montagem e retirada, observações, dados de contato) e **derivados, que não são armazenados**: saldo de estoque, valor pago, saldo a pagar, fim da garantia e valor total da compra.
- **Relacionamentos pertinentes:**

| Entidade A | Card. A | Relacionamento | Entidade B | Card. B |
| --- | --- | --- | --- | --- |
| CLIENTE | (0,n) | SOLICITA | ATENDIMENTO | (1,1) |
| FUNCIONARIO | (0,n) | CONDUZ | ATENDIMENTO | (1,1) |
| ATENDIMENTO | (0,1) | ORIGINA | RECEITA | (1,1) |
| RECEITA | (1,n) | POSSUI | RECEITA_MEDIDA | (1,1) |
| ATENDIMENTO | (0,1) | RESULTA EM | VENDA | (1,1) |
| RECEITA | (0,1) | É USADA EM | VENDA | (0,1) |
| VENDA | (0,n) | É PARCELADA EM | PARCELA | (1,1) |
| VENDA | (0,n) | RECEBE | PAGAMENTO | (1,1) |
| PARCELA | (0,n) | QUITA | PAGAMENTO | (0,1) |
| VENDA | (1,n) | É COMPOSTA POR | ITEM_VENDA | (1,1) |
| PRODUTO | (0,n) | REFERE-SE A | ITEM_VENDA | (1,1) |
| VENDA | (0,n) | DEMANDA | COMPRA | (1,1) |
| FORNECEDOR | (0,n) | FORNECE | COMPRA | (1,1) |
| COMPRA | (1,n) | É COMPOSTA POR | ITEM_COMPRA | (1,1) |
| PRODUTO | (0,n) | REFERE-SE A | ITEM_COMPRA | (1,1) |
| PRODUTO | (0,1) | ESPECIALIZA-SE EM | LENTE | (1,1) |
| PRODUTO | (0,1) | ESPECIALIZA-SE EM | ARMACAO | (1,1) |
| PRODUTO | (0,n) | É MOVIMENTADO EM | MOVIMENTO_ESTOQUE | (1,1) |
| ITEM_VENDA | (0,n) | É OBJETO DE | TROCA_DEVOLUCAO | (1,1) |
| ITEM_VENDA | (0,n) | GERA SAÍDA | MOVIMENTO_ESTOQUE | (0,1) |
| ITEM_COMPRA | (0,n) | GERA ENTRADA | MOVIMENTO_ESTOQUE | (0,1) |
| TROCA_DEVOLUCAO | (0,n) | ORIGINA | MOVIMENTO_ESTOQUE | (0,1) |

- **Restrições e políticas organizacionais aplicadas ao modelo:** receita opcional na venda (RN-09) e de uso exclusivo (RN-02); compra sempre ligada a um pedido (RN-06); garantia calculada da montagem (RN-07); medidas por olho e distância com no máximo 4 linhas por receita (RN-10, RN-13); pagamentos limitados ao total (RN-11); origem do movimento de estoque conforme o motivo (RN-12); produto lente ou armação (RN-14).

---

## 7. Diagrama Entidade-Relacionamento (DER)

  <img src="DER_Otica_Kadosh_Atualizado_Alta_Resolucao.jpeg" alt="DER da Ótica Kadosh" width="100%">


O DER foi elaborado no **brModelo** e mostra as 17 entidades, seus atributos (identificadores com círculo preenchido), os relacionamentos nomeados e as cardinalidades (mínimo, máximo) junto de cada entidade. A tabela de cardinalidades está na Seção 6.

---

## 8. Justificativa Técnica

**Atendimento como entidade própria.** Poderia ser só um atributo de VENDA, mas a ótica faz cerca de 100 atendimentos e 80 vendas por semana; os atendimentos sem venda (e as receitas deles) se perderiam. Como a RN-01 diz que não há venda sem atendimento, VENDA liga-se a ATENDIMENTO (0,1 – 1,1). Por isso **CLIENTE não se liga diretamente a VENDA**: o cliente chega à venda pelo atendimento, e uma segunda ligação criaria redundância e risco de inconsistência.

**Receita separada e opcional na venda.** Receita tem ciclo próprio (data e origem, com a regra de 1 ano), então é entidade, e não colunas de VENDA. A ligação receita–venda é (0,1) dos dois lados: a receita pode nunca virar venda, uma venda pode não ter receita (óculos de sol sem grau, RN-09), e a mesma receita não se repete em outro pedido (RN-02).

**RECEITA_MEDIDA como entidade fraca.** A alternativa era colocar colunas por olho e distância na receita (`esferico_od_longe`, `esferico_oe_perto`…), que repete grupos e dificulta consultas. Com a chave composta *receita + olho + distância*, o modelo aceita de 1 a 4 linhas, impede duplicar uma combinação e guarda DNP e altura por olho, como o gerente confirmou. A cardinalidade (1,n) do lado da receita é o que o brModelo permite; o limite de 4 é a RN-10, garantida pela chave.

**VENDA, ITEM_VENDA e ITEM_COMPRA.** Pedido e venda são a mesma entidade, pois a ótica tem um formulário só; a etapa do pedido fica no status. Os itens são entidades fracas com identificação composta (documento + número da linha), que reflete as linhas do formulário e do pedido ao fornecedor. A cardinalidade (1,n) do lado da venda e da compra impede pedido ou compra vazios.

**PRODUTO como generalização.** Armações e lentes têm características diferentes (material e tipo de um lado, índice, tratamento e bloco do outro), mas ITEM_VENDA, ITEM_COMPRA e MOVIMENTO_ESTOQUE as tratam do mesmo jeito. Uma tabela única teria muitos campos nulos e duas entidades separadas duplicariam relacionamentos. A generalização disjunta e total (RN-14), com `tipo` como discriminador, resolve os dois problemas.

**PARCELA e PAGAMENTO separados.** Parcela é o que foi combinado e ainda vai ser pago; pagamento é o que foi recebido, inclusive o sinal e valores parciais. Com um só registro, as parcelas futuras da planilha da ótica não teriam onde ficar. O pagamento pode ou não quitar uma parcela (0,1), e a parcela pode ser quitada por vários pagamentos (0,n).

**COMPRA ligada à VENDA.** A ótica relatou que cada compra atende um único pedido e que um pedido pode não gerar compra. Daí VENDA (0,n) e COMPRA (1,1), e a compra tem fornecedor obrigatório (FORNECEDOR 0,n – COMPRA 1,1).

**Estoque por movimentos.** Gravar o saldo em PRODUTO criaria um segundo número editável, que diverge das entradas e saídas. O saldo é **derivado** dos movimentos. Direção (entrada ou saída) e motivo (compra, venda, reaproveitamento, descarte, ajuste) ficam em campos separados; o motivo define de qual item ou troca o movimento vem (RN-12). Isso permite rastrear a origem de cada saldo.

**TROCA_DEVOLUCAO ligada ao item vendido.** A troca ocorre sobre uma peça específica, não sobre o pedido inteiro; ligar ao ITEM_VENDA (0,n – 1,1) identifica o que foi trocado. Peças reaproveitadas ou descartadas geram movimento de estoque (RN-08).

**Derivados não armazenados.** Saldo de estoque, valor pago, saldo a pagar, fim da garantia e total da compra são calculados. Armazená-los criaria divergências entre o total e suas origens.

**Escalabilidade e integração.** O modelo separa cadastro, documentos e movimentos, o que permite, nas próximas etapas, converter para o modelo lógico sem reestruturar; acrescentar novos perfis, meios de pagamento ou produtos é inserir domínio, e não mudar estrutura. A trilha de auditoria (RNF-05) entra na fase lógica, fora do DER conceitual.

---

## 9. Uso de Inteligência Artificial

O grupo usou ferramentas de IA em várias etapas e registra cada uso abaixo. As decisões de modelagem e o levantamento de campo são do grupo.

### Uso 1 — análise do material inicial

| Item | Registro |
| --- | --- |
| **Ferramenta e etapa** | ChatGPT, para entender o projeto, organizar o trabalho e preparar perguntas ao gerente da ótica. |
| **Motivação** | O grupo precisava entender por onde começar e como conduzir a pesquisa da Entrega 1. |
| **Prompt(s) utilizados** | "Baseado no arquivo do Esqueleto 1, atue como professor de modelagem de dados: quais são as perguntas interessantes a fazer para a ótica?" |
| **Resposta recebida** | Um roteiro com 40 perguntas sobre a rotina da ótica e orientação para organizar o trabalho. |
| **Fontes consultadas e verificadas** | Da [pasta de materiais do professor](https://drive.google.com/drive/folders/1QVVdiG4LxFE7L3BSnZDFmHyakaoPX94A), o grupo consultou o Esqueleto da Entrega 1 e comparou a estrutura do README com ele. |
| **Trechos rejeitados ou corrigidos** | Uma proposta com cerca de 120 perguntas foi reduzida para respeitar o tempo do gerente. Uma estrutura de README fora do Esqueleto foi descartada. |
| **Justificativa da escolha final** | 40 perguntas bastavam para investigar a rotina sem tornar a entrevista longa; o README seguiu o Esqueleto. |
| **Reflexão crítica** | A IA ajudou a planejar, mas sugeriu informações e uma estrutura que não correspondiam ao trabalho; o grupo selecionou as perguntas e conferiu o material. |

### Uso 2 — primeira versão do DER

| Item | Registro |
| --- | --- |
| **Ferramenta e etapa** | ChatGPT e Claude como apoio; brModelo para desenhar o DER. Claude também ajudou a converter o PDF exportado em JPEG e a melhorar a legibilidade. |
| **Motivação** | Ter uma base para compreender o fluxo da ótica e depois desenhar e revisar o diagrama no brModelo. |
| **Prompt(s) utilizados** | "Com base nessas respostas, crie um DER no modelo do brModelo"; "aprimore as informações do DER"; "transforme esse arquivo PDF em JPEG e melhore a qualidade da imagem". |
| **Resposta recebida** | Uma proposta inicial de DER, depois ampliada com atributos e relações, e uma versão JPEG da imagem. |
| **Fontes consultadas e verificadas** | O Esqueleto da Entrega 1 e as respostas da entrevista com o gerente. |
| **Trechos rejeitados ou corrigidos** | O primeiro DER era simples demais, e uma proposta posterior representava incorretamente informações fornecidas; o grupo revisou o desenho no brModelo. |
| **Justificativa da escolha final** | A proposta serviu de ponto de partida e foi ampliada e corrigida para refletir os dados e processos levantados. |
| **Reflexão crítica** | Os primeiros resultados não atenderam; a IA não conhece a ótica, e só a entrevista permitiu corrigir o modelo. |

### Uso 3 — base do README

| Item | Registro |
| --- | --- |
| **Ferramenta e etapa** | ChatGPT, para criar uma base do README. |
| **Motivação** | Organizar no GitHub o material já levantado. |
| **Prompt(s) utilizados** | "Com o DER criado e as perguntas, analise o Esqueleto 1 e crie um DER base para o GitHub." |
| **Resposta recebida** | Uma base de texto e o código de apoio à organização no GitHub. |
| **Fontes consultadas e verificadas** | Esqueleto da Entrega 1, comparado com a estrutura do README. |
| **Trechos rejeitados ou corrigidos** | Frases reescritas por não expressarem com clareza o que o grupo queria relatar. |
| **Justificativa da escolha final** | O README foi mantido como arquivo principal de apresentação. |
| **Reflexão crítica** | A IA ajudou a estruturar o texto; o grupo revisou cada frase antes de aceitar. |

### Uso 4 — alinhamento entre DER e dicionário

| Item | Registro |
| --- | --- |
| **Ferramenta e etapa** | ChatGPT, Codex e Claude, para comparar DER e dicionário; o dicionário em HTML inicial foi criado com ChatGPT. |
| **Motivação** | Verificar se DER e dicionário se complementavam e achar diferenças. |
| **Prompt(s) utilizados** | "Atue como especialista em modelagem de dados, analise os dois arquivos anexados, indique o que está divergente e crie um dicionário em HTML com o README e o DER anexados." |
| **Resposta recebida** | Análise das diferenças (atributos ausentes no DER) e uma versão do dicionário em HTML. |
| **Fontes consultadas e verificadas** | O Esqueleto e o DER do grupo; os nomes de entidades e atributos foram conferidos um a um. |
| **Trechos rejeitados ou corrigidos** | Foram acrescentados `ITEM_VENDA` e o registro de devolução, e retirada uma ligação direta entre RECEITA e CLIENTE. |
| **Justificativa da escolha final** | A comparação mostrou itens do dicionário que não estavam no desenho. |
| **Reflexão crítica** | A IA tornou as divergências visíveis, mas corrigir relacionamentos e cardinalidades exigiu alterar o DER, o que o grupo fez na etapa seguinte. |

### Uso 5 — imagem do DER no README

| Item | Registro |
| --- | --- |
| **Ferramenta e etapa** | ChatGPT, Codex e Claude, para orientar a inserção da imagem do DER no README. |
| **Motivação** | Dificuldade em inserir no README a imagem exportada. |
| **Prompt(s) utilizados** | "Atue como professor e me auxilie a organizar a imagem do DER no README." |
| **Resposta recebida** | Passo a passo e formas de organizar a imagem no repositório. |
| **Fontes consultadas e verificadas** | [Vídeo sobre inserção de imagens no GitHub](https://youtu.be/9ygf4hkLVnA?si=iCP3OWCSNehCurkn). |
| **Trechos rejeitados ou corrigidos** | A sugestão de manter a imagem em outro repositório foi rejeitada. |
| **Justificativa da escolha final** | Manter imagem e README no mesmo repositório facilita a visualização. |
| **Reflexão crítica** | A solução mais simples bastava; usar vários repositórios acrescentava trabalho sem benefício. |

### Uso 6 — avaliação crítica, correção do DER, dicionário e README

| Item | Registro |
| --- | --- |
| **Ferramenta e etapa** | Claude (Anthropic), em avaliação crítica do README, do DER e do dicionário, e na redação do dicionário em HTML e deste README. |
| **Motivação** | Receber uma avaliação rigorosa, no papel de professor de modelagem, antes da entrega, e corrigir os problemas apontados. |
| **Prompt(s) utilizados** | "Quero que aja como um avaliador/professor de modelagem, nível muito exigente, e avalie esse meu trabalho"; "Crie um DER correto e coerente, usando o DER que já montei e colocando essas informações"; "Verifica agora, por favor" (a cada nova exportação do DER); "Monte um dicionário correto, com todas as informações, que não esteja vazio"; "Faça o README para mim, em base do que foi falado aqui". |
| **Resposta recebida** | Lista de erros do DER (cardinalidades invertidas, chaves compostas incompletas, chaves estrangeiras como atributo, atributos derivados e duplicados), uma proposta de DER corrigido, conferências a cada nova versão do PDF, o dicionário em HTML e este README. |
| **Fontes consultadas e verificadas** | O grupo conferiu cada apontamento no brModelo, reexportou o DER várias vezes e o submeteu a nova conferência; as regras RN-09 e RN-13 e os domínios (formas de pagamento, funções, OD/OE) vêm da entrevista e das respostas do gerente. |
| **Trechos rejeitados ou corrigidos** | A IA sugeriu cardinalidade (1,4), que o brModelo não oferece; o grupo usou (1,n) e registrou o limite de 4 como regra (RN-10). O grupo corrigiu manualmente o DER e removeu do dicionário a tabela de pendências. |
| **Justificativa da escolha final** | Mantivemos as correções que removem erros reais do DER e as decisões marcadas com † no dicionário, para deixar claro o que ainda não foi validado com a ótica. |
| **Reflexão crítica** | A IA leu o DER por imagem ampliada e chegou a ler uma etiqueta cortada, por isso as conferências foram repetidas a cada versão. Também não teve acesso à pasta de aulas do Drive. Tipos, tamanhos, listas de status, perfis de acesso e prazos de retenção são hipóteses de projeto e foram marcados com †, pois só a ótica pode confirmá-los. |

---

## Critérios Atitudinais (20%)
**Estes critérios NÃO constam explicitamente como item de entrega no README.** Eles são avaliados por meio de **Avaliação 360º entre os integrantes do grupo** (cada membro avalia os colegas de equipe) e, no caso da Colaboração, também pela **colaboração equilibrada no histórico de commits** do repositório GitHub — não pela leitura do restante do repositório nem pela apresentação:

- **Participação (5%):** envolvimento nas discussões técnicas e nas decisões do grupo.
- **Comprometimento (5%):** cumprimento de prazos e responsabilidades assumidas.
- **Colaboração (5%):** respeito às contribuições dos colegas, cooperação na construção do projeto e colaboração equilibrada no histórico de commits do repositório GitHub.
- **Autonomia (5%):** busca independente de soluções e proposta de melhorias.

---

## Resumo dos Pesos

| Dimensão | Peso total |
| --- | --- |
| Conceitual (contexto, requisitos/regras, modelagem, justificativa técnica) | 30% |
| Procedimental (requisitos, fluxogramas, dicionário de dados, DER) | 50% |
| Atitudinal (participação, comprometimento, colaboração, autonomia) | 20% |

**Entrega final:** README.md completo + DER + Dicionário de Dados em HTML (com exceção dos cursos GTI) anexado no repositório GitHub do grupo.
