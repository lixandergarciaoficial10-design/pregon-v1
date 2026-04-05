import streamlit as st
from apify_client import ApifyClient

# CONFIGURACIÓN - PEGA TU TOKEN AQUÍ
APIFY_TOKEN = "TU_APIFY_TOKEN_AQUÍ" 
client = ApifyClient(APIFY_TOKEN)

def espiar_instagram(cuenta_target):
    """Llama al motor de Apify para extraer comentarios reales"""
    cuenta_limpia = cuenta_target.replace("@", "").strip()
    
    # Preparamos el robot de Apify (Instagram Scraper)
    run_input = {
        "directUrls": [f"https://www.instagram.com/{cuenta_limpia}/"],
        "resultsLimit": 20, # Traer los últimos 20 comentarios
        "resultsType": "comments",
        "searchLimit": 1,
        "searchType": "hashtag"
    }

    try:
        # Ejecutamos el robot en la nube de Apify (Ellos no se bloquean)
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        
        datos_crudos = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            datos_crudos.append({
                "usuario_ig": item.get("ownerUsername"),
                "comentario": item.get("text"),
                "fuente": "Instagram (Apify)",
                "vehiculo_interes": "Detectado en Radar"
            })
        return datos_crudos
    except Exception as e:
        st.error(f"Error en Apify: {e}")
        return []

def espiar_tiktok(t): return [] # Próxima fase

def limpiar_y_calificar(datos, plataforma):
    """IA de filtrado rápido"""
    leads_finales = []
    palabras_clave = ["precio", "cuanto", "info", "disponible", "donde", "ubicacion", "venden", "numero"]
    
    for item in datos:
        texto = item['comentario'].lower()
        # Si tiene interés real, score alto. Si no, 0.1
        score = 0.90 if any(p in texto for p in palabras_clave) else 0.10
        
        if score > 0.4: # Solo guardamos los que de verdad quieren comprar
            item['score_ia'] = score
            leads_finales.append(item)
            
    return leads_finales
