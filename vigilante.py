import requests
import streamlit as st
import time
from ia_engine import analizar_lead

# Tu llave de RapidAPI (Asegúrate de que sea la misma de tu cuenta personal)
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def limpiar_nombre_usuario(user):
    """Limpia el nombre de usuario de @ o links."""
    if "instagram.com/" in user or "tiktok.com/" in user:
        user = user.split("/")[-1].split("?")[0]
    return user.replace("@", "").strip().lower()

def espiar_instagram(username):
    user_limpio = limpiar_nombre_usuario(username)
    # URL para el "Extractor de datos de Instagram" (social-api-t)
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/posts"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
    }
    querystring = {"username_or_id_or_url": user_limpio}
    
    try:
        time.sleep(1.5) # Pausa para evitar el error 429
        response = requests.get(url, headers=headers, params=querystring, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('items', [])
            st.write(f"🔍 **IG:** `{user_limpio}` - {len(posts)} posts encontrados.")
            
            # Sacamos los comentarios
            lista_coms = []
            for post in posts[:5]:
                comms = post.get('comments', [])
                for c in comms:
                    lista_coms.append({
                        'text': c.get('text', ''),
                        'username': c.get('user', {}).get('username', 'anonimo')
                    })
            return lista_coms
        else:
            st.error(f"❌ Error IG ({response.status_code}): {response.text}")
            return []
    except Exception as e:
        st.error(f"Error técnico IG: {e}")
        return []

def espiar_tiktok(username):
    user_limpio = limpiar_nombre_usuario(username)
    # URL para el "Extractor de datos de TikTok"
    url = "https://tiktok-all-data-scrapper3.p.rapidapi.com/user_video_list/"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tiktok-all-data-scrapper3.p.rapidapi.com"
    }
    querystring = {"unique_id": user_limpio}
    
    try:
        time.sleep(1.5)
        response = requests.get(url, headers=headers, params=querystring, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('data', {}).get('videos', [])
            st.write(f"🔍 **TT:** `{user_limpio}` - {len(videos)} videos encontrados.")
            
            lista_coms = []
            for v in videos[:5]:
                comms = v.get('comments_data', [])
                for c in comms:
                    lista_coms.append({
                        'text': c.get('text', ''),
                        'username': c.get('unique_id', 'anonimo')
                    })
            return lista_coms
        else:
            st.error(f"❌ Error TT ({response.status_code}): {response.text}")
            return []
    except Exception as e:
        st.error(f"Error técnico TT: {e}")
        return []

def limpiar_y_calificar(lista_comentarios, plataforma):
    leads_limpios = []
    if not lista_comentarios:
        return []

    for c in lista_comentarios:
        texto = c.get('text', '')
        if not texto: continue
        
        analisis = analizar_lead(texto)
        score = analisis.get('score_ia', 0)
        
        if score >= 0.3:
            leads_limpios.append({
                "usuario_ig": c.get('username'),
                "comentario": texto,
                "score_ia": score,
                "vehiculo_interes": analisis.get('producto_interes', 'General'),
                "fuente": plataforma
            })
    return leads_limpios
