import streamlit as st
from groq import Groq
import json

# Esto busca la llave que guardaste en los Secrets de Streamlit
GROQ_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_KEY)

def analizar_lead(comentario):
    """
    Analiza un comentario de cualquier sector comercial en RD y extrae la intención de compra.
    """
    prompt = f"""
    Eres un experto en cierre de ventas y análisis de marketing en República Dominicana.
    Tu misión es detectar CUALQUIER intención de compra o interés comercial en este comentario: "{comentario}"

    REGLAS DE PUNTUACIÓN (Score de 0.0 a 1.0):
    - 0.9 a 1.0 (ALTA PRIORIDAD): Pregunta precio ("kanto e", "precio"), pide contacto ("ws", "numero"), o quiere comprar ya.
    - 0.6 a 0.8 (INTERÉS REAL): Pregunta detalles (color, tamaño, ubicación, año), métodos de pago (financian, inicial), o disponibilidad.
    - 0.4 a 0.5 (CURIOSIDAD): Preguntas generales sobre lo publicado o dudas leves.
    - 0.0 a 0.3 (BASURA/BULTO): Solo emojis, bendiciones, elogios vacíos ("duro", "nítido") o etiquetas sin mensaje.

    CONSIDERA LA JERGA DOMINICANA: 
    "Info", "Kanto", "Dime de eso", "Donde tan", "Cuanto pide", "Inisial", "Engancharse", "Apartar".

    Responde estrictamente en este formato JSON:
    {{
        "score_ia": valor_numerico, 
        "producto_interes": "nombre del producto/servicio detectado o General",
        "intencion": "breve resumen de qué busca el cliente"
    }}
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        # Convertimos la respuesta de texto a un diccionario de Python
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "score_ia": 0, 
            "producto_interes": "Error", 
            "intencion": f"Error de conexión: {e}"
        }
