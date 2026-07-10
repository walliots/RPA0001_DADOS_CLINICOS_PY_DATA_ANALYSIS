"""Executa as consultas SQL do questionário contra o MySQL e mostra os resultados.

Trabalho Final - Desenvolvimento e Projeto de Solução RPA I (PUC Minas)
Integrantes: Gabriel Brunet Dure, Guilherme Henrique Barros Assis,
Samantha Araújo Fernandes de Souza

Uso:
    python src/consultas.py
"""

from pathlib import Path

import pandas as pd

from db import obter_engine

CONSULTAS_DIR = Path(__file__).resolve().parent.parent / "sql" / "consultas"


def executar_consultas() -> dict[str, list[pd.DataFrame]]:
    engine = obter_engine()
    resultados: dict[str, list[pd.DataFrame]] = {}
    for arquivo in sorted(CONSULTAS_DIR.glob("*.sql")):
        sql = arquivo.read_text(encoding="utf-8")
        # separa em blocos (um por comando ";"), ignorando linhas de comentario
        blocos = []
        bloco_atual = []
        for linha in sql.splitlines():
            if linha.strip().startswith("--"):
                continue
            bloco_atual.append(linha)
            if linha.strip().endswith(";"):
                blocos.append("\n".join(bloco_atual))
                bloco_atual = []
        resultados[arquivo.name] = [pd.read_sql(text_sql.rstrip(";"), engine) for text_sql in blocos if text_sql.strip()]
    return resultados


def main() -> None:
    resultados = executar_consultas()
    for arquivo, dataframes in resultados.items():
        print(f"\n=== {arquivo} ===")
        for df in dataframes:
            print(df.to_string(index=False))


if __name__ == "__main__":
    main()
