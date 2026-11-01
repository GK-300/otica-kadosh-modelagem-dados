-- Consultas de DIAGNÓSTICO de auditoria para revisão do PR #1.
-- Somente SELECT; execute depois de carregar a massa em um banco descartável.
-- Duplicam, para conferência, as condições agora corrigidas em A04/A11 de script.sql.
USE otica_kadosh;

-- D04: sinal mínimo RN-18 ou quitação integral antes da liberação.
-- PARCIAL e QUITACAO_PARCELA não são sinal, e não entram neste cálculo.
-- Pagamento integral do pedido satisfaz o mínimo financeiro sem sinal separado.
SELECT v.ID_VENDA, v.DT_LIBERACAO_ENCOMENDA, t.VL_TOTAL,
       COALESCE(SUM(p.VL_PAGAMENTO), 0) AS sinal_ou_integral_ate_liberacao
  FROM VENDA v
  JOIN vw_venda_total t ON t.ID_VENDA = v.ID_VENDA
  LEFT JOIN PAGAMENTO p
    ON p.ID_VENDA = v.ID_VENDA
   AND p.TP_FINALIDADE IN ('SINAL','INTEGRAL')
   AND p.DT_PAGAMENTO <= v.DT_LIBERACAO_ENCOMENDA
 WHERE v.DT_LIBERACAO_ENCOMENDA IS NOT NULL AND t.VL_TOTAL > 0
 GROUP BY v.ID_VENDA, v.DT_LIBERACAO_ENCOMENDA, t.VL_TOTAL
HAVING COALESCE(SUM(p.VL_PAGAMENTO), 0) < 0.30 * t.VL_TOTAL
 ORDER BY v.ID_VENDA;

-- D11: ordem cronológica válida de orçamento, aprovação e fechamento.
-- A existência de um orçamento no mesmo atendimento continua não comprovando
-- qual orçamento foi efetivamente convertido; esta é uma verificação limitada.
SELECT v.ID_VENDA, v.DH_COMPRA, v.ID_ATENDIMENTO
  FROM VENDA v
 WHERE NOT EXISTS (
       SELECT 1
         FROM ORCAMENTO o
        WHERE o.ID_ATENDIMENTO = v.ID_ATENDIMENTO
          AND o.CD_STATUS = 'APROVADO'
          AND o.DH_APROVACAO IS NOT NULL
          AND o.DH_EMISSAO <= o.DH_APROVACAO
          AND o.DH_APROVACAO <= v.DH_COMPRA
          AND v.DH_COMPRA <= o.DH_VALIDADE
       )
 ORDER BY v.DH_COMPRA;
