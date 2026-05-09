# bajocoste-backend
bajocoste-backend
# 🧠 Bajocoste Backend — Motor de Simuladores con IA

Backend desarrollado en **FastAPI** para alimentar los simuladores financieros de **Bajocoste.cl**.  
Este servicio recibe datos desde formularios de WordPress (Forminator), selecciona el simulador correspondiente y genera una respuesta personalizada usando **OpenAI**.

---

## 🚀 Características principales

- Arquitectura **modular y escalable**  
- Soporte para **N simuladores** sin modificar `main.py`  
- Prompts organizados por archivo dentro de `/prompts`  
- Integración directa con **Forminator Webhooks**  
- Respuestas generadas con **OpenAI GPT-4o-mini**  
- Preparado para despliegue en **Render**  

---

## 📁 Estructura del proyecto

### 🧩 ¿Cómo funciona?

- `main.py` → recibe el JSON desde Forminator, identifica el simulador y ejecuta el prompt.  
- `/prompts/*.py` → cada archivo contiene el prompt de un simulador.  
- `/prompts/index.py` → centraliza todos los prompts en un diccionario.  

---

## 🔄 Flujo de datos

1. El usuario completa un formulario en WordPress.  
2. Forminator envía un webhook al backend con:  
   - `simulador`: ID del simulador  
   - parámetros del usuario  
3. El backend selecciona el prompt correcto.  
4. Inserta los valores del usuario en el prompt.  
5. Llama a OpenAI.  
6. Devuelve la respuesta a Forminator.  
7. Forminator la muestra en pantalla.

---

## 🧠 Ejemplo de request desde Forminator

### Simulador: Suscripciones

```json
{
  "simulador": "suscripciones",
  "cantidad": "5"
}

