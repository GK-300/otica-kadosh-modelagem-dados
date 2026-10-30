#!/usr/bin/env python3
"""
Ótica Kadosh — gerador do diagrama do modelo lógico (seção 2 da Entrega 2).

Lê o próprio script.sql (CREATE TABLE e ALTER TABLE ... FOREIGN KEY), de modo que
o diagrama sempre reflete o banco. As cardinalidades (mín,máx) são as do DER,
registradas na tabela REL abaixo (iguais às da seção 1.2 do README).

Uso:  python3 gerar_diagrama_logico.py script.sql modelo_logico
Saída: modelo_logico.dot, modelo_logico.png e modelo_logico.svg
Requisito: Graphviz instalado (comando `dot`) e Python 3.
"""
import re, subprocess, sys

SQL = sys.argv[1] if len(sys.argv) > 1 else 'script.sql'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'modelo_logico'

ddl = open(SQL, encoding='utf8').read()
# só a parte de CREATE TABLE / ALTER TABLE (antes da massa de dados)
ddl = ddl.split('-- 4. INSERT INTO')[0]

tables, order = {}, []
for m in re.finditer(r'CREATE TABLE (\w+) \((.*?)\n\) ENGINE', ddl, re.S):
    name, body = m.groups()
    cols, pk = [], []
    for line in body.split('\n'):
        line = line.strip().rstrip(',')
        if not line or line.startswith('--'):
            continue
        if line.startswith('PRIMARY KEY'):
            pk = [c.strip() for c in re.search(r'\((.*)\)', line).group(1).split(',')]
            continue
        cm = re.match(r'(\w+)\s+(\w+(?:\([\d,]+\))?)', line)
        if cm:
            cols.append(cm.groups())
    tables[name] = dict(cols=cols, pk=pk)
    order.append(name)

fks = []
for m in re.finditer(r'ALTER TABLE (\w+)\s+ADD CONSTRAINT (\w+)\s+FOREIGN KEY \(([^)]*)\)\s+'
                     r'REFERENCES (\w+) \(([^)]*)\)', ddl):
    t, _, c, p, pc = m.groups()
    fks.append((t, [x.strip() for x in c.split(',')], p, [x.strip() for x in pc.split(',')]))
assert len(tables) == 19 and len(fks) == 19, (len(tables), len(fks))

# (tabela filha, 1ª coluna da FK) -> (relacionamento, cardinalidade da tabela referenciada, da tabela filha)
REL = {
 ('ATENDIMENTO', 'ID_CLIENTE'): ('SOLICITA', '(0,n)', '(1,1)'),
 ('ATENDIMENTO', 'ID_FUNCIONARIO'): ('CONDUZ', '(0,n)', '(1,1)'),
 ('RECEITA', 'ID_ATENDIMENTO'): ('ORIGINA', '(0,1)', '(1,1)'),
 ('RECEITA_MEDIDA', 'ID_RECEITA'): ('POSSUI', '(1,n)', '(1,1)'),
 ('ORCAMENTO', 'ID_ATENDIMENTO'): ('ORIGINA ORÇAMENTO', '(0,n)', '(1,1)'),
 ('VENDA', 'ID_ATENDIMENTO'): ('RESULTA EM', '(0,1)', '(1,1)'),
 ('CONTEM', 'ID_VENDA'): ('CONTÉM', '(1,n)', '(1,1)'),
 ('CONTEM', 'ID_PRODUTO'): ('CONTÉM', '(0,n)', '(1,1)'),
 ('PAGAMENTO', 'ID_VENDA'): ('RECEBE', '(0,n)', '(1,1)'),
 ('PAGAMENTO', 'ID_PARCELA_QUITADA'): ('QUITA', '(0,1)', '(0,1)'),
 ('NOTA_FISCAL_SAIDA', 'ID_PAGAMENTO'): ('GERA', '(1,1)', '(1,1)'),
 ('TROCA_DEVOLUCAO', 'ID_NOTA_SAIDA'): ('REFERE-SE A', '(0,n)', '(1,1)'),
 ('COMPRA', 'ID_FORNECEDOR'): ('FORNECE', '(0,n)', '(1,1)'),
 ('COMPRA', 'ID_VENDA'): ('DEMANDA', '(0,n)', '(0,1)'),
 ('NOTA_FISCAL_ENTRADA', 'ID_COMPRA'): ('POSSUI', '(1,1)', '(1,1)'),
 ('ESTOQUE', 'ID_PRODUTO'): ('É MOVIMENTADO EM', '(0,n)', '(1,1)'),
 ('ESTOQUE', 'ID_COMPRA'): ('GERA ENTRADA', '(0,n)', '(0,1)'),
 ('LENTE', 'ID_PRODUTO'): ('ESPECIALIZA-SE EM', '(1,1)', '(0,1)'),
 ('ARMACAO', 'ID_PRODUTO'): ('ESPECIALIZA-SE EM', '(1,1)', '(0,1)'),
}

