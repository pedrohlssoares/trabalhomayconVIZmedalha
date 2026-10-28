"""Arquivo principal: junta app + layout + callbacks e roda o projeto."""
from src.app import app, server  # `server` é usado pelo gunicorn (Procfile)
from src.callbacks import registrar_callbacks
from src.layout import criar_layout

app.layout = criar_layout()
registrar_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
