import streamlit as st
from groq import Groq
import json

# Esto busca la llave que guardaste en los Secrets de Streamlit
GROQ_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_KEY)

def analizar_lead(comentario):
    prompt = f"""
    Eres un cerrador de ventas agresivo en República Dominicana. 
    Analiza este comentario: "{comentario}"
    
    TU MISIÓN: No descartes NADA que huela a dinero.
    
    CRITERIOS DE SCORE (0.0 a 1.0):
    - 1.0: Pregunta "Precio", "Info", "Cuanto", "WhatsApp", o "Donde tan".
    - 0.8: Pregunta por el inicial, financiamiento o si aceptan cambios.
    - 0.6: Comentarios de "Me interesa", "Quiero ir a verlo", o "¿Todavía lo tienen?".
    - 0.5: Preguntas sobre el estado del producto (km, año, condición, color).
    - 0.0: Solo emojis sin texto, o insultos.
    
    Cualquier duda sobre el producto debe tener al menos 0.5 de score.
    
    Responde estrictamente en JSON:
    {{"score_ia": valor, "producto_interes": "nombre", "intencion": "resumen"}}
    """
    # ... resto del código

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
