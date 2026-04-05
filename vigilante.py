import streamlit as st
from apify_client import ApifyClient

# CONFIGURACIÓN SEGURA
# Asegúrate de tener APIFY_TOKEN en los Secrets de Streamlit
try:
    APIFY_TOKEN = st.secrets["APIFY_TOKEN"]
    client = ApifyClient(APIFY_TOKEN)
except Exception as e:
    st.error("⚠️ Error: No se encontró el APIFY_TOKEN en los Secrets de Streamlit.")
    client = None

def espiar_instagram(cuenta_target):
    """Llama al motor profesional de Apify para extraer comentarios"""
    if client is None:
        return []

    cuenta_limpia = cuenta_target.replace("@", "").strip()
    
    # Configuración del robot especializado en comentarios
    run_input = {
        "directUrls": [f"https://www.instagram.com/{cuenta_limpia}/"],
        "resultsLimit": 30, # Extraemos los últimos 30 para asegurar volumen
    }

    try:
        # Usamos el actor especializado (más eficiente)
        run = client.actor("apify/instagram-comment-scraper").call(run_input=run_input)
        
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

def espiar_tiktok(t): 
    return [] # Pendiente para la v2

def limpiar_y_calificar(datos, plataforma):
    """Filtro de Inteligencia para detectar intención de compra"""
    leads_finales = []
    # Palabras que huelen a DINERO
    palabras_clave = ["precio", "cuanto", "info", "disponible", "donde", "ubicacion", "venden", "numero", "whatsapp", "interesa"]
    
    for item in datos:
        texto = item['comentario'].lower()
        
        # Si el comentario tiene una palabra clave, le damos prioridad alta (0.95)
        if any(p in texto for p in palabras_clave):
            item['score_ia'] = 0.95
            leads_finales.append(item)
        # Si es un comentario genérico pero largo, lo dejamos como interés bajo
        elif len(texto) > 15:
            item['score_ia'] = 0.45
            leads_finales.append(item)
            
    return leads_finales
