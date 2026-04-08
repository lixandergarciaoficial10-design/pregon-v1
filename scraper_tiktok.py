# ============================================
# 📡 SCRAPER TIKTOK - PREGÓN AI (PRO COMPLETO)
# ============================================
# ✔ Funciona con API (RapidAPI)
# ✔ Funciona sin API (modo demo)
# ✔ No rompe la app nunca
# ✔ Devuelve leads listos para guardar
# ============================================

import requests
import streamlit as st
from ia_engine import analizar_lead  # 👈 importante (nombre correcto)

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
    Devuelve lista de videos del usuario
    """

    # 🔴 MODO DEMO (sin API)
    if not HEADERS:
        return [
            {"play": "demo_video_1"},
            {"play": "demo_video_2"},
            {"play": "demo_video_3"}
        ]

    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"

    try:
        res = requests.get(
            url,
            headers=HEADERS,
            params={"username": usuario},
            timeout=10
        )

        data = res.json()
        videos = data.get("data", {}).get("videos", [])

        return videos[:3]

    except Exception as e:
        print("Error obteniendo videos:", e)
        return []


# ============================================
# 💬 OBTENER COMENTARIOS
# ============================================

def obtener_comentarios(video_url):
    """
    Devuelve comentarios de un video
    """

    # 🔴 MODO DEMO (sin API)
    if not HEADERS:
        return [
            {"text": "Precio?", "user": {"unique_id": "cliente1"}},
            {"text": "Cuánto cuesta?", "user": {"unique_id": "cliente2"}},
            {"text": "Me interesa", "user": {"unique_id": "cliente3"}},
            {"text": "Info al DM", "user": {"unique_id": "cliente4"}},
            {"text": "Tienen delivery?", "user": {"unique_id": "cliente5"}},
        ]

    url = "https://tiktok-scraper7.p.rapidapi.com/video/comments"

    try:
        res = requests.get(
            url,
            headers=HEADERS,
            params={"url": video_url},
            timeout=10
        )

        data = res.json()
        comentarios = data.get("data", {}).get("comments", [])

        return comentarios[:20]

    except Exception as e:
        print("Error obteniendo comentarios:", e)
        return []


# ============================================
# 🧠 PROCESAR COMENTARIOS (FUNCIÓN PRINCIPAL)
# ============================================

def procesar_comentarios(usuario):
    """
    Flujo completo:
    - obtiene videos
    - obtiene comentarios
    - analiza con IA
    - devuelve leads filtrados
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
                analisis = analizar_lead(texto)

                score = analisis.get("score_ia", 0)

                # 🔥 FILTRO (clientes con intención)
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
                print("Error IA:", e)
                continue

    return leads
