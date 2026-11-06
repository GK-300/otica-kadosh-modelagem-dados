-- Ótica Kadosh — revisão de integridade: diagnóstico somente leitura do vínculo VENDA–PARCELA.
-- Executar SOMENTE depois de carregar docs/script.sql num MySQL 8 descartável.
USE otica_kadosh;

-- Todos os grupos de parcelas devem pertencer a uma venda existente.
-- Esperado: 850 parcelas e zero órfãs.
SELECT COUNT(*) AS parcelas, COUNT(DISTINCT ID_VENDA) AS vendas_parceladas
  FROM PARCELA;
SELECT COUNT(*) AS parcelas_sem_venda
  FROM PARCELA p LEFT JOIN VENDA v ON v.ID_VENDA = p.ID_VENDA
 WHERE v.ID_VENDA IS NULL;

-- Não pode haver duas parcelas com o mesmo número na mesma venda.
SELECT ID_VENDA, NR_PARCELA, COUNT(*) AS repeticoes
  FROM PARCELA
 GROUP BY ID_VENDA, NR_PARCELA HAVING COUNT(*) > 1;

-- Uma quitação nunca pode cruzar vendas.
SELECT g.ID_PAGAMENTO, g.ID_VENDA AS venda_do_pagamento,
       p.ID_VENDA AS venda_da_parcela, p.ID_PARCELA
  FROM PAGAMENTO g
  JOIN PARCELA p ON p.ID_PARCELA = g.ID_PARCELA_QUITADA
 WHERE g.ID_VENDA <> p.ID_VENDA;

-- Consulta operacional: parcelas ainda abertas ou vencidas com cliente.
-- Não atribuir parcelas a cliente usando aproximações de data ou valor.
SELECT p.ID_PARCELA, p.ID_VENDA, p.NR_PARCELA,
       c.ID_CLIENTE, c.NM_CLIENTE, p.DT_VENCIMENTO,
       p.VL_PARCELA, vps.CD_SITUACAO
  FROM PARCELA p
  JOIN VENDA v ON v.ID_VENDA = p.ID_VENDA
  JOIN ATENDIMENTO a ON a.ID_ATENDIMENTO = v.ID_ATENDIMENTO
  JOIN CLIENTE c ON c.ID_CLIENTE = a.ID_CLIENTE
  JOIN vw_parcela_situacao vps ON vps.ID_PARCELA = p.ID_PARCELA
 WHERE vps.CD_SITUACAO IN ('ABERTA','ATRASADA')
 ORDER BY p.DT_VENCIMENTO, p.ID_VENDA, p.NR_PARCELA
 LIMIT 20;

-- A01–A12 continuam intencionalmente com 21 casos; não corrigir a massa.
