import requests
import streamlit as st
import time
from ia_engine import analizar_lead

RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def limpiar_nombre_usuario(user):
    if "instagram.com/" in user or "tiktok.com/" in user:
        user = user.split("/")[-1].split("?")[0]
    return user.replace("@", "").strip().lower()

def espiar_instagram(username):
    user_limpio = limpiar_nombre_usuario(username)
    # URL EXACTA PARA LA API "social-api-t" (La que tienes activa)
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
    }
    querystring = {"username_or_id_or_url": user_limpio}
    
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            # La estructura de esta API específica es data -> items
            posts = data.get('data', {}).get('items', [])
            st.write(f"✅ **IG:** `{user_limpio}` conectado. {len(posts)} posts.")
            
            comentarios = []
            for post in posts[:5]:
                # Esta API anida los comentarios en 'comments'
                for c in post.get('comments', []):
                    comentarios.append({
                        'text': c.get('text', ''),
                        'username': c.get('user', {}).get('username', 'anonimo')
                    })
            return comentarios
        return []
    except:
        return []

def espiar_tiktok(username):
    user_limpio = limpiar_nombre_usuario(username)
    # CAMBIO DE ENDPOINT PARA TIKTOK (Probando la ruta estándar de la API que tienes)
    url = "https://tiktok-all-data-scrapper3.p.rapidapi.com/user/posts" 
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tiktok-all-data-scrapper3.p.rapidapi.com"
    }
    querystring = {"unique_id": user_limpio}
    
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('data', {}).get('videos', [])
            st.write(f"✅ **TT:** `{user_limpio}` conectado. {len(videos)} videos.")
            
            comentarios = []
            for v in videos[:5]:
                for c in v.get('comments_data', []):
                    comentarios.append({
                        'text': c.get('text', ''),
                        'username': c.get('unique_id', 'anonimo')
                    })
            return comentarios
        return []
    except:
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    leads_limpios = []
    if not lista_comentarios: return []
    for c in lista_comentarios:
        res = analizar_lead(c.get('text', ''))
        if res.get('score_ia', 0) >= 0.3:
            leads_limpios.append({
                "usuario_ig": c.get('username'),
                "comentario": c.get('text'),
                "score_ia": res.get('score_ia'),
                "vehiculo_interes": res.get('producto_interes', 'General'),
                "fuente": plataforma
            })
    return leads_limpios
