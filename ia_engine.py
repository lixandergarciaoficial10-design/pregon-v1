import streamlit as st
from groq import Groq
import json

# Esto busca la llave que guardaste en los Secrets de Streamlit
GROQ_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_KEY)

def analizar_lead(comentario):
    """
    Toma un comentario de Instagram y lo convierte en datos para tu tabla.
    """
    prompt = f"""
    Eres un experto en ventas de vehículos en República Dominicana.
    Analiza este comentario de Instagram: "{comentario}"
    
    Determina:
    1. score_ia: Probabilidad de compra del 0.0 al 1.0.
    2. vehiculo_interes: Qué vehículo menciona (ej: 'Honda Civic', 'CRV', 'N/A').
    
    Responde estrictamente en este formato JSON:
    {{"score_ia": 0.0, "vehiculo_interes": "nombre"}}
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            response_format={"type": "json_object"}
        )
        # Convertimos la respuesta de texto a un diccionario de Python
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"score_ia": 0, "vehiculo_interes": f"Error: {e}"}
