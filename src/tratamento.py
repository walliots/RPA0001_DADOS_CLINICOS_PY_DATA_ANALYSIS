"""Correção dos dados integrados: duplicatas e valores ausentes.

Trabalho Final - Desenvolvimento e Projeto de Solução RPA I (PUC Minas)
Integrantes: Gabriel Brunet Dure, Guilherme Henrique Barros Assis,
Samantha Araújo Fernandes de Souza, Walmir Pereira de Lima

Regras do enunciado:
- Variáveis categóricas: preencher valores ausentes com a moda.
- Variáveis numéricas: preencher valores ausentes com a mediana.

Opera sobre o resultado de src/integracao.py
(datasets/processed/dados_integrados.csv) e salva o dataset tratado em
datasets/processed/dados_tratados.csv.
"""

from pathlib import Path

import pandas as pd

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "datasets" / "processed"
ENTRADA = PROCESSED_DIR / "dados_integrados.csv"
SAIDA = PROCESSED_DIR / "dados_tratados.csv"

COLUNAS_ID = ["id_cliente", "id_estado"]


def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(ignore_index=True)


def preencher_ausentes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for coluna in df.columns:
        if coluna in COLUNAS_ID or df[coluna].isna().sum() == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[coluna]):
            valor = df[coluna].median()
        else:
            valor = df[coluna].mode(dropna=True)[0]
        df[coluna] = df[coluna].fillna(valor)
    return df


def tratar_dados(caminho_entrada: Path = ENTRADA) -> pd.DataFrame:
    df = pd.read_csv(caminho_entrada, sep=";", encoding="utf-8-sig")
    df = remover_duplicatas(df)
    df = preencher_ausentes(df)
    return df


def main() -> None:
    df = tratar_dados()
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig")
    print(f"{len(df)} linhas tratadas salvas em {SAIDA}")
    print("Valores ausentes restantes:")
    print(df.isna().sum()[df.isna().sum() > 0])


if __name__ == "__main__":
    main()
