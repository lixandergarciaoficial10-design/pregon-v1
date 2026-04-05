import requests
import streamlit as st
from ia_engine import analizar_lead

# Llave de RapidAPI
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def limpiar_nombre_usuario(user):
    return user.replace("@", "").strip().lower()

def espiar_instagram(username):
    user_limpio = limpiar_nombre_usuario(username)
    # Usaremos un endpoint más genérico que suele ser más estable
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
    }
    querystring = {"username_or_id_or_url": user_limpio}
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        
        # Si la API responde 401 o 403, es falta de suscripción
        if response.status_code != 200:
            st.error(f"❌ Error de Conexión ({response.status_code}): Revisa tu suscripción en RapidAPI para esta API.")
            return []

        data = response.json()
        posts = data.get('data', {}).get('items', [])
        
        # Si posts es None o vacío pero hay respuesta 200
        if not posts:
            st.warning(f"⚠️ La cuenta @{user_limpio} no devolvió posts. ¿Está bien escrito el nombre?")
            return []

        st.write(f"🔍 **IG:** `{user_limpio}` encontrado. Analizando {len(posts)} posts...")
        
        lista_comentarios = []
        for post in posts[:5]:
            # Intentamos capturar comentarios si vienen incluidos
            comms = post.get('comments', [])
            for c in comms:
                lista_comentarios.append({'text': c.get('text', ''), 'username': c.get('user', {}).get('username', 'anonimo')})
        return lista_comentarios

    except Exception as e:
        st.error(f"Hubo un problema técnico: {e}")
        return []

def espiar_tiktok(username):
    user_limpio = limpiar_nombre_usuario(username)
    url = "https://tiktok-all-data-scrapper3.p.rapidapi.com/user_video_list/"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tiktok-all-data-scrapper3.p.rapidapi.com"
    }
    querystring = {"unique_id": user_limpio}
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        data = response.json()
        
        # Verificamos si la API devolvió un error de 'msg'
        if data.get('msg') == 'Success':
            videos = data.get('data', {}).get('videos', [])
            st.write(f"🔍 **TT:** `{user_limpio}` encontrado. Analizando {len(videos)} videos...")
            
            lista_coms = []
            for v in videos[:5]:
                for c in v.get('comments_data', []):
                    lista_coms.append({'text': c.get('text', ''), 'username': c.get('unique_id', 'anonimo')})
            return lista_coms
        else:
            st.warning(f"⚠️ TikTok no respondió correctamente para @{user_limpio}")
            return []
    except:
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    leads_limpios = []
    if not lista_comentarios: return []

    for c in lista_comentarios:
        analisis = analizar_lead(c.get('text', ''))
        if analisis.get('score_ia', 0) >= 0.3:
            leads_limpios.append({
                "usuario_ig": c.get('username'),
                "comentario": c.get('text'),
                "score_ia": analisis.get('score_ia'),
                "vehiculo_interes": analisis.get('producto_interes', 'General'),
                "fuente": plataforma
            })
    return leads_limpios
