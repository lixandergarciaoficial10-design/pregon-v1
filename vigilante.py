import requests
import streamlit as st
from ia_engine import analizar_lead

# Llave de RapidAPI desde los Secrets
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def espiar_instagram(username):
    """Busca los posts de un perfil en IG y extrae sus comentarios."""
    url = "https://instagram-scraper47.p.rapidapi.com/get_user_posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-scraper47.p.rapidapi.com"
    }
    querystring = {"username": username}
    
    lista_comentarios_total = []
    try:
        response = requests.get(url, headers=headers, params=querystring)
        # Tomamos los últimos 10 posts para cubrir la semana y media
        posts = response.json().get('body', {}).get('items', [])[:10] 
        
        for post in posts:
            # Extraemos los comentarios de cada post
            comments = post.get('comments', {}).get('items', [])
            for c in comments:
                lista_comentarios_total.append({
                    'text': c.get('text', ''),
                    'username': c.get('user', {}).get('username', 'anonimo')
                })
        return lista_comentarios_total
    except:
        return []

def espiar_tiktok(username):
    """Busca los videos de un perfil en TikTok y extrae sus comentarios."""
    url = "https://tiktok-all-data-scrapper3.p.rapidapi.com/user_video_list/"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tiktok-all-data-scrapper3.p.rapidapi.com"
    }
    querystring = {"unique_id": username}
    
    lista_comentarios_total = []
    try:
        response = requests.get(url, headers=headers, params=querystring)
        videos = response.json().get('data', {}).get('videos', [])[:10]
        
        for vid in videos:
            # En TikTok la estructura puede variar según la API, 
            # asumiendo que vienen comentarios básicos en el objeto del video:
            comms = vid.get('comments_data', []) 
            for c in comms:
                lista_comentarios_total.append({
                    'text': c.get('text', ''),
                    'username': c.get('unique_id', 'anonimo_tt')
                })
        return lista_comentarios_total
    except:
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    """Pasa la manguera a presión (IA) y baja el filtro a 0.3 para volumen total."""
    leads_limpios = []
    
    for c in lista_comentarios:
        texto = c.get('text', '')
        usuario = c.get('username', 'usuario_anonimo')
        
        if not texto: continue

        # EL CEREBRO ANALIZA EL COMENTARIO
        analisis = analizar_lead(texto)
        
        # FILTRO AGRESIVO: Bajamos a 0.3 para capturar TODO lo que huela a interés
        score = analisis.get('score_ia', 0)
        if score >= 0.3:
            leads_limpios.append({
                "usuario_ig": usuario,
                "comentario": texto,
                "score_ia": score,
                # Usamos producto_interes (General) en lugar de solo vehículos
                "vehiculo_interes": analisis.get('producto_interes', analisis.get('vehiculo_interes', 'General')),
                "fuente": plataforma
            })
    return leads_limpios
