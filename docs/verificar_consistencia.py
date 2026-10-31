#!/usr/bin/env python3
"""Conferência estática do inventário conceitual ↔ relacional.

Uso (na raiz do repositório): python docs/verificar_consistencia.py
Não executa SQL, nem valida cardinalidades, FKs ou dados.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
DICIONARIO = ROOT / "Dicionario_de_Dados_Otica_Kadosh.html"
SQL = ROOT / "docs" / "script.sql"

def ler(arquivo: Path) -> str:
    return arquivo.read_text(encoding="utf-8")

def extrair_mapeamento_readme(texto: str) -> tuple[set[str], set[str]]:
    inicio = texto.index("### Entidades → tabelas")
    fim = texto.index("### Atributos → colunas", inicio)
    trecho = texto[inicio:fim]
    entidades: set[str] = set()
    associativas: set[str] = set()
    for linha in trecho.splitlines():
        celulas = [parte.strip() for parte in linha.strip().strip("|").split("|")]
        if len(celulas) < 3:
            continue
        origem, tabela = celulas[:2]
        nome = re.fullmatch(r"`([A-Z][A-Z0-9_]*)`", tabela)
        if not nome:
            continue
        if origem.startswith("Relacionamento "):
            associativas.add(nome.group(1))
        elif re.fullmatch(r"[A-Z][A-Z0-9_]*", origem):
            entidades.add(origem)
            if origem != nome.group(1):
                raise ValueError(f"Mapeamento de entidade inesperado: {origem} → {tabela}")
    return entidades, associativas

def extrair_dicionario(texto: str) -> set[str]:
    inicio = texto.index('id="modelo"')
    fim = texto.index("<h3>Relacionamentos e cardinalidades", inicio)
    trecho = texto[inicio:fim]
    return set(re.findall(r"<tr><td>([A-Z][A-Z0-9_]*)</td><td>", trecho))

def extrair_sql(texto: str) -> list[str]:
    # Somente comandos CREATE TABLE, não menções em comentários/consultas.
    return re.findall(r"^CREATE\s+TABLE\s+`?([A-Z][A-Z0-9_]*)`?\s*\(", texto, flags=re.I | re.M)

def main() -> int:
    try:
        entidades, associativas = extrair_mapeamento_readme(ler(README))
        dicionario = extrair_dicionario(ler(DICIONARIO))
        sql_lista = extrair_sql(ler(SQL))
    except (OSError, ValueError) as erro:
        print(f"ERRO ao ler/interpretar artefatos: {erro}", file=sys.stderr)
        return 2

    sql = set(sql_lista)
    esperado = entidades | associativas
    erros = []
    if len(sql_lista) != len(sql):
        erros.append("CREATE TABLE duplicados: " + str(len(sql_lista) - len(sql)))
    if not associativas:
        erros.append("Nenhuma tabela associativa identificada no README")
    if entidades != dicionario:
        erros.append(f"README vs dicionário — faltam no dicionário: {sorted(entidades-dicionario)}; extras: {sorted(dicionario-entidades)}")
    if esperado != sql:
        erros.append(f"README vs SQL — faltam no SQL: {sorted(esperado-sql)}; extras: {sorted(sql-esperado)}")

    print(f"README: {len(entidades)} entidades + {len(associativas)} tabela(s) associativa(s)")
    print(f"Dicionário: {len(dicionario)} entidades | SQL: {len(sql_lista)} CREATE TABLE")
    if erros:
        for erro in erros:
            print("FALHA:", erro)
        return 1
    print("OK: inventários estruturais coincidem.")
    print("ATENÇÃO: não valida DER visual, cardinalidades, SQL executável ou integridade.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
