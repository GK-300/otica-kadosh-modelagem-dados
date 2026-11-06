#!/usr/bin/env python3
"""Gera o DER conceitual da Ótica Kadosh a partir das entidades SQL e dos relacionamentos do README.

Não transforma FKs em relações conceituais automaticamente: REL é uma transcrição
revisável das cardinalidades e dos nomes de relacionamento da seção 1.1.
Uso: python3 docs/gerar_der_conceitual.py docs/script.sql DER_OticaKadosh
Requer Graphviz (dot). Produz .dot, .png e .svg.
"""
import re
import subprocess
import sys

SQL = sys.argv[1] if len(sys.argv) > 1 else "docs/script.sql"
OUT = sys.argv[2] if len(sys.argv) > 2 else "DER_OticaKadosh"
source = open(SQL, encoding="utf8").read().split("-- 4. INSERT INTO")[0]

tables = {}
for m in re.finditer(r"CREATE TABLE (\w+) \((.*?)\n\) ENGINE", source, re.S):
    name, body = m.groups()
    if name == "CONTEM":
        continue  # no conceitual, CONTÉM é relacionamento N:N com atributos
    cols = []
    pk = []
    for line in body.split("\n"):
        item = line.strip()
        if item.startswith("PRIMARY KEY"):
            pk = [c.strip() for c in re.search(r"\((.*)\)", item).group(1).split(",")]
        else:
            cm = re.match(r"(\w+)\s+(\w+(?:\([\d,]+\))?)", item)
            if cm:
                cols.append(cm.group(1))
    tables[name] = (cols, pk)

# Entidade A, relacionamento, entidade B, cardinalidade em A, cardinalidade em B.
REL = [
    ("CLIENTE", "SOLICITA", "ATENDIMENTO", "(0,n)", "(1,1)"),
    ("FUNCIONARIO", "CONDUZ", "ATENDIMENTO", "(0,n)", "(1,1)"),
    ("ATENDIMENTO", "ORIGINA", "RECEITA", "(0,1)", "(1,1)"),
    ("RECEITA", "POSSUI", "RECEITA_MEDIDA", "(1,n)", "(1,1)"),
    ("ATENDIMENTO", "ORIGINA ORÇAMENTO", "ORCAMENTO", "(0,n)", "(1,1)"),
    ("ATENDIMENTO", "RESULTA EM", "VENDA", "(0,1)", "(1,1)"),
    ("VENDA", "CONTÉM\\nnº linha · qtd. · preço · obs.", "PRODUTO", "(1,n)", "(0,n)"),
    ("VENDA", "RECEBE", "PAGAMENTO", "(0,n)", "(1,1)"),
    ("VENDA", "PARCELA SALDO EM", "PARCELA", "(0,n)", "(1,1)"),
    ("PAGAMENTO", "QUITA", "PARCELA", "(0,1)", "(0,1)"),
    ("PAGAMENTO", "GERA", "NOTA_FISCAL_SAIDA", "(1,1)", "(1,1)"),
    ("NOTA_FISCAL_SAIDA", "REFERE-SE A", "TROCA_DEVOLUCAO", "(0,n)", "(1,1)"),
    ("FORNECEDOR", "FORNECE", "COMPRA", "(0,n)", "(1,1)"),
    ("VENDA", "DEMANDA", "COMPRA", "(0,n)", "(0,1)"),
    ("COMPRA", "POSSUI", "NOTA_FISCAL_ENTRADA", "(1,1)", "(1,1)"),
    ("COMPRA", "GERA ENTRADA", "ESTOQUE", "(0,n)", "(0,1)"),
    ("PRODUTO", "É MOVIMENTADO EM", "ESTOQUE", "(0,n)", "(1,1)"),
    ("PRODUTO", "ESPECIALIZA-SE EM", "LENTE", "(1,1)", "(0,1)"),
    ("PRODUTO", "ESPECIALIZA-SE EM", "ARMACAO", "(1,1)", "(0,1)"),
]
assert len(tables) == 18, len(tables)
assert len(REL) == 19, len(REL)
assert ("VENDA", "PARCELA") in {(a, b) for a, _, b, _, _ in REL}
for a, _, b, _, _ in REL:
    assert a in tables and b in tables, (a, b)

# Só atributos do próprio objeto: chaves estrangeiras pertencem ao modelo lógico.
fk_columns = {}
for match in re.finditer(r"ALTER TABLE (\w+)\s+ADD CONSTRAINT fk_\w+\s+FOREIGN KEY \(([^)]+)\)", source):
    name, cols = match.groups()
    fk_columns.setdefault(name, set()).update(c.strip() for c in cols.split(","))

def esc(txt):
    return txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

lines = [
    "graph DER {",
    'graph [rankdir=LR, bgcolor="white", overlap=false, splines=polyline, pad=0.55, '
    'nodesep=0.42, ranksep=1.05, fontname="Helvetica", labelloc=t, fontsize=26, '
    'label="Ótica Kadosh — modelo conceitual revisado\\n18 entidades · 19 relacionamentos · cardinalidades (mín,máx)"];',
    'node [fontname="Helvetica", fontsize=11];',
    'edge [color="#6a7a8a", fontname="Helvetica", fontsize=10, fontcolor="#263238"];',
]

for name, (cols, pk) in tables.items():
    attributes = [c for c in cols if c not in fk_columns.get(name, set()) or c in pk]
    items = [
        '<TR><TD BGCOLOR="#244563"><FONT COLOR="white"><B>%s</B></FONT></TD></TR>' % esc(name)
    ]
    for col in attributes:
        label = ("<U>%s</U>" % esc(col)) if col in pk else esc(col)
        items.append('<TR><TD ALIGN="LEFT" BGCOLOR="#f7f9fc">%s</TD></TR>' % label)
    lines.append('"%s" [shape=plain label=<<TABLE BORDER="1" COLOR="#244563" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">%s</TABLE>>];' %
                 (name, "".join(items)))

for i, (a, relation, b, ca, cb) in enumerate(REL, 1):
    rel_node = "R%02d" % i
    label = relation.replace("\\n", "\n")
    # \n só é usado no rótulo do relacionamento CONTÉM.
    label = label.replace('"', '\\"').replace("\n", "\\n")
    lines.append('"%s" [shape=diamond, style=filled, fillcolor="#ebf3f8", color="#3a6689", '
                 'fontsize=10, label="%s", margin=0.11];' % (rel_node, label))
    lines.append('"%s" -- "%s" [taillabel="%s", labeldistance=1.6];' % (a, rel_node, ca))
    lines.append('"%s" -- "%s" [headlabel="%s", labeldistance=1.6];' % (rel_node, b, cb))

lines.append("}")
with open(OUT + ".dot", "w", encoding="utf8") as file:
    file.write("\n".join(lines))
subprocess.run(["dot", "-Tpng", "-Gdpi=110", OUT + ".dot", "-o", OUT + ".png"], check=True)
subprocess.run(["dot", "-Tsvg", OUT + ".dot", "-o", OUT + ".svg"], check=True)
print("ok:", len(tables), "entidades,", len(REL), "relacionamentos")
