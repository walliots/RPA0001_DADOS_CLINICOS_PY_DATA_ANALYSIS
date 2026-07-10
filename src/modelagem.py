"""Normalização dos dados tratados no modelo do DER (tb_paciente + tabelas de domínio).

Lê datasets/processed/dados_tratados.csv (dataset já integrado e sem
duplicatas/nulos) e gera:
- tb_estado (a partir de estado_regiao.csv, id_estado -> cod_estado)
- tb_classe_trabalho, tb_estado_civil, tb_raca, tb_escolaridade
  (tabelas de dominio, com codigos gerados a partir dos valores unicos)
- tb_paciente (tabela fato, com FKs para as tabelas acima)
"""

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "datasets" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "datasets" / "processed"
TRATADOS = PROCESSED_DIR / "dados_tratados.csv"


def construir_tabela_dominio(serie: pd.Series, coluna_codigo: str, coluna_valor: str) -> pd.DataFrame:
    valores = sorted(serie.dropna().unique())
    return pd.DataFrame(
        {coluna_codigo: range(1, len(valores) + 1), coluna_valor: valores}
    )


def construir_tb_estado() -> pd.DataFrame:
    estados = pd.read_csv(RAW_DIR / "estado_regiao.csv", sep=";").drop_duplicates()
    return estados.rename(columns={"id_estado": "cod_estado"})[
        ["cod_estado", "estado", "sigla", "regiao", "pais"]
    ]


def construir_tabelas() -> dict[str, pd.DataFrame]:
    dados = pd.read_csv(TRATADOS, sep=";", encoding="utf-8-sig")

    tb_estado = construir_tb_estado()
    tb_classe_trabalho = construir_tabela_dominio(
        dados["classe_trabalho"], "cod_classe_trabalho", "classe_trabalho"
    )
    tb_estado_civil = construir_tabela_dominio(
        dados["estado_civil"], "cod_estado_civil", "estado_civil"
    )
    tb_raca = construir_tabela_dominio(dados["raca"], "cod_raca", "raca")
    tb_escolaridade = construir_tabela_dominio(
        dados["escolaridade"], "cod_escolaridade", "escolaridade"
    )

    paciente = dados.merge(tb_classe_trabalho, on="classe_trabalho", how="left")
    paciente = paciente.merge(tb_estado_civil, on="estado_civil", how="left")
    paciente = paciente.merge(tb_raca, on="raca", how="left")
    paciente = paciente.merge(tb_escolaridade, on="escolaridade", how="left")

    tb_paciente = paciente.rename(
        columns={
            "id_cliente": "cod_paciente",
            "id_estado": "cod_estado",
            "qtde_filhos": "qtd_filho",
        }
    )[
        [
            "cod_paciente",
            "cod_estado_civil",
            "cod_raca",
            "cod_escolaridade",
            "cod_classe_trabalho",
            "cod_estado",
            "genero",
            "idade",
            "qtd_filho",
            "salario",
            "peso",
            "colesterol",
        ]
    ]
    tb_paciente["qtd_filho"] = tb_paciente["qtd_filho"].astype(int)

    return {
        "tb_estado": tb_estado,
        "tb_classe_trabalho": tb_classe_trabalho,
        "tb_estado_civil": tb_estado_civil,
        "tb_raca": tb_raca,
        "tb_escolaridade": tb_escolaridade,
        "tb_paciente": tb_paciente,
    }


def main() -> None:
    tabelas = construir_tabelas()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for nome, df in tabelas.items():
        destino = PROCESSED_DIR / f"{nome}.csv"
        df.to_csv(destino, sep=";", index=False, encoding="utf-8-sig")
        print(f"{nome}: {len(df)} linhas -> {destino}")


if __name__ == "__main__":
    main()
