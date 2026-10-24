

# Entrega 1 — Modelo Conceitual (DER)
### Modelagem de um sistema de gestão de informações para uma organização de pequeno porte

**Organização estudada: Ótica Kadosh** · Projeto acadêmico de Modelagem de Dados

---

## Metadados

- **Nomes dos alunos e RGM**

| Integrante | RGM | Usuário no GitHub |
| --- | --- | --- |
| Victor Augusto Silva Marcilio | 47190175 | [Victordev14](https://github.com/Victordev14) |
| João Felipe de Sousa Pires | 48165379 | [jfpiresoficial](https://github.com/jfpiresoficial) |
| Cauã Batista Freire | 48355127 | [cauabf-prev](https://github.com/cauabf-prev) |
| João Victor Gobi Romero | 48114642 | [joaovromero](https://github.com/joaovromero) |
| Guilherme Araujo de Oliveira | 47116862 | [GK-300](https://github.com/GK-300) |

---

## 1. Caracterização da Organização

- **Nome e natureza da organização:** **Ótica Kadosh**, estabelecimento comercial **com fins lucrativos** que vende produtos ópticos (armações e lentes). Fica na Av. Diogo da Costa Tavares, 125, Jardim Romano, São Paulo/SP, CEP 08191-000.
- **Contexto e porte:** pequeno comércio com **três funcionários**: um optometrista (**Guilherme de Souza Silva**), um gerente (**Marcos Vinícius Silva Menezes**) e um consultor óptico (**Kaique Batista dos Santos**). O gerente informou cerca de **100 atendimentos e 80 vendas por semana**, o que indica que parte dos atendimentos não termina em venda. A ótica atende clientes presencialmente, vende armações e lentes, recebe pagamentos à vista, parcelados ou em partes, mantém estoque, compra de fornecedores quando falta produto e trata trocas e devoluções.
- **Problemas e necessidades identificados:** pedidos, estoque e parcelas são controlados em **papel e planilhas separadas**, e um banco de dados usado antes apresentava falhas frequentes. Hoje não há vínculo seguro entre atendimento, receita, pedido, pagamentos, compras ao fornecedor, estoque e trocas, e cada consulta exige abrir vários registros. O sistema precisa relacionar tudo isso, saber o saldo de estoque e o saldo a pagar de cada pedido e proteger os dados de saúde dos clientes. Os problemas de gestão estão numerados de P1 a P5 na tabela ao final desta seção.
- **Justificativa da escolha:** o grupo tem acesso presencial à ótica e ao gerente. O negócio é pequeno o bastante para o primeiro DER, mas tem processos encadeados e observáveis (atendimento, receita, venda, pagamento, compra, montagem, retirada, garantia e troca) que exigem relacionamentos variados: 1:1, 1:N, entidades fracas e generalização.
- **Evidências da organização:**
  - Endereço: Av. Diogo da Costa Tavares, 125, Jardim Romano, São Paulo/SP.
  - Contato da loja: (11) 99349-4371. Entrevistado: **Marcos Vinícius Silva Menezes**, gerente.
  - **Data da visita e entrevista:** 05/09/2026, presencial, com observação do formulário de pedido, do comprovante entregue ao cliente e do laudo produzido na ótica. Depois da visita, o gerente respondeu por mensagem a dúvidas pontuais (venda sem receita e medidas por olho).
  - Fotografia feita no interior da ótica durante a visita: [Fotografia da visita](https://github.com/jfpiresoficial/otica-kadosh-modelagem-dados/blob/main/Otica%20kadoshi.jpeg).
  - As fotos do formulário e do laudo contêm dados pessoais e de saúde reais; por isso **não foram publicadas**.

**Problemas de gestão numerados.** Cada um aparece no DER e terá ao menos uma consulta gerencial no script SQL. Os processos de negócio da Seção 2 usam o prefixo PR para não se confundir com estes códigos.

| Código | Problema | Onde aparece no DER |
| --- | --- | --- |
| P1 | Pedidos, receitas e pagamentos ficam em papel e planilhas separadas, sem vínculo seguro entre atendimento, orçamento, venda e pagamento; cada consulta exige abrir vários registros. | CLIENTE, ATENDIMENTO, RECEITA, ORCAMENTO, VENDA, PAGAMENTO |
| P2 | O saldo de estoque de armações e lentes não é controlado de forma segura. | PRODUTO, MOVIMENTO_ESTOQUE, COMPRA |
| P3 | A garantia não tem controle por produto vendido: um ano para a armação e seis meses para a lente, contados da montagem (RN-07). | VENDA, CONTÉM, PRODUTO, LENTE, ARMACAO |
| P4 | A conversão de atendimentos em vendas não é medida; a loja faz cerca de 100 atendimentos e 80 vendas por semana. | ATENDIMENTO, VENDA |
| P5 | Os dados de saúde das receitas precisam de proteção; lente de grau só é vendida com receita (RN-16). | RECEITA, RECEITA_MEDIDA, VENDA, LENTE |

---





## 2. Processos de Negócio


**Principais processos mapeados:**


| ID | Processo | Entrada | Sequência e responsável | Saída e integração |
| --- | --- | --- | --- | --- |
| PR01 | Cadastro e atendimento | Cliente procura a loja. | Funcionário consulta/cadastra CLIENTE e registra ATENDIMENTO. | Histórico do cliente, mesmo sem venda. |
| PR02 | Receita e medidas | Receita trazida ou avaliação interna. | Registrar RECEITA, origem, data, emissor interno quando houver e medidas OD/OE × LONGE/PERTO. | Prescrição acessível pelo atendimento, com acesso restrito. |
| PR03 | Orçamento | Seleção de produtos e quantidades. | Consultor registra ORCAMENTO e condições em OFERECE; informa validade e registra aprovação. | Oferta preservada mesmo sem conversão. |
| PR04 | Venda | Orçamento aprovado e válido. | Converter em VENDA do mesmo atendimento; registrar linhas de CONTÉM, preços, quantidades e total. | Pedido comercial rastreável, com receita quando exigida. |
| PR05 | Sinal e parcelas | Condição de pagamento acordada. | Registrar PAGAMENTO; sinal pode gerar parcelas futuras por GERA; recebimento posterior pode QUITA uma parcela. | Plano do saldo sem duplicação do sinal. |
| PR06 | Compras e fornecedores | Reposição ou necessidade de uma venda. | Gerente registra COMPRA, FORNECEDOR e produtos em ADQUIRE; registra chegada. | Compra pode existir sem venda; recebimento gera entrada. |
| PR07 | Estoque | Compra recebida, venda executada ou pós-venda aceito. | Registrar MOVIMENTO_ESTOQUE com produto, quantidade, condição, direção e uma origem. | Saldos disponível e segregado calculados sem dupla baixa. |
| PR08 | Encomenda e montagem | Sinal suficiente e previsão informada. | Registrar liberação, envio ao fornecedor e montagem/finalização. | Datas previstas e realizadas preservadas; início da garantia comercial. |
| PR09 | Retirada | Óculos prontos e canhoto apresentado. | Conferir canhoto e registrar retirada efetiva. | Entrega registrada; previsão não se confunde com realização. |
| PR10 | Manutenção | Solicitação de ajustes após a entrega. | Registrar atendimento de manutenção e serviço realizado. | Histórico do suporte gratuito relatado. |
| PR11 | Troca, devolução e garantia | Solicitação referente a produto vendido. | Registrar TROCA_DEVOLUCAO, linha afetada, avaliação e decisão; executar movimentos/acertos autorizados. | Retorno, substituição e descarte rastreados; recusas preservadas. |
| PR12 | Cancelamento e referência fiscal | Solicitação de desistência ou emissão fiscal externa. | Registrar instantes para análise comercial e referência do documento fiscal emitido. | Decisão auditável e referência fiscal; sem presumir integração externa. |


**Fluxogramas:** a representação gráfica é opcional no esqueleto. O grupo documenta os processos em sequência textual na tabela acima, sem fluxograma. O levantamento não confirmou laboratório externo independente do fornecedor nem ordem de serviço; essas entidades não foram acrescentadas.


## 3. Requisitos do Sistema


### 3.1 Requisitos Funcionais


| ID | O sistema deve permitir | Cobertura no modelo |
| --- | --- | --- |
| RF-01 | Cadastrar e consultar clientes e seus contatos. | CLIENTE |
| RF-02 | Registrar atendimentos vinculados a cliente e funcionário, inclusive manutenção sem venda. | ATENDIMENTO, SOLICITA e CONDUZ |
| RF-03 | Registrar receita, origem, data, emissor interno e medidas por olho/distância. | RECEITA, RECEITA_MEDIDA, ORIGINA, EMISSOR DE e POSSUI |
| RF-04 | Conferir receita exigida para lente de grau pelo atendimento da venda. | LENTE.possui_grau; RN-02, RN-03 e RN-16 |
| RF-05 | Emitir e guardar orçamentos com produtos, quantidades, preços, aprovação e validade. | ORCAMENTO e OFERECE |
| RF-06 | Registrar venda originada de orçamento e atendimento, com linhas de produto e total. | VENDA, CONTÉM e RN-31 |
| RF-07 | Registrar sinal e demais recebimentos sem exceder o saldo devido. | PAGAMENTO e RECEBE |
| RF-08 | Gerar parcelas futuras a partir do sinal e registrar sua quitação posterior. | PARCELA, GERA e QUITA |
| RF-09 | Cadastrar fornecedores e compras de reposição ou por demanda de venda. | FORNECEDOR, COMPRA, ADQUIRE e DEMANDA |
| RF-10 | Registrar movimentos e consultar saldo por produto e condição. | MOVIMENTO_ESTOQUE; RN-12 e RN-30 |
| RF-11 | Registrar previsão, liberação da encomenda, envio, montagem e retirada. | Datas e horários de VENDA; chegada de COMPRA |
| RF-12 | Registrar conferência do canhoto e gerar comprovante resumido do pedido. | VENDA.canhoto_conferido e dados da venda |
| RF-13 | Calcular garantia comercial por produto vendido, a partir da montagem. | PRODUTO, CONTÉM e VENDA.data_montagem_finalizacao |
| RF-14 | Registrar avaliação, aprovação ou recusa de troca/devolução e respectivos movimentos. | TROCA_DEVOLUCAO e ORIGINA |
| RF-15 | Registrar acertos financeiros autorizados e conciliar o saldo sem apagar pagamentos. | Campos financeiros da ocorrência; RN-11 e RN-33 |
| RF-16 | Consultar histórico integrado de atendimento, orçamento, receita, venda e recebimentos. | Relacionamentos do DER |
| RF-17 | Registrar solicitação de cancelamento e referência de documento fiscal emitido externamente. | Campos específicos de VENDA |
| RF-18 | Controlar acesso por perfil e auditar leituras sensíveis e alterações. | Política proposta do dicionário HTML, seções 5 e 6 |


### 3.2 Requisitos Não Funcionais


Os requisitos de qualidade são propostas técnicas para orientar a implementação futura; não descrevem recursos já instalados na loja.


| ID | Característica | Critério proposto |
| --- | --- | --- |
| RNF-01 | Segurança e privacidade | Acesso individual e por perfil, com mínimo necessário e proteção de dados de saúde. |
| RNF-02 | Integridade | Validar identificadores, vínculos, totalização, XOR de origens e compatibilidade dos caminhos. |
| RNF-03 | Recuperação | Proposta técnica: cópia de segurança diária e teste periódico de restauração; retenção e infraestrutura a definir com a loja. |
| RNF-04 | Usabilidade | Permitir localizar cliente, histórico e situação do pedido em uma consulta integrada; validar a interface com a equipe. |
| RNF-05 | Rastreabilidade | Registrar autor, instante, operação, objeto e resultado; proteger registros de auditoria. |
| RNF-06 | Desempenho | Projetar índices para consultas por cliente, período e produto; medir desempenho na implementação, sem afirmar meta não validada. |
| RNF-07 | Disponibilidade | Planejar operação durante o horário de atendimento e recuperação de falhas; níveis de serviço ainda não contratados. |


## 4. Regras de Negócio


**Regras operacionais:**


| ID | Regra | Origem |
| --- | --- | --- |
| RN-01 | Toda venda pertence a um atendimento; um atendimento pode não resultar em venda e resulta em no máximo uma. | Levantamento e DER |
| RN-02 | A receita é obtida pelo atendimento da venda, sem ligação direta RECEITA–VENDA. Quando exigida, deve pertencer ao mesmo atendimento e cliente; a prescrição daquele pedido não é reutilizada em outro pedido. | Levantamento; ajuste do professor |
| RN-03 | A ótica aceita receita trazida com até um ano da emissão na data de aceitação do pedido; caso contrário, realiza novo teste. Trata-se de prática relatada, sem definir validade legal geral. | Entrevista |
| RN-04 | Os preços são por armação e por par de lentes. O total original da venda é a soma das quantidades multiplicadas pelos preços das linhas de CONTÉM. | Formulário e entrevista |
| RN-05 | A venda pode ter pagamentos em momentos diferentes. PAGAMENTO representa recebimento; PARCELA representa compromisso futuro. | Entrevista e modelagem |
| RN-06 | A venda pode usar estoque e não gerar compra. COMPRA possui um fornecedor e pode atender uma venda ou repor estoque sem venda de origem. | Confirmação do grupo e DER final |
| RN-07 | A garantia comercial relatada começa na montagem/finalização: um ano para armação e seis meses para lente; calcular por produto vendido. | Entrevista |
| RN-08 | Em troca ou devolução aceita, peças intactas podem ser reaproveitadas e peças sem reaproveitamento são descartadas, com movimentos separados. | Entrevista |
| RN-09 | Venda sem lente de grau pode não possuir receita, como no caso relatado de óculos de sol sem grau. | Resposta do gerente |
| RN-10 | Cada receita possui de uma a quatro medidas: uma por combinação de OD/OE e LONGE/PERTO. A chave composta impede combinação repetida; validar o mínimo ao concluir o cadastro. | Laudo e modelagem |
| RN-11 | Recebimentos não devem exceder o saldo devido. Pagamentos originais são preservados; cobranças, abatimentos e restituições autorizados são conciliados separadamente. | Decisão técnica de integridade |
| RN-12 | Movimentos têm quantidade positiva, direção, condição e motivo compatíveis. Saída não pode exceder o saldo da condição movimentada; retorno, substituição e descarte não repetem a baixa original. | Modelagem do estoque |
| RN-13 | DNP e altura são registradas por olho. Se repetidas entre longe e perto para o mesmo olho, manter coerência, salvo diferenciação validada pelo responsável. | Resposta do gerente e decisão técnica |
| RN-14 | PRODUTO tem especialização total e disjunta: todo produto é LENTE ou ARMACAO, nunca os dois. Os subtipos herdam id_produto. | Nota do DER |
| RN-15 | O optometrista emite o laudo interno; o consultor conduz o atendimento comercial que fecha a venda. O emissor da receita pode ser diferente do funcionário do atendimento comercial. | Respostas do gerente; adaptação ao DER |
| RN-16 | Lente com possui_grau verdadeiro exige receita no atendimento da venda, trazida pelo cliente ou emitida internamente. | Resposta do gerente |
| RN-17 | Depois do sinal, o saldo pode ser parcelado no cartão em até dez parcelas de no mínimo R$ 50,00; o sinal não integra essas parcelas. | Confirmação de 15/10/2026 |
| RN-18 | Encomenda só é liberada após recebimento de sinal de pelo menos 30% do total e registro da previsão de conclusão. Uma venda aberta pode existir antes desse recebimento. | Resposta do gerente |
| RN-19 | Segundo o gerente, a garantia da armação cobre defeito de fabricação, mola e parafuso; a da lente cobre adaptação, erro de grau, eficácia do tratamento e arranhões, conforme regulamento da ótica. O regulamento não foi apresentado ao grupo. | Relato de 14/10/2026 |
| RN-20 | O suporte relatado após a entrega é gratuito e vitalício para ajustes, plaquetas e parafusos; registrar como atendimento de manutenção. | Resposta do gerente |
| RN-21 | A entrega é feita ao portador do canhoto de compra e venda; registrar a conferência ao preencher a retirada efetiva. | Resposta do gerente |
| RN-22 | Registrar tipo, número e data do documento fiscal efetivamente emitido. O relato de emissão quando solicitada não constitui dispensa fiscal nem validação jurídica. | Relato do gerente; limite do levantamento |
| RN-23 | Toda venda, inclusive pronta entrega, é precedida de orçamento. Orçamentos são guardados mesmo sem venda, com emissão e validade usual de 24 horas. Conversão exige aprovação dentro da validade e ocorre no máximo uma vez. | Confirmações do grupo |
| RN-24 | Na desistência sem defeito, a política comercial relatada considera o pedido ainda não enviado ao fornecedor e o limite de 24 horas da compra. Solicitação não significa cancelamento automático; preservar a decisão. | Relato de 15/10/2026 |
| RN-25 | Troca depende de avaliação do produto e causa do dano, podendo ser aprovada ou recusada. Parecer e data são exigidos na decisão; não presumir política de reembolso ou crédito. | Resposta do gerente |
| RN-26 | Lentes são compradas, vendidas e contadas por par; armações por unidade. O custo_unitario de lente corresponde ao custo por par. | Confirmação de 15/10/2026 |
| RN-27 | O campo “A partir das” é horário previsto de retirada. O índice de refração registra o valor numérico; observações da linha descrevem características adicionais da lente. | Formulário e resposta do gerente |
| RN-28 | PARCELA possui id_parcela próprio. Somente pagamento com finalidade SINAL participa de GERA; cada parcela tem um gerador e pode existir sem QUITA. QUITA é opcional e 1:1: um pagamento quita no máximo uma parcela e cada parcela é quitada por no máximo um pagamento. Gerador e quitador devem pertencer à mesma venda. | DER final e restrição técnica |
| RN-29 | CONTÉM distingue linhas por numero_linha único dentro da venda. O mesmo produto pode ocorrer em duas linhas com preços diferentes. A ocorrência aponta numero_linha_venda e seu produto deve coincidir com o dessa linha; quantidade afetada deve respeitar a quantidade vendida. | Confirmação do usuário e nota do DER |
| RN-30 | Cada MOVIMENTO_ESTOQUE possui exatamente uma origem: VENDA, COMPRA ou TROCA_DEVOLUCAO (exclusão mútua/XOR). O produto da origem deve ser compatível; em substituição, o movimento identifica o produto efetivamente entregue. | Nota do DER e modelagem |
| RN-31 | O atendimento ligado diretamente à VENDA deve ser o mesmo que originou o ORCAMENTO dessa venda. | Nota final do DER |
| RN-32 | O recebimento SINAL gera o plano do saldo: número e soma das parcelas são validados por venda, mesmo que haja mais de um recebimento de sinal. O sinal nunca é contado novamente como parcela quitada. | Decisão técnica de integridade |
| RN-33 | Campos de reembolso e abatimento registram apenas acertos efetivamente autorizados; não comprovam que a loja oferece essas alternativas em todos os casos. | Limite do levantamento e campos do DER |
| RN-34 | A loja mantém no mínimo 100 pares de lentes e 500 armações em estoque; abaixo disso, precisa repor. As lentes são contadas por par (RN-26). | Resposta do gerente |


**Restrições organizacionais:** cumprir a unidade comercial por produto, preservar o histórico, separar previstos de realizados, exigir avaliação antes da decisão de pós-venda e aplicar acesso mínimo aos dados pessoais. As políticas comerciais relatadas não representam parecer jurídico. Regulamento de garantia, base legal de cada tratamento e prazos de retenção deverão ser formalizados pela organização antes do uso real.


## 5. Dicionário de Dados Conceitual (Preliminar)


O DER final contém **16 entidades, 106 atributos desenhados nas entidades e 9 atributos nos três relacionamentos com atributos**. Essa contagem não inclui referências propostas para a transformação relacional nem repete o identificador herdado nos subtipos. Não corresponde a uma contagem de colunas físicas implementadas.


- [Ver código do dicionário](https://github.com/jfpiresoficial/otica-kadosh-modelagem-dados/blob/main/Dicionario_de_Dados_Otica_Kadosh.html)
- [Visualizar no GitHub Pages](https://jfpiresoficial.github.io/otica-kadosh-modelagem-dados/)

O [Dicionário de Dados em HTML](./Dicionario_de_Dados_Otica_Kadosh.html) segue o exemplo do professor: notação formal, tipo físico proposto, obrigatoriedade, significado, índices, auditoria e acesso. A coluna abaixo apresenta o nome padronizado e, entre parênteses, o nome exibido no DER. Prefixos: ID_ identificador, NM_ nome, DT_ data, DH_ data e hora, HR_ horário, NR_ número textual/ordinal, QT_ quantidade, VL_ valor, TP_/CD_ categoria/domínio, IN_ indicador e DS_ descrição.



**Privacidade:** os documentos descrevem estruturas e regras; não publicam registros reais de clientes nem prescrições. OD/OE = olho direito/esquerdo; DNP = distância nasopupilar.


### CLIENTE


Pessoa física que solicita os atendimentos e é titular dos pedidos.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_CLIENTE` (`id_cliente`) | Código interno do cadastro; não sofre operação matemática. | Obrigatório: Sim (PK). Gerado pelo sistema; nunca reutilizado. |
| `NM_CLIENTE` (`nome`) | Nome completo do cliente, como escrito no pedido. Identifica o cliente nos atendimentos e no comprovante. | Obrigatório: Sim. É o nome do cliente, nunca o do funcionário do campo “Consultor”. |
| `DT_NASCIMENTO` (`data_nasc`) | Data de nascimento (campo “Data Nasc.” do pedido). Ajuda a confirmar identidade e faixa etária. | Obrigatório: Não. Preenchimento obrigatório não confirmado com a ótica. |
| `NR_CPF` (`cpf`) | CPF, somente dígitos. Dado pessoal protegido pela LGPD. | Obrigatório: Não. Se informado: 11 dígitos válidos e único no cadastro. |
| `DS_EMAIL` (`email`) | Endereço de e-mail para contato. | Obrigatório: Não. Se informado, deve ter formato válido. |
| `NR_TELEFONE_FIXO` (`telefone_fixo`) | Telefone fixo com DDD, somente dígitos (campo “Tel. Fixo”). | Obrigatório: Não. Sem regra específica. |
| `NR_TELEFONE_CELULAR` (`telefone_celular`) | Celular com DDD (campo “Tel. Celular”). Canal usado para avisar que os óculos ficaram prontos. | Obrigatório: Não. Ao menos um meio de contato (celular, fixo ou e-mail) deve existir no cadastro. |
| `DS_LOGRADOURO` (`logradouro`) | Rua, avenida ou similar do endereço. | Obrigatório: Não. Sem regra específica. |
| `NR_ENDERECO` (`numero_endereco`) | Número do imóvel (campo “Nº” ao lado do CEP). Texto, pois pode ter complemento como “12-A”. | Obrigatório: Não. Sem regra específica. |
| `NM_BAIRRO` (`bairro`) | Bairro do endereço. | Obrigatório: Não. Sem regra específica. |
| `NM_CIDADE` (`cidade`) | Cidade do endereço. | Obrigatório: Não. Sem regra específica. |
| `NR_CEP` (`cep`) | CEP, somente dígitos. | Obrigatório: Não. Se informado: 8 dígitos. |


### FUNCIONARIO


Integrante da equipe: gerente, consultor óptico ou optometrista.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_FUNCIONARIO` (`id_funcionario`) | Código interno do funcionário. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `NM_FUNCIONARIO` (`nome`) | Nome do integrante da equipe; aparece como “Consultor” no pedido. | Obrigatório: Sim. Sem regra específica. |
| `TP_FUNCAO` (`funcao`) | Papel exercido na ótica. Define o que a pessoa pode fazer no sistema (Seção 6). | Obrigatório: Sim. Domínio: OPTOMETRISTA, GERENTE, CONSULTOR_OPTICO (relatado na entrevista de 05/09/2026). |
| `NR_TELEFONE` (`telefone`) | Telefone de contato do funcionário. | Obrigatório: Não. Guarda de telefone individual não confirmada. |
| `IN_ATIVO` (`ativo`) | Indica se o funcionário pode receber novas atribuições. | Obrigatório: Sim. Padrão TRUE. No desligamento, inativar; conservar o vínculo com atendimentos, laudos e vendas históricos. |


### ATENDIMENTO


Evento que relaciona um cliente a um funcionário e preserva a atividade realizada.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_ATENDIMENTO` (`id_atendimento`) | Código interno do atendimento. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `DH_ATENDIMENTO` (`data_hora`) | Data e hora em que o atendimento ocorreu. É diferente da “Data da Compra” da venda. | Obrigatório: Sim. Sem regra específica. |
| `TP_MEIO_CONTATO` (`meio_contato`) | Como o cliente chegou à ótica (campo “Meio de contato” do pedido). | Obrigatório: Não. Lista de valores não confirmada; texto livre por enquanto. |
| `TP_ATENDIMENTO` (`tipo_atendimento`) | Distingue atendimento comercial, avaliação e manutenção. | Obrigatório: Sim. Domínio proposto: COMERCIAL, AVALIACAO, MANUTENCAO. Não presume uma venda em todo atendimento. |
| `DS_SERVICO` (`descricao_servico`) | Descrição do ajuste ou manutenção realizada. | Obrigatório: Não. Obrigatória em manutenção. RN-20: plaquetas, ajustes e parafusos do suporte relatado são gratuitos; registrar sem gerar cobrança por esses serviços. |


### RECEITA


Prescrição trazida pelo cliente ou laudo interno registrado no atendimento.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_RECEITA` (`id_receita`) | Código interno da receita. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `DT_RECEITA` (`data_receita`) | Data anotada na receita ou no laudo. | Obrigatório: Sim. RN-03: receita trazida é aceita se tiver até 1 ano; senão a ótica faz novo teste. É prática da ótica, não prazo legal geral. |
| `TP_ORIGEM` (`origem`) | De onde veio a prescrição. | Obrigatório: Sim. Domínio: TRAZIDA (apresentada pelo cliente) ou LAUDO_OTICA (teste feito na ótica). |
| `DS_OBSERVACAO` (`observacao`) | Anotação complementar do laudo (espaço “Obs.”). | Obrigatório: Não. Só quando houver anotação. |


### RECEITA_MEDIDA


Linha de medidas para um olho e uma distância dentro de uma receita.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_RECEITA` (`id_receita`) | Receita a que a medida pertence. | Obrigatório: Sim (PK, FK). FK para RECEITA; parte da chave. |
| `CD_OLHO` (`olho`) | Olho a que a linha se refere. | Obrigatório: Sim (PK). Domínio: OD (direito) ou OE (esquerdo). Medida de um olho nunca é atribuída ao outro. |
| `CD_DISTANCIA` (`distancia`) | Finalidade visual da linha. | Obrigatório: Sim (PK). Domínio: LONGE ou PERTO. Nem sempre as duas são preenchidas. |
| `VL_ESFERICO` (`esferico`) | Grau esférico em dioptrias (DE no laudo; coluna “Esférico” no pedido). | Obrigatório: Não. Faixa de validação clínica ainda não confirmada. Não bloquear prescrições por uma faixa genérica; eventual passo e limites dependem de validação pelo responsável técnico. |
| `VL_CILINDRICO` (`cilindro`) | Grau cilíndrico em dioptrias (DC no laudo; coluna “Cilíndrico” no pedido). | Obrigatório: Não. Convenção de sinal e limites ainda não confirmados. Quando houver componente cilíndrico que exija orientação, informar o eixo. Não assumir apenas valores negativos sem validação. |
| `VL_EIXO` (`eixo`) | Eixo do cilindro em graus. | Obrigatório: Não. Entre 0 e 180. |
| `VL_ACUIDADE_VISUAL` (`acuidade_visual`) | Acuidade visual (AV) registrada no laudo. | Obrigatório: Não. Texto, pois pode ser fração (20/20) ou decimal (0,8). |
| `VL_DNP` (`dnp`) | Distância nasopupilar, em mm, usada na montagem das lentes. | Obrigatório: Não. Registrada por olho (confirmado pelo gerente). |
| `VL_ALTURA` (`altura`) | Altura da lente na armação, em mm. | Obrigatório: Não. Registrada por olho (confirmado pelo gerente). |


### ORCAMENTO


Oferta comercial preservada mesmo quando não é convertida em venda.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_ORCAMENTO` (`id_orcamento`) | Identificador do orçamento. | Obrigatório: Sim (PK). Gerado pelo sistema; não reutilizado. |
| `DH_EMISSAO` (`data_hora_emissao`) | Data e hora em que o orçamento foi emitido. | Obrigatório: Sim. RN-23: data e hora da emissão; início da validade usual de 24 horas. |
| `DH_VALIDADE` (`data_hora_validade`) | Data e hora limite da oferta. | Obrigatório: Sim. RN-23: padrão DH_EMISSAO + 24 horas. Registrar prazo efetivamente concedido; eventual exceção precisa de justificativa e autorização auditadas, sem inventar outro prazo padrão. |
| `DH_APROVACAO` (`data_hora_aprovacao`) | Data e hora da aceitação pelo cliente. | Obrigatório: Não (condicional). Obrigatória para conversão: DH_EMISSAO ≤ DH_APROVACAO ≤ DH_VALIDADE. Oferta vencida exige nova proposta; preservar a anterior. |
| `CD_STATUS` (`status`) | Etapa do orçamento. | Obrigatório: Sim. Domínio proposto: EM_ELABORACAO, EMITIDO, APROVADO, RECUSADO, CANCELADO. A conversão é identificada pelo vínculo com VENDA, sem status duplicado. |
| `DS_OBSERVACAO` (`observacao`) | Observação da proposta comercial. | Obrigatório: Não. Não registrar dados de saúde em texto comercial; usar RECEITA quando necessário. |


### VENDA


Pedido comercial com valor, datas de execução, retirada e referência fiscal.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_VENDA` (`id_venda`) | Número do pedido. Chave técnica única, pois a unicidade do número impresso no bloco não foi confirmada. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `DH_COMPRA` (`data_hora_compra`) | Data e hora do fechamento da compra, para aferir o intervalo de 24 horas. | Obrigatório: Sim. Obrigatória; usada na análise comercial de cancelamento (RN-24). |
| `VL_TOTAL` (`valor_total`) | Total cobrado pelo pedido (campo “Total: R$”), antes de considerar o que já foi pago. | Obrigatório: Sim. Soma de quantidade × preço_unitario de CONTÉM. Preservar o valor original; ajustes autorizados ficam na ocorrência. RN-04 e RN-29. |
| `CD_STATUS` (`status`) | Etapa do pedido no acompanhamento. | Obrigatório: Sim. Proposta: ABERTO, AGUARDANDO_PRODUTO, EM_MONTAGEM, PRONTO, RETIRADO, CANCELADO. Estados a validar com a ótica. |
| `DS_OBSERVACAO` (`observacao`) | Anotação livre do pedido (“Obs.”). | Obrigatório: Não. Sem regra específica. |
| `DT_MONTAGEM_FINALIZACAO` (`data_montagem_finalizacao`) | Data em que lente e armação foram montadas e os óculos finalizados. | Obrigatório: Não. RN-07 e RN-19: inicia a garantia comercial por linha de CONTÉM: 1 ano para ARMACAO e 6 meses para LENTE. Não calcular término enquanto esta data for nula. |
| `DT_RETIRADA` (`data_retirada`) | Data em que o cliente retirou os óculos. | Obrigatório: Não. Retirada efetiva (confirmado). Nula até a retirada. Não é anterior à montagem. |
| `HR_PREVISTA_RETIRADA` (`horario_previsto_retirada`) | Horário prometido para retirada, transcrito do campo A partir das. | Obrigatório: Não. RN-27: horário previsto, não efetivo. Combinar com DT_PREVISTA_CONCLUSAO para comunicar a disponibilidade prevista. |
| `DT_PREVISTA_CONCLUSAO` (`data_prevista_conclusao`) | Data prometida para os óculos estarem prontos. | Obrigatório: Não (condicional). Obrigatória antes de liberar uma encomenda (RN-18). É distinta da montagem e da retirada efetivas. Não há prazo fixo em dias confirmado. |
| `DT_LIBERACAO_ENCOMENDA` (`data_liberacao_encomenda`) | Data em que a fabricação foi autorizada após conferir a entrada. | Obrigatório: Não (condicional). Só registrar quando os pagamentos identificados como SINAL atingirem pelo menos 30% de VL_TOTAL e existir previsão de conclusão. Validar no ato da liberação e auditar a transição. |
| `IN_CANHOTO_CONFERIDO` (`canhoto_conferido`) | Registra a apresentação do comprovante no momento da entrega. | Obrigatório: Não (condicional). TRUE obrigatório quando DT_RETIRADA for preenchida (RN-21). O relato aceita o portador do canhoto; não criar exigência de titularidade ou documento pessoal não confirmada. |
| `TP_DOCUMENTO_FISCAL` (`tipo_documento_fiscal`) | Tipo do documento fiscal efetivamente emitido em sistema externo. | Obrigatório: Não. Preencher somente quando houver documento. A espécie fiscal e as condições de emissão dependem de validação contábil; o comprovante de pedido não é classificado automaticamente como documento fiscal. |
| `NR_DOCUMENTO_FISCAL` (`numero_documento_fiscal`) | Referência ao documento fiscal da operação. | Obrigatório: Não. Exigir junto com o tipo e a data quando a emissão for registrada. Não pressupõe autorização ou integração automática com o Fisco. |
| `DT_EMISSAO_FISCAL` (`data_emissao_fiscal`) | Data da emissão do documento fiscal referenciado. | Obrigatório: Não. A RN-22 descreve prática relatada, não uma dispensa legal. A implementação deve respeitar as obrigações fiscais aplicáveis. |
| `DH_ENVIO_FORNECEDOR` (`data_hora_envio_fornecedor`) | Instante do primeiro envio do pedido ao fornecedor para execução. | Obrigatório: Não. Registro técnico para RN-24; distinto da liberação interna e da chegada. Deve ser preenchido no envio efetivo e preservado no histórico. |
| `DH_SOLICITACAO_CANCELAMENTO` (`data_hora_solicitacao_cancelamento`) | Instante da solicitação de cancelamento por desistência. | Obrigatório: Não. Proposta para registrar pedido e avaliar RN-24. Uma solicitação não cancela automaticamente a venda; motivo, decisão e responsável ficam na auditoria. |


### PAGAMENTO


Recebimento efetivo de uma venda; pode ser sinal, pagamento integral ou quitação de parcela.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_PAGAMENTO` (`id_pagamento`) | Código interno do recebimento. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `VL_PAGAMENTO` (`valor`) | Quantia recebida nesta operação (campo “Sinal/Pago” é o primeiro pagamento). | Obrigatório: Sim. Maior que zero. Ao registrar recebimento, não exceder o saldo devedor vigente nem o saldo da parcela vinculada. Reembolsos são registrados em TROCA_DEVOLUCAO, não como pagamento negativo. |
| `DT_PAGAMENTO` (`data_pagamento`) | Data em que o recebimento ocorreu. | Obrigatório: Sim. Registro proposto para acompanhar pagamentos parciais. |
| `TP_FORMA` (`forma`) | Meio pelo qual o cliente pagou. | Obrigatório: Sim. Domínio PIX, DINHEIRO, DEBITO, CREDITO. O plano parcelado da RN-17 usa CREDITO. A estrutura não presume calendário de repasses nem taxas da operadora. |
| `TP_FINALIDADE` (`finalidade`) | Finalidade do recebimento, distinguindo o sinal dos demais pagamentos. | Obrigatório: Sim. Domínio técnico proposto: SINAL, INTEGRAL, PARCIAL ou QUITACAO_PARCELA. Somente SINAL participa de GERA. RN-17, RN-18 e RN-28. |


### PARCELA


Compromisso futuro gerado por um pagamento de sinal; existe antes da quitação.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_PARCELA` (`id_parcela`) | Identificador próprio da parcela, independente do identificador da venda. | Obrigatório: Sim (PK). Identificador único e não nulo. A parcela liga-se ao sinal por GERA; não possui id_venda no DER. RN-28. |
| `NR_PARCELA` (`numero_parcela`) | Número da parcela dentro da venda. | Obrigatório: Sim. Inteiro de 1 a 10, único dentro do plano da venda obtida pelo pagamento gerador; não integra a PK. RN-17 e RN-28. |
| `VL_PARCELA` (`valor`) | Valor combinado da parcela. | Obrigatório: Sim. Mínimo de R$ 50,00; soma do plano igual ao saldo após o sinal; até 10 parcelas por venda. RN-17. |
| `DT_VENCIMENTO` (`data_vencimento`) | Data em que a parcela vence. | Obrigatório: Sim. Sem regra específica. |
| `DT_QUITACAO` (`data_quitacao`) | Data da quitação efetivamente registrada para a parcela. | Obrigatório: Não (condicional). Permanece nula enquanto não houver QUITA. Quando quitada, deve ser compatível com a data do pagamento vinculado. RN-28. |
| `CD_STATUS` (`status`) | Situação operacional da parcela, coerente com vencimento e quitação. | Obrigatório: Sim. Domínio proposto: ABERTA, PAGA ou ATRASADA. Recalcular/validar para não manter status contraditório; PAGA exige QUITA e data_quitacao. RN-28. |


### FORNECEDOR


Organização que fornece produtos à ótica.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_FORNECEDOR` (`id_fornecedor`) | Código interno do fornecedor. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `NM_FORNECEDOR` (`nome`) | Nome pelo qual a ótica identifica o fornecedor. | Obrigatório: Sim. Confirmado na entrevista. |
| `NR_CNPJ` (`cnpj`) | CNPJ somente dígitos. | Obrigatório: Não. Identificador cadastral externo, sem cálculo matemático; normalizar formato e validar quando informado. Unicidade proposta, não obrigatoriedade de coleta. |
| `DS_ENDERECO` (`endereco`) | Endereço do fornecedor em texto. | Obrigatório: Não. Registro pela ótica não confirmado. |
| `DS_CONTATO` (`contato`) | Telefone ou canal de mensagem usado para pedir produtos. | Obrigatório: Não. Confirmado: o contato é registrado e usado nas solicitações. |


### COMPRA


Solicitação a um fornecedor, para reposição de estoque ou para atender uma venda.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_COMPRA` (`id_compra`) | Código interno da solicitação. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `DT_PEDIDO` (`data_pedido`) | Data em que a ótica pediu os produtos ao fornecedor. | Obrigatório: Sim. Diferente da “Data da Compra” da venda. |
| `DT_CHEGADA` (`data_chegada`) | Data em que os produtos chegaram à ótica. | Obrigatório: Não. Nula até a chegada. Não é anterior a DT_PEDIDO. |
| `CD_STATUS` (`status`) | Situação da solicitação. | Obrigatório: Sim. Proposta: SOLICITADA, RECEBIDA, CANCELADA. |


### PRODUTO


Generalização dos produtos comprados, vendidos e movimentados no estoque.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_PRODUTO` (`id_produto`) | Código interno do produto. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `CD_TIPO` (`tipo`) | Categoria do produto. | Obrigatório: Sim. LENTE ou ARMACAO; exatamente um subtipo compatível. RN-14. |
| `DS_REFERENCIA` (`referencia`) | Código ou modelo comercial (“Ref. Armação” no pedido). | Obrigatório: Sim. Formato e unicidade não confirmados. |
| `NM_MARCA` (`marca`) | Marca do produto. | Obrigatório: Não. Existência de cadastro geral de marcas não confirmada. |
| `CD_UNIDADE_ESTOQUE` (`unidade_estoque`) | Unidade usada consistentemente em entradas, saídas e saldos do produto. | Obrigatório: Sim. PAR para lentes e UNIDADE para armações; mesma unidade em compra, venda e movimento. RN-26. |


### LENTE


Especialização de PRODUTO com características próprias de uma lente.


**Identificação herdada:** `ID_PRODUTO` de PRODUTO; não acrescentar outro identificador no DER conceitual.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `VL_INDICE` (`indice`) | Índice de refração da lente escolhida, associado ao afinamento relatado pelo gerente. | Obrigatório: Não. Registrar o índice informado, por exemplo 1,56 ou 1,74; exemplos não são lista fechada. RN-27. |
| `DS_TRATAMENTO` (`tratamento`) | Tratamento aplicado (antirreflexo, filtro etc.). | Obrigatório: Não. O formulário oferece opções; forma de registro no estoque a validar. |
| `IN_POSSUI_GRAU` (`possui_grau`) | Indica se o produto de lente exige prescrição no pedido. | Obrigatório: Sim. TRUE exige receita vinculada ao atendimento da venda; FALSE não exige prescrição por esse motivo. RN-16. A classificação não confirma oferta de todos os tipos de lente. |


### ARMACAO


Especialização de PRODUTO com características próprias de uma armação.


**Identificação herdada:** `ID_PRODUTO` de PRODUTO; não acrescentar outro identificador no DER conceitual.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `TP_ARMACAO` (`tipo_armacao`) | Tipo da armação escolhido pelo cliente (“Tipo de Armação”). | Obrigatório: Não. Aplica-se só à armação. |
| `DS_MATERIAL` (`material`) | Material da armação. | Obrigatório: Não. Uso pela ótica não confirmado. |


### TROCA_DEVOLUCAO


Ocorrência de pós-venda referente a uma linha e ao produto nela vendido.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_OCORRENCIA` (`id_ocorrencia`) | Código interno da ocorrência. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `TP_OCORRENCIA` (`tipo`) | Classificação da ocorrência. | Obrigatório: Sim. Domínio: TROCA ou DEVOLUCAO. |
| `DT_OCORRIDO` (`data_ocorrido`) | Data do fato que levou à troca ou devolução, anotada no pedido. | Obrigatório: Sim. Diferente da data do registro no sistema. |
| `CD_STATUS` (`status`) | Situação da ocorrência. | Obrigatório: Sim. Proposta: ABERTA, EM_AVALIACAO, APROVADA, RECUSADA, CONCLUIDA. Aprovação/recusa exige parecer e data de avaliação. CONCLUIDA exige execução dos movimentos/acertos autorizados. |
| `NR_LINHA_VENDA` (`numero_linha_venda`) | Número da linha de CONTÉM afetada por esta ocorrência. | Obrigatório: Sim. Deve existir na venda da ocorrência; o produto de OBJETO DE deve coincidir com o produto dessa linha. RN-29. |
| `QT_AFETADA` (`quantidade_afetada`) | Quantidade do item envolvida nesta ocorrência. | Obrigatório: Sim. Maior que zero e não superior à quantidade da linha referenciada; controlar ocorrências anteriores para evitar retorno duplicado. RN-25 e RN-29. |
| `DS_DANO` (`descricao_dano`) | Descrição do que quebrou ou foi danificado. | Obrigatório: Não. Obrigatória quando houver dano; ajuda a decidir se a peça é reaproveitável. |
| `DS_PARECER_AVALIACAO` (`parecer_avaliacao`) | Estado observado, causa avaliada e justificativa da decisão. | Obrigatório: Não (condicional). RN-25: obrigatório ao aprovar ou recusar; não concluir automaticamente culpa do cliente. Identidade de quem decide registrada na auditoria. |
| `DT_AVALIACAO` (`data_avaliacao`) | Data da avaliação do produto. | Obrigatório: Não (condicional). RN-25: obrigatória na decisão; não anterior a DT_OCORRIDO. |
| `VL_COBRADO` (`valor_cobrado`) | Quantia cobrada do cliente, quando houver. | Obrigatório: Não. Critérios comerciais não confirmados. Valor adicional autorizado para a ocorrência, não negativo; informar zero quando explicitamente sem cobrança. Não confundir nulo (a decidir) com zero. RN-20: não cobrar os serviços de suporte gratuito relatados. |
| `VL_ABATIMENTO` (`valor_abatimento`) | Redução autorizada do valor devido pelo pedido em decorrência da ocorrência. | Obrigatório: Não (condicional). não negativo; os abatimentos autorizados não podem tornar negativo o total vigente da venda nem exceder o valor do item devolvido. Informar zero quando explicitamente sem redução. A política comercial não foi confirmada. |
| `VL_REEMBOLSADO` (`valor_reembolso`) | Valor efetivamente restituído ao cliente, se houver restituição autorizada. | Obrigatório: Não (condicional). Não negativo, limitado ao crédito do cliente apurado para a venda; exige DT_REEMBOLSO quando positivo. Campo de contingência proposto: a existência de reembolso na prática da ótica não foi confirmada. |
| `DT_REEMBOLSO` (`data_reembolso`) | Data do reembolso efetivamente realizado, se houver. | Obrigatório: Não. obrigatória se VL_REEMBOLSADO > 0, não anterior à ocorrência; nula se não houve reembolso. Não preencher com data presumida. |


### MOVIMENTO_ESTOQUE


Lançamento de entrada ou saída de um produto, com origem e condição identificadas.


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `ID_MOVIMENTO` (`id_movimento`) | Código interno do lançamento. | Obrigatório: Sim (PK). Gerado pelo sistema. |
| `DT_MOVIMENTO` (`data`) | Data do lançamento no controle de estoque. | Obrigatório: Sim. Sem regra específica. |
| `QT_MOVIMENTO` (`quantidade`) | Unidades movimentadas. | Obrigatório: Sim. Sempre positiva; o sinal vem da direção. |
| `CD_DIRECAO` (`direcao`) | Efeito no saldo. | Obrigatório: Sim. Domínio: ENTRADA ou SAIDA. |
| `CD_MOTIVO` (`motivo`) | Por que o movimento aconteceu. | Obrigatório: Sim. Domínios técnicos propostos: COMPRA, VENDA, REAPROVEITAMENTO, DEVOLUCAO_AVARIA, DESCARTE e SUBSTITUICAO. Cada motivo deve ser compatível com uma origem. RN-12 e RN-30. |
| `CD_CONDICAO` (`condicao`) | Condição do estoque movimentado, distinguindo peças aptas de segregadas. | Obrigatório: Sim. Domínio proposto DISPONIVEL, SEGREGADO. Descarte de peça devolvida sai de SEGREGADO, não do saldo disponível. |


### Atributos dos relacionamentos


CONTÉM, OFERECE e ADQUIRE são relacionamentos do DER, e não entidades ITEM_VENDA, ITEM_ORCAMENTO ou ITEM_COMPRA.


#### CONTÉM — VENDA / PRODUTO


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `NR_LINHA` (`numero_linha`) | Número que distingue a linha dentro da venda. | Obrigatório: Sim. Único por venda; distingue o mesmo produto com preços diferentes. RN-29. |
| `QT_PRODUTO` (`quantidade`) | Quantidade vendida nesta linha. | Obrigatório: Sim. Maior que zero; lentes por par e armações por unidade. RN-26. |
| `VL_PRECO_UNITARIO` (`preco_unitario`) | Preço aplicado na venda, por unidade comercial. | Obrigatório: Sim. Não negativo; preservar o preço histórico da linha. RN-04. |
| `DS_OBSERVACAO` (`observacao`) | Observação da linha, incluindo características da lente escolhida. | Obrigatório: Não. Não substitui medidas da receita. RN-27. |


#### OFERECE — ORCAMENTO / PRODUTO


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `QT_PRODUTO` (`quantidade`) | Quantidade proposta do produto. | Obrigatório: Sim. Maior que zero e compatível com a unidade comercial. RN-23 e RN-26. |
| `VL_PRECO_UNITARIO` (`preco_unitario`) | Preço proposto por unidade comercial. | Obrigatório: Sim. Não negativo; preservar oferta emitida. RN-23. |
| `DS_OBSERVACAO` (`observacao`) | Observação específica do produto oferecido. | Obrigatório: Não. Sem dados de saúde em texto comercial. |


#### ADQUIRE — COMPRA / PRODUTO


| Atributo | Descrição | Regra de negócio associada |
| --- | --- | --- |
| `QT_PRODUTO` (`quantidade`) | Quantidade solicitada na compra. | Obrigatório: Sim. Maior que zero; lentes contadas por par. RN-26. |
| `VL_CUSTO_UNITARIO` (`custo_unitario`) | Custo por unidade de armação ou por par de lentes. | Obrigatório: Sim. Não negativo; total da associação = quantidade × custo_unitario. RN-26. |


## 6. Modelagem Conceitual (Entidades, Atributos, Relacionamentos)


### 6.1 Entidades reconhecidas


| Entidade | Justificativa |
| --- | --- |
| `CLIENTE` | Pessoa física que solicita os atendimentos e é titular dos pedidos. |
| `FUNCIONARIO` | Integrante da equipe: gerente, consultor óptico ou optometrista. |
| `ATENDIMENTO` | Evento que relaciona um cliente a um funcionário e preserva a atividade realizada. |
| `RECEITA` | Prescrição trazida pelo cliente ou laudo interno registrado no atendimento. |
| `RECEITA_MEDIDA` | Linha de medidas para um olho e uma distância dentro de uma receita. |
| `ORCAMENTO` | Oferta comercial preservada mesmo quando não é convertida em venda. |
| `VENDA` | Pedido comercial com valor, datas de execução, retirada e referência fiscal. |
| `PAGAMENTO` | Recebimento efetivo de uma venda; pode ser sinal, pagamento integral ou quitação de parcela. |
| `PARCELA` | Compromisso futuro gerado por um pagamento de sinal; existe antes da quitação. |
| `FORNECEDOR` | Organização que fornece produtos à ótica. |
| `COMPRA` | Solicitação a um fornecedor, para reposição de estoque ou para atender uma venda. |
| `PRODUTO` | Generalização dos produtos comprados, vendidos e movimentados no estoque. |
| `LENTE` | Especialização de PRODUTO com características próprias de uma lente. |
| `ARMACAO` | Especialização de PRODUTO com características próprias de uma armação. |
| `TROCA_DEVOLUCAO` | Ocorrência de pós-venda referente a uma linha e ao produto nela vendido. |
| `MOVIMENTO_ESTOQUE` | Lançamento de entrada ou saída de um produto, com origem e condição identificadas. |


### 6.2 Atributos e classificações


- Identificadores simples: atributos `id_*` das entidades, exceto RECEITA_MEDIDA, que usa `id_receita + olho + distancia`.
- LENTE e ARMACAO herdam a identificação de PRODUTO, conforme especialização total e disjunta.
- Dados de cadastro e eventos são atributos simples no desenho. O endereço do cliente foi decomposto em logradouro, número, bairro, cidade e CEP.
- Quantidade, preço e observação da venda pertencem ao relacionamento CONTÉM; os demais atributos de relacionamentos estão na Seção 5.
- Saldo de estoque, saldo devedor, total de orçamento/compra e término da garantia são cálculos; não foram adicionados como novos atributos ao DER.
- A presença de atributo comum no desenho não determina, por si só, NOT NULL: a obrigatoriedade detalhada é proposta técnica do dicionário, condicionada ao evento.


### 6.3 Relacionamentos pertinentes


As cardinalidades nas duas colunas correspondem à participação de cada entidade nomeada na mesma linha.


| Entidade A | Relacionamento | Entidade B | Cardinalidade em A | Cardinalidade em B | Significado |
| --- | --- | --- | --- | --- | --- |
| CLIENTE | SOLICITA | ATENDIMENTO | (0,n) | (1,1) | Um cliente pode solicitar vários atendimentos; cada atendimento tem um cliente. |
| FUNCIONARIO | CONDUZ | ATENDIMENTO | (0,n) | (1,1) | Cada atendimento é conduzido por um funcionário. |
| ATENDIMENTO | ORIGINA | RECEITA | (0,1) | (1,1) | O atendimento pode registrar uma receita; a receita pertence a um atendimento. |
| FUNCIONARIO | EMISSOR DE | RECEITA | (0,n) | (0,1) | Emissor interno opcional para receita trazida; obrigatório para laudo interno. |
| RECEITA | POSSUI | RECEITA_MEDIDA | (1,n) | (1,1) | Cada medida pertence a uma receita; limite complementar de quatro combinações. |
| ATENDIMENTO | ORIGINA ORCAMENTO | ORCAMENTO | (0,n) | (1,1) | Um atendimento pode gerar vários orçamentos; cada orçamento tem um atendimento. |
| ATENDIMENTO | RESULTA EM | VENDA | (0,1) | (1,1) | Atendimento pode terminar sem venda; toda venda possui atendimento. |
| ORCAMENTO | ORIGINA VENDA | VENDA | (0,1) | (1,1) | Um orçamento converte no máximo uma vez; toda venda vem de um orçamento. |
| VENDA | CONTÉM | PRODUTO | (1,n) | (0,n) | Venda possui produtos; produto pode existir sem venda. A linha tem número, quantidade, preço e observação. |
| ORCAMENTO | OFERECE | PRODUTO | (1,n) | (0,n) | Orçamento oferece produtos com quantidade, preço e observação. |
| VENDA | RECEBE | PAGAMENTO | (0,n) | (1,1) | Venda pode estar aberta sem recebimento; cada pagamento pertence a uma venda. |
| PAGAMENTO | GERA | PARCELA | (0,n) | (1,1) | Somente um sinal gera o plano de parcelas futuras; cada parcela tem um gerador. |
| PAGAMENTO | QUITA | PARCELA | (0,1) | (0,1) | Recebimento pode quitar uma parcela; parcela futura pode ainda não estar quitada. |
| FORNECEDOR | FORNECE | COMPRA | (0,n) | (1,1) | Cada compra tem exatamente um fornecedor. |
| VENDA | DEMANDA | COMPRA | (0,n) | (0,1) | Compra pode repor estoque sem venda; quando vinculada, atende uma venda. |
| COMPRA | ADQUIRE | PRODUTO | (1,n) | (0,n) | Compra solicita produtos com quantidade e custo. |
| VENDA | TEM OCORRÊNCIA | TROCA_DEVOLUCAO | (0,n) | (1,1) | Ocorrência pertence a uma única venda. |
| TROCA_DEVOLUCAO | OBJETO DE | PRODUTO | (1,1) | (0,n) | Ocorrência afeta um produto da linha referenciada. |
| VENDA | GERA SAÍDA | MOVIMENTO_ESTOQUE | (0,n) | (0,1) | Movimento pode ter uma venda como origem. |
| COMPRA | GERA ENTRADA | MOVIMENTO_ESTOQUE | (0,n) | (0,1) | Movimento pode ter uma compra como origem. |
| TROCA_DEVOLUCAO | ORIGINA | MOVIMENTO_ESTOQUE | (0,n) | (0,1) | Ocorrência pode originar vários movimentos de retorno, substituição ou descarte. |
| MOVIMENTO_ESTOQUE | MOVIMENTADO EM | PRODUTO | (1,1) | (0,n) | Todo movimento refere-se a um produto; produto pode não ter movimentos. |
| PRODUTO | ESPECIALIZA-SE EM | LENTE | (1,1) | (0,1) | Todo produto é especializado em um único subtipo (total e disjunta); a lente herda o identificador do produto. |
| PRODUTO | ESPECIALIZA-SE EM | ARMACAO | (1,1) | (0,1) | Todo produto é especializado em um único subtipo (total e disjunta); a armação herda o identificador do produto. |


### 6.4 Restrições e políticas aplicadas


1. O atendimento da venda deve ser o mesmo que originou seu orçamento (RN-31). A receita necessária é encontrada nesse atendimento, sem vínculo direto RECEITA–VENDA.
2. O funcionário comercial é obtido por VENDA → ATENDIMENTO → CONDUZ → FUNCIONARIO; não há relacionamento próprio de vendedor em VENDA no DER final. Para fechamento comercial, validar a função CONSULTOR_OPTICO. A autoria do laudo é obtida por EMISSOR DE.
3. Um sinal pode gerar várias parcelas; a parcela futura não precisa ter pagamento quitador. QUITA modela quitação integral em uma única operação por parcela. Pagamento parcial de parcela ou liquidação de várias parcelas em um único recebimento exigiria evolução desse relacionamento.
4. Validar que gerador e quitador da parcela pertencem à mesma venda. A venda da parcela é obtida por PARCELA → GERA → PAGAMENTO → RECEBE → VENDA, sem ligação direta.
5. O identificador de CONTÉM na futura projeção relacional deve incluir o número da linha. A chave apenas (venda, produto) perderia as duas linhas do mesmo produto. O losango e a nota do DER registram essa intenção; a transformação automática do editor precisa ser conferida.
6. OFERECE e ADQUIRE, como desenhados, descrevem uma associação por par de entidades. A repetição do mesmo produto em linhas distintas foi confirmada apenas para VENDA; não acrescentar número de linha aos outros relacionamentos sem novo requisito.
7. A especialização é total e disjunta conforme a nota do DER. O losango usado no editor é uma adaptação gráfica; não deve ser interpretado como uma associação ternária exigindo simultaneamente lente e armação.
8. Cada movimento possui exatamente uma das três origens. Não acrescentar motivo AJUSTE sem origem, pois isso contrariaria o XOR do DER final.
9. Campo nulo significa que a informação ainda não foi registrada ou não se aplica; zero monetário significa valor explicitamente definido como zero. Não preencher avaliação, retirada, reembolso ou quitação com datas presumidas.


## 7. Diagrama Entidade-Relacionamento (DER)


### DER da Ótica Kadosh

<img width="3673" height="2898" alt="DER_Otica_Kadosh_reorganizado" src="./DER_Otica_Kadosh_reorganizado.png" />





A imagem é a exportação do DER final elaborado no brModelo. As regras de exclusão mútua, especialização e linhas repetidas estão nas notas do diagrama e nas seções 4, 6 e 8. A evolução para o modelo relacional deve preservar essas regras; não basta aceitar automaticamente a conversão do editor.


## 8. Justificativa Técnica


### 8.1 Separação dos eventos


CLIENTE e FUNCIONARIO são cadastros reutilizados. ATENDIMENTO preserva o contato com a ótica mesmo sem compra; ORCAMENTO conserva a oferta e sua validade; VENDA registra a contratação. Essa separação explica as participações opcionais antes do fechamento e a obrigatoriedade de atendimento e orçamento em toda venda.


### 8.2 Produtos e relacionamentos com atributos


Por orientação do professor, a venda e a compra se ligam diretamente a PRODUTO por CONTÉM e ADQUIRE. OFERECE registra as condições do orçamento. Quantidade e preço são propriedades da associação, preservando valores históricos sem alterar o cadastro do produto. O mesmo produto pode ocorrer em mais de uma linha de venda: a futura associação relacional deve ser identificada por venda e número da linha. A chave apenas venda/produto não atende esse requisito.


### 8.3 Parcelas e recebimentos


PAGAMENTO é um fato ocorrido, enquanto PARCELA é uma obrigação futura. Retirou-se a ligação direta VENDA–PARCELA. A parcela tem identificador próprio e é alcançada pelo sinal que a gerou; QUITA opcional permite registrar vencimentos antes do recebimento. As cardinalidades 0:1 de QUITA limitam esta versão à quitação integral de uma parcela por um pagamento. A restrição de mesma venda entre sinal e quitador deve ser validada na transação.


### 8.4 Receita e responsáveis


A ligação direta RECEITA–VENDA foi retirada por orientação do professor. A receita necessária é obtida pelo atendimento, que também identifica o cliente. A igualdade entre o atendimento direto da venda e o atendimento de seu orçamento impede caminhos contraditórios. EMISSOR DE identifica o autor do laudo, enquanto CONDUZ identifica o responsável pelo atendimento; não foi criado um vínculo de vendedor que não esteja no desenho.


### 8.5 Medidas e especialização


RECEITA_MEDIDA permite diferentes valores por olho e distância, com chave composta e no máximo quatro combinações válidas. PRODUTO concentra referência, marca e unidade de estoque; LENTE e ARMACAO guardam características específicas. A nota total e disjunta define a semântica pretendida da adaptação gráfica usada no editor; a implementação deve assegurar exatamente um subtipo.


### 8.6 Compras, estoque e pós-venda


COMPRA pode repor estoque sem venda de origem, por isso DEMANDA é opcional do lado da compra. TROCA_DEVOLUCAO liga-se diretamente à venda e ao produto; o número da linha resolve a referência quando o produto se repete. MOVIMENTO_ESTOQUE registra cada efeito físico, com exatamente uma origem e condição disponível/segregada; saldos são derivados dos lançamentos.


### 8.7 Escopo, integridade e evolução


Esta é a Entrega 1, de modelo conceitual. Tipos físicos, tamanhos, índices, chaves estrangeiras e controles administrativos do HTML são uma proposta documentada para a próxima etapa, não um banco implementado. As associações N:N precisarão de estruturas associativas na transformação relacional; isso não recoloca ITEM_VENDA e ITEM_COMPRA como entidades no DER conceitual. Laboratório, adquirente de cartão e regras comerciais de crédito/reembolso não foram inventados. A política de acesso e a auditoria são requisitos a implementar.


### 8.8 Conferência com o esqueleto


| Pedido do professor | Localização | Atendimento documental |
| --- | --- | --- |
| Caracterização, acesso e evidências | Seção 1 | Organização, porte, problemas, contato, visita e referência à fotografia. |
| Processos e integração | Seção 2 | Entradas, responsáveis, sequência e resultados; fluxograma opcional. |
| Requisitos e regras | Seções 3 e 4 | 18 RF, 7 RNF e 34 regras com origem indicada. |
| Dicionário conceitual por entidade | Seção 5 | 16 tabelas de entidades e três de atributos de relacionamentos. |
| Entidades, atributos e relacionamentos | Seção 6 | Classificações, cardinalidades e restrições complementares. |
| DER anexado em imagem | Seção 7 | Imagem PNG do DER incluída no repositório e exibida diretamente no README. |
| Justificativa técnica | Seção 8 | Decisões e limites da representação. |
| Uso de IA | Seção 9 | Ferramentas, prompts, respostas, correções e reflexão. |
| Dicionário HTML conforme exemplo | Arquivo HTML, seções 1 a 6 | Notação, tabelas, índices propostos, log e matriz de acesso. |


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
| **Ferramenta e etapa** | Claude (Anthropic), em avaliação crítica do README, do DER e do dicionário, e na redação do dicionário em HTML e do README daquela revisão. |
| **Motivação** | Receber uma avaliação rigorosa, no papel de professor de modelagem, antes da entrega, e corrigir os problemas apontados. |
| **Prompt(s) utilizados** | "Quero que aja como um avaliador/professor de modelagem, nível muito exigente, e avalie esse meu trabalho"; "Crie um DER correto e coerente, usando o DER que já montei e colocando essas informações"; "Verifica agora, por favor" (a cada nova exportação do DER); "Monte um dicionário correto, com todas as informações, que não esteja vazio"; "Faça o README para mim, em base do que foi falado aqui". |
| **Resposta recebida** | Lista de erros do DER (cardinalidades invertidas, chaves compostas incompletas, chaves estrangeiras como atributo, atributos derivados e duplicados), uma proposta de DER corrigido, conferências a cada nova versão do PDF, o dicionário em HTML e este README. |
| **Fontes consultadas e verificadas** | O grupo conferiu cada apontamento no brModelo, reexportou o DER várias vezes e o submeteu a nova conferência; as regras RN-09 e RN-13 e os domínios (formas de pagamento, funções, OD/OE) vêm da entrevista e das respostas do gerente. |
| **Trechos rejeitados ou corrigidos** | A IA sugeriu cardinalidade (1,4), que o brModelo não oferece; o grupo usou (1,n) e registrou o limite de 4 como regra (RN-10). O grupo corrigiu manualmente o DER e removeu do dicionário a tabela de pendências. |
| **Justificativa da escolha final** | Mantivemos as correções que removem erros reais do DER e as decisões marcadas com † no dicionário, para deixar claro o que ainda não foi validado com a ótica. |
| **Reflexão crítica** | A IA leu o DER por imagem ampliada e chegou a ler uma etiqueta cortada, por isso as conferências foram repetidas a cada versão. Também não teve acesso à pasta de aulas do Drive. Tipos, tamanhos, listas de status, perfis de acesso e prazos de retenção são hipóteses de projeto e foram marcados com †, pois só a ótica pode confirmá-los. |

---

### Uso 7 - revisão após esclarecimentos do gerente (15/10/2026)

| Item | Registro |
| --- | --- |
| Ferramenta e etapa | ChatGPT/Codex: revisão do README, dicionário e roteiro de ajustes no DER. |
| Motivação | Corrigir divergências e incorporar respostas adicionais do gerente. |
| Prompt utilizado | "pronto? agora pode criar o dicionario e e readme, em base nisso e me fala oque fzer no der"; "concerte tudo em base oque o prfessor falou, (flxograma nn prcisa) o der só me explica oque precisa ser alterado e como". |
| Resposta recebida | Documentos revisados e guia de mudanças no diagrama; nova conferência pela avaliação do professor, com processos textuais e rastreabilidade, sem fluxograma. |
| Fontes consultadas e verificadas | README, HTML e DER publicados, esqueleto do professor e respostas transmitidas pelo grupo nesta conversa. Naquela revisão, a conferência final e a atualização do DER ainda eram etapas posteriores. |
| Trechos rejeitados ou corrigidos | Exemplo inicial de entrada de R$ 200 em venda de R$ 700 corrigido pelo usuário para R$ 210; parcela confirmada como mínimo de R$ 50. Removidas pendências já esclarecidas sobre orçamento, unidade das lentes e horário previsto. |
| Justificativa da escolha final | Manter as confirmações e identificar separadamente propostas técnicas; não atribuir ao gerente uma política de reembolso não informada. |
| Reflexão crítica | A IA não entrevistou o gerente diretamente e não valida práticas fiscais ou comerciais juridicamente. A coerência gráfica depende de o grupo aplicar e conferir o roteiro no brModelo. |


### Uso 8 — alinhamento ao DER final e preparação dos arquivos para GitHub


| Item | Registro |
| --- | --- |
| Ferramenta e etapa | ChatGPT/Codex, revisão do DER e geração do README e do dicionário HTML. |
| Motivação | Aplicar os apontamentos do professor e manter os documentos iguais ao DER final. |
| Prompt(s) utilizados | “Ajuste o DER com base nas alterações solicitadas pelo professor”; “Eu preciso que você atue como um fullstack em modelagem e dados, e cria um readme e o dicionario em html em base neste der [...] segue fielmente o dicionario e o esqueleto [...] é para colocar no github”. |
| Resposta recebida | Orientações para modificar o diagrama, conferência das exportações, PDF orientado para leitura e arquivos README/HTML com inventário comum. |
| Fontes consultadas e verificadas | DER.OFICIAL(1).pdf; Esqueleto da Entrega 1; exemplos 02-03g e 02-03h; README anterior e esclarecimentos desta conversa. Referências técnicas oficiais constam no HTML. A IA comparou os arquivos; essa comparação não substitui a revisão acadêmica do grupo. |
| Trechos rejeitados ou corrigidos | Removidas ligações diretas VENDA–PARCELA e VENDA–RECEITA; removidas entidades conceituais de itens de venda/compra/orçamento da documentação final para seguir o desenho. Corrigida a exigência indevida de compra sempre ter venda. Retirada orientação anterior de usar triângulo inexistente na versão do editor utilizada. |
| Justificativa da escolha final | Manter o DER elaborado pelo grupo e registrar suas restrições textuais; distinguir fatos levantados de propostas de implementação. |
| Reflexão crítica | A leitura de imagens pode confundir linhas e rótulos. Um atributo numero_linha não garante sozinho uma implementação correta das linhas repetidas; a próxima etapa precisa validar chaves e restrições. Tipos e políticas propostas não devem ser apresentados como práticas confirmadas da loja. |


### Uso 9 — reorganização do DER, especialização de PRODUTO e revisão final


| Item | Registro |
| --- | --- |
| Ferramenta e etapa | Claude (Anthropic), com acesso ao navegador: leitura do DER no brModelo, reorganização do layout, atualização do dicionário e do README e conferência final. |
| Motivação | Deixar o DER mais legível sem mudar seu conteúdo, incluir a especialização de PRODUTO nos documentos e corrigir os erros encontrados na última conferência. |
| Prompt(s) utilizados | “Quero que faça uma versão desse diagrama contendo as mesmas coisas só que preciso que fique mais organizado”; “agora quero que faça o dicionário desse diagrama utilizando o mesmo modelo do diagrama do Github adicione apenas o que não aparece nele”; “Agora coloque a foto do DER que vc fez mas antes compare os dois para ter a certeza de que estão iguais”; “Confira uma ultima vez o trabalho e veja se já está nos conformes”; “Quero que vc faça a correção dos erros de digitação do diagrama também”. |
| Resposta recebida | Versão reorganizada do DER (apenas posições e alinhamento dos rótulos), linhas do relacionamento ESPECIALIZA-SE EM no README e no dicionário HTML, conferência final dos arquivos, aplicação do novo layout e das correções no modelo do grupo no brModelo e nova imagem do DER. |
| Fontes consultadas e verificadas | DER público do grupo no brModelo, README e dicionário HTML do repositório. A IA comparou entidades, atributos, relacionamentos, cardinalidades e notas entre o diagrama reorganizado e o original, e entre a imagem e o README. Essa comparação não substitui a revisão acadêmica do grupo. |
| Trechos rejeitados ou corrigidos | Corrigidos no diagrama os textos “TEM OCOREÊNCIA” (agora “TEM OCORRÊNCIA”) e “finalidadde” (agora “finalidade”). Restaurados a legenda dos prefixos e os links da Seção 5 do README. Imagem do README trocada pela versão sem os erros de digitação. |
| Justificativa da escolha final | Manter o conteúdo do DER elaborado pelo grupo e mudar somente a organização visual, para que diagrama, dicionário e README continuem iguais. |
| Reflexão crítica | O grupo não tinha a versão reorganizada salva, então o layout foi reaplicado no brModelo a partir da imagem. A IA pode errar ao ler imagens e o resultado precisa ser conferido pelo grupo. A decisão sobre o conteúdo do modelo continua sendo do grupo. |



### Uso 10 — revisão de consistência documental (24/10/2026)

| Item | Registro |
| --- | --- |
| Ferramenta e etapa | ChatGPT (OpenAI), conectado ao GitHub: revisão da Entrega 1 e correções documentais no README e no dicionário HTML. |
| Motivação | Corrigir divergências confirmadas entre arquivos do mesmo projeto antes de avançar à Entrega 2. |
| Prompt(s) utilizados | “Reanalise [...] baseado no esqueleto da entrega 1 e no que tá lá no GitHub [...] encontre os problemas”; “Pega essas três [...] e estrutura [...] como você vai fazer a mudança”; “Analisa de novo o GitHub e tenta achar um porquê esses problemas estão aí”; “Pode ir lá no meu github e fazer os commits”. |
| Resposta recebida | Identificadas três inconsistências: RN-34 presente somente no README, links antigos de imagem/PDF no rodapé do HTML e afirmação no README sobre PDF não publicado. Proposta e execução de três commits documentais em branch separada no fork. |
| Fontes consultadas e verificadas | Esqueleto da Entrega 1 fornecido ao grupo, README, HTML, árvore de arquivos, histórico de commits e imagem do DER no GitHub. A RN-34 foi reproduzida conforme o README, sem novo levantamento de campo. |
| Trechos rejeitados ou corrigidos | Não foi criado um PDF apenas para manter um link antigo, nem foram alterados o DER, seus relacionamentos ou regras comerciais. Referências históricas a PDFs usados na elaboração foram preservadas. |
| Justificativa da escolha final | Manter o modelo conceitual e corrigir somente divergências verificáveis na documentação publicada. |
| Reflexão crítica | A IA não participou da entrevista com o gerente e não pode inferir a intenção dos autores dos commits. A conferência automatizada dos arquivos não substitui a revisão dos integrantes e do professor. |


## Critérios Atitudinais (20%)


Participação (5%), comprometimento (5%), colaboração (5%) e autonomia (5%) serão avaliados pela avaliação 360º entre integrantes e, quanto à colaboração, pelo histórico de commits. Este README não atribui notas nem declara contribuições individuais que não tenham sido verificadas.


## Resumo dos Pesos


| Dimensão | Peso total |
| --- | --- |
| Conceitual | 30% |
| Procedimental | 50% |
| Atitudinal | 20% |


**Entrega final:** `README.md` completo + DER em imagem + `Dicionario_de_Dados_Otica_Kadosh.html` anexados no mesmo repositório. A fotografia da visita é referenciada na Seção 1. A página HTML pode ser aberta após download ou publicada via GitHub Pages; o GitHub exibe o código do HTML na visualização padrão.
