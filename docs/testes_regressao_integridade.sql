-- Verificações de regressão para as correções de integridade do PR #2.
-- Executar no MySQL 8 SOMENTE após carregar docs/script.sql num banco de TESTE.
-- Este arquivo não modifica dados. O script.sql principal APAGA otica_kadosh.
USE otica_kadosh;

-- RN-21: em uma retirada efetiva o canhoto deve ter sido confirmado.
-- Esperado na massa de dados atual: 0.
SELECT 'RN21: retirada sem canhoto ou sem data' AS teste, COUNT(*) AS violacoes
  FROM VENDA
 WHERE (DT_RETIRADA IS NOT NULL AND COALESCE(IN_CANHOTO_CONFERIDO, FALSE) <> TRUE)
    OR (CD_STATUS = 'RETIRADO'
        AND (DT_RETIRADA IS NULL OR COALESCE(IN_CANHOTO_CONFERIDO, FALSE) <> TRUE));

-- RN-06: compras recebidas obrigatoriamente têm data da chegada.
-- Esperado na massa de dados atual: 0.
SELECT 'RN06: recebida sem chegada' AS teste, COUNT(*) AS violacoes
  FROM COMPRA
 WHERE CD_STATUS = 'RECEBIDA' AND DT_CHEGADA IS NULL;

-- Demonstração do caso-limite que escapava ao CHECK anterior.
-- NULL não é FALSE em SQL: CHECK rejeita FALSE, mas aceita UNKNOWN.
-- Esperado: expressao_anterior = NULL, expressao_nova = 0.
SELECT (NULL = TRUE) AS expressao_anterior,
       (COALESCE(NULL, FALSE) = TRUE) AS expressao_nova;

-- G09: contar eventos e vendas distintas afetadas separadamente.
-- Um pedido pode produzir vários eventos; cancelar uma venda a tira das
-- duas métricas (numerador e denominador).
SELECT DATE_FORMAT(v.DH_COMPRA, '%Y-%m') AS mes,
       COUNT(*) AS ocorrencias,
       COUNT(DISTINCT v.ID_VENDA) AS vendas_afetadas
  FROM TROCA_DEVOLUCAO t
  JOIN NOTA_FISCAL_SAIDA n ON n.ID_NOTA_SAIDA = t.ID_NOTA_SAIDA
  JOIN PAGAMENTO p ON p.ID_PAGAMENTO = n.ID_PAGAMENTO
  JOIN VENDA v ON v.ID_VENDA = p.ID_VENDA
 WHERE v.CD_STATUS <> 'CANCELADO' AND v.DH_COMPRA >= '2026-09-01'
 GROUP BY DATE_FORMAT(v.DH_COMPRA, '%Y-%m')
 ORDER BY mes;

-- Exemplo sintético (sem alteração da base): duas ocorrências ligadas
-- à mesma venda continuam sendo apenas uma venda afetada.
-- Esperado: ocorrencias = 3; vendas_afetadas = 2.
WITH exemplo AS (
  SELECT 1 AS ID_VENDA UNION ALL
  SELECT 1 UNION ALL
  SELECT 2
)
SELECT COUNT(*) AS ocorrencias, COUNT(DISTINCT ID_VENDA) AS vendas_afetadas
  FROM exemplo;

-- RN-22: comparar valor registrado na nota de saída e no pagamento.
-- Diagnóstico (não restrição fiscal automática): esperado na massa atual: 0.
SELECT n.ID_NOTA_SAIDA, n.NR_NOTA, n.VL_TOTAL AS valor_nota,
       p.ID_PAGAMENTO, p.VL_PAGAMENTO AS valor_pagamento
  FROM NOTA_FISCAL_SAIDA n
  JOIN PAGAMENTO p ON p.ID_PAGAMENTO = n.ID_PAGAMENTO
 WHERE n.VL_TOTAL <> p.VL_PAGAMENTO;

-- Numeração de saída repetida: investigar se há série fiscal omitida no modelo.
-- Não impor UNIQUE antes da confirmação da regra fiscal e da série.
-- Esperado na massa fictícia: 0.
SELECT NR_NOTA, COUNT(*) AS repeticoes
  FROM NOTA_FISCAL_SAIDA
 GROUP BY NR_NOTA
HAVING COUNT(*) > 1;

-- A numeração de entrada é controlada por fornecedor. Números iguais entre
-- fornecedores diferentes não são, por si só, inconsistência.
-- Esperado na massa fictícia: 0.
SELECT c.ID_FORNECEDOR, n.NR_NOTA, COUNT(*) AS repeticoes
  FROM NOTA_FISCAL_ENTRADA n
  JOIN COMPRA c ON c.ID_COMPRA = n.ID_COMPRA
 GROUP BY c.ID_FORNECEDOR, n.NR_NOTA
HAVING COUNT(*) > 1;
