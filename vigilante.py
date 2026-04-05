import requests
import streamlit as st
from ia_engine import analizar_lead

# Llave de RapidAPI
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def limpiar_nombre_usuario(user):
    return user.replace("@", "").strip().lower()

def espiar_instagram(username):
    """Cambiamos a una API más potente para Instagram."""
    user_limpio = limpiar_nombre_usuario(username)
    
    # Probaremos con un endpoint de búsqueda de perfil más directo
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
    }
    querystring = {"username_or_id_or_url": user_limpio}
    
    lista_comentarios_total = []
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        data = response.json()
        
        # Estructura típica de APIs de alto rendimiento
        posts = data.get('data', {}).get('items', [])
        st.write(f"🔍 **IG:** Buscando `{user_limpio}`... Se encontraron {len(posts)} publicaciones.")
        
        for post in posts[:5]:
            # Accedemos a la sección de comentarios
            comments = post.get('comments', [])
            for c in comments:
                texto = c.get('text', '')
                user = c.get('user', {}).get('username', 'anonimo')
                if texto:
                    lista_comentarios_total.append({'text': texto, 'username': user})
        
        return lista_comentarios_total
    except Exception as e:
        st.error(f"Error en Red IG: {e}")
        return []

def espiar_tiktok(username):
    """Cambiamos a una API de TikTok más estable."""
    user_limpio = limpiar_nombre_usuario(username)
    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tiktok-scraper7.p.rapidapi.com"
    }
    querystring = {"unique_id": user_limpio, "count": "10"}
    
    lista_comentarios_total = []
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        data = response.json()
        
        videos = data.get('data', {}).get('videos', [])
        st.write(f"🔍 **TT:** Buscando `{user_limpio}`... Se encontraron {len(videos)} videos.")
        
        for vid in videos:
            # En TikTok a veces hay que pedir los comentarios aparte, 
            # pero muchas APIs los incluyen en el objeto del video
            comms = vid.get('comments', [])
            for c in comms:
                lista_comentarios_total.append({
                    'text': c.get('text', ''),
                    'username': c.get('author', {}).get('unique_id', 'anonimo_tt')
                })
        return lista_comentarios_total
    except Exception as e:
        st.error(f"Error en Red TT: {e}")
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    leads_limpios = []
    if not lista_comentarios:
        return []

    for c in lista_comentarios:
        texto = c.get('text', '')
        usuario = c.get('username', 'usuario_anonimo')
        
        if not texto: continue

        analisis = analizar_lead(texto)
        if analisis.get('score_ia', 0) >= 0.3:
            leads_limpios.append({
                "usuario_ig": usuario,
                "comentario": texto,
                "score_ia": analisis.get('score_ia'),
                "vehiculo_interes": analisis.get('producto_interes', 'General'),
                "fuente": plataforma
            })
    
    if leads_limpios:
        st.success(f"✅ ¡La IA detectó {len(leads_limpios)} interesados en {plataforma}!")
    return leads_limpios
