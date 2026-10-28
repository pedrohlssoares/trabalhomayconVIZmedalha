"""Parte visual: estrutura da página, filtros e espaços dos gráficos."""
from dash import dcc, html

from src.data_processing import TIPOS, df, opcoes_anos, opcoes_paises

CARD = {"flex": "1 1 45%", "minWidth": "380px", "padding": "10px"}
LINHA = {"display": "flex", "flexWrap": "wrap"}


def criar_layout():
    anos = opcoes_anos(df)
    paises = opcoes_paises(df)
    pais_padrao = "Brazil" if any(p["value"] == "Brazil" for p in paises) else paises[0]["value"]

    return html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px"}, children=[
        html.H1("Quadro de Medalhas Olímpicas - Jogos de Verão", style={"textAlign": "center"}),

        # Filtro 2: tipo de medalha (vale para o mapa, a área empilhada e as barras)
        html.Div(style={"textAlign": "center", "marginBottom": "10px"}, children=[
            html.Label("Tipo de medalha: ", style={"fontWeight": "bold"}),
            dcc.RadioItems(id="rd-medalha", options=TIPOS, value="Todos",
                           style={"display": "inline-block"},
                           labelStyle={"display": "inline-block", "marginRight": "18px"}),
        ]),

        # Gráfico 1 do tutorial: mapa
        dcc.Graph(id="g-mapa", style={"height": "50vh", "width": "100%"}),

        html.Div(style=LINHA, children=[
            # Gráfico 2 do tutorial: área empilhada (top 10 países ao longo do tempo)
            html.Div(dcc.Graph(id="g-area"), style=CARD),

            # Gráfico 3 do tutorial: barras (top 10) + filtro 3: Ano olímpico (país sede)
            html.Div(style=CARD, children=[
                html.Label("Ano olímpico (país sede)"),
                dcc.Dropdown(id="dd-ano", options=anos, placeholder="Todos os anos"),
                dcc.Graph(id="g-barras"),
            ]),
        ]),

        # Filtro 1: país -> pizza com ouro, prata e bronze
        html.Div(style={"padding": "10px", "maxWidth": "650px"}, children=[
            html.Label("País"),
            dcc.Dropdown(id="dd-pais", options=paises, value=pais_padrao, clearable=False),
            dcc.Graph(id="g-pizza"),
        ]),
    ])
