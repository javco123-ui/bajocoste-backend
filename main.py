from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Pregunta(BaseModel):
    pregunta: str

@app.post("/ia")
def responder(data: Pregunta):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente financiero."},
            {"role": "user", "content": data.pregunta}
        ]
    )
    return {"respuesta": completion.choices[0].message.content}