fkcols = {t: set() for t in tables}
for t, c, p, pc in fks:
    fkcols[t].update(c)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

o = ['digraph G {',
     'graph [rankdir=LR, bgcolor="white", nodesep=0.55, ranksep=1.5, splines=true, pad=0.4, '
     'fontname="Helvetica", labelloc=t, fontsize=26, label=<<B>Modelo lógico — Ótica Kadosh</B><BR/>'
     '<FONT POINT-SIZE="15">19 tabelas · 19 chaves estrangeiras · cardinalidades (mín,máx) em cada ponta '
     '· PK = chave primária, FK = chave estrangeira</FONT>>];',
     'node [shape=plain, fontname="Helvetica", fontsize=12];',
     'edge [fontname="Helvetica", fontsize=10, arrowhead=none, color="#44546a", fontcolor="#222222", '
     'labelfontsize=12, labelfontname="Helvetica-Bold", labeldistance=1.7];']

for t in order:
    d = tables[t]
    rows = [f'<TR><TD COLSPAN="3" BGCOLOR="#1f4e79"><FONT COLOR="white"><B>{t}</B></FONT></TD></TR>']
    for n, ty in d['cols']:
        ispk, isfk = n in d['pk'], n in fkcols[t]
        mk = ', '.join(x for x, b in (('PK', ispk), ('FK', isfk)) if b)
        bg = '#fff2cc' if ispk else ('#deebf7' if isfk else 'white')
        nm = f'<B>{n}</B>' if ispk else n
        mkc = f'<B><FONT POINT-SIZE="11" COLOR="#7f6000">{mk}</FONT></B>' if mk else ' '
        rows.append(f'<TR><TD BGCOLOR="{bg}" ALIGN="LEFT" PORT="l_{n}">{nm}</TD>'
                    f'<TD BGCOLOR="{bg}" ALIGN="LEFT"><FONT COLOR="#555555">{esc(ty)}</FONT></TD>'
                    f'<TD BGCOLOR="{bg}" ALIGN="LEFT">{mkc}</TD></TR>')
    o.append(f'"{t}" [label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" '
             f'COLOR="#1f4e79">{"".join(rows)}</TABLE>>];')

# O ângulo afasta os rótulos de cardinalidade das ligações que saem ou chegam na mesma tabela.
ANG = {}      # (tabela filha, 1ª coluna da FK) -> ângulo; 1ª FK da tabela filha gira para um lado, a 2ª para o outro
cont = {}
for t, c, p, pc in fks:
    j = cont.get(t, 0); cont[t] = j + 1
    ANG[(t, c[0])] = (-35, 35)[j % 2]
ANG.update({('LENTE', 'ID_PRODUTO'): -70, ('ESTOQUE', 'ID_PRODUTO'): 40})   # ajustes finos de legibilidade
seen = {}
for t, c, p, pc in fks:
    name, cp, cf = REL[(t, c[0])]
    k = seen.get(p, 0); seen[p] = k + 1
    extra = ' (FK composta)' if len(c) > 1 else ''
    o.append(f'"{p}" -> "{t}":"l_{c[0]}":w [label=<<I>{esc(name)}{extra}</I>>, '
             f'taillabel="{cp}", headlabel="{cf}", labelangle={ANG[(t, c[0])]}];')
o.append('}')
open(OUT + '.dot', 'w', encoding='utf8').write('\n'.join(o))
subprocess.run(['dot', '-Tpng', '-Gdpi=110', OUT + '.dot', '-o', OUT + '.png'], check=True)
subprocess.run(['dot', '-Tsvg', OUT + '.dot', '-o', OUT + '.svg'], check=True)
print('ok:', len(tables), 'tabelas,', len(fks), 'FKs')
