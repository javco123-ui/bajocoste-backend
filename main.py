from fastapi import FastAPI, Request
from openai import OpenAI
import os
from prompts.index import PROMPTS
from fastapi.responses import PlainTextResponse

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/ia")
async def responder(request: Request):
    data = await request.json()
    print("Datos recibidos desde Forminator:", data)


    # Caso 1: Forminator está probando el webhook
    if not data:
        return {"status": "ok"}

    # 1) Identificar el simulador
    simulador = data.get("form_title")
    if not simulador:
        return {"error": "Falta el campo 'simulador'."}

    # 2) Obtener el prompt base desde el diccionario centralizado
    prompt_base = PROMPTS.get(simulador)
    if not prompt_base:
        return {"error": f"Simulador '{simulador}' no encontrado."}

    # 3) Construir el prompt dinámico con los parámetros del usuario
    try:
        prompt_final = prompt_base.format(**data)
    except Exception as e:
        return {"error": f"Error formateando el prompt: {str(e)}"}

    # 4) Llamar a OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en finanzas personales."},
            {"role": "user", "content": prompt_final}
        ]
    )

    return PlainTextResponse(completion.choices[0].message.content)

