from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Pregunta(BaseModel):
    pregunta: str | None = None

@app.post("/ia")
def responder(data: Pregunta):
    # Caso 1: Forminator está probando el webhook (envía {} o vacío)
    if not data.pregunta:
        return {"status": "ok"}

    # Caso 2: El usuario envió una pregunta real
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente financiero."},
            {"role": "user", "content": data.pregunta}
        ]
    )
    return {"respuesta": completion.choices[0].message.content}

