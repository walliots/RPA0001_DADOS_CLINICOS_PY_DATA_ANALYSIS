"""Integração dos datasets brutos via inner join.

Trabalho Final - Desenvolvimento e Projeto de Solução RPA I (PUC Minas)
Integrantes: Gabriel Brunet Dure, Guilherme Henrique Barros Assis,
Samantha Araújo Fernandes de Souza, Walmir Pereira de Lima

Junta dados_clinicos + dados_pacientes (por id_cliente) e o resultado
+ estado_regiao (por id_estado), conforme pede o enunciado do trabalho.

Nenhum tratamento de dados (duplicatas, valores ausentes) é feito aqui
— isso fica a cargo de src/tratamento.py, na etapa seguinte do pipeline.
"""

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "datasets" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "datasets" / "processed"


def carregar_dados_clinicos(caminho: Path = RAW_DIR / "dados_clinicos.csv") -> pd.DataFrame:
    return pd.read_csv(caminho, sep="|")


def carregar_dados_pacientes(caminho: Path = RAW_DIR / "dados_pacientes.csv") -> pd.DataFrame:
    return pd.read_csv(caminho, sep=";", encoding="utf-8-sig")


def carregar_estado_regiao(caminho: Path = RAW_DIR / "estado_regiao.csv") -> pd.DataFrame:
    return pd.read_csv(caminho, sep=";")


def integrar_dados() -> pd.DataFrame:
    clinicos = carregar_dados_clinicos()
    pacientes = carregar_dados_pacientes()
    estados = carregar_estado_regiao()

    dados = clinicos.merge(pacientes, on="id_cliente", how="inner")
    dados = dados.merge(estados, on="id_estado", how="inner")
    return dados


def main() -> None:
    dados = integrar_dados()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    destino = PROCESSED_DIR / "dados_integrados.csv"
    dados.to_csv(destino, sep=";", index=False, encoding="utf-8-sig")
    print(f"{len(dados)} linhas integradas salvas em {destino}")


if __name__ == "__main__":
    main()
