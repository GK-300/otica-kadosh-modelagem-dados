# Revisão de integridade — vínculo entre VENDA e PARCELA (branch de integridade)

## Problema confirmado

No DER da Entrega 1, PARCELA se ligava apenas opcionalmente a PAGAMENTO por QUITA.
No SQL anterior, PARCELA tinha só ID_PARCELA, NR_PARCELA, VL_PARCELA e DT_VENCIMENTO.
Uma parcela ainda aberta não tinha caminho relacional até VENDA/CLIENTE.
Além disso, a FK simples PAGAMENTO.ID_PARCELA_QUITADA → PARCELA.ID_PARCELA
não impedia que um pagamento da venda A quitasse uma parcela da venda B.

Esta é uma limitação específica do modelo e compromete o acompanhamento das
parcelas em aberto; não é recomendação genérica de "adicionar mais tabelas".

## Decisão técnica e riscos

- Novo relacionamento conceitual VENDA (0,n) — PARCELA SALDO EM —
  PARCELA (1,1). Uma venda sem parcelamento permanece válida.
- A tabela PARCELA recebe ID_VENDA INT NOT NULL com FK para VENDA. Não
  alterar a identidade própria ID_PARCELA, preservada do DER original.
- UNIQUE (ID_VENDA, NR_PARCELA) impede repetir número dentro da mesma venda;
  UNIQUE (ID_PARCELA, ID_VENDA) dá alvo explícito para a FK composta.
- PAGAMENTO mantém ID_VENDA e ID_PARCELA_QUITADA (opcional, UNIQUE). A
  FK composta (ID_PARCELA_QUITADA, ID_VENDA) → PARCELA (ID_PARCELA, ID_VENDA)
  rejeita quitações cruzadas. Pagamentos de sinal e integrais continuam
  com ID_PARCELA_QUITADA NULL (não mudam).
- ON DELETE/UPDATE RESTRICT conserva a política do projeto.
- Nenhuma nova entidade e nenhuma tabela extra: permanecem 19 tabelas.
  O modelo lógico passa a 20 FKs e 10 UNIQUE nomeadas.

## Migração da massa de dados

A massa gerada com semente fixa 20261030 já guardava a venda em
cada objeto de parcela, mas o escritor SQL omitira esse dado. A
regeneração preserva as 850 parcelas e os valores, datas e IDs existentes.
São 232 vendas parceladas; o gerador determina sem ambiguidade a venda
de origem. Somente o ID_VENDA é acrescentado aos INSERT de PARCELA.

Não deduzir a venda de uma parcela aberta apenas pelo valor e vencimento:
há pelo menos um caso com duas vendas candidatas (IDs 607 e 619) e
a parcela de ID 708 pertence à venda 619. A ordem determinística do
gerador permite identificar a associação original.

## Verificações e efeitos colaterais

1. Checar que a nova coluna é obrigatória e referencia uma venda existente.
2. Conferir 850 parcelas e 232 vendas parceladas; nenhuma chave ausente.
3. Impedir (em MySQL 8) uma quitação cruzada por INSERT de teste.
4. Validar números de parcela únicos por venda e manter o QUITA 1:1.
5. Preservar a massa de pagamentos, notas, produtos e as 21 anomalias
   intencionais das auditorias A01–A12.
6. A consulta J07 passa a mostrar parcelas abertas/atrasadas por cliente.
7. Gerar novamente DER e diagrama lógico a partir do esquema revisado,
   atualizar dicionário e README, e revisar legibilidade e apresentação.

## O que NÃO foi resolvido

- A soma das parcelas em cada plano continua sendo uma regra agregada;
  UNIQUE e FK não garantem, sozinhas, a igualdade com o saldo da venda.
- A data de vencimento e a situação de atraso dependem da data de
  referência da consulta.
- O vínculo da PARCELA à VENDA melhora a rastreabilidade, mas
  não implementa automaticamente um modelo preditivo de inadimplência.
- A apresentação de slides foi produzida antes desta revisão e deve ser
  atualizada quanto à quantidade de FKs e ao novo relacionamento.
- Alteração conceitual proposta pelo grupo e sujeita à aprovação antes
  do merge; não foi validada como política nova pelo gerente da ótica.

Este arquivo documenta a justificativa de um ajuste preciso, não
autoriza expandir outras relações sem confirmação.
