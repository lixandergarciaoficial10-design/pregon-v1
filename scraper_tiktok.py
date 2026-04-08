# ============================================
# 📡 SCRAPER TIKTOK - PREGÓN AI (VERSIÓN SEGURA)
# ============================================
# ✔ No rompe si falta API
# ✔ Tiene fallback (datos simulados)
# ✔ Código limpio y organizado
# ============================================

import requests
import streamlit as st
from ia_engine import analizar_comentario

# ============================================
# 🔐 CONFIGURACIÓN
# ============================================

RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY")

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
} if RAPIDAPI_KEY else None


# ============================================
# 🎥 OBTENER VIDEOS
# ============================================

def obtener_videos(usuario):
    """
    Obtiene los últimos videos del usuario.
    Si no hay API → usa datos simulados.
    """

    # 🔴 SIN API → MODO DEMO
    if not HEADERS:
        return [
            {"play": "demo1"},
            {"play": "demo2"},
            {"play": "demo3"}
        ]

    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params={"username": usuario},
            timeout=10
        )

        data = response.json()
        videos = data.get("data", {}).get("videos", [])

        return videos[:3]

    except Exception as e:
        print(f"Error obteniendo videos: {e}")
        return []


# ============================================
# 💬 OBTENER COMENTARIOS
# ============================================

def obtener_comentarios(video_url):
    """
    Obtiene comentarios de un video.
    Si no hay API → devuelve comentarios fake.
    """

    # 🔴 SIN API → MODO DEMO
    if not HEADERS:
        return [
            {"text": "Precio?", "user": {"unique_id": "cliente1"}},
            {"text": "Me interesa", "user": {"unique_id": "cliente2"}},
            {"text": "Cuánto cuesta?", "user": {"unique_id": "cliente3"}},
            {"text": "Info por favor", "user": {"unique_id": "cliente4"}},
        ]

    url = "https://tiktok-scraper7.p.rapidapi.com/video/comments"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params={"url": video_url},
            timeout=10
        )

        data = response.json()
        comentarios = data.get("data", {}).get("comments", [])

        return comentarios[:20]

    except Exception as e:
        print(f"Error obteniendo comentarios: {e}")
        return []


# ============================================
# 🧠 PROCESAR COMENTARIOS
# ============================================

def procesar_comentarios(usuario):
    """
    Flujo completo:
    - obtiene videos
    - obtiene comentarios
    - analiza con IA
    - devuelve leads reales
    """

    leads = []

    videos = obtener_videos(usuario)

    if not videos:
        return []

    for video in videos:

        video_url = video.get("play")

        if not video_url:
            continue

        comentarios = obtener_comentarios(video_url)

        for c in comentarios:

            texto = c.get("text")
            user = c.get("user", {}).get("unique_id")

            if not texto:
                continue

            try:
                analisis = analizar_comentario(texto)
                score = analisis.get("score_ia", 0)

                # 🔥 FILTRO DE CLIENTES
                if score >= 0.6:
                    leads.append({
                        "usuario": user or "anonimo",
                        "comentario": texto,
                        "score_ia": score,
                        "intencion": analisis.get("intencion", ""),
                        "producto_interes": analisis.get("producto_interes", "General"),
                        "fuente": "TikTok"
                    })

            except Exception as e:
                print(f"Error IA: {e}")
                continue

    return leads
