import requests
import streamlit as st
from ia_engine import analizar_lead

# Llave de RapidAPI desde los Secrets
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def limpiar_nombre_usuario(user):
    """Limpia el @ y espacios en blanco para que la API no falle."""
    return user.replace("@", "").strip().lower()

def espiar_instagram(username):
    """Busca los posts de un perfil en IG y extrae sus comentarios."""
    user_limpio = limpiar_nombre_usuario(username)
    url = "https://instagram-scraper47.p.rapidapi.com/get_user_posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-scraper47.p.rapidapi.com"
    }
    querystring = {"username": user_limpio}
    
    lista_comentarios_total = []
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        # Accedemos a los posts
        posts = data.get('body', {}).get('items', [])
        st.write(f"🔍 **IG:** Intentando con `{user_limpio}`... Se encontraron {len(posts)} posts.")
        
        for post in posts[:10]:
            # Intentamos varias rutas por si la API cambia la estructura
            comments = post.get('comments', {}).get('items', [])
            if not comments:
                comments = post.get('comment_list', [])
                
            for c in comments:
                texto = c.get('text', '')
                user = c.get('user', {}).get('username', 'anonimo')
                if texto:
                    lista_comentarios_total.append({'text': texto, 'username': user})
        
        return lista_comentarios_total
    except Exception as e:
        st.error(f"Error en API Instagram: {e}")
        return []

def espiar_tiktok(username):
    """Busca los videos de un perfil en TikTok y extrae sus comentarios."""
    user_limpio = limpiar_nombre_usuario(username)
    url = "https://tiktok-all-data-scrapper3.p.rapidapi.com/user_video_list/"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tiktok-all-data-scrapper3.p.rapidapi.com"
    }
    querystring = {"unique_id": user_limpio}
    
    lista_comentarios_total = []
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        # En esta API específica, a veces los videos vienen en 'data' o directamente en la raíz
        videos = data.get('data', {}).get('videos', [])
        if not videos and 'videos' in data: videos = data['videos']
        
        st.write(f"🔍 **TT:** Intentando con `{user_limpio}`... Se encontraron {len(videos)} videos.")
        
        for vid in videos[:10]:
            comms = vid.get('comments_data', [])
            for c in comms:
                lista_comentarios_total.append({
                    'text': c.get('text', ''),
                    'username': c.get('unique_id', 'anonimo_tt')
                })
        
        return lista_comentarios_total
    except Exception as e:
        st.error(f"Error en API TikTok: {e}")
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    """Analiza y filtra los leads."""
    leads_limpios = []
    
    if not lista_comentarios:
        st.info(f"ℹ️ No se pudieron leer comentarios de {plataforma} (posiblemente la cuenta es privada o no hay comentarios nuevos).")
        return []

    for c in lista_comentarios:
        texto = c.get('text', '')
        usuario = c.get('username', 'usuario_anonimo')
        
        if not texto: continue

        analisis = analizar_lead(texto)
        score = analisis.get('score_ia', 0)
        
        if score >= 0.3:
            leads_limpios.append({
                "usuario_ig": usuario,
                "comentario": texto,
                "score_ia": score,
                "vehiculo_interes": analisis.get('producto_interes', 'General'),
                "fuente": plataforma
            })
            
    st.write(f"✅ **IA:** ¡Se detectaron {len(leads_limpios)} leads con interés real!")
    return leads_limpios
