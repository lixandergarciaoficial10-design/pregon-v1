import requests
import streamlit as st
import time
from ia_engine import analizar_lead

# Llave de RapidAPI desde los Secrets
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def limpiar_nombre_usuario(user):
    """Extrae el username limpio si el usuario pega un link de IG/TT."""
    if "instagram.com/" in user or "tiktok.com/" in user:
        # Ejemplo: de 'https://.../username/' saca 'username'
        user = user.rstrip('/').split('/')[-1].split('?')[0]
    return user.replace("@", "").strip().lower()

def espiar_instagram(username):
    user_limpio = limpiar_nombre_usuario(username)
    # Host de la API que tienes activa según tu factura
    host = "instagram-scraper-api2.p.rapidapi.com"
    url = f"https://{host}/v1/posts"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host
    }
    querystring = {"username_or_id_or_url": user_limpio}
    
    try:
        time.sleep(1) # Evitar error 429
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('items', [])
            st.write(f"🔍 **IG:** `{user_limpio}` conectado. Leyendo {len(posts)} posts...")
            
            lista_coms = []
            for post in posts[:10]: # Revisamos los últimos 10 posts
                # Buscamos comentarios en las rutas posibles de esta API
                comms = post.get('comments', []) or post.get('comment_list', [])
                for c in comms:
                    lista_coms.append({
                        'text': c.get('text') or c.get('content') or "",
                        'username': c.get('user', {}).get('username') or "anonimo"
                    })
            return lista_coms
        else:
            st.warning(f"⚠️ IG @{user_limpio}: Error {response.status_code}")
            return []
    except:
        return []

def espiar_tiktok(username):
    user_limpio = limpiar_nombre_usuario(username)
    # Host de la API TikTok que tienes activa
    host = "tiktok-all-data-scrapper3.p.rapidapi.com"
    url = f"https://{host}/user/posts" 
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host
    }
    querystring = {"unique_id": user_limpio}
    
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('data', {}).get('videos', [])
            st.write(f"🔍 **TT:** `{user_limpio}` conectado. Leyendo {len(videos)} videos...")
            
            lista_coms = []
            for v in videos[:10]:
                comms = v.get('comments_data', [])
                for c in comms:
                    lista_coms.append({
                        'text': c.get('text') or c.get('content') or "",
                        'username': c.get('unique_id') or "anonimo_tt"
                    })
            return lista_coms
        return []
    except:
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    """Filtra los comentarios con la IA y devuelve los leads reales."""
    leads_limpios = []
    if not lista_comentarios: 
        return []

    for c in lista_comentarios:
        texto = c.get('text', "")
        usuario = c.get('username', "anonimo")
        
        if len(texto) < 3: continue 

        # El cerebro analiza el texto
        analisis = analizar_lead(texto)
        score = analisis.get('score_ia', 0)
        
        # Filtro de interés (0.2 para no perder nada en las pruebas)
        if score >= 0.2:
            leads_limpios.append({
                "usuario_ig": usuario,
                "comentario": texto,
                "score_ia": score,
                "vehiculo_interes": analisis.get('producto_interes', 'General'),
                "fuente": plataforma
            })
    return leads_limpios
