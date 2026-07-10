"""Conexão e persistência das tabelas modeladas no MySQL.

Trabalho Final - Desenvolvimento e Projeto de Solução RPA I (PUC Minas)
Integrantes: Gabriel Brunet Dure, Guilherme Henrique Barros Assis,
Samantha Araújo Fernandes de Souza, Walmir Pereira de Lima

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


def ler_credenciais() -> dict:
    load_dotenv(ROOT_DIR / ".env")
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "3306"),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "nome_banco": os.environ.get("DB_NAME", "dados_clinicos"),
    }


def garantir_banco(credenciais: dict) -> None:
    """Cria o banco (schema) no servidor MySQL, caso ainda não exista."""
    url_servidor = (
        f"mysql+pymysql://{credenciais['user']}:{credenciais['password']}"
        f"@{credenciais['host']}:{credenciais['port']}?charset=utf8mb4"
    )
    engine_servidor = create_engine(url_servidor)
    with engine_servidor.begin() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS {credenciais['nome_banco']} "
                "CHARACTER SET utf8mb4"
            )
        )
    engine_servidor.dispose()


def obter_engine():
    credenciais = ler_credenciais()
    garantir_banco(credenciais)
    url = (
        f"mysql+pymysql://{credenciais['user']}:{credenciais['password']}"
        f"@{credenciais['host']}:{credenciais['port']}/{credenciais['nome_banco']}"
        "?charset=utf8mb4"
    )
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
