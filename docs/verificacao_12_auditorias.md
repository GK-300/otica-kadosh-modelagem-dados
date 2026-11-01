# Checagem A01–A12 — PR #1

Fonte: `docs/script.sql` e regras RN-03, RN-04, RN-10, RN-11, RN-12, RN-14, RN-16, RN-18, RN-22, RN-23, RN-28 e RN-35 do README.

## Método e alcance

A massa do script foi lida por comandos `INSERT INTO ... VALUES`, respeitando aspas e ponto e vírgula dentro dos textos. As condições relevantes de cada auditoria foram **reproduzidas por cálculo independente nos registros extraídos**, inclusive vínculos e agregações. Isso permite conferir a consistência dos dados e dos filtros, **mas não equivale a executar as consultas no MySQL 8**. O script também executa três `UPDATE` e três `DELETE` efetivos (D01: um; D02: dois) antes das auditorias; eles não mudam os vínculos/valores usados para identificar as 21 anomalias listadas abaixo.

## Inventário dos 12 cenários

| Auditoria | IDs encontrados na massa (identificador principal) | Quantidade | Conclusão |
| --- | --- | ---: | --- |
| A01: pagamento sem nota | PAGAMENTO 443, 444 | 2 | Consulta mantida. A `UNIQUE` da nota limita duplicidade, mas não garante existência. |
| A02: compra sem nota | COMPRA 8 (`RECEBIDA`) | 1 | Consulta mantida. As 3 compras `SOLICITADA` da massa possuem nota; sob a **RN-35 escrita**, toda compra não cancelada deve ter uma. Alterar para filtrar só `RECEBIDA` exigiria revisar a RN-35. |
| A03: pagamento acima do total | VENDA 103, 319 | 2 | Consulta mantida. Total é derivado das linhas de `CONTEM`. |
| A04: entrada insuficiente | VENDA 128, 299 | 2 | **Corrigida.** A consulta original somava também `PARCIAL` e `QUITACAO_PARCELA`; a nova considera `SINAL` e pagamento `INTEGRAL` antecipado. Filtrar apenas `SINAL` seria incorreto para vendas integralmente pagas. |
| A05: lente de grau sem receita | VENDA 425, 454 | 2 | Consulta mantida. Só considera vendas não canceladas. |
| A06: produto sem subtipo | PRODUTO 351 | 1 | Consulta mantida. O subtipo é obrigatório na regra RN-14. |
| A07: saída com saldo negativo | ESTOQUE 1804 | 1 | Consulta mantida. A ordem por data e ID permite detectar saldo negativo após a saída. |
| A08: receita sem medida | RECEITA 45, 167 | 2 | Consulta mantida. |
| A09: venda sem linha | VENDA 712 | 1 | Consulta mantida. |
| A10: quitação com valor diferente | PAGAMENTO 530, 638 | 2 | Consulta mantida. |
| A11: orçamento ausente/inválido | VENDA 157, 306, 442 | 3 | **Corrigida.** Antes, um orçamento aprovado **após** a compra podia validar retroativamente a venda. Agora testa emissão ≤ aprovação ≤ venda ≤ validade. |
| A12: receita vencida/futura | VENDA 182, 213 | 2 | **Ampliada** para detectar receita emitida no futuro em relação à compra. Não há caso desse tipo na massa atual. |

**Total: 21 casos intencionais (2+1+2+2+2+1+1+2+1+2+3+2).**

## Testes de fronteira do raciocínio

- A04: pedido de R$ 100 e `SINAL=15` → apontar; `SINAL=30` → não apontar; `INTEGRAL=100` → não apontar; `PARCIAL=40` sem sinal/integral → apontar.
- A11: emitido 10:00, venda 11:00, aprovado 12:00, válido até 18:00 → **apontar**; aprovado 10:30 e venda 11:00 → não apontar. O DER ainda não permite provar qual orçamento foi convertido quando houver vários no atendimento.
- A12: receita emitida após a data de compra → apontar; receita dentro de um ano anterior à compra → não apontar.

## Pendências reais

1. Executar `docs/script.sql` num banco **descartável** MySQL 8 e comparar os resultados reais de A01–A12. O script apaga `otica_kadosh` por meio de `DROP DATABASE IF EXISTS`.
2. Para A04, `DT_LIBERACAO_ENCOMENDA` e `DT_PAGAMENTO` guardam **somente datas**. O modelo não verifica se o sinal foi recebido **antes da liberação dentro do mesmo dia**. Isso requer validação de campo e eventual mudança coordenada de tipo/atributo.
3. Confirmar com a ótica a interpretação do pagamento integral e o momento de emissão da nota fiscal de entrada em compras `SOLICITADA`. O código segue a documentação vigente, sem criar regras novas.
4. A01–A12 são auditorias, não proteções transacionais: detectar uma violação após a carga não garante bloqueá-la na gravação.
5. A data corrente afeta as consultas de situação das parcelas, mas não altera os 21 casos intencionais desta conferência.

## Divergência documental corrigida

A massa contém **352 PRODUTO**, sendo **231 ARMACAO**, **120 LENTE** e **1 produto sem subtipo**. A tabela do README indicava 351/230/120. O README foi ajustado para refletir os `INSERT` reais.
