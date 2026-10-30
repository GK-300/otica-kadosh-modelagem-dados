#!/usr/bin/env python3
"""Gera a massa de dados fictícia da Ótica Kadosh (seção 4 do docs/script.sql).

Uso:  python3 gerar_massa.py saida.sql
Escreve os comandos INSERT de todas as tabelas, na ordem das chaves estrangeiras. O script.sql
já traz esse resultado; o programa serve para reproduzir ou ajustar a massa.

Determinístico (semente fixa 20261030): rodar de novo gera exatamente os mesmos dados.
Volumes de setembro e outubro de 2026 conforme a seção 1.1 do README. Todos os dados são inventados.
"""
import random, sys, math
import datetime as dt
from datetime import timedelta, datetime, date, time
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict

R = random.Random(20261030)
TODAY = date(2026, 10, 30)
START = date(2026, 9, 1)
OUT = sys.argv[1] if len(sys.argv) > 1 else "02_massa.sql"


# ---------------------------------------------------------------- utilidades
def money(x):
    return Decimal(str(round(float(x), 2))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def q(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, datetime):
        return "'%s'" % v.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(v, date):
        return "'%s'" % v.isoformat()
    if isinstance(v, time):
        return "'%s'" % v.strftime("%H:%M:%S")
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def wchoice(items, weights):
    return R.choices(items, weights=weights, k=1)[0]


def digits(n):
    return "".join(str(R.randint(0, 9)) for _ in range(n))


def cpf():
    while True:
        n = [R.randint(0, 9) for _ in range(9)]
        if len(set(n)) == 1:
            continue
        for _ in range(2):
            s = sum(v * w for v, w in zip(n, range(len(n) + 1, 1, -1)))
            n.append((s * 10 % 11) % 10)
        return "".join(map(str, n))


def cnpj():
    n = [R.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    for _ in range(2):
        w = list(range(len(n) - 7 + 1, 1, -1)) + list(range(9, 1, -1))
        w = w[: len(n)]
        s = sum(v * x for v, x in zip(n, w))
        d = s % 11
        n.append(0 if d < 2 else 11 - d)
    return "".join(map(str, n))


def slug(s):
    t = s.lower()
    for a, b in zip("áàâãäéèêëíìîïóòôõöúùûüç", "aaaaaeeeeiiiiooooouuuuc"):
        t = t.replace(a, b)
    return "".join(c for c in t if c.isalnum() or c == " ").replace(" ", ".")


OUT_ROWS = {}  # tabela -> (colunas, linhas)


def add_table(name, cols, rows):
    OUT_ROWS[name] = (cols, rows)


# ---------------------------------------------------------------- 1. funcionários e fornecedores
FUNC = [
    (1, "Helena Prado Ribeiro", "GERENTE", "11988100001", True),
    (2, "Diego Martins Oliveira", "CONSULTOR_OPTICO", "11988100002", True),
    (3, "Camila Fernandes Lopes", "OPTOMETRISTA", "11988100003", True),
    (4, "Rafael Nogueira Silva", "CONSULTOR_OPTICO", "11988100004", False),  # ex-funcionário, inativado
]
add_table("FUNCIONARIO", ["ID_FUNCIONARIO", "NM_FUNCIONARIO", "TP_FUNCAO", "NR_TELEFONE", "IN_ATIVO"], FUNC)
EX_FUNC_ATE = date(2026, 9, 12)  # data em que o ex-consultor deixou a ótica

FORN_NOMES = [
    ("Armações Vitória Distribuidora Ltda", "Rua do Comércio, 410, Bom Retiro, São Paulo/SP", "vendas@armacoesvitoria.example.com"),
    ("Solaris Moda Óptica Ltda", "Av. Santos Dumont, 1200, Santana, São Paulo/SP", "pedidos@solarisoptica.example.com"),
    ("Nórdica Atacado de Óculos Ltda", "Rua Florêncio de Abreu, 88, Centro, São Paulo/SP", "atacado@nordicaoculos.example.com"),
    ("Brisa Armações e Acessórios Ltda", "Rua José Paulino, 305, Bom Retiro, São Paulo/SP", "contato@brisaarmacoes.example.com"),
    ("Cristal Lab Lentes Oftálmicas Ltda", "Av. Industrial, 2500, Santo André/SP", "comercial@cristallab.example.com"),
    ("Visiomax Laboratório Óptico Ltda", "Rua Bela Cintra, 770, Consolação, São Paulo/SP", "pedidos@visiomaxlab.example.com"),
]
FORN = []
for i, (n, e, c) in enumerate(FORN_NOMES, 1):
    FORN.append((i, n, cnpj(), e, c))
add_table("FORNECEDOR", ["ID_FORNECEDOR", "NM_FORNECEDOR", "NR_CNPJ", "DS_ENDERECO", "DS_CONTATO"], FORN)
LEAD = {1: 4, 2: 7, 3: 5, 4: 9, 5: 12, 6: 10}  # prazo médio de entrega por fornecedor (dias)

# ---------------------------------------------------------------- 2. produtos
MARCAS_ARM = ["Solaris", "Nórdica", "Vértice", "Lumiar", "Kairo", "Brisa", "Atlas", "Maré", "Aurora", "Zênite"]
MODELOS = ["Aviador", "Redondo", "Retangular", "Gatinho", "Quadrado", "Oval", "Wayfarer", "Hexagonal"]
CORES = ["Preto", "Tartaruga", "Dourado", "Prata", "Azul", "Vinho", "Cinza", "Rosa", "Grafite"]
TP_ARM = ["Aro fechado", "Fio de nylon", "Parafusada", "Solar"]
MAT_ARM = ["Acetato", "Metal", "Titânio", "TR90", "Alumínio"]
N_ARM, N_LEN = 230, 120
produtos, armacoes, lentes = [], [], []
base_price, weight, supplier_of, is_grau, ptype = {}, {}, {}, {}, {}
for i in range(1, N_ARM + 1):
    ref = "ARM-%d %s %s" % (1000 + i, R.choice(MODELOS), R.choice(CORES))
    produtos.append((i, "ARMACAO", ref, R.choice(MARCAS_ARM)))
    tp = wchoice(TP_ARM, [40, 20, 20, 20])
    armacoes.append((i, "ARMACAO", tp, R.choice(MAT_ARM)))
    base_price[i] = min(950, max(130, round(R.lognormvariate(5.7, 0.45) / 10) * 10))
    weight[i] = R.lognormvariate(0, 0.9)
    supplier_of[i] = R.choice([1, 2, 3, 4])
    ptype[i] = "ARMACAO"
IDX = [(1.50, 1.0, 120, 300), (1.56, 2.0, 180, 400), (1.59, 2.0, 250, 500), (1.61, 2.0, 350, 700), (1.67, 1.5, 500, 1000), (1.74, 0.6, 900, 1600)]
TRAT = ["Antirreflexo", "Blue Light", "Fotossensível", "Antirrisco", "Polarizada", "Sem tratamento"]
MARCAS_LEN = ["Opticron", "Visiomax", "Clarivue", "Lentara"]
for k in range(1, N_LEN + 1):
    pid = N_ARM + k
    idx = wchoice(IDX, [x[1] for x in IDX])
    trat = wchoice(TRAT, [30, 28, 12, 12, 6, 12])
    grau = not (trat == "Polarizada" and R.random() < 0.7) and R.random() < 0.9
    ref = "LNT-%d %.2f %s" % (2000 + k, idx[0], trat)
    produtos.append((pid, "LENTE", ref, R.choice(MARCAS_LEN)))
    lentes.append((pid, "LENTE", Decimal(str(idx[0])), None if trat == "Sem tratamento" else trat, grau))
    base_price[pid] = R.randint(idx[2] // 10, idx[3] // 10) * 10
    weight[pid] = R.lognormvariate(0, 0.9)
    supplier_of[pid] = R.choice([5, 6])
    is_grau[pid] = grau
    ptype[pid] = "LENTE"
# produto sem especialização (caso de teste da auditoria A06 / RN-14)
produtos.append((N_ARM + N_LEN + 1, "ARMACAO", "ARM-9999 Cadastro incompleto", None))
add_table("PRODUTO", ["ID_PRODUTO", "CD_TIPO", "DS_REFERENCIA", "NM_MARCA"], produtos)
add_table("ARMACAO", ["ID_PRODUTO", "CD_TIPO", "TP_ARMACAO", "DS_MATERIAL"], armacoes)
add_table("LENTE", ["ID_PRODUTO", "CD_TIPO", "VL_INDICE", "DS_TRATAMENTO", "IN_POSSUI_GRAU"], lentes)
ARM_IDS = list(range(1, N_ARM + 1))
LEN_IDS = [N_ARM + k for k in range(1, N_LEN + 1)]
LEN_GRAU = [p for p in LEN_IDS if is_grau[p]]
LEN_SEMGRAU = [p for p in LEN_IDS if not is_grau[p]]
ARM_SOLAR = [a[0] for a in armacoes if a[2] == "Solar"]
ARM_OPT = [a[0] for a in armacoes if a[2] != "Solar"]


def pick(ids):
    return R.choices(ids, weights=[weight[i] for i in ids], k=1)[0]


# ---------------------------------------------------------------- 3. clientes
FEM = "Ana Maria Juliana Fernanda Patrícia Aline Camila Bruna Letícia Larissa Carla Renata Débora Tatiane Priscila Vanessa Sandra Luciana Elaine Rosana Gabriela Beatriz Amanda Natália Simone Cristina Eliane Mônica Viviane Daniela".split()
MAS = "João José Carlos Paulo Lucas Marcos Rafael Felipe Bruno Anderson Rodrigo Eduardo Ricardo Fábio Gustavo Leandro Diego Thiago Vinícius Daniel Márcio Sérgio Alexandre Renan Wesley Cléber Edson Jonas Heitor Otávio".split()
SOB = "Silva Santos Oliveira Souza Pereira Costa Rodrigues Almeida Nascimento Lima Araújo Fernandes Carvalho Gomes Martins Rocha Ribeiro Alves Monteiro Mendes Barros Freitas Barbosa Pinto Moura Cavalcanti Dias Castro Campos Cardoso Teixeira Correia Ramos Moreira Nunes Vieira Machado Lopes Marques Batista".split()
RUAS = ["Rua das Acácias", "Rua dos Ipês", "Av. Marechal Rondon", "Rua Piracema", "Rua Nova Esperança", "Rua São Benedito", "Av. Ragueb Chohfi", "Rua Tuiuti", "Rua Boa Vista", "Rua das Palmeiras", "Rua Jacuí", "Travessa do Sol", "Rua Santa Clara", "Rua Dom Pedro II", "Rua Itapura"]
BAIRROS = ["Jardim Romano", "Itaim Paulista", "Vila Curuçá", "Jardim Helena", "São Miguel Paulista", "Jardim Pantanal", "Vila Nova Curuçá", "Jardim Robru", "Vila Jacuí", "Jardim Keralux"]
BAIRRO_W = [22, 18, 12, 10, 12, 6, 6, 5, 5, 4]
N_CLI = 900
N_CLI_ATENDIDOS = 820  # os demais (821..900) estão cadastrados, mas sem atendimento no período
clientes, used_cpf = [], set()
for cid in range(1, N_CLI + 1):
    fem = R.random() < 0.58
    nome = "%s %s %s" % (R.choice(FEM if fem else MAS), R.choice(SOB), R.choice(SOB))
    nasc = date(1940, 1, 1) + timedelta(days=R.randint(0, (date(2012, 12, 31) - date(1940, 1, 1)).days))
    c = None
    if R.random() < 0.86:
        c = cpf()
        while c in used_cpf:
            c = cpf()
        used_cpf.add(c)
    cel = "119" + digits(8) if R.random() < 0.88 else None
    fixo = "11" + R.choice("23") + digits(7) if R.random() < 0.22 else None
    email = "%s%d@example.com" % (slug(nome), R.randint(1, 99)) if R.random() < 0.45 else None
    if not (cel or fixo or email):
        cel = "119" + digits(8)  # RF-01: ao menos um meio de contato
    if R.random() < 0.9:
        rua = R.choice(RUAS)
        num = str(R.randint(1, 1800))
        bairro = wchoice(BAIRROS, BAIRRO_W)
        cidade = wchoice(["São Paulo", "Ferraz de Vasconcelos", "Poá"], [92, 4, 4])
        cep = "08" + digits(6)
    else:
        rua = num = bairro = cidade = cep = None
    clientes.append((cid, nome, nasc, c, email, fixo, cel, rua, num, bairro, cidade, cep))
add_table("CLIENTE", ["ID_CLIENTE", "NM_CLIENTE", "DT_NASCIMENTO", "NR_CPF", "DS_EMAIL", "NR_TELEFONE_FIXO", "NR_TELEFONE_CELULAR", "DS_LOGRADOURO", "NR_ENDERECO", "NM_BAIRRO", "NM_CIDADE", "NR_CEP"], clientes)

# ---------------------------------------------------------------- 4. atendimentos (planejamento)
open_days = [START + timedelta(days=i) for i in range((TODAY - START).days + 1) if (START + timedelta(days=i)).weekday() != 6]
weeks = ((TODAY - START).days + 1) / 7.0
N_ATEND = round(weeks * 100)  # ≈ 100 atendimentos por semana
N_VENDA = round(N_ATEND * 0.83)  # ≈ 80 vendas efetivas por semana, descontados os cancelamentos (≈ 4%)
N_AVAL, N_MANUT = round(N_ATEND * 0.05), round(N_ATEND * 0.035)
N_SEMVENDA = N_ATEND - N_VENDA - N_AVAL - N_MANUT
kinds = ["VENDA"] * N_VENDA + ["AVALIACAO"] * N_AVAL + ["MANUTENCAO"] * N_MANUT + ["SEM_VENDA"] * N_SEMVENDA
R.shuffle(kinds)


def rand_dt(d):
    if d.weekday() == 5:
        h = R.randint(9, 12)
    else:
        h = R.randint(9, 17)
    return datetime(d.year, d.month, d.day, h, R.randint(0, 59), R.randint(0, 59))


day_w = [1.3 if d.weekday() in (4, 5) else 1.0 for d in open_days]
cli_pool = list(range(1, N_CLI_ATENDIDOS + 1))
R.shuffle(cli_pool)
seen_cli = []


def next_client():
    if seen_cli and R.random() < 0.15:
        return R.choice(seen_cli)
    c = cli_pool.pop() if cli_pool else R.choice(seen_cli)
    seen_cli.append(c)
    return c


ats = []
for kind in kinds:
    d = R.choices(open_days, weights=day_w, k=1)[0]
    ats.append({"kind": kind, "dh": rand_dt(d), "hist": False})
# histórico reduzido (amostra de vendas antigas, só para garantias e períodos diferentes)
for _ in range(18):
    d = date(2026, 5, 1) + timedelta(days=R.randint(0, 19))
    ats.append({"kind": "VENDA", "dh": rand_dt(d), "hist": True})
for _ in range(10):
    d = date(2025, 11, 3) + timedelta(days=R.randint(0, 17))
    ats.append({"kind": "VENDA", "dh": rand_dt(d), "hist": True})
ats.sort(key=lambda a: a["dh"])
for i, a in enumerate(ats, 1):
    a["id"] = i
    a["cli"] = R.randint(1, N_CLI_ATENDIDOS) if a["hist"] else next_client()
    k = a["kind"]
    if k == "AVALIACAO":
        a["func"] = 3
        a["tp"] = "AVALIACAO"
    elif k == "MANUTENCAO":
        a["func"] = wchoice([2, 1], [60, 40])
        a["tp"] = "MANUTENCAO"
    else:
        a["tp"] = "COMERCIAL"
        if a["dh"].date() <= EX_FUNC_ATE and not a["hist"]:
            a["func"] = wchoice([2, 4, 1], [40, 40, 20])
        else:
            a["func"] = wchoice([2, 1], [75, 25])
    a["meio"] = wchoice(["Presencial", "WhatsApp", "Instagram", "Indicação", "Telefone", None], [50, 20, 12, 10, 4, 4])
    a["serv"] = R.choice(["Ajuste de plaquetas", "Troca de parafuso", "Alinhamento da armação", "Limpeza e ajuste das hastes"]) if k == "MANUTENCAO" else None

# ---------------------------------------------------------------- 5. orçamento, venda, linhas, receita
orcs, vendas, linhas, receitas, medidas = [], [], [], [], []
OBS_VENDA = [None] * 8 + ["Cliente pediu aviso por WhatsApp quando ficar pronto", "Retirada após as 17h", "Armação própria do cliente na montagem", "Pedido de pronta entrega"]
OBS_LENTE = [None, None, None, "Antirreflexo", "Blue Light", "Resistente a arranhões", "Fotossensível"]


def medidas_de(rid):
    pat = wchoice(["2L", "4", "2P", "1"], [55, 30, 8, 7])
    combos = {"2L": [("OD", "LONGE"), ("OE", "LONGE")], "4": [("OD", "LONGE"), ("OE", "LONGE"), ("OD", "PERTO"), ("OE", "PERTO")], "2P": [("OD", "PERTO"), ("OE", "PERTO")], "1": [("OD", "LONGE")]}[pat]
    base = {}
    for olho in ("OD", "OE"):
        esf = R.randint(-24, 12) * 0.25
        cil = 0.0 if R.random() < 0.45 else -R.randint(1, 10) * 0.25
        base[olho] = (esf, cil, R.randint(0, 18) * 10 if cil else None, R.choice(["20/20", "20/25", "20/30", "20/40", "20/50", "20/70"]), R.randint(58, 70) / 2.0, R.randint(34, 48) / 2.0)
    add = R.choice([1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5])
    out = []
    for olho, dist in combos:
        esf, cil, eixo, av, dnp, alt = base[olho]
        if dist == "PERTO":
            esf, dnp = esf + add, dnp - 2.0
        out.append((rid, olho, dist, money(esf), money(cil) if cil else None, eixo, av, Decimal(str(dnp)), Decimal(str(alt))))
    return out


venda_by_at = {}
for a in ats:
    d = a["dh"]
    a["orcs"] = []
    if a["kind"] in ("VENDA", "SEM_VENDA"):
        if a["kind"] == "VENDA":
            if R.random() < 0.07:  # orçamento recusado antes do aprovado
                e = d + timedelta(minutes=R.randint(15, 25))
                a["orcs"].append({"em": e, "val": e + timedelta(hours=24), "apr": None, "st": "RECUSADO", "obs": "Cliente achou o valor alto; pediu outra opção"})
            e = d + timedelta(minutes=R.randint(30, 60))
            same = R.random() < 0.85 or (d + timedelta(days=1)).date() > TODAY
            apr = e + timedelta(minutes=R.randint(10, 50)) if same else e + timedelta(hours=R.randint(3, 22))
            if apr.date() > TODAY:
                apr = e + timedelta(minutes=R.randint(10, 30))
            a["orcs"].append({"em": e, "val": e + timedelta(hours=24), "apr": apr, "st": "APROVADO", "obs": None})
            a["apr"] = apr
        else:
            if R.random() < 0.82:
                e = d + timedelta(minutes=R.randint(30, 60))
                recent = (TODAY - e.date()).days <= 1
                st = wchoice(["RECUSADO", "EMITIDO", "CANCELADO", "EM_ELABORACAO"], [50, 30, 10, 10 if recent else 0])
                a["orcs"].append({"em": e, "val": e + timedelta(hours=24), "apr": None, "st": st, "obs": "Cliente vai pensar" if st == "EMITIDO" else None})

# --- vendas
sales = [a for a in ats if a["kind"] == "VENDA"]
cur_sales = [a for a in sales if not a["hist"]]
n_cancel = round(len(cur_sales) * 0.04)
cancel_set = set(a["id"] for a in R.sample([a for a in cur_sales if (TODAY - a["dh"].date()).days >= 2], n_cancel))


def build_lines(a):
    pat = wchoice(["COMPLETO", "DUPLO", "SO_ARM", "SO_LENTE"], [71, 4, 14, 11])
    solar = R.random() < 0.15
    out = []

    def conjunto():
        if solar:
            return [(pick(ARM_SOLAR or ARM_IDS), 1), (pick(LEN_SEMGRAU), 1)]
        return [(pick(ARM_OPT), 1), (pick(LEN_GRAU), 1)]

    if pat == "COMPLETO":
        out = conjunto()
    elif pat == "DUPLO":
        out = conjunto() + [(pick(ARM_OPT), 1), (pick(LEN_GRAU), 1)]
    elif pat == "SO_ARM":
        out = [(pick(ARM_SOLAR if R.random() < 0.5 and ARM_SOLAR else ARM_OPT), 1)]
    else:
        out = [(pick(LEN_GRAU), 1)]
    return out


for a in sales:
    ls = build_lines(a)
    a["lines"] = [(p, qt, money(base_price[p] * R.uniform(0.92, 1.0) // 5 * 5)) for p, qt in ls]
    a["total"] = sum(Decimal(qt) * pr for p, qt, pr in a["lines"])
    a["needs_rx"] = any(is_grau.get(p) for p, _, _ in a["lines"])
    a["cancel"] = a["id"] in cancel_set
    a["encomenda"] = a["needs_rx"]

# --- casos plantados (auditoria): escolhidos entre vendas atuais antigas, retiradas e não canceladas
elig = [a for a in cur_sales if not a["cancel"] and (TODAY - a["dh"].date()).days >= 25]
R.shuffle(elig)
elig_enc = [a for a in elig if a["encomenda"]]
elig_enc_ok = list(elig_enc)
PLANT = {}


def take(lst, n, tag):
    got = []
    for a in lst:
        if a["id"] in PLANT:
            continue
        PLANT[a["id"]] = tag
        got.append(a)
        if len(got) == n:
            break
    return got


p_a05 = take(elig_enc_ok, 2, "A05")  # lente de grau sem receita
p_a04 = take(elig_enc_ok, 2, "A04")  # encomenda liberada com sinal abaixo de 30%
p_a11 = take(elig_enc_ok, 2, "A11")  # venda sem orçamento aprovado
p_a12 = take(elig_enc_ok, 2, "A12")  # receita trazida com mais de um ano
p_a08 = take(elig_enc_ok, 2, "A08")  # receita sem medidas
p_a03 = take(elig, 2, "A03")  # pagamentos acima do total
p_a09 = None  # venda sem linhas (criada à parte)

# --- orçamento aprovado removido nos casos A11 (o atendimento fica só com orçamento recusado/emitido)
for a in p_a11:
    a["orcs"] = [{"em": a["dh"] + timedelta(minutes=40), "val": a["dh"] + timedelta(minutes=40) + timedelta(hours=24), "apr": None, "st": "EMITIDO", "obs": "Orçamento sem registro de aprovação"}]
    a["apr"] = a["dh"] + timedelta(minutes=70)  # a venda foi lançada sem aprovação registrada
# um terceiro caso: aprovação registrada depois da validade
late = take([a for a in elig_enc_ok], 1, "A11")
for a in late:
    e = a["dh"] + timedelta(minutes=40)
    a["orcs"] = [{"em": e, "val": e + timedelta(hours=24), "apr": e + timedelta(hours=27), "st": "APROVADO", "obs": None}]
    a["apr"] = e + timedelta(hours=27)

for a in sales:
    if a["kind"] == "VENDA":
        a["dh_compra"] = a.get("apr") or a["dh"] + timedelta(minutes=90)
        if a["dh_compra"].date() > TODAY:
            a["dh_compra"] = datetime(TODAY.year, TODAY.month, TODAY.day, 17, 30)

# --- cronograma de cada venda
for a in sales:
    d = a["dh_compra"].date()
    a["dt"] = d
    a["lib"] = a["prev"] = a["mont"] = a["ret"] = a["envio"] = a["hr"] = a["canhoto"] = None
    a["canc_dh"] = None
    a["status"] = None
    if a["cancel"]:
        a["status"] = "CANCELADO"
        a["canc_dh"] = a["dh_compra"] + timedelta(hours=R.randint(2, 20))
        continue
    if not a["encomenda"]:  # pronta entrega
        a["prev"] = d
        a["mont"] = d
        a["ret"] = d
        a["canhoto"] = True
        a["status"] = "RETIRADO"
        continue
    L = R.randint(5, 10)
    a["L"] = L
    a["prev"] = d + timedelta(days=L)
    a["pay_pattern"] = None

# --- pagamentos e parcelas
pays, parcelas = [], []  # dicts (ids depois)
FORMA_SINAL = (["PIX", "CREDITO", "DEBITO", "DINHEIRO"], [30, 35, 20, 15])
FORMA_QUIT = (["CREDITO", "PIX", "DEBITO"], [55, 30, 15])


def add_pay(a, val, dtp, forma, fin, parcela=None):
    p = {"venda": a, "val": money(val), "dt": dtp, "forma": forma, "fin": fin, "parcela": parcela}
    pays.append(p)
    return p


for a in sales:
    if a["cancel"]:
        continue
    d = a["dt"]
    T = a["total"]
    if a["hist"] or not a["encomenda"]:
        pat = "INTEGRAL"
    else:
        age = (TODAY - d).days
        if age <= 1 and R.random() < 0.3:
            pat = "SEM_PAGAMENTO"
        else:
            pat = wchoice(["INTEGRAL", "SINAL_PARCIAL", "PARCELADO"], [45, 10, 45])
    if PLANT.get(a["id"]) == "A04":
        pat = "PARCELADO"
    if pat != "INTEGRAL" and T < 160:
        pat = "INTEGRAL"
    a["pay_pattern"] = pat
    if pat == "SEM_PAGAMENTO":
        a["status"] = "ABERTO"
        continue
    if pat == "INTEGRAL":
        add_pay(a, T, d, wchoice(*(["PIX", "CREDITO", "DEBITO", "DINHEIRO"], [35, 30, 20, 15])), "INTEGRAL")
        if a["encomenda"]:
            a["lib"] = d
    else:
        pct = 0.15 if PLANT.get(a["id"]) == "A04" else R.uniform(0.30, 0.50)
        sinal = money(math.ceil(float(T) * pct))
        if sinal <= 0:
            sinal = money(1)
        add_pay(a, sinal, d, wchoice(*FORMA_SINAL), "SINAL")
        a["lib"] = d
        bal = T - sinal
        if pat == "SINAL_PARCIAL":
            a["_saldo_parcial"] = bal  # pago na retirada (se já ocorreu)
        else:
            n = wchoice([2, 3, 4, 5, 6], [15, 25, 30, 15, 15])
            while n > 1 and bal / n < 50:
                n -= 1
            if n < 2 or bal < 100:
                a["_saldo_parcial"] = bal
                a["pay_pattern"] = "SINAL_PARCIAL"
            else:
                base = (bal / n).quantize(Decimal("0.01"), rounding="ROUND_DOWN") if False else money(int(float(bal) / n * 100) / 100.0)
                vals = [base] * (n - 1) + [bal - base * (n - 1)]
                for k, v in enumerate(vals, 1):
                    pa = {"nr": k, "val": v, "venc": d + timedelta(days=30 * k), "venda": a}
                    parcelas.append(pa)
                    if pa["venc"] <= TODAY and R.random() < 0.82:
                        pdt = min(TODAY, pa["venc"] + timedelta(days=R.randint(0, 6)))
                        pg = add_pay(a, v, pdt, wchoice(*FORMA_QUIT), "QUITACAO_PARCELA", pa)
                        pa["pag"] = pg

# --- cronograma das encomendas (depende da liberação)
for a in sales:
    if a["cancel"] or not a["encomenda"] or a["status"] == "ABERTO":
        continue
    d, L = a["dt"], a["L"]
    lib = a["lib"]
    a["envio"] = datetime(lib.year, lib.month, lib.day, 16, 0) + timedelta(days=R.randint(0, 1))
    if a["envio"].date() > TODAY:
        a["envio"] = None
    mont = a["prev"] - timedelta(days=R.randint(0, 2))
    ret = mont + timedelta(days=wchoice([0, 1, 2, 3, 5, 7], [25, 20, 15, 15, 15, 10]))
    if a["hist"]:
        pass
    a["mont"] = mont if mont <= TODAY else None
    a["ret"] = ret if (a["mont"] and ret <= TODAY) else None
    a["hr"] = time(R.randint(10, 17), R.choice([0, 30]))
    if a["ret"]:
        a["canhoto"] = True
        a["status"] = "RETIRADO"
    elif a["mont"]:
        a["status"] = "PRONTO"
    elif a["envio"] and (d + timedelta(days=L // 2)) <= TODAY:
        a["status"] = "EM_MONTAGEM"
    else:
        a["status"] = "AGUARDANDO_PRODUTO"
for a in sales:
    if a["status"] == "ABERTO":
        a["lib"] = None

# saldo (SINAL_PARCIAL) pago na retirada
for a in sales:
    if a.get("_saldo_parcial") is not None and a["ret"]:
        add_pay(a, a["_saldo_parcial"], a["ret"], wchoice(["PIX", "DEBITO", "DINHEIRO", "CREDITO"], [35, 25, 20, 20]), "PARCIAL")

# --- casos plantados: pagamento extra (A03)
for a in p_a03:
    add_pay(a, a["total"] * Decimal("0.4"), a["dt"] + timedelta(days=1), "PIX", "PARCIAL")

# --- venda sem linhas (A09): lançada hoje, sem itens e sem pagamento
base_at = [a for a in ats if a["kind"] == "SEM_VENDA" and a["dh"].date() >= TODAY - timedelta(days=1) and a["orcs"]]
if base_at:
    x = base_at[0]
    x["kind"] = "VENDA"
    x["orcs"] = [{"em": x["dh"] + timedelta(minutes=30), "val": x["dh"] + timedelta(minutes=30) + timedelta(hours=24), "apr": x["dh"] + timedelta(minutes=50), "st": "APROVADO", "obs": None}]
    x.update(lines=[], total=Decimal("0.00"), needs_rx=False, cancel=False, encomenda=False, hist=False, dh_compra=x["dh"] + timedelta(minutes=50), status="ABERTO", lib=None, prev=None, mont=None, ret=None, envio=None, hr=None, canhoto=None, canc_dh=None, pay_pattern="SEM_PAGAMENTO")
    x["dt"] = x["dh_compra"].date()
    sales.append(x)
    sales.sort(key=lambda s: s["dh_compra"])

# ---------------------------------------------------------------- 6. receitas e medidas
LAUDO_OBS = [None, None, None, "Uso contínuo", "Primeira receita", "Cliente relata dor de cabeça ao ler"]
rx_rows = []
for a in ats:
    need = False
    tag = PLANT.get(a["id"])
    if a["kind"] == "VENDA" and a.get("needs_rx") and not a.get("cancel", False) or (a["kind"] == "VENDA" and a.get("needs_rx")):
        need = True
    if a["kind"] == "AVALIACAO":
        need = True
    if a["kind"] == "SEM_VENDA" and R.random() < 0.25:
        need = True
    if tag == "A05":
        need = False  # lente de grau sem receita
    if not need:
        continue
    d = a["dh"].date()
    if a["kind"] == "AVALIACAO":
        origem = "LAUDO_OTICA"
    elif tag == "A12":
        origem = "TRAZIDA"
    else:
        origem = wchoice(["TRAZIDA", "LAUDO_OTICA"], [55, 45])
    if origem == "TRAZIDA":
        dtr = d - timedelta(days=R.randint(10, 300))
        if tag == "A12":
            dtr = d - timedelta(days=R.randint(380, 700))
    else:
        dtr = d
    rx_rows.append({"at": a, "dt": dtr, "origem": origem, "obs": R.choice(LAUDO_OBS), "sem_medida": tag == "A08"})
rx_rows.sort(key=lambda r: r["at"]["id"])
receita_tbl, medida_tbl = [], []
for i, r in enumerate(rx_rows, 1):
    receita_tbl.append((i, r["dt"], r["origem"], r["obs"], r["at"]["id"]))
    if not r["sem_medida"]:
        medida_tbl += medidas_de(i)
add_table("RECEITA", ["ID_RECEITA", "DT_RECEITA", "TP_ORIGEM", "DS_OBSERVACAO", "ID_ATENDIMENTO"], receita_tbl)
add_table("RECEITA_MEDIDA", ["ID_RECEITA", "CD_OLHO", "CD_DISTANCIA", "VL_ESFERICO", "VL_CILINDRICO", "VL_EIXO", "VL_ACUIDADE_VISUAL", "VL_DNP", "VL_ALTURA"], medida_tbl)

# ---------------------------------------------------------------- 7. tabelas de atendimento, orçamento, venda, contém
add_table("ATENDIMENTO", ["ID_ATENDIMENTO", "DH_ATENDIMENTO", "TP_MEIO_CONTATO", "TP_ATENDIMENTO", "DS_SERVICO", "ID_CLIENTE", "ID_FUNCIONARIO"],
          [(a["id"], a["dh"], a["meio"], a["tp"], a["serv"], a["cli"], a["func"]) for a in ats])
orc_list = []
for a in ats:
    for o in a["orcs"]:
        orc_list.append((o["em"], a["id"], o))
orc_list.sort(key=lambda t: (t[0], t[1]))
add_table("ORCAMENTO", ["ID_ORCAMENTO", "DH_EMISSAO", "DH_VALIDADE", "DH_APROVACAO", "CD_STATUS", "DS_OBSERVACAO", "ID_ATENDIMENTO"],
          [(i, o["em"], o["val"], o["apr"], o["st"], o["obs"], aid) for i, (_, aid, o) in enumerate(orc_list, 1)])

sales.sort(key=lambda s: (s["dh_compra"], s["id"]))
for i, s in enumerate(sales, 1):
    s["vid"] = i
vrows, crows = [], []
for s in sales:
    obs = "Cancelamento solicitado pelo cliente dentro de 24 horas" if s["cancel"] else R.choice(OBS_VENDA)
    vrows.append((s["vid"], s["dh_compra"], s["status"], obs, s["mont"], s["ret"], s["hr"], s["prev"], s["lib"], s["canhoto"], s["envio"], s["canc_dh"], s["id"]))
    for n, (p, qt, pr) in enumerate(s["lines"], 1):
        o = R.choice(OBS_LENTE) if ptype[p] == "LENTE" else None
        crows.append((s["vid"], n, qt, pr, o, p))
add_table("VENDA", ["ID_VENDA", "DH_COMPRA", "CD_STATUS", "DS_OBSERVACAO", "DT_MONTAGEM_FINALIZACAO", "DT_RETIRADA", "HR_PREVISTA_RETIRADA", "DT_PREVISTA_CONCLUSAO", "DT_LIBERACAO_ENCOMENDA", "IN_CANHOTO_CONFERIDO", "DH_ENVIO_FORNECEDOR", "DH_SOLICITACAO_CANCELAMENTO", "ID_ATENDIMENTO"], vrows)
add_table("CONTEM", ["ID_VENDA", "NR_LINHA", "QT_PRODUTO", "VL_PRECO_UNITARIO", "DS_OBSERVACAO", "ID_PRODUTO"], crows)

# ---------------------------------------------------------------- 8. parcelas, pagamentos, notas
parcelas.sort(key=lambda p: (p["venda"]["vid"], p["nr"]))
for i, p in enumerate(parcelas, 1):
    p["id"] = i
# A10: quitação com valor diferente do valor da parcela
quit_pays = [p for p in pays if p["fin"] == "QUITACAO_PARCELA" and p["dt"] <= TODAY - timedelta(days=10)]
R.shuffle(quit_pays)
for p, delta in zip(quit_pays[:2], (Decimal("15.00"), Decimal("-12.00"))):
    p["val"] = p["val"] + delta
pays.sort(key=lambda p: (p["dt"], p["venda"]["vid"], p["fin"] != "SINAL"))
for i, p in enumerate(pays, 1):
    p["id"] = i
add_table("PARCELA", ["ID_PARCELA", "NR_PARCELA", "VL_PARCELA", "DT_VENCIMENTO"], [(p["id"], p["nr"], p["val"], p["venc"]) for p in parcelas])
add_table("PAGAMENTO", ["ID_PAGAMENTO", "VL_PAGAMENTO", "DT_PAGAMENTO", "TP_FORMA", "TP_FINALIDADE", "ID_VENDA", "ID_PARCELA_QUITADA"],
          [(p["id"], p["val"], p["dt"], p["forma"], p["fin"], p["venda"]["vid"], p["parcela"]["id"] if p["parcela"] else None) for p in pays])
# A01: dois pagamentos sem nota fiscal de saída
sem_nota = set(p["id"] for p in R.sample([p for p in pays if p["fin"] in ("INTEGRAL", "PARCIAL") and START <= p["dt"] <= TODAY - timedelta(days=12)], 2))
nfs = []
nr = 10230
for p in pays:
    if p["id"] in sem_nota:
        continue
    nr += R.randint(1, 3)
    trib = money(float(p["val"]) * 0.0814) if R.random() < 0.92 else None
    nfs.append((len(nfs) + 1, "%06d" % nr, p["dt"], p["val"], trib, p["id"]))
    p["nota"] = len(nfs)
add_table("NOTA_FISCAL_SAIDA", ["ID_NOTA_SAIDA", "NR_NOTA", "DT_EMISSAO", "VL_TOTAL", "VL_TRIBUTOS", "ID_PAGAMENTO"], nfs)

# ---------------------------------------------------------------- 9. trocas e devoluções (≈ 4% das vendas)
N_TROCA = round(len(cur_sales) * 0.043)
cand = [p for p in pays if p.get("nota") and p["fin"] in ("INTEGRAL", "SINAL") and p["venda"]["status"] == "RETIRADO" and not p["venda"]["hist"] and p["venda"]["ret"] and (TODAY - p["venda"]["ret"]).days >= 3 and p["venda"]["lines"]]
R.shuffle(cand)
trocas, seen_v = [], set()
DANOS = ["Armação quebrou na ponte", "Lente com risco profundo", "Parafuso da haste soltando", "Erro de grau percebido pelo cliente", "Mola da haste com defeito", "Lente descolou do tratamento", "Armação desalinhada"]
for p in cand:
    if len(trocas) >= N_TROCA:
        break
    v = p["venda"]
    if v["vid"] in seen_v:
        continue
    seen_v.add(v["vid"])
    ret = v["ret"]
    ocor = ret + timedelta(days=R.randint(2, 40))
    if ocor > TODAY:
        ocor = TODAY - timedelta(days=R.randint(0, 3))
    if ocor <= ret:
        continue
    age = (TODAY - ocor).days
    if age <= 3:
        st = wchoice(["ABERTA", "EM_AVALIACAO"], [60, 40])
    elif age <= 10:
        st = wchoice(["EM_AVALIACAO", "APROVADA", "RECUSADA", "CONCLUIDA"], [30, 25, 20, 25])
    else:
        st = wchoice(["CONCLUIDA", "APROVADA", "RECUSADA", "EM_AVALIACAO"], [55, 15, 25, 5])
    tp = wchoice(["TROCA", "DEVOLUCAO"], [70, 30])
    linha = R.choice(v["lines"])
    qt = 1
    aval = ocor + timedelta(days=R.randint(1, 5)) if st in ("APROVADA", "RECUSADA", "CONCLUIDA") else None
    if aval and aval > TODAY:
        aval = TODAY
    parecer = None
    cobr = abat = reemb = dreemb = None
    if aval:
        parecer = "Dano de fabricação confirmado; produto aceito" if st != "RECUSADA" else "Dano por mau uso; ocorrência recusada"
        if st != "RECUSADA":
            cobr = money(0) if R.random() < 0.7 else money(R.choice([40, 60, 80, 120]))
            abat = money(0) if R.random() < 0.8 else money(R.choice([30, 50]))
            if tp == "DEVOLUCAO" and st == "CONCLUIDA":
                reemb = money(float(linha[2]) * qt)
                dreemb = min(TODAY, aval + timedelta(days=R.randint(0, 3)))
    trocas.append({"nf": p["nota"], "tp": tp, "dt": ocor, "st": st, "qt": qt, "dano": R.choice(DANOS), "parecer": parecer, "aval": aval, "cobr": cobr, "abat": abat, "reemb": reemb, "dreemb": dreemb, "prod": linha[0], "reuse": R.random() < (0.35 if tp == "DEVOLUCAO" else 0.2)})
trocas.sort(key=lambda t: (t["dt"], t["nf"]))
add_table("TROCA_DEVOLUCAO", ["ID_OCORRENCIA", "TP_OCORRENCIA", "DT_OCORRIDO", "CD_STATUS", "QT_AFETADA", "DS_DANO", "DS_PARECER_AVALIACAO", "DT_AVALIACAO", "VL_COBRADO", "VL_ABATIMENTO", "VL_REEMBOLSADO", "DT_REEMBOLSO", "ID_NOTA_SAIDA"],
          [(i, t["tp"], t["dt"], t["st"], t["qt"], t["dano"], t["parecer"], t["aval"], t["cobr"], t["abat"], t["reemb"], t["dreemb"], t["nf"]) for i, t in enumerate(trocas, 1)])

# ---------------------------------------------------------------- 10. compras, notas de entrada e estoque
compras = []  # dict


def new_compra(forn, ped, special=None):
    lead = max(2, LEAD[forn] + R.randint(-2, 3))
    cheg = ped + timedelta(days=lead)
    st = "RECEBIDA" if cheg <= TODAY else "SOLICITADA"
    c = {"forn": forn, "ped": ped, "cheg": cheg if st == "RECEBIDA" else None, "st": st, "venda": None}
    compras.append(c)
    return c


for f in range(1, 7):  # compras iniciais (reposição de agosto)
    new_compra(f, date(2026, 8, R.randint(3, 10)))
for f in range(1, 7):  # compras do período (4 por fornecedor ≈ 12 por mês)
    for base in (date(2026, 9, 3), date(2026, 9, 17), date(2026, 10, 1), date(2026, 10, 15)):
        ped = base + timedelta(days=R.randint(-2, 3))
        if f == 2 and base.month == 10 and base.day == 15:
            ped = date(2026, 10, 24)
        if f == 5 and base.month == 10 and base.day == 15:
            ped = date(2026, 10, 27)
        if f == 6 and base.month == 10 and base.day == 15:
            ped = date(2026, 10, 22)
        new_compra(f, ped)
cancel_c = [c for c in compras if c["forn"] == 3 and c["ped"] >= date(2026, 9, 10)][0]
cancel_c["st"], cancel_c["cheg"] = "CANCELADA", None
compras.sort(key=lambda c: (c["ped"], c["forn"]))
for i, c in enumerate(compras, 1):
    c["id"] = i

# demanda de saída por produto
exits = defaultdict(list)  # produto -> [(data, qt, motivo, venda_ref)]
for s in sales:
    if s["hist"] or s["cancel"] or not s["lines"]:
        continue
    for p, qt, pr in s["lines"]:
        exits[p].append((s["dt"], qt))
for t in trocas:
    if t["tp"] == "TROCA" and t["st"] in ("APROVADA", "CONCLUIDA"):
        t["subst_dt"] = min(TODAY, t["aval"] + timedelta(days=1))
        exits[t["prod"]].append((t["subst_dt"], 1))

LENS_BASE = [0, 0, 1, 1, 1]
estoque = []  # (data, qt, dir, motivo, cond, prod, compra_id)
recebidas = defaultdict(list)
for c in compras:
    if c["st"] == "RECEBIDA":
        recebidas[c["forn"]].append(c)
for f in recebidas:
    recebidas[f].sort(key=lambda c: c["cheg"])
entries_by_compra = defaultdict(list)
for p in range(1, N_ARM + N_LEN + 1):
    arrs = recebidas[supplier_of[p]]
    ex = sorted(exits.get(p, []))
    for k, c in enumerate(arrs):
        lo = c["cheg"]
        hi = arrs[k + 1]["cheg"] if k + 1 < len(arrs) else date(2100, 1, 1)
        need = sum(qt for d, qt in ex if lo <= d < hi)
        extra = 0
        if k == 0:
            extra = R.randint(2, 6) if ptype[p] == "ARMACAO" else R.choice(LENS_BASE)
        qty = need + extra
        if qty > 0:
            estoque.append((c["cheg"], qty, "ENTRADA", "COMPRA", "DISPONIVEL", p, c["id"]))
            entries_by_compra[c["id"]].append((p, qty))
# saídas por venda
for s in sales:
    if s["hist"] or s["cancel"]:
        continue
    for p, qt, pr in s["lines"]:
        estoque.append((s["dt"], qt, "SAIDA", "VENDA", "DISPONIVEL", p, None))
# movimentos de trocas e devoluções
for t in trocas:
    p, st = t["prod"], t["st"]
    if st in ("ABERTA", "EM_AVALIACAO"):
        estoque.append((t["dt"], 1, "ENTRADA", "DEVOLUCAO_AVARIA", "SEGREGADO", p, None))
    elif st in ("APROVADA", "CONCLUIDA"):
        if t["reuse"]:
            estoque.append((t["aval"], 1, "ENTRADA", "REAPROVEITAMENTO", "DISPONIVEL", p, None))
        else:
            estoque.append((t["dt"], 1, "ENTRADA", "DEVOLUCAO_AVARIA", "SEGREGADO", p, None))
            if st == "CONCLUIDA":
                estoque.append((min(TODAY, t["aval"] + timedelta(days=1)), 1, "SAIDA", "DESCARTE", "SEGREGADO", p, None))
        if t["tp"] == "TROCA":
            estoque.append((t["subst_dt"], 1, "SAIDA", "SUBSTITUICAO", "DISPONIVEL", p, None))
# A07: saída acima do saldo (um erro de digitação do tipo 40 em vez de 4)
armacao_baixa = sorted(ARM_IDS, key=lambda p: sum(1 for e in estoque if e[5] == p))[0]
estoque.append((date(2026, 10, 14), 40, "SAIDA", "VENDA", "DISPONIVEL", armacao_baixa, None))

# demanda por venda: compras que atendem uma venda (DEMANDA)
lens_forn_compras = [c for c in compras if c["forn"] in (5, 6) and c["st"] == "RECEBIDA" and c["ped"] >= date(2026, 9, 1)]
R.shuffle(lens_forn_compras)
used_v = set()
linked = 0
for c in lens_forn_compras:
    if linked >= 3:
        break
    prods = set(p for p, _ in entries_by_compra[c["id"]])
    for s in cur_sales:
        if s in sales and not s["cancel"] and s["encomenda"] and s["vid"] not in used_v and (c["ped"] - s["dt"]).days in (0, 1, 2, 3):
            if any(p in prods for p, _, _ in s["lines"]):
                c["venda"] = s["vid"]
                used_v.add(s["vid"])
                linked += 1
                break

# notas de entrada
nfe = []
nre = 48200
sem_nfe = [c for c in compras if c["st"] == "RECEBIDA" and c["ped"] >= date(2026, 9, 1)]
sem_nfe_id = R.choice(sem_nfe)["id"]  # A02: compra recebida sem nota fiscal de entrada
for c in compras:
    if c["st"] == "CANCELADA" or c["id"] == sem_nfe_id:
        continue
    nre += R.randint(5, 40)
    custo = sum(qt * base_price[p] * 0.38 for p, qt in entries_by_compra[c["id"]]) or R.randint(2500, 9000)
    emis = c["ped"] + timedelta(days=R.randint(0, 2))
    if c["cheg"]:
        emis = min(emis, c["cheg"])
    emis = min(emis, TODAY)
    nfe.append((len(nfe) + 1, str(nre), emis, money(custo), money(custo * 0.07), c["id"]))
add_table("COMPRA", ["ID_COMPRA", "DT_PEDIDO", "DT_CHEGADA", "CD_STATUS", "ID_FORNECEDOR", "ID_VENDA"],
          [(c["id"], c["ped"], c["cheg"], c["st"], c["forn"], c["venda"]) for c in compras])
add_table("NOTA_FISCAL_ENTRADA", ["ID_NOTA_ENTRADA", "NR_NOTA", "DT_EMISSAO", "VL_TOTAL", "VL_TRIBUTOS", "ID_COMPRA"], nfe)
estoque.sort(key=lambda e: (e[0], 0 if e[2] == "ENTRADA" else 1, e[5]))
add_table("ESTOQUE", ["ID_MOVIMENTO", "DT_MOVIMENTO", "QT_MOVIMENTO", "CD_DIRECAO", "CD_MOTIVO", "CD_CONDICAO", "ID_PRODUTO", "ID_COMPRA"],
          [(i,) + e for i, e in enumerate(estoque, 1)])

# ---------------------------------------------------------------- saída
ORDER = ["FUNCIONARIO", "CLIENTE", "FORNECEDOR", "PRODUTO", "LENTE", "ARMACAO", "ATENDIMENTO", "RECEITA", "RECEITA_MEDIDA", "ORCAMENTO", "VENDA", "CONTEM", "PARCELA", "PAGAMENTO", "NOTA_FISCAL_SAIDA", "TROCA_DEVOLUCAO", "COMPRA", "NOTA_FISCAL_ENTRADA", "ESTOQUE"]
with open(OUT, "w", encoding="utf8") as f:
    for t in ORDER:
        cols, rows = OUT_ROWS[t]
        f.write("-- %s: %d linhas\n" % (t, len(rows)))
        for i in range(0, len(rows), 250):
            chunk = rows[i:i + 250]
            f.write("INSERT INTO %s (%s) VALUES\n" % (t, ", ".join(cols)))
            f.write(",\n".join("(" + ", ".join(q(v) for v in r) + ")" for r in chunk))
            f.write(";\n")
        f.write("\n")

# resumo
print("atendimentos", len(ats), "(hist:", sum(1 for a in ats if a["hist"]), ") vendas", len(sales), "(cancel:", sum(1 for s in sales if s['cancel']), ")")
for t in ORDER:
    print("%-22s %6d" % (t, len(OUT_ROWS[t][1])))
print("plantados:", {k: sum(1 for v in PLANT.values() if v == k) for k in set(PLANT.values())}, "sem_nota:", len(sem_nota), "compra_sem_nfe:", sem_nfe_id, "compras ligadas a venda:", linked)
print("vendas com parcelas:", len(set(p["venda"]["vid"] for p in parcelas)), "de", sum(1 for s in sales if not s["hist"] and not s["cancel"]), "efetivas do período")
