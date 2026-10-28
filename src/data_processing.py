"""Leitura e tratamento dos dados. Nenhum código visual aqui."""
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_DADOS = BASE_DIR / "data" / "Summer_olympic_Medals.csv"
SEPARADOR = ","          # (no tutorial o CSV usa ";", este usa ",")

# O tutorial usa só os jogos a partir de 1992. Para usar toda a base, coloque 1896.
ANO_INICIAL = 1992

# Nomes ajustados para o mapa reconhecer o país (como no tutorial: "United States")
CORRECOES_PAIS = {
    "United States": "United States of America",
    "Great Britain": "United Kingdom",
}

COLUNAS = ["Year", "Host_country", "Host_city", "Country_Name", "Gold", "Silver", "Bronze"]

TIPOS = ["Todos", "Ouro", "Prata", "Bronze"]
COLUNA_MEDALHA = {"Ouro": "Gold", "Prata": "Silver", "Bronze": "Bronze"}
CORES = {"Todos": "goldenrod", "Ouro": "gold", "Prata": "silver", "Bronze": "#CD7F32"}
TEXTO_TIPO = {"Todos": "total de medalhas", "Ouro": "medalhas de ouro",
              "Prata": "medalhas de prata", "Bronze": "medalhas de bronze"}

LABELS = {"medalhas": "Medalhas", "Country_Name": "País", "Year": "Ano"}


# ---------------------------------------------------------------------------
# FUNÇÕES
# ---------------------------------------------------------------------------
def carregar_dados() -> pd.DataFrame:
    """Lê o CSV, corrige nomes de países e filtra o período."""
    bruto = pd.read_csv(CAMINHO_DADOS, sep=SEPARADOR)

    faltando = [c for c in COLUNAS if c not in bruto.columns]
    if faltando:
        raise KeyError(f"Colunas não encontradas: {faltando}. Existentes: {bruto.columns.tolist()}")

    df = bruto[COLUNAS].copy()
    df["Country_Name"] = df["Country_Name"].str.strip().replace(CORRECOES_PAIS)
    df = df[df["Year"] >= ANO_INICIAL]
    return df


def com_medalhas(dados: pd.DataFrame, tipo: str | None) -> pd.DataFrame:
    """Cria a coluna 'medalhas' conforme o tipo escolhido (Ouro, Prata, Bronze ou Todos)."""
    d = dados.copy()
    if tipo in COLUNA_MEDALHA:
        d["medalhas"] = d[COLUNA_MEDALHA[tipo]]
    else:  # "Todos" (ou nenhum filtro)
        d["medalhas"] = d[["Gold", "Silver", "Bronze"]].sum(axis=1)
    return d


def opcoes_paises(dados: pd.DataFrame) -> list[dict]:
    return [{"label": p, "value": p} for p in sorted(dados["Country_Name"].unique())]


def opcoes_anos(dados: pd.DataFrame) -> list[dict]:
    """Um item por edição: '2016 - Brazil (Rio de Janeiro)' (mais recente primeiro)."""
    sedes = dados.groupby("Year")[["Host_country", "Host_city"]].first().sort_index(ascending=False)
    return [{"label": f"{ano} - {r.Host_country} ({r.Host_city})", "value": int(ano)}
            for ano, r in sedes.iterrows()]


# DataFrame carregado uma única vez, quando o projeto sobe
df = carregar_dados()
