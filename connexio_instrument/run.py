# run.py
from app import app

def post_greeting(name: str):
    return f"Hello {name}", 200

app.add_api("openapi.yaml")

