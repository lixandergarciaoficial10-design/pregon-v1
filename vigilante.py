import streamlit as st
from apify_client import ApifyClient

try:
    APIFY_TOKEN = st.secrets["APIFY_TOKEN"]
    client = ApifyClient(APIFY_TOKEN)
except:
    client = None

def espiar_instagram(cuenta_target):
    if client is None: return []
    usuario = cuenta_target.replace("@", "").strip()
    
    # Usamos el actor más estable de todos para perfiles
    run_input = {
        "directUrls": [f"https://www.instagram.com/{usuario}/"],
        "resultsLimit": 1, 
        "searchLimit": 1,
        "searchType": "hashtag"
    }

    try:
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        datos_crudos = []
        
        # --- ESTO ES PARA EL EXPERTO O PARA NOSOTROS AHORA ---
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        # Si quieres ver qué está llegando de verdad, descomenta la línea de abajo en tu prueba
        # st.write(items) 

        for item in items:
            # Instagram Scraper a veces pone los comentarios en 'latestComments'
            comentarios = item.get("latestComments", [])
            
            if not comentarios:
                # Intentamos otra ruta donde Apify suele guardar comentarios
                comentarios = item.get("comments", [])

            for com in comentarios:
                datos_crudos.append({
                    "usuario_ig": com.get("ownerUsername") or com.get("owner", {}).get("username"),
                    "comentario": com.get("text"),
                    "fuente": "Instagram",
                    "vehiculo_interes": "Escaneo Directo"
                })
        
        return datos_crudos
    except Exception as e:
        st.error(f"Error técnico: {e}")
        return []

def espiar_tiktok(t): return []

def limpiar_y_calificar(datos, plataforma):
    # Aceptamos TODO para validar que la conexión funciona
    for item in datos:
        item['score_ia'] = 0.95
    return datos
