# run.py
from app import app
from opentelemetry.instrumentation.connexion import ConnexionInstrumentor


def post_greeting(name: str):
    return f"Hello {name}", 200

app.add_api("openapi.yaml")

ConnexionInstrumentor().instrument_app(app)
