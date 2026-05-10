from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from prompts.index import PROMPTS

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("API KEY:", os.getenv("OPENAI_API_KEY"))

@app.post("/ia")
async def responder(request: Request):
    data = await request.json()
    print("Datos recibidos:", data)

    # 1) Validar que viene el simulador
    simulador = data.get("simulador")
    if not simulador:
        return PlainTextResponse("Error: falta el campo 'simulador'.", status_code=400)

    # 2) Obtener el prompt base
    prompt_base = PROMPTS.get(simulador)
    if not prompt_base:
        return PlainTextResponse(f"Error: simulador '{simulador}' no encontrado.", status_code=400)

    # 3) Construir el prompt dinámico
    try:
        prompt_final = prompt_base.format(**data)
        print("Prompt final:", prompt_final)
    except Exception as e:
        return PlainTextResponse(f"Error formateando el prompt: {str(e)}", status_code=400)

    # 4) Llamar a OpenAI
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en finanzas personales."},
                {"role": "user", "content": prompt_final}
            ]
        )

        # SDK nuevo → usar .content
        respuesta = completion.choices[0].message.content
        return PlainTextResponse(respuesta)

    except Exception as e:
        print("Error OpenAI:", e)
        return PlainTextResponse("Error interno procesando la solicitud.", status_code=500)
