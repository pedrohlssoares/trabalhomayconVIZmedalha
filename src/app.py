"""Apenas inicializa o Dash e expõe o servidor (usado pelo gunicorn)."""
from dash import Dash

app = Dash(__name__, title="Quadro de Medalhas Olímpicas")
server = app.server
