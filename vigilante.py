import requests
import streamlit as st
from ia_engine import analizar_lead

# Esta es tu llave única de RapidAPI que vimos en las capturas
RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]

def espiar_instagram(username):
    """Busca los posts de un dealer en IG y saca sus leads."""
    url = "https://instagram-scraper47.p.rapidapi.com/get_user_posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-scraper47.p.rapidapi.com"
    }
    # Aquí la API busca por el nombre del usuario (ej: dealer_perez)
    querystring = {"username": username}
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        posts = response.json().get('body', {}).get('items', [])
        return posts # Devuelve la lista de fotos/videos del dealer
    except:
        return []

def espiar_tiktok(username):
    """Busca los videos de un dealer en TikTok."""
    url = "https://tiktok-all-data-scrapper3.p.rapidapi.com/user_video_list/"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tiktok-all-data-scrapper3.p.rapidapi.com"
    }
    querystring = {"unique_id": username}
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        videos = response.json().get('data', {}).get('videos', [])
        return videos
    except:
        return []

def limpiar_y_calificar(comentarios, plataforma):
    """Pasa la manguera a presión (IA) para dejar solo los leads reales."""
    leads_limpios = []
    for c in comentarios:
        texto = c.get('text', '')
        usuario = c.get('user', {}).get('username', 'usuario_anonimo')
        
        # EL CEREBRO ANALIZA EL COMENTARIO
        analisis = analizar_lead(texto)
        
        # SI LA IA DICE QUE ES UN CLIENTE DE VERDAD (Score > 0.7)
        if analisis.get('score_ia', 0) >= 0.7:
            leads_limpios.append({
                "usuario_ig": usuario,
                "comentario": texto,
                "score_ia": analisis.get('score_ia'),
                "vehiculo_interes": analisis.get('vehiculo_interes'),
                "fuente": plataforma
            })
    return leads_limpios
