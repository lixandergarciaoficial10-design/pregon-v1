import requests
import streamlit as st
from ia_engine import analizar_lead

def rastrear_comentarios(url_post, plataforma):
    """
    Detecta si es Instagram o TikTok y usa la herramienta correcta.
    """
    headers = {
        "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
        "X-RapidAPI-Host": "" # Esto cambiará según la API que elijas
    }

    if plataforma == "Instagram":
        api_url = "https://instagram-looper.p.rapidapi.com/post-comments"
        headers["X-RapidAPI-Host"] = "instagram-looper.p.rapidapi.com"
    else:
        # Aquí pondremos la de TikTok que elijas en el paso 1
        api_url = "https://tiktok-full-info.p.rapidapi.com/comments"
        headers["X-RapidAPI-Host"] = "tiktok-full-info.p.rapidapi.com"

    try:
        response = requests.get(api_url, headers=headers, params={"url": url_post})
        data = response.json().get('data', [])
        
        leads_finales = []
        for item in data:
            texto = item.get('text')
            usuario = item.get('user', {}).get('username')
            
            # El cerebro (Groq) no cambia, analiza igual sea TikTok o IG
            analisis = analizar_lead(texto)
            
            if analisis.get('score_ia', 0) >= 0.7:
                leads_finales.append({
                    "usuario_ig": usuario,
                    "comentario": texto,
                    "score_ia": analisis.get('score_ia'),
                    "vehiculo": analisis.get('vehiculo_interes'),
                    "fuente": plataforma # Para saber de dónde vino el cuarto
                })
        return leads_finales
    except Exception as e:
        return f"Error: {e}"
