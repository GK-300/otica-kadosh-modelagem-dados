# Auditoria de consistência — PR #1 (Entrega 2)

Escopo: comparação da revisão conceitual documentada no `README.md`, do inventário do dicionário HTML e das instruções `CREATE TABLE` do `docs/script.sql`. Esta revisão **não executa** o SQL no MySQL e **não substitui** a conferência visual do DER ou do modelo lógico; essas validações têm etapas próprias.

## Resultado confirmado

- **18 entidades conceituais → 19 tabelas físicas não é um erro.** As 18 entidades listadas na seção 1.2 do README geram 18 tabelas. O relacionamento N:N `VENDA — CONTÉM — PRODUTO`, com atributos `NR_LINHA`, `QT_PRODUTO`, `VL_PRECO_UNITARIO` e `DS_OBSERVACAO`, gera a 19ª tabela, `CONTEM`. Não adicionar uma 19ª entidade ao DER para forçar igualdade.
- O inventário de entidades do dicionário HTML corresponde à relação de entidades da seção «Entidades → tabelas» do README. `CONTEM` não é entidade autônoma no DER; sua tabela no SQL deriva do relacionamento.
- No script, `NOTA_FISCAL_SAIDA` e `NOTA_FISCAL_ENTRADA` são tabelas de entidades do DER revisado. A distinção em relação às versões anteriores é **mudança de modelo documentada**, não duplicação automática.

## Lacunas reais de rastreabilidade — já assumidas no README

| Origem no DER | Efeito verificável no modelo lógico | Decisão segura nesta etapa |
| --- | --- | --- |
| `ORCAMENTO` não se relaciona diretamente com `VENDA` ou `PRODUTO`. | É possível localizar orçamentos e vendas do mesmo atendimento, mas não demonstrar qual proposta foi convertida nem os itens originalmente ofertados. | Manter como **limitação**, não inferir origem por simples coexistência. Discutir com o grupo antes de revisar DER, dicionário, SQL e consultas em conjunto. |
| `PARCELA` não se liga à `VENDA` nem ao pagamento que originou o plano. | Uma parcela ainda em aberto não pode ser associada de forma confiável a um cliente ou venda. | Não criar FK isolada no SQL, pois isso diverge do DER; propor alteração conceitual coordenada no PR de chaves e cardinalidades. |
| `TROCA_DEVOLUCAO` referencia nota fiscal, mas não identifica a linha/produto vendido. | Histórico da ocorrência existe, mas a rastreabilidade da unidade devolvida é insuficiente. | Não presumir produto a partir da nota: revisar o caso de negócio e a participação de `CONTEM`. |
| `ESTOQUE` referencia produto e, opcionalmente, compra; não tem origem direta de saída por venda. | `CD_MOTIVO` descreve a origem, mas não comprova qual transação provocou a saída. | Manter a limitação explícita; propor alteração de vínculos somente após validar regras para movimentos. |
| `COMPRA` não detalha itens e custos unitários. | Entradas de estoque indicam produto e quantidade recebidos, mas não constituem histórico integral do pedido. | Evitar declarar que as compras têm itens auditáveis até revisão do DER. |

## Verificações pendentes (sem afirmar êxito)

1. Inspecionar visualmente `DER_OticaKadosh.png` e `docs/modelo_logico.png`, inclusive cardinalidades e legibilidade. A conferência textual do inventário não valida a geometria do desenho.
2. Executar `docs/script.sql` em **banco descartável** MySQL 8. O script contém `DROP DATABASE IF EXISTS otica_kadosh` e apaga integralmente o banco de mesmo nome.
3. Conferir erros do MySQL, integridade de chaves e resultados das auditorias A01–A12 antes de declarar implementação validada.
4. Confirmar com o grupo qual versão conceitual será congelada para a entrega e se as lacunas acima serão corrigidas na Entrega 2 ou documentadas como limitações.

## Regra para futuras alterações

Toda inclusão de vínculo/atributo de negócio deve ser refletida de maneira consistente no **DER → README → dicionário → modelo lógico → SQL → massa de dados → consultas**. Não corrigir lacunas conceituais apenas adicionando uma FK ao script.

A auditoria automática em `docs/verificar_consistencia.py` verifica somente **nomes e inventários estruturais**. Um resultado positivo não garante correção semântica ou execução do SQL.

## Revisão adicional das consultas de auditoria (31/10/2026)

Foram conferidas as consultas A04 e A11 de `docs/script.sql`. Há dois **riscos confirmados na lógica das consultas**, independentemente da existência de registros que os acionem na massa atual:

1. **A04 — sinal de 30%:** o filtro soma todos os `PAGAMENTO` anteriores à data de liberação, mesmo que `TP_FINALIDADE` seja `PARCIAL`, `INTEGRAL` ou `QUITACAO_PARCELA`. Isso não mede especificamente o sinal definido pela RN-18. Solução de diagnóstico: contar apenas `TP_FINALIDADE = 'SINAL'`. **Ressalva:** uma venda paga integralmente pode exigir uma interpretação de negócio distinta; confirmar com o grupo antes de alterar a regra definitiva.
2. **A11 — orçamento válido:** a consulta exige status `APROVADO` e que a venda tenha ocorrido até a validade, mas não testa se `DH_APROVACAO <= DH_COMPRA` ou se a aprovação veio depois da emissão. Isso permite que a auditoria deixe de apontar uma venda feita **antes** da aprovação. Solução de diagnóstico: exigir `DH_EMISSAO <= DH_APROVACAO <= DH_COMPRA <= DH_VALIDADE`. Essa verificação ainda não cria vínculo inequívoco de um orçamento específico com a venda.

As consultas propostas ficam isoladas em `docs/consultas_diagnostico_pr1.sql` para não alterar diretamente a Entrega 2 sem teste no MySQL. Elas não modificam dados nem substituem as A04/A11 originais. A execução e o resultado sobre a massa de dados seguem **pendentes**.
