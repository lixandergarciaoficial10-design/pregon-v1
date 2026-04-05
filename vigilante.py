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
        data = response.json()
        
        # DEBUG: Ver que responde la API
        posts = data.get('body', {}).get('items', [])
        st.write(f"DEBUG IG: Se encontraron {len(posts)} posts para @{username}")
        
        # Tomamos los últimos 10 posts
        for post in posts[:10]:
            # Algunas APIs anidan los comentarios diferente, probamos ambas rutas
            comments = post.get('comments', {}).get('items', [])
            if not comments: # Intento alternativo por si la estructura cambia
                comments = post.get('comment_list', [])
                
            for c in comments:
                texto = c.get('text', '')
                user = c.get('user', {}).get('username', 'anonimo')
                if texto:
                    lista_comentarios_total.append({'text': texto, 'username': user})
        
        st.write(f"DEBUG IG: Total comentarios leídos: {len(lista_comentarios_total)}")
        return lista_comentarios_total
    except Exception as e:
        st.error(f"Error en API Instagram: {e}")
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
        data = response.json()
        videos = data.get('data', {}).get('videos', [])
        
        st.write(f"DEBUG TT: Se encontraron {len(videos)} videos para @{username}")
        
        for vid in videos[:10]:
            # En TikTok la estructura suele ser 'comments_data' o requiere otra llamada
            comms = vid.get('comments_data', [])
            for c in comms:
                lista_comentarios_total.append({
                    'text': c.get('text', ''),
                    'username': c.get('unique_id', 'anonimo_tt')
                })
        
        st.write(f"DEBUG TT: Total comentarios leídos: {len(lista_comentarios_total)}")
        return lista_comentarios_total
    except Exception as e:
        st.error(f"Error en API TikTok: {e}")
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    """Analiza y filtra los leads con un umbral muy bajo (0.3)"""
    leads_limpios = []
    
    if not lista_comentarios:
        st.warning(f"Advertencia: La lista de comentarios para {plataforma} llegó vacía.")
        return []

    for c in lista_comentarios:
        texto = c.get('text', '')
        usuario = c.get('username', 'usuario_anonimo')
        
        if not texto: continue

        analisis = analizar_lead(texto)
        score = analisis.get('score_ia', 0)
        
        # Si el score es mayor a 0.3, lo guardamos
        if score >= 0.3:
            leads_limpios.append({
                "usuario_ig": usuario,
                "comentario": texto,
                "score_ia": score,
                "vehiculo_interes": analisis.get('producto_interes', analisis.get('vehiculo_interes', 'General')),
                "fuente": plataforma
            })
            
    st.write(f"DEBUG IA: De los comentarios leídos, {len(leads_limpios)} pasaron el filtro de intención.")
    return leads_limpios
