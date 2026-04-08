# ============================================
# 📡 SCRAPER TIKTOK - PREGÓN AI
# ============================================
# Este archivo se encarga de:
# 1. Obtener videos de una cuenta de TikTok
# 2. Extraer comentarios de esos videos
# 3. Analizar cada comentario con IA
# 4. Devolver solo clientes con intención de compra
# ============================================

import requests
import streamlit as st
from ia_engine import analizar_comentario


# ============================================
# 🔐 CONFIGURACIÓN
# ============================================

# API KEY desde secrets
RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY", None]

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
}


# ============================================
# 🎥 OBTENER VIDEOS DE UN USUARIO
# ============================================

def obtener_videos(usuario):
    """
    Obtiene los últimos videos de una cuenta de TikTok.
    """

    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params={"username": usuario}
        )

        data = response.json()

        # Extraemos lista de videos
        videos = data.get("data", {}).get("videos", [])

        return videos[:3]  # SOLO los últimos 3 videos

    except Exception as e:
        print(f"Error obteniendo videos: {e}")
        return []


# ============================================
# 💬 OBTENER COMENTARIOS DE UN VIDEO
# ============================================

def obtener_comentarios(video_url):
    """
    Obtiene comentarios de un video específico.
    """

    url = "https://tiktok-scraper7.p.rapidapi.com/video/comments"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params={"url": video_url}
        )

        data = response.json()

        comentarios = data.get("data", {}).get("comments", [])

        return comentarios[:20]  # limitamos a 20 comentarios

    except Exception as e:
        print(f"Error obteniendo comentarios: {e}")
        return []


# ============================================
# 🧠 PROCESAR COMENTARIOS CON IA
# ============================================

def procesar_comentarios(usuario):
    """
    Función principal:

    - Busca videos
    - Extrae comentarios
    - Analiza con IA
    - Devuelve leads listos
    """

    leads = []

    # 1. Obtener videos del usuario
    videos = obtener_videos(usuario)

    if not videos:
        return []

    # 2. Iterar cada video
    for video in videos:

        video_url = video.get("play")  # URL del video

        if not video_url:
            continue

        # 3. Obtener comentarios del video
        comentarios = obtener_comentarios(video_url)

        # 4. Analizar cada comentario
        for c in comentarios:

            texto = c.get("text")
            user = c.get("user", {}).get("unique_id")

            if not texto:
                continue

            # 5. IA analiza el comentario
            analisis = analizar_comentario(texto)

            score = analisis.get("score_ia", 0)

            # 6. FILTRO (solo clientes reales)
            if score >= 0.6:

                leads.append({
                    "usuario": user,
                    "comentario": texto,
                    "score_ia": score,
                    "intencion": analisis.get("intencion"),
                    "producto_interes": analisis.get("producto_interes"),
                    "fuente": "TikTok"
                })

    return leads
