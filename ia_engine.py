# ============================================
# 🧠 IA ENGINE - PREGÓN AI
# ============================================
# Este archivo se encarga de analizar comentarios
# y determinar si una persona tiene intención de compra.
# ============================================

import streamlit as st
from groq import Groq
import json

# ============================================
# 🔐 CONFIGURACIÓN DEL CLIENTE GROQ
# ============================================

# Obtenemos la API KEY desde los secrets de Streamlit
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Creamos el cliente de Groq
client = Groq(api_key=GROQ_API_KEY)


# ============================================
# 🧠 FUNCIÓN PRINCIPAL DE ANÁLISIS
# ============================================

def analizar_comentario(texto):
    """
    Esta función recibe un comentario de TikTok o Instagram
    y devuelve un análisis en formato JSON con:

    - score_ia (probabilidad de compra)
    - intencion (qué quiere el cliente)
    - producto_interes (si se puede inferir)

    """

    # ========================================
    # 🧾 PROMPT INTELIGENTE
    # ========================================
    # Aquí le damos instrucciones claras a la IA
    # para que analice como un vendedor experto
    # dominicano.

    prompt = f"""
    Eres un vendedor experto en República Dominicana.

    Analiza este comentario:
    "{texto}"

    Determina si la persona quiere comprar.

    Reglas:
    - Si pregunta "precio", "info", "disponible" → score alto (0.8 - 1.0)
    - Si dice "me interesa", "dónde queda" → score medio (0.5 - 0.7)
    - Si es irrelevante → score bajo (0.0 - 0.3)

    Responde SOLO en JSON:

    {{
        "score_ia": numero,
        "intencion": "explicación corta",
        "producto_interes": "si aplica"
    }}
    """

    try:
        # ====================================
        # 📡 LLAMADA A GROQ
        # ====================================
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )

        # Convertimos la respuesta a diccionario Python
        resultado = json.loads(response.choices[0].message.content)

        return resultado

    except Exception as e:
        # En caso de error devolvemos algo controlado
        return {
            "score_ia": 0,
            "intencion": f"Error: {str(e)}",
            "producto_interes": "N/A"
        }
