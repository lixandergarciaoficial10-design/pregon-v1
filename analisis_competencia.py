# ============================================
# 📊 ANÁLISIS DE COMPETENCIA - PREGÓN AI
# ============================================
# Este archivo:
# - analiza múltiples cuentas de TikTok
# - calcula métricas clave
# - genera ranking
# - usa IA para conclusiones
# ============================================

import requests
import streamlit as st
import statistics
from ia_engine import analizar_comentario

# ============================================
# 🔐 CONFIGURACIÓN RAPIDAPI
# ============================================

RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
}


# ============================================
# 🎥 OBTENER VIDEOS DE UNA CUENTA
# ============================================

def obtener_videos(usuario):
    """
    Obtiene últimos videos de una cuenta
    """

    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"

    try:
        res = requests.get(url, headers=HEADERS, params={"username": usuario})
        data = res.json()

        videos = data.get("data", {}).get("videos", [])

        return videos[:5]  # limitamos a 5

    except:
        return []


# ============================================
# 📊 ANALIZAR UNA CUENTA
# ============================================

def analizar_cuenta(usuario):
    """
    Devuelve métricas de una cuenta:
    - promedio views
    - máximo views
    - videos
    """

    videos = obtener_videos(usuario)

    if not videos:
        return None

    views = [v.get("play_count", 0) for v in videos]

    promedio = int(statistics.mean(views)) if views else 0
    maximo = max(views) if views else 0

    return {
        "usuario": usuario,
        "promedio_views": promedio,
        "max_views": maximo,
        "videos": videos
    }


# ============================================
# 🏆 ANALIZAR TODAS LAS CUENTAS
# ============================================

def analizar_competencia(lista_usuarios):
    """
    Procesa múltiples cuentas y devuelve ranking
    """

    resultados = []

    for user in lista_usuarios:
        data = analizar_cuenta(user)

        if data:
            resultados.append(data)

    # Ordenamos por promedio de views
    ranking = sorted(resultados, key=lambda x: x["promedio_views"], reverse=True)

    return ranking


# ============================================
# 🧠 GENERAR INSIGHT CON IA
# ============================================

def generar_insight(ranking):
    """
    Usa IA para generar conclusión inteligente
    """

    if not ranking:
        return "No hay datos suficientes"

    resumen = ""

    for r in ranking[:3]:
        resumen += f"{r['usuario']} tiene promedio de {r['promedio_views']} views.\n"

    prompt = f"""
    Analiza estos datos de TikTok:

    {resumen}

    Dame una conclusión clara de qué tipo de contenido está funcionando mejor.
    """

    # reutilizamos IA
    respuesta = analizar_comentario(prompt)

    return respuesta.get("intencion", "No disponible")
