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
Eres un experto en ventas en República Dominicana.

Analiza este comentario:
"{texto}"

Tu objetivo es detectar intención de compra REAL.

Reglas:

- score_ia = 1.0 → quiere comprar YA (precio, info, whatsapp, donde queda)
- score_ia = 0.7 → interesado (me interesa, todavía disponible)
- score_ia = 0.5 → curiosidad (pregunta general)
- score_ia = 0.0 → sin valor (emoji, spam, chiste)

IMPORTANTE:
- Si menciona dinero, precio o compra → mínimo 0.7
- No seas conservador, detecta oportunidades

Responde SOLO en JSON:

{{
  "score_ia": numero,
  "intencion": "explicación corta y clara",
  "producto_interes": "producto si se puede inferir"
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
