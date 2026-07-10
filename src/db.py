"""Conexão e persistência das tabelas modeladas no MySQL.

Credenciais lidas de variáveis de ambiente (ou de um arquivo .env na
raiz do projeto, não versionado):

    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=...
    DB_NAME=dados_clinicos

Uso:
    python src/db.py            # cria o schema e carrega as tabelas
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from modelagem import construir_tabelas

ROOT_DIR = Path(__file__).resolve().parent.parent
SCHEMA_SQL = ROOT_DIR / "sql" / "ddl" / "schema.sql"

# Ordem de carga: tabelas de domínio primeiro, tb_paciente por último (FKs)
ORDEM_CARGA = [
    "tb_estado",
    "tb_classe_trabalho",
    "tb_estado_civil",
    "tb_raca",
    "tb_escolaridade",
    "tb_paciente",
]


def obter_engine():
    load_dotenv(ROOT_DIR / ".env")
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "3306")
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "")
    nome_banco = os.environ.get("DB_NAME", "dados_clinicos")
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{nome_banco}?charset=utf8mb4"
    return create_engine(url)


def criar_schema(engine) -> None:
    sql = SCHEMA_SQL.read_text(encoding="utf-8")
    with engine.begin() as conn:
        for comando in sql.split(";"):
            comando = comando.strip()
            if comando:
                conn.execute(text(comando))


def carregar_tabelas(engine) -> None:
    tabelas = construir_tabelas()
    with engine.begin() as conn:
        for nome in ORDEM_CARGA:
            tabelas[nome].to_sql(nome, conn, if_exists="append", index=False)
            print(f"{nome}: {len(tabelas[nome])} linhas carregadas")


def main() -> None:
    engine = obter_engine()
    criar_schema(engine)
    carregar_tabelas(engine)


if __name__ == "__main__":
    main()
