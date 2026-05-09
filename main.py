from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Datos(BaseModel):
    prompt: str | None = None

@app.post("/ia")
def responder(data: Datos):

    # Caso 1: Forminator está probando el webhook
    if not data.prompt:
        return {"status": "ok"}

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente financiero experto en análisis y recomendaciones personalizadas."},
            {"role": "user", "content": data.prompt}
        ]
    )

    return {"respuesta": completion.choices[0].message.content}


