"""Lógica de interação: todos os @app.callback ficam aqui."""
import plotly.express as px
from dash import Input, Output

from src.data_processing import CORES, LABELS, TEXTO_TIPO, com_medalhas, df

PERIODO = f"{df['Year'].min()} a {df['Year'].max()}"


def registrar_callbacks(app):
    # Mapa: total de medalhas por país (filtro: tipo de medalha)
    @app.callback(Output("g-mapa", "figure"), Input("rd-medalha", "value"))
    def grafico_mapa(tipo):
        tipo = tipo or "Todos"
        d = com_medalhas(df, tipo).groupby("Country_Name", as_index=False)["medalhas"].sum()
        d = d[d["medalhas"] > 0]
        fig = px.choropleth(d, locations="Country_Name", locationmode="country names",
                            color="medalhas", color_continuous_scale="YlOrRd", labels=LABELS,
                            title=f"{TEXTO_TIPO[tipo].capitalize()} por país - {PERIODO}")
        return fig.update_layout(margin={"l": 0, "r": 0, "t": 40, "b": 0})

    # Área empilhada: top 10 países ao longo do tempo (filtro: tipo de medalha)
    @app.callback(Output("g-area", "figure"), Input("rd-medalha", "value"))
    def grafico_area(tipo):
        tipo = tipo or "Todos"
        d = com_medalhas(df, tipo)
        top10 = d.groupby("Country_Name")["medalhas"].sum().nlargest(10).index.tolist()
        d = d[d["Country_Name"].isin(top10)]
        # preenche com 0 os anos em que o país não tem medalha (evita buracos no empilhado)
        largo = d.pivot_table(index="Year", columns="Country_Name", values="medalhas",
                              aggfunc="sum", fill_value=0)[top10]
        longo = largo.reset_index().melt(id_vars="Year", var_name="Country_Name",
                                         value_name="medalhas")
        return px.area(longo, x="Year", y="medalhas", color="Country_Name", labels=LABELS,
                       title=f"Top 10 países - {TEXTO_TIPO[tipo]} - {PERIODO}")

    # Barras: top 10 países (filtros: tipo de medalha e ano olímpico)
    @app.callback(Output("g-barras", "figure"),
                  Input("rd-medalha", "value"), Input("dd-ano", "value"))
    def grafico_barras(tipo, ano):
        tipo = tipo or "Todos"
        d = com_medalhas(df, tipo)
        if ano:
            d = d[d["Year"] == ano]
        d = d.groupby("Country_Name", as_index=False)["medalhas"].sum()
        d = d[d["medalhas"] > 0].nlargest(10, "medalhas")
        quando = str(ano) if ano else PERIODO
        return px.bar(d, x="Country_Name", y="medalhas", labels=LABELS,
                      color_discrete_sequence=[CORES[tipo]],
                      title=f"Top 10 países - {TEXTO_TIPO[tipo]} - {quando}")

    # Pizza: ouro, prata e bronze do país escolhido
    @app.callback(Output("g-pizza", "figure"), Input("dd-pais", "value"))
    def grafico_pizza(pais):
        d = df[df["Country_Name"] == pais][["Gold", "Silver", "Bronze"]].sum()
        dados = {"Medalha": ["Ouro", "Prata", "Bronze"],
                 "Total": [int(d["Gold"]), int(d["Silver"]), int(d["Bronze"])]}
        return px.pie(dados, names="Medalha", values="Total", color="Medalha",
                      color_discrete_map={k: CORES[k] for k in ("Ouro", "Prata", "Bronze")},
                      title=f"Medalhas de {pais} - {PERIODO}")
